# Publication Guard

The public guard checks the candidate tree for generic publication risks without storing real private project names in version control.

It always checks for generic contamination patterns, prohibited artifact extensions, machine-specific paths, simulated credential syntax, raw-report paths, binary/non-UTF-8 files, private datasets, and trading-account exports.

An optional private denylist can be supplied with `PUBLICATION_PRIVATE_DENYLIST_FILE`. That file must live outside this repository, must never be committed, and may contain real private terms for a local-only scan. If a private denylist match is found, the guard reports only `private_denylist_match_detected` and a masked value.

The guard must pass without an external denylist so public CI remains reproducible.
