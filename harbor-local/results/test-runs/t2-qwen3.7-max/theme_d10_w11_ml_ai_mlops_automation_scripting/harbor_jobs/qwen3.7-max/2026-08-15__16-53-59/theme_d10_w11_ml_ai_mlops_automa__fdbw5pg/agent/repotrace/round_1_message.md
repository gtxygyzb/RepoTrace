========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize how this repository is organized and where
this request is likely to land. They are supplemental context — use
your own judgment to decide how to implement and verify the change.
========================================================================

## Where this request likely lands
  - main.go  (entry point; defines main)
Mentioned by the request but not present yet (likely to be created):
  - pipeline.go
  - executor.go
  - state.go
  - artifacts.go
  - report.go

## How the code connects
  The repository has 6 source file(s) and no detected cross-file dependency, so a change here is largely self-contained.

## What a change could affect
  No in-repository callers of the likely targets were detected — the change is unlikely to break other files.
========================================================================