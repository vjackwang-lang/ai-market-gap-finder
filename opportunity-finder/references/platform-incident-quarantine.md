# Platform Incident Quarantine — V1.4

Fresh pain is not automatically a product opportunity.

Quarantine a signal as `platform_incident_only=true` when its root cause is mainly controlled by the platform vendor and a third party lacks a stable user-controlled repair surface. Examples:

- vendor backend outage;
- authentication outage or account-side authorization loop;
- temporary quota-policy regression;
- official desktop client regression that only the vendor can patch;
- cloud service capacity problem;
- inaccessible private server-side state.

Do **not** quarantine when there is a stable local repair or prevention path that a third party can actually own, such as:

- repairing documented local files/databases;
- converting a public/stable file format;
- preflight validation before a vendor action;
- local backup/restore through documented interfaces;
- deterministic migration through a supported API.

The point is to stop Event Radar from becoming an outage-news generator.
