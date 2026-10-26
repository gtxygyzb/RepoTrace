========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
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
  - internal/engine/engine.go (rounds 2,3,5: SSTable writers/readers, compaction, memtable flush, indexes/bloom filters must be rebuilt)
  - internal/mvcc/snapshot.go (rounds 2,6: snapshot state and cursors must be invalidated on RESTORE)
  - internal/tx/transaction.go (transactions must be invalidated on RESTORE)
  - internal/mvcc/seqnum.go (round 2: seqnum counter must be resettable to restored max)
  - internal/wal/wal.go (round 7: WAL segment files must be cleared and re-initialized on RESTORE)
  - cmd/kvstore/main.go (rounds 2,4,6: command dispatch must add BACKUP/RESTORE commands)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================