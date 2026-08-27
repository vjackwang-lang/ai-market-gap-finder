# Changelog

## 1.6.2 — 2026-08-26

- Privacy hardening after the first live PostHog readback: PostHog had automatically enriched the opted-in test event with GeoIP-derived city/country/coordinate fields.
- The telemetry client now sends `$geoip_disable: true` on every PostHog event to explicitly disable GeoIP enrichment.
- Live V1.6.2 privacy readback passed: new events had `$geoip_disable=true` and no GeoIP-derived country/city/coordinate fields.
- Fixed release-version telemetry labeling: publisher config now always supplies `skill_version=1.6.2`, so the frozen scoring criteria version `1.6.1` cannot override it.
- Added short-window local idempotency for completed-scan / Winner-Benchmark / Event-Radar events after live readback showed duplicate host sends ~30 seconds apart.
- Kept `$process_person_profile: false`, the strict coarse-field allowlist, explicit opt-in, fail-closed consent, and zero-impact network-failure behavior.
- No opportunity discovery, scoring, Winner Benchmark, feasibility, kill-gate, or commercial-logic changes. Scoring criteria remain frozen at 1.6.1.

## 1.6.1 — 2026-08-26

- Added one-time local telemetry consent manager and fail-closed first-run opt-in protocol.
- Configured official public release for PostHog Cloud US using a Project ingestion token; no Personal API key is packaged.
- Moved anonymous ID and consent state to `~/.opportunity-finder/` so updates do not overwrite user choice.
- Disabled PostHog person-profile processing and preserved the strict coarse-field allowlist.
- Telemetry/network failures can no longer interrupt the core Skill workflow.

## 1.6.1-public-telemetry-rc

- Added PostHog-ready optional telemetry transport while preserving telemetry OFF by default.
- Added strict HTTPS enforcement and kept the existing field allowlist.
- Added `POSTHOG_SETUP.md`; publisher telemetry remained pre-setup in 1.6.0.
- No scoring, discovery, kill-gate, or business-logic changes.

## V1.6.1 — Public Free Release

- Promoted the host-tested V1.6 core from release candidate to public free release packaging.
- Added deterministic `render_source_ledger.py` so public reports retain clickable full-scheme source links.
- Fixed telemetry template version to 1.6.1.
- Added public privacy notice, marketplace listing copy, demo script, publish checklist, live-host acceptance summary, and lightweight brand assets.
- Core opportunity scoring and decision thresholds remain frozen; no post-validation feature creep was added.

## V1.6.1 — Traceability + Mandatory Winner Benchmark

- Added `references/source-traceability.md`.
- Material demand, competition, pricing, install/growth, platform-capability, and implementation claims now require original source URLs and dates/observation dates.
- Final reports must include a compact Source Ledger; untraceable material claims must be marked unverified and cannot promote a candidate to SHIP.
- Broad scans now require at least one traceable Winner Benchmark before concluding zero-SHIP.
- Winner Benchmarks must capture job-to-be-done, signal-quality caveats, and an adjacent unresolved job; raw install magnitude alone does not count.
- `validate_scan.py` now validates domain coverage, source traceability, and Winner Benchmark completeness deterministically.
- Added regression tests for missing source URLs, missing Winner Benchmark, and incomplete winner adjacency.
- Preserved V1.5 host-ready folder naming and telemetry-off-by-default behavior.

## V1.5.0 — Host-Ready Packaging

- Standardized distributable root folder to `opportunity-finder/` to match Agent Skills frontmatter name.
- Added host-layout smoke tests for `.agents/skills/` and `.codebuddy/skills/` conventions.
- Preserved V1.4 live-scan scoring, feasibility gates, competition maturity, platform incident quarantine, and exploration coverage validation.
