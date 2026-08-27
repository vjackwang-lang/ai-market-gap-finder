# Live Host Acceptance — WorkBuddy

Date: 2026-08-26
Status: PASS

The final V1.6 WorkBuddy run used the same natural-language test prompt as the prior host scan and did not require the user to manually invoke the Skill.

Observed acceptance results:

- `scan_complete: true`
- workflow domains covered: 5
- candidates evaluated: 10
- traceable Winner Benchmarks: 3
- candidates with traceable evidence: 10/10
- final decisions: 0 SHIP / 1 WATCH / 9 SKIP
- one WATCH candidate included a measurable recheck trigger instead of a forced build recommendation

The live run demonstrated the intended behavior: broad exploration, Winner Benchmarking, traceable evidence, kill-first discipline, technical/economic filtering, and willingness to return zero build recommendations.

Public-release polish added after the host run: Source Ledger rendering must preserve full URL schemes as clickable Markdown links.

## V1.6.2 privacy readback

A later opted-in WorkBuddy scan confirmed the privacy hardening in the live PostHog project:

- `$geoip_disable=true` on the new events
- no GeoIP-derived country, city, latitude, or longitude properties on the new events
- only the allowlisted coarse scan/result fields were present
- the scan itself completed with 13 candidates and 0 SHIP / 0 TEST / 0 WATCH / 13 SKIP

One release-metadata issue was discovered: the agent supplied the frozen scoring criteria version (`1.6.1`) as `skill_version`. The public package now ignores agent-supplied Skill version values and always uses publisher release config (`1.6.2`).
