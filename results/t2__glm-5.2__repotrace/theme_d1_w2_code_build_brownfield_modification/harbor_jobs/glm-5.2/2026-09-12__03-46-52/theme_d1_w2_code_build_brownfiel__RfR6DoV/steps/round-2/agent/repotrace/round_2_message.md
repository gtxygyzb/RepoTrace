========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
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
  - parse_logic_and (round 1 precedence work — must now short-circuit)
  - logical operator codegen/VM opcodes (currently evaluate both operands)
  - try_parse_assign (round 1 compound assignments — must handle index assignment target)
  - fn statement parsing (must disambiguate fn-as-statement from fn-as-expression)
  - array index read path (codegen/VM — must be extended to support store)
  - named function call mechanism (must also resolve closure values)

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================