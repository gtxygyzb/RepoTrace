========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - internal/memtable/memtable.go: implementation
  - internal/mvcc/seqnum.go: implementation
  - internal/mvcc/snapshot.go: implementation
  - internal/tx/transaction.go: implementation
  - internal/wal/wal.go: implementation
New in this round (to be created):
  - internal/engine/engine.go
  - cmd/kvstore/main.go
Prior components this round may touch:
  - WAL single-file implementation (rounds 1, 2, 4)
  - Engine memtable flush and WAL truncation logic (rounds 1, 3)
  - Engine startup/replay path (round 1)
  - Server-side cursor implementation (round 6)
  - MVCC snapshot cursor iteration (round 6)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================