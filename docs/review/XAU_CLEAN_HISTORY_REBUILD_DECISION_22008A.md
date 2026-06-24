# XAU Clean History Rebuild Decision 22008A

Classification: clean_root_rebuild_required_and_prepared.

Reason:

The original local root commit contained encoded private sentinel material in the publication guard and guard tests. A successor commit would not be enough because the old commit would remain reachable in the local sanitized history.

Decision:

- rebuild local repository history as a new root commit;
- keep branch name `main`;
- keep no remote configured;
- ensure the old commit is not reachable;
- preserve documentation-only content;
- do not perform any remote action.

Post-rebuild requirement:

- final local history must contain one sanitized root commit;
- the original commit must not be reachable;
- publication guard and tests must pass after the rebuild;
- final commit and tree hashes must be recorded outside the repository in the local mission report.
