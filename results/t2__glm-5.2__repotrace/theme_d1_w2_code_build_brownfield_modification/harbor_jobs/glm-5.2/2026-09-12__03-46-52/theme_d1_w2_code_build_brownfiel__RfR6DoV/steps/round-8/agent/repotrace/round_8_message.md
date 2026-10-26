========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
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
  - let-statement parsing (try_parse_assign / parse_stmt) from prior rounds
  - array literal parsing (parse_primary) from round 2
  - function-definition parsing (parse_fn_expr) from round 2
  - function-call parsing (parse_postfix) from round 6
  - compile_store / compile_load / add_local / resolve_local from rounds 2 and 5
  - VM local-variable opcodes in vm_run

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================