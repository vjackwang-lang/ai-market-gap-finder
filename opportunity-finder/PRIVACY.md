# Privacy Notice — Opportunity Finder

Opportunity Finder is designed to run primarily inside the user's own Agent host, using the user's own model/search/tool access where available.

## Default behavior

- Anonymous product telemetry requires **explicit opt-in** before the first network event is sent.
- If consent state is unknown, telemetry behaves as OFF.
- Declining telemetry does not reduce any Skill feature.
- Consent is stored locally under `~/.opportunity-finder/telemetry.json` (or `OPPORTUNITY_FINDER_HOME`). A small `telemetry_dedupe.json` file stores only recent event fingerprints/timestamps to prevent duplicate analytics counts; it contains no prompt, URL, file, report, or evidence content.
- The local portfolio ledger stays local and makes no network calls.

## What the public package contains

The package contains a PostHog **Project token** and US ingestion host so opted-in events can reach the publisher's analytics project. A Project token is used only for event ingestion and is not a personal/admin API credential.

## Never collected by the bundled telemetry client

The client rejects prompt text, arbitrary user queries, file names/content, URLs, API keys/tokens, generated reports, company/customer names, email addresses, private repository names/content, and raw evidence records.

## Optional opt-in telemetry

Only coarse product-usage fields from the strict allowlist may be sent: platform, Skill version, scan mode, broad category, time window, SHIP/TEST/WATCH/SKIP result counts, portfolio role, and coarse actions/feedback. PostHog person-profile processing is disabled for these events. The client also sends `$geoip_disable: true` so PostHog does not enrich opted-in events with GeoIP-derived city, country, postal-code, or coordinate properties.

## Disable at any time

`python scripts/telemetry_consent.py disable`

See `references/telemetry-policy.md` for the full field policy.
