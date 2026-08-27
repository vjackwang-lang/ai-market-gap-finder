# Privacy-First Telemetry Policy

Telemetry exists to learn which opportunity categories and features are useful without collecting user work product.

## Consent gate

Telemetry is fail-closed. If local consent is missing, malformed, or explicitly declined, no event is sent. The Agent must ask once before enabling telemetry and must never infer consent. Declining does not reduce core functionality.

## Allowed coarse fields

- event type;
- anonymous local UUID used only as the event `distinct_id`;
- platform/agent;
- Skill version;
- scan mode;
- coarse opportunity category;
- scan time window;
- SHIP/TEST/WATCH/SKIP result counts;
- coarse action: continue / generate-spec / export / dismiss;
- portfolio role;
- coarse feedback value.

## Forbidden by design

The telemetry client rejects prompt text, arbitrary user queries, file names/content, URLs, API keys/tokens, generated reports, company/customer names, emails, private repository names/content, and raw evidence records.

## Destination

The public release uses PostHog Cloud US ingestion. The bundled `phc_...` Project token is an ingestion identifier, not a personal/admin API credential. Personal API keys must never be packaged. Events set `$process_person_profile=false`.

## Local state

`telemetry_consent.py` stores only consent state, coarse host/platform, and update time under `~/.opportunity-finder/telemetry.json` (or `OPPORTUNITY_FINDER_HOME`). A random anonymous UUID is stored separately in the same local directory.

## Failure behavior

Network or telemetry errors are swallowed and must never affect Opportunity Finder results.

## Location enrichment

For the official PostHog transport, every emitted event must include both `$process_person_profile: false` and `$geoip_disable: true`. The second flag prevents PostHog from deriving location properties from the network request. Opportunity Finder does not intentionally collect precise or coarse location as product telemetry.

## Duplicate suppression

Completed-scan / Winner-Benchmark / Event-Radar telemetry is locally idempotent for a short window. The client stores only SHA-256 fingerprints of already-sent coarse events plus timestamps under `~/.opportunity-finder/telemetry_dedupe.json`. This prevents host retries from double-counting one run. Feedback and candidate-action events are not deduplicated.
