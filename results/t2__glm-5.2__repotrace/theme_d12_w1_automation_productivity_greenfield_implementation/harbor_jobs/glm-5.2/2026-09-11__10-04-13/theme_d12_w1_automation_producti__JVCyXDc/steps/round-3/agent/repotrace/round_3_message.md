========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - cmd/flowr/main.go: CLI entry point
New in this round (to be created):
  - go.mod
Prior components this round may touch:
  - R1 retries: scalar form must coexist with structured retry: and remain fixed/initial_ms=100
  - R1/R2 report.json schema: new retry_attempts field on every step entry, conditionally_skipped status with its neutral field set
  - R1/R2 events.ndjson: new step_conditionally_skipped event; retry_delay_ms field on retry step_started events
  - R1/R2 DAG scheduler: must evaluate when before launch, treat conditionally-skipped dependents as eligible, exclude skipped steps from order_attempted
  - R2 content-addressed cache: conditionally-skipped steps bypass cache entirely (no lookup, no write, no cache_key file)
  - R2 resource reservations: conditionally-skipped steps must not reserve resources

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================