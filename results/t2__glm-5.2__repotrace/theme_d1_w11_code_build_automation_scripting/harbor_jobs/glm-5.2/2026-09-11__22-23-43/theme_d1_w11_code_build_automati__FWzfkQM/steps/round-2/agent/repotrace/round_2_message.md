========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - lib/manifest.sh is depended on by 7 files (e.g. lib/common.sh, lib/depgraph.sh, lib/builder.sh, lib/reporter.sh); changing it ripples widely.
  - lib/common.sh is depended on by 6 files (e.g. lib/manifest.sh, lib/depgraph.sh, lib/builder.sh, lib/configgen.sh); changing it ripples widely.
  - lib/cache.sh is depended on by 2 files (e.g. lib/builder.sh, tests/run_tests.sh); changing it ripples widely.

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
  - lib/builder.sh: setup_build_env/build_package/test_package must become profile-specific and support parallel scheduling/output buffering
  - lib/cache.sh: init_cache/is_cache_valid/update_cache/invalidate_cache/clean_cache must become profile-namespaced and profile-scoped
  - lib/artifact.sh: pack_artifact must produce profile-specific archive names and source from profile build dirs
  - lib/depgraph.sh: build_dep_map/resolve_build_order are reused for parallel readiness and extended with DOT graph/reverse-dependency output
  - lib/common.sh: clean_package must become profile-scoped

## Verification
  - Build and run tests after modification, e.g. `make`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================