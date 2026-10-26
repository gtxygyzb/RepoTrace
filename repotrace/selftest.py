"""Host-side selftest: run the collect script on a local directory, build the
graph, extract entities with the deterministic fallback, and render the
message. No container, no LLM.

Usage:
    python3 -m repotrace.selftest [dir] [instruction-file]
Defaults: dir = the d1_w1 task starter, instruction = its round-1 request.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .entities import extract_entities_fallback
from .graph import COLLECT_SCRIPT, parse_collect_output
from .message import build_message

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / "data/EvoCodeBench/theme_d1_w1_code_build_greenfield_implementation/environment/app-starter"
DEFAULT_INSTR = ROOT / "data/EvoCodeBench/theme_d1_w1_code_build_greenfield_implementation/steps/round-2/instruction.md"


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    instr_file = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_INSTR
    if not target.is_dir():
        print(f"not a directory: {target}")
        return 1
    instruction = instr_file.read_text() if instr_file.is_file() else "refactor the CLI"

    out = subprocess.run(
        ["sh", "-s", str(target)], input=COLLECT_SCRIPT,
        capture_output=True, text=True, timeout=120,
    )
    graph = parse_collect_output(out.stdout, root=str(target))
    print(f"files={len(graph.files)} edges={len(graph.edges)} "
          f"symbols={sum(len(v) for v in graph.file_symbols.values())}")
    print("top-5 by PageRank:")
    for f in graph.top(5):
        print(f"  {f}  pr={graph.pagerank.get(f, 0):.5f} "
              f"fan-in={graph.fan_in.get(f, 0)} fan-out={graph.fan_out.get(f, 0)}")

    ent = extract_entities_fallback(instruction, graph)
    print(f"\nentities ({ent.source}): files={ent.target_files} symbols={ent.target_symbols}")

    print("\n----- injected message preview -----")
    print(build_message(graph, ent, round_no=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
