========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
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
  - lex_string
  - lexer_tokenize/lex_ident
  - parse_comparison/parse_term
  - try_parse_assign
  - parse_stmt/parse_block
  - compile_expr/compile_call

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================