"""RepoTrace structural analysis: file-level dependency graph + PageRank.

Pure-python, no third-party dependencies. The collection step runs INSIDE the
task container (via environment.exec, or locally for tests); parsing and
scoring run wherever the agent process lives (host for terminus-2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# One shell script, uploaded into the container once per trial and executed
# as `sh /tmp/repotrace_collect.sh [root]`. Emits sections parsed by
# parse_collect_output. Kept POSIX-ish; every grep may legitimately find
# nothing, so sections are separated by markers and we never chain with &&.
COLLECT_SCRIPT = r"""
if [ -n "$1" ]; then
  root="$1"
else
  root=""
  for d in /app /workspace /repo /src /code /project "$HOME/repo" "$HOME/app"; do
    if [ -d "$d" ]; then root="$d"; break; fi
  done
  [ -n "$root" ] || root="$PWD"
fi
echo '===ROOT==='
echo "$root"
cd "$root" 2>/dev/null || { echo '===END==='; exit 0; }
echo '===FILES==='
find . -type f \( -name '*.go' -o -name '*.py' -o -name '*.js' -o -name '*.jsx' \
  -o -name '*.ts' -o -name '*.tsx' -o -name '*.java' -o -name '*.rs' \
  -o -name '*.rb' -o -name '*.c' -o -name '*.h' -o -name '*.cc' -o -name '*.cpp' \
  -o -name '*.sh' -o -name '*.bash' \) \
  -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/node_modules/*' \
  -not -path '*/dist/*' -not -path '*/__pycache__/*' \
  | sed 's|^\./||' | sort | head -3000
echo '===GO_IMPORTS==='
grep -rH --include='*.go' -oE '"[a-zA-Z0-9_.~-]+(/[a-zA-Z0-9_.~-]+)+"' . 2>/dev/null | head -20000
echo '===PY_IMPORTS==='
grep -rH --include='*.py' -oE '^[[:space:]]*(from|import)[[:space:]]+[a-zA-Z0-9_.]+' . 2>/dev/null | head -20000
echo '===JS_IMPORTS==='
grep -rH --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' \
  -oE "(from[[:space:]]+'[^']+'|from[[:space:]]+\"[^\"]+\"|require\('[^']+'\))" . 2>/dev/null | head -20000
echo '===CALLS==='
grep -rHn --include='*.go' -oE '[A-Za-z_][A-Za-z0-9_]*\(' . 2>/dev/null | head -40000
grep -rHn --include='*.py' -oE '[a-zA-Z_][a-zA-Z0-9_]*\(' . 2>/dev/null | head -40000
grep -rHn --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' \
  -oE '[a-zA-Z_$][a-zA-Z0-9_$]*\(' . 2>/dev/null | head -40000
grep -rHn --include='*.c' --include='*.cpp' --include='*.cc' \
  -oE '[A-Za-z_][A-Za-z0-9_]*\(' . 2>/dev/null | head -40000
# shell: 命令名 = 行首 或 ; | & && || 之后的首个标识符
grep -rHn --include='*.sh' --include='*.bash' \
  -oE '(^|[;|&])[[:space:]]*[A-Za-z_][A-Za-z0-9_]*' . 2>/dev/null | head -40000
echo '===SYMBOLS==='
grep -rHn --include='*.go' -oE '^func[[:space:]]+(\([^)]*\)[[:space:]]*)?[A-Za-z_][A-Za-z0-9_]*' . 2>/dev/null | head -10000
grep -rHn --include='*.py' -oE '^[[:space:]]*(def|class)[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' . 2>/dev/null | head -10000
grep -rHn --include='*.js' --include='*.ts' -oE '(function[[:space:]]+[A-Za-z_][A-Za-z0-9_]*|class[[:space:]]+[A-Za-z_][A-Za-z0-9_]*)' . 2>/dev/null | head -10000
# C/C++: 定义行通常是 返回类型 函数名( ... 在行首;提取最后一个标识符作为函数名
# (含 .h 声明,让头文件作为 API 节点出现在图上)
grep -rHn --include='*.c' --include='*.cpp' --include='*.cc' --include='*.h' \
  --include='*.hpp' --include='*.hh' \
  -oE '^[A-Za-z_][A-Za-z0-9_ \*]*[A-Za-z_][A-Za-z0-9_]*\s*\(' . 2>/dev/null | head -10000
# shell: 函数定义 name() { 或 function name {
grep -rHn --include='*.sh' --include='*.bash' \
  -oE '^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*\(\)|^[[:space:]]*function[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' \
  . 2>/dev/null | head -10000
echo '===END==='
"""

_REMOTE_SCRIPT_PATH = "/tmp/repotrace_collect.sh"

_SOURCE_EXT = (".go", ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".rs",
               ".rb", ".c", ".h", ".cc", ".cpp", ".sh", ".bash")


@dataclass
class RepoGraph:
    root: str = ""
    files: list[str] = field(default_factory=list)
    edges: set[tuple[str, str]] = field(default_factory=set)  # (importer, imported) — ALL file-level edges (imports + call-derived)
    import_edges: set[tuple[str, str]] = field(default_factory=set)  # (importer, imported) — import edges ONLY
    file_symbols: dict[str, list[str]] = field(default_factory=dict)
    symbol_files: dict[str, set[str]] = field(default_factory=dict)
    # function-level: name -> defining file(s)
    func_defs: dict[str, set[str]] = field(default_factory=dict)
    # function-level call edges: ((caller_file, caller_func), (callee_file, callee_func))
    func_edges: set[tuple[tuple[str, str], tuple[str, str]]] = field(default_factory=set)
    pagerank: dict[str, float] = field(default_factory=dict)
    fan_in: dict[str, int] = field(default_factory=dict)
    fan_out: dict[str, int] = field(default_factory=dict)

    def dependents(self, targets: list[str], hops: int = 2, cap: int = 30) -> list[str]:
        """Files that (transitively) import any target — the impact scope."""
        rev: dict[str, set[str]] = {}
        for a, b in self.edges:
            rev.setdefault(b, set()).add(a)
        seen: set[str] = set(targets)
        frontier = list(targets)
        for _ in range(hops):
            nxt: list[str] = []
            for f in frontier:
                for d in rev.get(f, ()):
                    if d not in seen:
                        seen.add(d)
                        nxt.append(d)
            frontier = nxt
        out = [f for f in seen if f not in targets]
        out.sort(key=lambda f: self.pagerank.get(f, 0.0), reverse=True)
        return out[:cap]

    def top(self, n: int = 10) -> list[str]:
        return sorted(self.files, key=lambda f: self.pagerank.get(f, 0.0),
                      reverse=True)[:n]


def _longest_suffix_dir(import_path: str, dir_set: set[str]) -> str | None:
    """Resolve an import path to a repo directory by longest suffix match.

    Handles Go module prefixes: 'jobforge/internal/spec' -> 'internal/spec'
    when the repo root itself is the module root.
    """
    parts = import_path.strip('"').split("/")
    for i in range(len(parts)):
        cand = "/".join(parts[i:])
        if cand in dir_set:
            return cand
    return None


def _resolve_py_module(module: str, file_set: set[str], dir_set: set[str]) -> list[str]:
    path = module.replace(".", "/")
    cands = [path + ".py", path + "/__init__.py"]
    # also try stripping leading package qualifiers (absolute import from root)
    parts = path.split("/")
    for i in range(1, len(parts)):
        sub = "/".join(parts[i:])
        cands += [sub + ".py", sub + "/__init__.py"]
    hits = [c for c in cands if c in file_set]
    if hits:
        return hits
    if path in dir_set:  # importing a package dir
        return [f for f in file_set if f.startswith(path + "/") and
                f.count("/") == path.count("/") + 1]
    return []


def _resolve_js_ref(ref: str, importer: str, file_set: set[str]) -> list[str]:
    if not ref.startswith("."):
        return []  # bare package import (node_modules) — out of repo
    base = importer.rsplit("/", 1)[0] if "/" in importer else ""
    raw = (base + "/" + ref) if base else ref.lstrip("./")
    # normalize ./ and ../
    parts: list[str] = []
    for p in raw.split("/"):
        if p in ("", "."):
            continue
        if p == "..":
            if parts:
                parts.pop()
        else:
            parts.append(p)
    norm = "/".join(parts)
    for ext in (".ts", ".tsx", ".js", ".jsx"):
        if norm + ext in file_set:
            return [norm + ext]
    for idx in ("/index.ts", "/index.tsx", "/index.js", "/index.jsx"):
        if norm + idx in file_set:
            return [norm + idx]
    return [norm] if norm in file_set else []


def graph_to_dict(g: RepoGraph) -> dict:
    """Full per-round graph snapshot for persistence/analysis."""
    return {
        "root": g.root,
        "files": [
            {
                "path": f,
                "pagerank": round(g.pagerank.get(f, 0.0), 8),
                "fan_in": g.fan_in.get(f, 0),
                "fan_out": g.fan_out.get(f, 0),
                "symbols": g.file_symbols.get(f, []),
            }
            for f in sorted(g.files)
        ],
        "edges": sorted([list(e) for e in g.edges]),
        "import_edges": sorted([list(e) for e in g.import_edges]),
        "func_edges": sorted(
            [[list(a), list(b)] for a, b in g.func_edges]
        ),
        "func_defs": {k: sorted(v) for k, v in g.func_defs.items()},
    }


def graph_delta(prev: RepoGraph | None, cur: RepoGraph) -> dict:
    """Round-over-round structural change — the evolution signal."""
    if prev is None:
        return {
            "files_added": sorted(cur.files), "files_removed": [],
            "edges_added": sorted([list(e) for e in cur.edges]), "edges_removed": [],
        }
    pf, cf = set(prev.files), set(cur.files)
    return {
        "files_added": sorted(cf - pf),
        "files_removed": sorted(pf - cf),
        "edges_added": sorted([list(e) for e in cur.edges - prev.edges]),
        "edges_removed": sorted([list(e) for e in prev.edges - cur.edges]),
    }


def pagerank(nodes: list[str], edges: set[tuple[str, str]],
             damping: float = 0.85, iters: int = 40) -> dict[str, float]:
    n = len(nodes)
    if n == 0:
        return {}
    idx = {f: i for i, f in enumerate(nodes)}
    out: list[list[int]] = [[] for _ in nodes]
    for a, b in edges:
        if a in idx and b in idx and a != b:
            out[idx[a]].append(idx[b])
    pr = [1.0 / n] * n
    for _ in range(iters):
        new = [(1.0 - damping) / n] * n
        for i, targets in enumerate(out):
            if targets:
                share = damping * pr[i] / len(targets)
                for t in targets:
                    new[t] += share
            else:  # dangling node: spread uniformly
                share = damping * pr[i] / n
                for j in range(n):
                    new[j] += share
        pr = new
    return {f: pr[i] for f, i in idx.items()}


def parse_collect_output(text: str, root: str = "") -> RepoGraph:
    g = RepoGraph(root=root)
    sections: dict[str, list[str]] = {}
    cur: str | None = None
    for line in text.splitlines():
        m = re.match(r"^===([A-Z_]+)===$", line.strip())
        if m:
            cur = m.group(1)
            sections[cur] = []
            continue
        if cur and line.strip():
            sections[cur].append(line.strip())

    g.files = [f for f in sections.get("FILES", []) if f.endswith(_SOURCE_EXT)]
    if sections.get("ROOT"):
        g.root = sections["ROOT"][0]
    file_set = set(g.files)
    dir_set = {f.rsplit("/", 1)[0] for f in g.files if "/" in f}

    def record(importer: str, targets: list[str]) -> None:
        for t in targets:
            if t in file_set and t != importer:
                g.edges.add((importer, t))
                g.import_edges.add((importer, t))

    for line in sections.get("GO_IMPORTS", []):
        f, _, imp = line.partition(":")
        f = f.lstrip("./")
        d = _longest_suffix_dir(imp, dir_set)
        if d:
            record(f, [x for x in file_set if x.startswith(d + "/")])
    for line in sections.get("PY_IMPORTS", []):
        f, _, stmt = line.partition(":")
        f = f.lstrip("./")
        m = re.search(r"(?:from|import)\s+([a-zA-Z0-9_.]+)", stmt)
        if m:
            record(f, _resolve_py_module(m.group(1), file_set, dir_set))
    for line in sections.get("JS_IMPORTS", []):
        f, _, stmt = line.partition(":")
        f = f.lstrip("./")
        m = re.search(r"['\"]([^'\"]+)['\"]", stmt)
        if m:
            record(f, _resolve_js_ref(m.group(1), f, file_set))

    func_starts: dict[str, list[tuple[int, str]]] = {}
    def_lines: set[tuple[str, int]] = set()
    for line in sections.get("SYMBOLS", []):
        parts = line.split(":", 2)  # grep -Hn: file:lineno:matched_text
        if len(parts) < 3:
            continue
        f, _ln, textm = parts
        f = f.lstrip("./")
        if f not in file_set:
            continue
        try:
            lineno = int(_ln.strip())
        except ValueError:
            lineno = 0
        # matched text may end with the func name (Go), '(' (C/C++), or '()'
        # (shell `name() {`)
        m = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(?\)?\s*$", textm.strip())
        if not m:
            continue
        name = m.group(1)
        g.file_symbols.setdefault(f, []).append(name)
        g.symbol_files.setdefault(name, set()).add(f)
        g.func_defs.setdefault(name, set()).add(f)
        func_starts.setdefault(f, []).append((lineno, name))
        def_lines.add((f, lineno))
    for f in func_starts:
        func_starts[f].sort()

    def _enclosing_func(file: str, lineno: int) -> str:
        cur = "?"
        for ln, fn in func_starts.get(file, []):
            if ln > lineno:
                break
            cur = fn
        return cur

    # Function-level call edges: call site `name(` (Go/Py/JS/C) or bare command
    # `name` (shell) in caller file, matched to a function `name` defined
    # (elsewhere) => (caller_func -> callee). Same-package Go/Python/shell calls
    # are captured because bare names don't need import edges.
    call_re = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)(?:\(|$)")
    for line in sections.get("CALLS", []):
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        f, _ln, text = parts
        f = f.lstrip("./")
        if f not in file_set:
            continue
        try:
            lineno = int(_ln.strip())
        except ValueError:
            lineno = 0
        if (f, lineno) in def_lines:
            continue  # the line is a function signature, not a call site
        caller_func = _enclosing_func(f, lineno)
        if caller_func == "?":
            continue  # call site not inside any function (e.g. a header decl)
        for m in call_re.finditer(text):
            callee = m.group(1)
            if callee in ("main", "init") or callee not in g.func_defs:
                continue
            for df in g.func_defs[callee]:
                # skip the enclosing func calling itself (recursion is noise
                # for architecture understanding; keep cross-func edges only)
                if (df, callee) == (f, caller_func):
                    continue
                # C: a call resolves to the .c implementation, not the .h
                # declaration (headers only carry the API surface)
                if df.endswith((".h", ".hpp", ".hh", ".hxx")):
                    continue
                g.func_edges.add(((f, caller_func), (df, callee)))
                # also keep the coarse file-level edge for PageRank purposes
                if df != f:
                    g.edges.add((f, df))

    g.pagerank = pagerank(g.files, g.edges)
    g.fan_in = {f: 0 for f in g.files}
    g.fan_out = {f: 0 for f in g.files}
    for a, b in g.edges:
        g.fan_out[a] = g.fan_out.get(a, 0) + 1
        g.fan_in[b] = g.fan_in.get(b, 0) + 1
    return g
