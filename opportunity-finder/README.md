# Opportunity Finder V1.6 — Public Free Release

A free flagship Agent Skill for discovering fresh AI-native micro-product opportunities and studying what already wins in Skill/plugin/MCP ecosystems.

## Why this release exists

This public free release was hardened through live WorkBuddy host testing. V1.6 closes the two gaps found in the first host scan:

1. **Source Traceability Gate** — material claims must be traceable to original URLs plus source/observation dates. Install counts, prices, release dates, platform capabilities, competitor features, and demand claims cannot float as unsupported numbers.
2. **Mandatory Winner Benchmark** — a broad scan must benchmark at least one current winner and identify an adjacent unresolved job before it can conclude `0 SHIP`.

> Detect → Kill-test → Build → List → Collect → Grow / Harvest / Sell / Kill → Repeat.

A short-lived product can be successful if it ships quickly, costs almost nothing to operate, and captures cash, distribution, or useful first-party demand signals.

## Core rules

- **Installs are exposure, not payment.** Whole-repository installs, Packs, official distribution, and duplicate/fork effects can inflate apparent demand.
- **Winner ≠ clone target.** Study the unresolved job immediately before/after a winning Skill.
- **Broad scan requires a traceable Winner Benchmark.** A leaderboard mention without an original URL, observation date, signal-quality note, job-to-be-done, and adjacent unresolved job does not count.
- **Material claims need original sources.** Prefer official docs, original GitHub issues/repos, original community posts, marketplace pages, and first-party pricing pages over search snippets or AI summaries.
- **Use mature intelligence upstream.** BigIdeasDB, PainHunt, PainSignal, MonetScope, public web search, or user-owned MCP/data can be inputs; do not rebuild their databases.
- **Kill first.** Search for a free incumbent, platform-native fix, one-prompt substitute, support burden, and seller-paid runtime before recommending SHIP.
- **Prove it can actually be built.** Name the required surfaces, stable interfaces, test path, build-estimate confidence, and current workaround friction before SHIP.
- **Free must buy an asset.** A free flagship must target installs, ranking, reviews, author trust, opt-in telemetry, demand submissions, or related-product conversion.
- **Decision output, not idea spam.** Return at most three finalists with a launch hypothesis, economics, 30-second demo, source ledger, and stop condition.

## Core capabilities

- **Quick Commerce Scan** — fresh, small opportunities that can ship in hours.
- **Winner Benchmark** — reverse-engineer high-install/high-growth Skills and find adjacent unresolved jobs.
- **Event Radar** — find demand created by new models, releases, breaking changes, or new AI workflows.
- **Competition Kill Check** — actively search for free incumbents, platform fixes, and cheaper substitutes.
- **Seller Economics** — estimate build hours, cash cost, marketplace fee, runtime-cost owner, and break-even users.
- **Feasibility Gate** — reject inaccessible private state, undefined implementation paths, trivial workarounds, and fragile private-API dependencies.
- **Source Traceability Gate** — require original URLs and dates for material market claims and output a Source Ledger.
- **Competition Maturity** — separate early alternatives from a mature free incumbent instead of applying one blunt competition penalty.
- **Platform Incident Quarantine** — discard outages/backend regressions with no stable user-controlled product surface.
- **Exploration Coverage Gate** — broad scans must cover multiple workflow domains before declaring there is no SHIP candidate.
- **Portfolio Role** — FREE_ANCHOR / PAID_ACTIVATION / PAID_UTILITY / PAINKILLER / BUNDLE_COMPONENT / EVENT_SKU.
- **Privacy-first telemetry client** — optional, default OFF, strict coarse-field allowlist.

## Preferred economics

The Skill favors products where end users run their own Claude/Codex/WorkBuddy model, local scripts, or BYOK APIs. Seller marginal runtime cost should be close to zero whenever practical.

## Install

Use the Agent Skills-compatible installation method supported by the host client, or upload/import the entire `opportunity-finder` folder/package where local Skill import is supported. Do not rename the skill folder unless you also change the frontmatter `name`, because the Agent Skills specification requires them to match.

## Example prompts

- “Find three AI micro-products I can ship this weekend.”
- “Study the fastest-growing Skills and find adjacent unsolved jobs.”
- “Run Event Radar for the last 7 days of Claude/Codex ecosystem changes.”
- “Recheck this idea and try to kill it before I build.”
- “Estimate seller cost and break-even users for these candidates.”

## Deterministic scoring

```bash
python scripts/score_opportunities.py examples/candidates.example.json --pretty
```

The scorer uses only Python standard library and frozen weights in `config/criteria.json`.

For broad scans, validate exploration, Winner Benchmark, and source traceability:

```bash
python scripts/validate_scan.py candidates.json scored.json --pretty
```

A broad scan is incomplete if it lacks enough workflow domains, a traceable Winner Benchmark, or original-source evidence for its candidates.


## Traceable report output

For a deterministic clickable Source Ledger from a scan JSON:

```bash
python scripts/render_source_ledger.py candidates.json --output source-ledger.md
```

The renderer preserves full `https://` URLs and emits Markdown links so public reports do not silently strip source schemes.

## Telemetry

Telemetry is **explicit opt-in** and the core Skill works fully without it. The public package contains only a PostHog **Project token** for the publisher's analytics project; this is an ingestion identifier, not a personal/admin API secret.

On first use, the Skill checks local consent state and asks once before any network event is sent. Consent is stored locally under `~/.opportunity-finder/telemetry.json` (or `OPPORTUNITY_FINDER_HOME`). Users can disable telemetry at any time:

```bash
python scripts/telemetry_consent.py disable
```

Only coarse allowlisted usage fields can be transmitted. Prompts, arbitrary queries, URLs, files, reports, API keys, company/customer names, emails, private repository data, and raw evidence are rejected by design. See `PRIVACY.md` and `references/telemetry-policy.md`.

## Package contents

- `SKILL.md` — main agent workflow.
- `config/criteria.json` — frozen Quick-Commerce scoring and scan-gate rules.
- `config/telemetry.defaults.json` — publisher PostHog ingestion destination; consent is not stored here.
- `config/telemetry.example.json` — safe fork/publisher template.
- `POSTHOG_SETUP.md` — publisher setup and consent requirements.
- `scripts/score_opportunities.py` — deterministic scoring and simple unit economics.
- `scripts/validate_scan.py` — deterministic domain/Winner/traceability validation.
- `scripts/telemetry_client.py` — privacy-first telemetry client.
- `scripts/telemetry_consent.py` — one-time local opt-in/opt-out state manager.
- `scripts/local_ledger.py` — local-only portfolio learning ledger.
- `references/source-traceability.md` — original-source and Source Ledger rules.
- `references/` — business model, evidence, feasibility, competition, winner benchmark, signal hierarchy, telemetry rules.
- `examples/` — synthetic test candidate data.
- `tests/` — offline unit tests.
- `QA_REPORT.md` — release QA and live-host acceptance status.
- `LIVE_HOST_ACCEPTANCE.md` — sanitized evidence from the final WorkBuddy scan.
- `HOST_COMPAT_REPORT.md` — local host-layout smoke-test result.
- `PRIVACY.md` — concise public privacy notice.
- `MARKETPLACE_LISTING.md` — ready-to-use public listing copy.
- `DEMO.md` — 30-second demo script and evaluation prompt.
- `PUBLISH_CHECKLIST.md` — final publish steps.
- `assets/` — lightweight public brand assets.

## Internal vs public use

The public Skill may be used as the same scanning engine internally. Do **not** publish the company's private portfolio ledger, actual SKU revenue history, conversion data, or internal Opportunity Trader feedback model. Those are separate private assets.
