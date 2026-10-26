========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
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
  - SSTable data block write format (round 3: writeSSTable/SSTableWriter)
  - SSTable data block read path (round 3: SSTableReader/readBlock)
  - CRC-32 per-block checksum (round 3) — must cover compressed bytes
  - VERIFY command (round 3) — must validate compressed blocks
  - compactL0ToL1 (round 3) — emits SSTables in new compressed format
  - SCAN/SNAP_SCAN/TX_SCAN commands (round 1+) — boundary semantics flip to exclusive end

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================