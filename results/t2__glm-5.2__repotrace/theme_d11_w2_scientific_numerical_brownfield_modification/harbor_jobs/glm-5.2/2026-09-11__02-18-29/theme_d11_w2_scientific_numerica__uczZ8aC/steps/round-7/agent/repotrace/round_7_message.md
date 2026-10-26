========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - src/vector.c is depended on by 9 files (e.g. src/sparse.c, src/precond.c, src/heat.c, src/convdiff.c); changing it ripples widely.
  - src/sparse.c is depended on by 7 files (e.g. src/precond.c, src/heat.c, src/convdiff.c, src/poisson.c); changing it ripples widely.
  - src/precond.c is depended on by 4 files (e.g. src/heat.c, src/solvers.c, src/main.c, src/eigen.c); changing it ripples widely.
  - src/convdiff.c is depended on by 3 files (e.g. src/heat.c, src/poisson.c, src/main.c); changing it ripples widely.
  - src/heat.c is depended on by 3 files (e.g. src/convdiff.c, src/poisson.c, src/main.c); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - src/vector.c: implementation
  - src/sparse.c: implementation
  - src/precond.c: implementation
  - src/convdiff.c: implementation
  - src/heat.c: implementation
  - src/poisson.c: implementation
  - src/solvers.c: implementation
  - src/dense.c: implementation
Prior components this round may touch:
  - round-4 3-column convergence history format and write_history_file
  - cmd_sparse_solve, cmd_poisson, and cmd_convdiff --history output
  - SolveResult, cg_solve, and gmres_solve history arrays used by history writers
  - round-4 eigenvalue power/inverse iteration routines reused for condition estimation
  - round-6 cmd_matvec symmetric Matrix Market handling, which must remain unchanged

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================