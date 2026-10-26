========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
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
  - WAL (binary format change — AppendSingle/AppendBatch/Replay must read/write expire_at)
  - MemTable (PointEntry struct gains expire_at; Add/AllEntries/EntriesInRange/PrefixScan/RangeTombstones must filter or expose expiration)
  - SSTable / SSTableReader (data block entry format change adds expire_at after seqnum)
  - Engine (GET/SCAN/STATS/TTL command logic must account for expiration and MVCC visibility)
  - CLI main (PUT/TX_PUT/BATCH PUT parsing gains --ttl flag; new TTL command; STATS output changes)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================