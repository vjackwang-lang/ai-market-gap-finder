# QA Report — Opportunity Finder 1.6.2 Public Free Release

Date: 2026-08-26

## Status

**PASS — privacy-hardened public package is host-ready. Live readback confirmed GeoIP enrichment is absent on new events.**

## Offline validation

- 63/63 automated tests PASS after V1.6.2 privacy hardening and release-version telemetry regression coverage.
- Python compile PASS.
- Agent Skills parent directory matches `name: opportunity-finder`.
- `SKILL.md` remains below 500 lines.
- Quick-Commerce scoring / feasibility / competition / source-traceability / Winner gates unchanged except metadata version bump.
- Public Source Ledger renderer keeps full clickable `https://` URLs.

## Telemetry validation

- Official publisher defaults point to PostHog Cloud US.
- Only a PostHog **Project token** (`phc_...`) is packaged; no Personal API key/admin secret is packaged.
- No user consent state is packaged. Missing/unknown/malformed consent fails closed.
- First-run protocol asks once; No retains full Skill functionality.
- Consent and anonymous UUID persist outside the Skill directory under `~/.opportunity-finder/`.
- Strict telemetry allowlist rejects prompts, arbitrary queries, URLs, files, API keys, reports, emails, company/customer names, private repo data, and raw evidence.
- PostHog person-profile processing is disabled on emitted events.
- PostHog GeoIP enrichment is explicitly disabled with `$geoip_disable: true`.
- Telemetry network errors cannot interrupt the core Skill workflow.
- Duplicate completed-scan telemetry is suppressed locally for a short window so host retries do not inflate usage counts; failed sends remain retryable.

## Live readback result

- Live opted-in WorkBuddy events arrived with `$geoip_disable=true`.
- New events had no GeoIP-derived country, city, latitude, or longitude fields.
- A release-label mismatch was found and fixed offline: telemetry now ignores any agent-supplied `skill_version` and always uses publisher config `1.6.2`.
- No additional CEO-side rerun is required because this final change is a deterministic metadata override covered by regression tests.
