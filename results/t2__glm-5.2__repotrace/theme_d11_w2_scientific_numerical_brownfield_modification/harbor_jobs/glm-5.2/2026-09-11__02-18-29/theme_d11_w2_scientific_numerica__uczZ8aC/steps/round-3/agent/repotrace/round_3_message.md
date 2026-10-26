========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - src/vector.c is depended on by 7 files (e.g. src/sparse.c, src/precond.c, src/heat.c, src/solvers.c); changing it ripples widely.
  - src/sparse.c is depended on by 5 files (e.g. src/precond.c, src/heat.c, src/solvers.c, src/poisson.c); changing it ripples widely.
  - src/precond.c is depended on by 3 files (e.g. src/heat.c, src/solvers.c, src/main.c); changing it ripples widely.
  - src/dense.c is depended on by 2 files (e.g. src/io.c, src/main.c); changing it ripples widely.
  - src/heat.c is depended on by 2 files (e.g. src/poisson.c, src/main.c); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - src/vector.c: implementation
  - src/sparse.c: implementation
  - src/precond.c: implementation
  - src/dense.c: implementation
  - src/heat.c: implementation
  - src/poisson.c: implementation
  - src/solvers.c: implementation
  - src/io.c: implementation
New in this round (to be created):
  - include/convdiff.h
  - src/convdiff.c
Prior components this round may touch:
  - main command dispatch/CLI parsing in src/main.c
  - usage
  - existing command handlers cmd_dense_solve/cmd_sparse_solve/cmd_poisson/cmd_heat must remain unchanged
  - validate_ssor_omega reused for --ssor-omega validation
  - run_solver_and_print/print_solve_summary reused for convergence reporting

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================