========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - lib/common.sh is depended on by 8 files (e.g. lib/manifest.sh, lib/depgraph.sh, lib/cache.sh, lib/journal.sh); changing it ripples widely.
  - lib/manifest.sh is depended on by 7 files (e.g. lib/common.sh, lib/depgraph.sh, lib/builder.sh, lib/reporter.sh); changing it ripples widely.
  - lib/cache.sh is depended on by 3 files (e.g. lib/builder.sh, tests/run_tests.sh, lib/reporter.sh); changing it ripples widely.
  - lib/depgraph.sh is depended on by 3 files (e.g. lib/cache.sh, lib/builder.sh, tests/run_tests.sh); changing it ripples widely.
  - lib/journal.sh is depended on by 2 files (e.g. lib/builder.sh, tests/run_tests.sh); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - lib/common.sh: implementation
  - lib/manifest.sh: implementation
  - lib/cache.sh: implementation
  - lib/depgraph.sh: implementation
  - lib/journal.sh: implementation
  - lib/builder.sh: implementation
  - lib/artifact.sh: artifact storage
  - lib/configgen.sh: implementation
Prior components this round may touch:
  - lib/manifest.sh (parse_manifest / get_manifest_value extended to read [targets] and [hooks] sections)
  - lib/builder.sh (build_package and test_package gain pre/post hook invocation; new cmd_run/cmd_hooks/cmd_targets)
  - lib/journal.sh (journal_append_event emits hook_run and target_run event types)
  - lib/common.sh (CLI dispatch and usage text register run/hooks/targets commands)

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================