# PostHog Telemetry Setup

Opportunity Finder 1.6.2 uses optional, anonymous, coarse product telemetry through PostHog Cloud US. Core Skill functionality does not depend on telemetry.

## Publisher configuration

The official public package is already configured with the publisher's PostHog **Project token** and US ingestion host in `config/telemetry.defaults.json`. This is an ingestion identifier, not a Personal API key. Forks should replace it with their own Project token using `config/telemetry.example.json` as a template.

- Host: `https://us.i.posthog.com`
- Event endpoint: `https://us.i.posthog.com/i/v0/e/`
- Event prefix: `opportunity_finder_`

## Consent

The Skill must ask once before enabling telemetry. Use:

```bash
python scripts/telemetry_consent.py status
python scripts/telemetry_consent.py enable --platform workbuddy
python scripts/telemetry_consent.py disable --platform workbuddy
```

Never silently enable telemetry. A user who declines keeps full functionality.

Every PostHog event sets `$process_person_profile: false` and `$geoip_disable: true`; the latter explicitly disables GeoIP-derived location enrichment.

## Allowed data

Only coarse usage such as platform, Skill version, scan mode, broad category, time window, SHIP/TEST/WATCH/SKIP counts, portfolio role, coarse action, and coarse feedback. Prompts, files, URLs, API keys, reports, private project names, emails, and raw evidence are rejected.

## QA event

After consent is enabled in a test home directory, a test event can be sent with `scripts/telemetry_client.py`. Confirm it appears as `opportunity_finder_scan_completed` in PostHog before public launch.
