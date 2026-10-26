========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - lib/common.sh is depended on by 7 files (e.g. lib/manifest.sh, lib/depgraph.sh, lib/cache.sh, lib/builder.sh); changing it ripples widely.
  - lib/manifest.sh is depended on by 7 files (e.g. lib/common.sh, lib/depgraph.sh, lib/builder.sh, lib/reporter.sh); changing it ripples widely.
  - lib/cache.sh is depended on by 3 files (e.g. lib/builder.sh, tests/run_tests.sh, lib/reporter.sh); changing it ripples widely.
  - lib/depgraph.sh is depended on by 3 files (e.g. lib/cache.sh, lib/builder.sh, tests/run_tests.sh); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - lib/common.sh: implementation
  - lib/manifest.sh: implementation
  - lib/cache.sh: implementation
  - lib/depgraph.sh: implementation
  - lib/builder.sh: implementation
  - lib/artifact.sh: artifact storage
  - lib/configgen.sh: implementation
  - lib/reporter.sh: report generation
New in this round (to be created):
  - lib/journal.sh
Prior components this round may touch:
  - lib/builder.sh
  - lib/reporter.sh
  - lib/cache.sh
  - lib/common.sh
  - tests/run_tests.sh

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================