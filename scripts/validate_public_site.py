"""SCC/VVIP fail-closed status-only site release guard.

Validate the deployed static pages as well as evidence.json; a JSON-only
review cannot guarantee that old hard-coded scientific claims disappear.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

STATUS = "methodology_under_independent_review"
WITHHELD = "withheld_pending_independent_review"
PAGES = ("index.html", "news.html", "methodology.html")
UNAPPROVED_PATTERNS = {
    "reported rate ratio": r"\bRR\s*[0-9]",
    "empirical p-value": r"\bempirical\s+p\s*[=:]?\s*0?\.",
    "numeric control mean": r"\bcontrol\s+mean\s*[=:]?\s*[0-9]",
    "scientific headline of excess": r"\bthe primary result is currently negative\b",
    "legacy count": r"\b205,757\b",
}


def validate(root: Path) -> list[str]:
    errors = []
    try:
        evidence = json.loads((root / "data/evidence.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Missing or invalid public evidence record: {type(exc).__name__}"]
    for key, expected in (
        ("study_status", STATUS), ("scientific_results_status", WITHHELD),
        ("publication_approved", False), ("causal_claim_allowed", False),
        ("historical_results", []),
    ):
        if evidence.get(key) != expected or (
            isinstance(expected, bool) and type(evidence.get(key)) is not bool
        ):
            errors.append(f"Unapproved evidence field: {key}")
    for forbidden in ("exploratory_signal", "historical_primary_results", "all_analysis_windows"):
        if forbidden in evidence:
            errors.append(f"Scientific estimate field forbidden in public payload: {forbidden}")
    for filename in PAGES:
        try:
            html = (root / filename).read_text(encoding="utf-8")
        except OSError:
            errors.append(f"Missing public page: {filename}")
            continue
        for label, regex in UNAPPROVED_PATTERNS.items():
            if re.search(regex, html, flags=re.IGNORECASE):
                errors.append(f"{filename}: {label}")
        if filename == "index.html" and "withheld" not in html.lower():
            errors.append("index.html: no visible results-withheld explanation")
    try:
        script = (root / "assets/app.js").read_text(encoding="utf-8")
    except OSError:
        errors.append("Missing front-end script")
    else:
        for token in ("data-r23", "data-r25", "rate_ratio", "empirical_one_sided_p", "innerHTML"):
            if token in script:
                errors.append(f"Front-end script may display unreviewed data: {token}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    errors = validate(parser.parse_args().root)
    if errors:
        for issue in errors:
            print(f"FAIL: {issue}")
        return 1
    print("PASS: Public Observatory status-only; scientific results withheld.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
