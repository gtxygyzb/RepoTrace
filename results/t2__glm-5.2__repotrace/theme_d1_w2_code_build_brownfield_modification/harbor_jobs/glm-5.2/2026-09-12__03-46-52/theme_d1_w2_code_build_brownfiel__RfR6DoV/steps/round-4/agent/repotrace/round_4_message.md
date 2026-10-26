========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
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
  - parse_for (round 1 added for..in; round 3 changed it to iterate indices — now must also iterate map keys)
  - try_parse_assign (round 2 added index assignment for arrays — must extend to dot/bracket field assignment)
  - parse_primary / parse_factor (rounds 2, 3 added closures, indexing — now must add map literals and postfix . / [] access)
  - compile_node (rounds 2, 3 — must add map literal, field load/store, builtins)
  - compile_load / compile_store (round 2 — must handle map field load/store)
  - value_truthy (round 2 — must treat non-empty map as truthy, empty map as falsy)

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================