# Scripts Layout

This directory groups non-manuscript Python helpers so the workspace root stays focused on active paper, protocol, and entry-point files.

- `analysis/` contains active analysis implementations. Root-level wrappers remain in place for backward-compatible entry points such as `python print_results.py`.
- `maintenance/` contains one-off repair, download, and extraction utilities that are not part of the normal experiment pipeline.

When reorganizing scripts, preserve the root wrappers for any command already referenced by documents or previous session notes.