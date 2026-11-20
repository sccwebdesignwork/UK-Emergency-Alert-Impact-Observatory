# UK Emergency Alert Impact Observatory

[![SCC Nexus](https://sccnexus.co.uk/assets/brand/scc-nexus-wordmark.webp)](https://sccnexus.co.uk/)

An **SCC Nexus** public-interest research observatory: https://sccnexus.co.uk/

Public, evidence-led companion to the private UK Emergency Alert Impact Research engine. The programme follows the SCC Nexus discipline **Search · Corroborate · Communicate**.

The Observatory publishes only validated, non-sensitive outputs. It does **not** treat statistical association as proof of causation and does not publish personal or identifiable safeguarding/health records.

## Public site

https://sccwebdesignwork.github.io/UK-Emergency-Alert-Impact-Observatory/

SCC Nexus project brief: https://sccnexus.co.uk/projects/emergency-alert-impact.html

News and verified source log: https://sccwebdesignwork.github.io/UK-Emergency-Alert-Impact-Observatory/news.html

## Current status — 20 November 2026

This is a **status-only** public evidence surface. The older August figures remain in Git history but are withheld pending independent numerical reconciliation with the November research candidate. No scientific claim of alert-caused injury or safety is approved.

- 2023 and 2025: retrospective national test analyses under review.
- 8 January 2026 and 14 August 2026: official geographically targeted weather/wildfire alerts documented.
- For actual warnings use the official https://www.gov.uk/alerts/current-alerts page.

## Publication controls

A `data/evidence.json` update is not enough to secure a static site with hard-coded results. The Pages workflow now validates **all public HTML**, the non-numeric status record and the front-end script before release. Run `python -m unittest discover -s tests -v` and `python scripts/validate_public_site.py .` before pushing.

The private Research repository owns scientific code. The SCC Control Tower owns decisions; the Drive history retains original evidence. A green CI run is not peer-review or publication approval.

## Contact, corrections and collaboration

**hello@sccnexus.co.uk**  
https://sccnexus.co.uk/contact.html

Factual corrections, source suggestions, methodological challenges and research collaboration are welcome. Please do not send credentials or sensitive personal records by email.

## GitHub Pages

The included Pages workflow publishes the static site from `main`. Repository Pages must be configured to use **GitHub Actions**. The workflow intentionally uses the repository-scoped `GITHUB_TOKEN` permissions (`pages: write`, `id-token: write`) rather than a personal access token.
