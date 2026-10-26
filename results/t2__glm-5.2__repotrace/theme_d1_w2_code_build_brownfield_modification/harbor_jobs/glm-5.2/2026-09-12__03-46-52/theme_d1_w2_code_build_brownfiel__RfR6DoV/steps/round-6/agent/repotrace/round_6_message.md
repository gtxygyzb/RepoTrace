========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - src/lexer.c is depended on by 3 files (e.g. src/codegen.c, src/parser.c, src/main.c); changing it ripples widely.
  - src/ast.c is depended on by 2 files (e.g. src/parser.c, src/main.c); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - src/lexer.c: implementation
  - src/ast.c: implementation
  - src/codegen.c: implementation
  - src/parser.c: implementation
  - src/vm.c: implementation
  - src/ast.h: implementation
  - src/codegen.h: implementation
  - src/common.h: implementation
Prior components this round may touch:
  - round 4: hash-map dot access via parse_primary/parse_postfix and BC_HASHMAP_GET — must now type-dispatch instead of unconditionally treating dot as hashmap field.
  - round 2: array values and `len`/`p` builtins — split() must produce arrays usable by existing array/index machinery.

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================