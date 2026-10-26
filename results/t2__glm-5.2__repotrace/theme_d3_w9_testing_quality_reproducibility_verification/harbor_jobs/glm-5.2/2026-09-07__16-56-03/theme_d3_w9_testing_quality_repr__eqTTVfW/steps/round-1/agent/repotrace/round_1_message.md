========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
New in this round (to be created):
  - cmd/repro-verify/main.go
  - docs/spec_v1.md

## Verification
  - Build and run tests after modification.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================