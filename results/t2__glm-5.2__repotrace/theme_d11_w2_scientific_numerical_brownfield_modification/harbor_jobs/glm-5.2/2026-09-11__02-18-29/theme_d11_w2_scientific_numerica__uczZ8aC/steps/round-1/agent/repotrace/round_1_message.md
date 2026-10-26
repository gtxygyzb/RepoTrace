========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - src/dense.c is depended on by 2 files (e.g. src/io.c, src/main.c); changing it ripples widely.
  - src/vector.c is depended on by 2 files (e.g. src/io.c, src/main.c); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - src/dense.c: implementation
  - src/vector.c: implementation
  - src/io.c: implementation
  - include/dense.h: implementation
  - include/io.h: implementation
  - include/vector.h: implementation
  - src/main.c: CLI entry point
New in this round (to be created):
  - include/sparse.h
  - src/sparse.c
  - include/solvers.h
  - src/solvers.c
  - include/precond.h
  - src/precond.c
  - include/poisson.h
  - src/poisson.c
  - Makefile
Prior components this round may touch:
  - src/main.c
  - include/io.h
  - src/io.c
  - Makefile

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================