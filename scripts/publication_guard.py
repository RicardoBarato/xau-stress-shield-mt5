import os
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

FORBIDDEN_EXTENSIONS = {
    ".ex5",
    ".set",
    ".tst",
    ".log",
    ".html",
    ".htm",
    ".csv",
    ".xlsx",
    ".zip",
    ".env",
}

GENERIC_PATTERNS = [
    re.compile(r"\b[A-Z0-9]+_" + r"PRIVATE_" + r"RESEARCH\b", re.IGNORECASE),
    re.compile(r"\b" + r"INTERNAL_" + r"PROJECT_" + r"[A-Z0-9_]+\b", re.IGNORECASE),
    re.compile(r"\b" + r"PRIVATE_" + r"REPOSITORY_" + r"(?!SENTINEL\b)[A-Z0-9_]+\b", re.IGNORECASE),
    re.compile(r"\bunreleased\.[a-z0-9.-]+\.invalid\b", re.IGNORECASE),
    re.compile(r"\b[A-Z]:\\[^\r\n]*", re.IGNORECASE),
    re.compile(r"\b(account|account_id|account_number|login|server|password|token|api_key)\s*[:=]", re.IGNORECASE),
    re.compile(r"\b(credentials|secrets|raw_reports|raw-reports|reports/raw|data/raw)[/\\]", re.IGNORECASE),
    re.compile(r"\b(" + r"private_" + r"dataset|" + r"trading_" + r"account_" + r"export|" + r"binary_" + r"artifact)\b", re.IGNORECASE),
]


def mask_term(term):
    if len(term) <= 4:
        return "***"
    return f"{term[:2]}***{term[-2:]}"


def load_private_denylist():
    denylist_path = os.environ.get("PUBLICATION_PRIVATE_DENYLIST_FILE")
    if not denylist_path:
        return []
    path = pathlib.Path(denylist_path).expanduser().resolve()
    if not path.is_file():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def iter_candidate_files(root):
    for path in root.rglob("*"):
        rel_parts = set(path.relative_to(root).parts) if path != root else set()
        if ".git" in path.parts or "__pycache__" in rel_parts or path.is_dir():
            continue
        yield path


errors = []
private_terms = load_private_denylist()

for path in iter_candidate_files(ROOT):
    rel = path.relative_to(ROOT)
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        errors.append(f"forbidden extension: {rel}")
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"binary or non-utf8: {rel}")
        continue
    for pattern in GENERIC_PATTERNS:
        if pattern.search(text):
            errors.append(f"generic_policy_match_detected: {rel}")
            break
    for term in private_terms:
        if term.lower() in text.lower():
            errors.append(f"private_denylist_match_detected: {rel}: {mask_term(term)}")
            break

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("publication_guard_passed")
