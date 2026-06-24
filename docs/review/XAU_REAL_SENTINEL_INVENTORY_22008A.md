# XAU Real Sentinel Inventory 22008A

Status: real_sentinels_found_and_removed.

Pre-remediation inventory found encoded private sentinel material in:

- `scripts/publication_guard.py`
- `tests/test_xau_stress_shield_public_candidate_guard.py`

Report placeholders:

- PRIVATE_PROJECT_SENTINEL_A
- PRIVATE_PROJECT_SENTINEL_B
- PRIVATE_REPOSITORY_SENTINEL
- PRIVATE_DOMAIN_SENTINEL

No real private project names are reproduced in this report.

Decision: the old local history had to be rebuilt because the original root commit contained the encoded sentinel material.
