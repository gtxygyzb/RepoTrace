========================================================================
[RepoTrace] Repository guidance for the current request (round 9)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - helpers.go is depended on by 4 files (e.g. main.go, schema.go, manifest.go, cli.go); changing it ripples widely.
  - main.go is depended on by 2 files (e.g. schema.go, cli.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - helpers.go: implementation
  - main.go: CLI entry point
  - manifest.go: implementation
  - schema.go: implementation
  - cli.go: implementation
  - types.go: implementation
Prior components this round may touch:
  - buildRejects (round 3 rejects output)
  - writeAuditLog / audit-log feature (round 3) — tagged rejects is a projection of audit-log reject records
  - --dedup-policy first-arrival trailing columns (round 6)
  - buildManifest / writeManifest / writeSignature (round 5) — manifest/signature must reflect chosen rejects bytes
  - schema sidecar digest (round 8) — schema/digest must reflect chosen rejects bytes
  - ingest (rounds 4, 7) — flow must plumb rejects-format config

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================