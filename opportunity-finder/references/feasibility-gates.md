# Feasibility Gates V1.4

Demand is not enough. A candidate cannot be a Quick-Commerce `SHIP` unless a third-party Skill/tool can actually reach and change the required surface through a stable, testable path.

## Gate 1 — Surface accessibility

Identify every required surface: local files, public web, browser DOM, documented API, plugin API, database file, desktop app state, proprietary cloud project state, payment state, etc.

Hard reject when the product's core value requires a surface that the proposed distribution format cannot access reliably. Do not assume a Skill can read another product's private cloud state, internal UI database, scheduled-task registry, or undocumented private API.

## Gate 2 — Concrete implementation path

Before `SHIP`, name at least one implementable path:

- stable documented API;
- local file/database format that can be safely read/written;
- browser/DOM workflow the host is allowed to automate;
- open-source library with a fixture-based test path;
- supported plugin/extension interface.

If no concrete path exists, set `no_concrete_implementation_path=true` and `SKIP` or redesign the product.

## Gate 3 — Build-estimate confidence

A fast estimate is not evidence. State:

- required surfaces;
- stable interfaces/libraries;
- minimum test fixture;
- permissions/OS assumptions;
- build-estimate confidence from 0 to 1.

A candidate with low confidence cannot `SHIP` even if its numerical score is high.

## Gate 4 — Workaround friction

Measure the current workaround, not just the complaint.

- 0–2 minutes, documented toggle/settings fix: usually not a paid product.
- <5 minutes and rarely repeated: apply `trivial_workaround` unless a free anchor has a clear strategic asset.
- repeated manual workaround, fragile multi-step process, or material failure risk: higher score.

A platform migration problem can look severe in community posts while the actual fix is one setting. Search official docs and current comments before scoring.

## Gate 5 — Platform fix status

If the platform has already documented the new behavior, is actively rolling out a native fix, or has an official migration path, apply `platform_fix_in_progress` or `platform_capture_soon` as appropriate.

Event SKUs remain valid only when the remaining gap is concrete enough to ship before the native fix closes the window.

## Gate 6 — Private/unstable dependency

Avoid products whose core function depends on reverse-engineered private APIs, undocumented cloud state, or brittle internal databases unless:

- the dependency is read-only and recoverable;
- breakage risk is explicit;
- support burden is compatible with the price;
- the opportunity is intentionally short-lived.

Otherwise apply `unstable_private_api_dependency` or hard reject if there is no stable path.

## Gate 7 — Platform incident quarantine

Before treating a fresh complaint as a product opportunity, ask whether a third party actually controls a stable repair surface. Vendor outages, auth failures, backend quota regressions, and official-client bugs with no stable local repair path are `platform_incident_only` and hard-reject. See `platform-incident-quarantine.md`.
