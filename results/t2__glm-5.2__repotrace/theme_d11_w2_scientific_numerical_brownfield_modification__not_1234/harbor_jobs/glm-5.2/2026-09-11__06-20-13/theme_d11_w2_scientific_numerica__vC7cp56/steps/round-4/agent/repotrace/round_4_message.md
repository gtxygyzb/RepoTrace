========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - nlsolve.c: implementation
Prior components this round may touch:
  - rcm_ordering
  - build_adjacency
  - main
  - precond_setup
  - precond_apply

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================