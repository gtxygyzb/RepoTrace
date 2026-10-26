========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - lib/manifest.sh is depended on by 7 files (e.g. lib/common.sh, lib/depgraph.sh, lib/builder.sh, lib/reporter.sh); changing it ripples widely.
  - lib/common.sh is depended on by 6 files (e.g. lib/manifest.sh, lib/depgraph.sh, lib/builder.sh, lib/configgen.sh); changing it ripples widely.
  - lib/cache.sh is depended on by 3 files (e.g. lib/builder.sh, tests/run_tests.sh, lib/reporter.sh); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - lib/manifest.sh: implementation
  - lib/common.sh: implementation
  - lib/cache.sh: implementation
  - lib/builder.sh: implementation
  - lib/depgraph.sh: implementation
  - lib/artifact.sh: artifact storage
  - lib/configgen.sh: implementation
  - lib/reporter.sh: report generation
Prior components this round may touch:
  - lib/cache.sh (round 1 transitive cache invalidation, round 2 cache profiles)
  - lib/common.sh clean_package (used by builder/clean flows)
  - lib/builder.sh (round 2 parallel build/clean integration)

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================