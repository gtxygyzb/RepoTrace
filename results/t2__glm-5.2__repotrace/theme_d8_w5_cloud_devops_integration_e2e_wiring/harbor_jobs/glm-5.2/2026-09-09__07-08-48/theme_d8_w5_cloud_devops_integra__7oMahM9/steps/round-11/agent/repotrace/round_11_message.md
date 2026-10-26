========================================================================
[RepoTrace] Repository guidance for the current request (round 11)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - pipeline.sh: pipeline logic
Prior components this round may touch:
  - main
  - status
  - history

## Verification
  - Build and run tests after modification, e.g. `bash -n <changed script>`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================