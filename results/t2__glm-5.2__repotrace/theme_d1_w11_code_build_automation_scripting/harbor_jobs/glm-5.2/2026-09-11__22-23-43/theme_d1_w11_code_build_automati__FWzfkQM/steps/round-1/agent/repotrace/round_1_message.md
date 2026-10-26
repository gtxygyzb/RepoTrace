========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - lib/manifest.sh is depended on by 7 files (e.g. lib/common.sh, lib/configgen.sh, lib/depgraph.sh, lib/reporter.sh); changing it ripples widely.
  - lib/common.sh is depended on by 4 files (e.g. lib/manifest.sh, lib/configgen.sh, lib/builder.sh, lib/artifact.sh); changing it ripples widely.
  - lib/cache.sh is depended on by 2 files (e.g. tests/run_tests.sh, lib/builder.sh); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - lib/manifest.sh: implementation
  - lib/common.sh: implementation
  - lib/cache.sh: implementation
  - lib/configgen.sh: implementation
  - lib/artifact.sh: artifact storage
  - lib/builder.sh: implementation
  - lib/depgraph.sh: implementation
  - lib/reporter.sh: report generation

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================