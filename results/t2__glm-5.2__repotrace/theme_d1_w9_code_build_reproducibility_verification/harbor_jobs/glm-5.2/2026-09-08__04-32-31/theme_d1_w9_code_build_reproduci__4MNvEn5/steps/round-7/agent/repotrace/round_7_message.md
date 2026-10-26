========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - main.go: CLI entry point
Prior components this round may touch:
  - computeChainHash (round 4)
  - cmdAudit (round 4)
  - export command (round 6)
  - storeArtifact (round 1)
  - gcStore (round 1)
  - cmdStatus (round 5)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================