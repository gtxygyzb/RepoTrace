========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
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
  - cmd/kvstore/main.go
  - internal/engine/engine.go
Prior components this round may touch:
  - AppendSingle (op_type 4 encoding)
  - AppendBatch (batched MERGE entries)
  - Replay (decoding op_type 4)
  - PointEntry / AllEntries / EntriesInRange (memtable must expose merge entries for folding)
  - compactL0ToL1 (merge-run collapse respecting open snapshots)
  - writeSSTable / SSTableReader (persist and read op_type 4)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================