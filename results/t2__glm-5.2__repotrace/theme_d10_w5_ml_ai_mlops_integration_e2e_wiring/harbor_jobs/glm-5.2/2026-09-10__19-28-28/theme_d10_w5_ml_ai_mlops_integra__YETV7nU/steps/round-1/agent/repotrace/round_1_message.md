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
  - main.go
  - go.mod
  - config.go
  - pipeline.go
  - data.go
  - transform.go
  - split.go
  - train.go
  - evaluate.go
  - register.go

## Verification
  - Build and run tests after modification.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================