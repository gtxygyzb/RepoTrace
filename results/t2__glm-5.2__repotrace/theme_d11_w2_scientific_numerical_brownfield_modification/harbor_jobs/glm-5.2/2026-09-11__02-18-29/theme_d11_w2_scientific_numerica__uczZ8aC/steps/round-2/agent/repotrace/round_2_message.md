========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - src/vector.c is depended on by 6 files (e.g. src/sparse.c, src/precond.c, src/io.c, src/solvers.c); changing it ripples widely.
  - src/sparse.c is depended on by 4 files (e.g. src/precond.c, src/solvers.c, src/poisson.c, src/main.c); changing it ripples widely.
  - src/dense.c is depended on by 2 files (e.g. src/io.c, src/main.c); changing it ripples widely.
  - src/precond.c is depended on by 2 files (e.g. src/solvers.c, src/main.c); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - src/vector.c: implementation
  - src/sparse.c: implementation
  - src/dense.c: implementation
  - src/precond.c: implementation
  - src/io.c: implementation
  - src/poisson.c: implementation
  - src/solvers.c: implementation
  - include/dense.h: implementation
New in this round (to be created):
  - include/heat.h
  - src/heat.c
Prior components this round may touch:
  - cg_solve
  - gmres_solve
  - SolveResult
  - result_create
  - solve_result_destroy
  - write_history_file

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================