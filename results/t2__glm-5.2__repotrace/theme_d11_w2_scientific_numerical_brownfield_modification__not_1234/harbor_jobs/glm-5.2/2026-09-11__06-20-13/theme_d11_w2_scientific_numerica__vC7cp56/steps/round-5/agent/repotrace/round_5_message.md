========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - nlsolve.c: implementation
Prior components this round may touch:
  - solve_cg
  - solve_bicgstab
  - ic0_factorize
  - precond_setup
  - main

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================