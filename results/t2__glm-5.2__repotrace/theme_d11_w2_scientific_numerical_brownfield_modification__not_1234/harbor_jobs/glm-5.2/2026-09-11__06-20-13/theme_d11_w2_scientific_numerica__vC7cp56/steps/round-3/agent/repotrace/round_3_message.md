========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - nlsolve.c: implementation
Prior components this round may touch:
  - read_matrix (Matrix Market reader, round 1)
  - build_csr / add_entry (CSR construction, round 1)
  - solve_cg (CG solver, rounds 1-2)
  - solve_bicgstab (BiCGSTAB solver, rounds 1-2)
  - precond_apply / precond_setup / compute_diag (SSOR preconditioner, round 1)
  - main (CLI/reporting, rounds 1-2)

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================