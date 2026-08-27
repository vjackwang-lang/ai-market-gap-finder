---
name: opportunity-finder
description: Finds fresh AI-native micro-product opportunities worth shipping now by studying real demand, high-install/high-growth Skills, recent platform changes, and live competition. Uses kill-first validation, productizability gates, seller economics, and Quick-Commerce portfolio logic rather than generic startup ideation.
license: See LICENSE.txt
compatibility: Best with live web/search access. Optional deterministic scoring, local history, and privacy-first telemetry use Python 3.9+ standard library only. Designed for Agent Skills-compatible clients where supported.
metadata:
  version: "1.6.2"
  public-name: "Find Opportunities"
  aliases: "find-opportunities, opportunity-scout, micro-opportunity-hunter"
  target-market: "ai-power-users-and-solo-builders"
  objective: "quick-commerce-ai-micro-products"
  public-positioning: "free-flagship-category-anchor"
---

# Find Opportunities

Find **fresh opportunities worth shipping now**.

This Skill is not a generic startup idea generator, not a giant pain-point database, and not primarily an evaluator for an idea the user already has. It is optimized for solo AI builders who can ship Skills, MCP tools, CLIs, utilities, micro-apps, and other digital products quickly.

## Default commercial thesis

Unless the user overrides it:

> Detect → Kill-test → Build → List → Collect → Grow / Harvest / Sell / Kill → Repeat.

Prefer opportunities where:

- target users already use Claude Code, Codex, Cursor, OpenClaw, WorkBuddy, MCP, Skills, or adjacent AI-agent workflows;
- demand appeared recently or is visibly accelerating;
- users already congregate in a natural discovery channel;
- a useful product can ship in hours, preferably within one workday;
- seller cash cost and ongoing runtime cost are near zero;
- users can use their own model subscription, API key, local compute, or BYOK where practical;
- free buys a measurable asset, or a low price can trigger an impulse purchase;
- a short-lived product may still be successful if build and maintenance cost are low.

Long-term defensibility, subscriptions, and giant TAM are bonuses, not gates.

## Public flagship role

When this Skill itself is published, default role is `FREE_ANCHOR`.

It should earn one or more measurable assets:

- installs and category/search rank;
- reviews and author trust;
- optional privacy-safe usage signals;
- opt-in demand submissions;
- a natural entry point to related micro-products.

Do not secretly collect prompts, files, URLs, API keys, reports, company names, emails, or private repository data. See `references/telemetry-policy.md`.

## First-run privacy protocol

Before the first scan in a host that can execute local scripts:

1. Run `python scripts/telemetry_consent.py status`.
2. If `consent_state` is `unknown`, ask **once**:

   > Share anonymous usage data to improve Opportunity Finder? It sends only platform, Skill version, scan mode, broad category, time window, result counts, and coarse actions/feedback. It never sends prompts, files, URLs, API keys, reports, company/customer names, emails, private repository data, or raw evidence. Choosing No does not reduce any feature.

3. If the user says Yes, run `python scripts/telemetry_consent.py enable --platform <host>`.
4. If the user says No, run `python scripts/telemetry_consent.py disable --platform <host>`.
5. Never infer consent, never preselect Yes, and do not ask again after a stored Yes/No unless the user asks to change the setting.
6. If the consent helper cannot run, continue normally with telemetry OFF.

After a completed scan, if telemetry is enabled, send only the allowlisted coarse event via `scripts/telemetry_client.py`. Telemetry failure must never block or change the scan result.

## Core modes

### 1. Quick Commerce Scan

Find tiny opportunities that can plausibly ship in less than one workday and monetize or acquire users quickly.

### 2. Winner Benchmark

Study high-install, high-growth, high-rated, or newly trending Skills/plugins/MCP tools. Reverse-engineer:

- job-to-be-done;
- target user and platform;
- why the user installs instead of merely prompting the base model;
- discovery keywords / obvious product name;
- 30-second demo;
- current complaints and issues;
- manual step immediately before/after use;
- adjacent unresolved job;
- whether the winner belongs to a coherent product suite.

**Do not trust raw install counts blindly.** Read `references/signal-hierarchy.md` and `references/winner-patterns.md`.

### 3. Category Anchor Scan

Look for a narrow category where one free, obvious, useful Skill could become the discovery gateway for later related products.

A good anchor:

- solves a common entry problem;
- has an obvious search phrase;
- can remain free at near-zero marginal cost;
- naturally reveals adjacent paid/utility needs;
- does not depend on users browsing an author storefront.

### 4. Event Radar

Search for opportunities created by recent changes:

- new model or agent capabilities;
- breaking changes and regressions;
- API deprecations;
- marketplace/ranking/payment changes;
- new file formats;
- newly popular workflows that create second-order pain.

Event SKUs may have a short lifespan. That is acceptable if they can ship and sell before the window closes.

### 5. Recheck / Kill Test

Revisit a candidate and search only for evidence that changes the decision: new competitors, free substitutes, platform features, pricing evidence, demand changes, support burden, legal/distribution constraints, or a closing window.

## Target-user lock

Prioritize evidence from people already using:

- Claude Code / Claude Skills;
- Codex / Codex CLI;
- Cursor;
- OpenClaw;
- WorkBuddy;
- Gemini CLI or other agent-native environments;
- MCP-heavy workflows;
- AI-assisted professional workflows in research, design, engineering, automation, operations, creative work, and niche professions.

Do not restrict discovery to trade, e-commerce, B2B, or the builder's existing industry.

## Signal hierarchy

Prefer evidence closest to economic behavior:

1. actual payment / paid workaround;
2. repeated active usage or installs with independent usage evidence;
3. time or money spent on workarounds;
4. repeated recent complaints from independent sources;
5. explicit willingness-to-pay language;
6. search/install intent;
7. upvotes/stars/comments;
8. AI-generated scores and TAM estimates.

A high install number alone is not proof of active use or payment.

## Strong phrases to mine

- “I'm tired of…”
- “Every time I use…”
- “Why does Claude/Codex/Cursor keep…”
- “Does anyone have a skill/plugin for…”
- “I wish there was…”
- “My workaround is…”
- “I built this because…”
- “I still have to manually…”
- “This broke after the update…”
- “Is there a way to automate/fix/check…”

Also look for **second-order pain**:

> AI solved the original job, but real use created a new problem around reliability, compatibility, verification, state, cost, physical-world fit, handoff, quality, or workflow friction.

## Scan workflow

### Step 1 — Set freshness windows

Default: last **30 days**. Always inspect 24-hour and 7-day signals where sources allow it. Expand to 90–180 days only to establish recurrence.

### Step 2 — Run a traceable Winner Benchmark before broad discovery

For a **broad** scan, benchmark at least the configured minimum number of current winners before concluding the market has no attractive opportunity. Each benchmark must include a live original source URL and an observation date.

Inspect where available:

- Skills/agent leaderboards: All-time + Trending + Hot;
- official/curated Skills;
- GitHub stars/forks/issues/recent repositories;
- plugin/MCP marketplaces;
- Product Hunt / Hacker News launches;
- community posts showing installs, usage, or repeated adoption.

For each benchmark, record: product, source URL, observation date, signal type, signal-quality caveats, job-to-be-done, why the user installs it, the manual step before/after use, and at least one adjacent unresolved job. Read `references/winner-benchmark.md`.

For every apparent winner, identify whether the signal may be inflated or ambiguous because of:

- whole-repository installation;
- Pack/collection installation;
- official distribution advantage;
- detected duplicate/fork;
- abrupt growth without independent usage evidence.

If ambiguity is material, set `ambiguous_install_signal=true`.

### Step 3 — Quarantine platform incidents, then benchmark substitutes

Before spending scan budget on a candidate, identify its root cause. If the pain is primarily an outage, authentication failure, quota policy, backend regression, or official client bug and there is **no stable user-controlled repair surface**, classify it `platform_incident_only=true` and quarantine it. Do not turn every fresh platform incident into a third-party product idea.

Then check relevant categories described in `references/competitor-map.md`:

- pain databases / signal-mining platforms;
- opportunity feeds / radars;
- startup idea validators;
- open-source Claude/Codex validation Skills;
- generic idea generators.

Classify free competition as `none`, `emerging`, or `mature`. A few fresh alternatives can validate demand and receive only a small penalty; reserve `mature_free_incumbent` for an adopted, functionally complete free solution that materially closes the gap. See `references/competition-maturity.md`.

Do not rebuild mature data infrastructure if the same information can be accessed via public search, an existing tool, or a user's own subscription/API.

### Step 3A — Prove productizability before scoring

Read `references/feasibility-gates.md`. For each serious candidate, prove:

- the required product surface is actually accessible to the proposed Skill/tool;
- at least one stable implementation path exists;
- a fixture-based or sandbox test path exists;
- build-hour estimate has explicit confidence;
- the current workaround is not merely a documented toggle or sub-5-minute fix;
- current official docs do not already remove the pain.

If the core value requires inaccessible private cloud state, set `inaccessible_required_surface=true`. If no concrete implementation path can be named, set `no_concrete_implementation_path=true`.

A severe complaint is not automatically a product opportunity. Verify workaround friction and current platform behavior.

### Step 4 — Scan power-user communities without getting trapped in coding-agent bugs

Prioritize:

1. Reddit communities for Claude, Codex, Cursor, OpenClaw, AI agents, and relevant professions.
2. GitHub Issues/Discussions/feature requests/README “why I built this” explanations.
3. Skill/plugin/MCP marketplaces and their ratings/reviews/issues.
4. HN, Product Hunt, YouTube/X, specialist forums, and profession-specific communities when useful.

For a **broad** scan, cover at least the configured minimum number of distinct workflow domains before concluding there is no SHIP candidate. Include adjacent AI-assisted professional workflows such as research/knowledge, design/3D/CAD, office/data, creator/media, automation/operations, and niche professions. If most core coding-agent candidates die as platform bugs or crowded utilities, expand outward rather than repeatedly mining the same cluster.

Do not use SEO listicles as primary demand evidence.

### Step 5 — Collect evidence, not ideas

For each signal record:

- exact user/workflow;
- pain or desired outcome;
- current workaround;
- recurrence/frequency if inferable;
- cost of failure or annoyance;
- **original source URL and source/publication date when available; always record observation date**;
- claim type: demand / competition / platform / pricing / winner / other;
- whether the user already installs AI extensions/tools;
- whether the pain is caused/amplified by AI adoption;
- strongest behavioral/economic evidence level.

Do not cite a search-result summary when the original post, issue, repository, marketplace page, release note, or official documentation is available. Material numbers such as installs, stars, prices, dates, vote counts, competitor counts, or platform capabilities must be traceable to the source that supports them.

Use `references/evidence-schema.md` and `references/source-traceability.md`.

### Step 6 — Cluster and deduplicate

Merge semantically identical pains. One clever comment is not enough for SHIP unless it has unusually strong behavioral proof.

### Step 7 — Kill the candidate in three layers

Before scoring, record `competition.maturity` and whether the root cause is a platform-only incident.

**Market kill**

- mature strong free incumbent;
- platform feature already solving it;
- one prompt is sufficient;
- current official workaround takes only a few minutes;
- platform fix/migration path is already rolling out;
- the supposed gap is merely a missing filter in an established platform.

**Feasibility kill**

- the proposed Skill cannot access the required state or artifact;
- core behavior depends on undocumented/private APIs with no robust fallback;
- no concrete implementation library/API/interface can be named;
- build-hour estimate is mostly guesswork and cannot be tested on a fixture.

**Distribution kill**

- no obvious search phrase;
- users do not naturally install extensions/tools;
- requires paid ads or audience building;
- marketplace discovery is weak and no concentrated community exists.

**Economics kill**

- seller pays unbounded model/API cost;
- support burden can exceed likely product price;
- MVP is really a multi-week SaaS;
- legal/permission/payment complexity dominates the product.

Platform capture is a penalty, not an automatic rejection, when the window is open and the product can ship very fast.

### Step 8 — Classify portfolio role

Assign exactly one:

- `FREE_ANCHOR`
- `PAID_ACTIVATION`
- `PAID_UTILITY`
- `PAINKILLER`
- `BUNDLE_COMPONENT`
- `EVENT_SKU`

For `FREE_ANCHOR`, explicitly name the asset it buys from the allowlist in `config/criteria.json`. Free without an asset is penalized automatically.

### Step 9 — Calculate seller economics

Estimate:

- build hours;
- direct cash cost;
- internal hourly cost assumption;
- suggested price;
- marketplace fee;
- seller variable cost per paid user;
- runtime model/API cost owner: `user`, `seller`, `mixed`, or `none`;
- expected support burden;
- break-even paid users when price > 0.

Prefer local execution + BYOK + user-owned model/API + near-zero seller marginal cost.

Run:

`python scripts/score_opportunities.py candidates.json --pretty`

For a broad scan, also validate exploration coverage before declaring “nothing worth shipping”:

`python scripts/validate_scan.py candidates.json scored.json --pretty`

### Step 10 — Score Quick Commerce

Read `references/scoring-rubric.md`. Score 0–10 on:

- freshness;
- AI power-user density;
- evidence quality;
- repeated evidence;
- natural distribution;
- build speed;
- seller economics;
- technical feasibility;
- workaround friction;
- portfolio value;
- competition window;
- event tailwind.

Weights are frozen in `config/criteria.json`. Do not tune them to make a favorite idea pass.

A candidate cannot reach SHIP if evidence quality, technical feasibility, workaround friction, or build-estimate confidence is below the configured minimum even when the total score is high.

### Step 11 — Output no more than 3 finalists with source traceability

Before finalizing, build a compact **Source Ledger** containing every source used for material demand, competition, pricing, install/growth, platform-capability, and workaround claims. Every ledger row must include the original URL and observation/source date. For public Markdown output, render every source as a clickable Markdown link with the full `http://` or `https://` URL; never strip the URL scheme. When a scan JSON is available, prefer `python scripts/render_source_ledger.py candidates.json --output source-ledger.md` and reuse that ledger rather than retyping URLs.

For each finalist provide:

1. `SHIP / TEST / WATCH / SKIP`
2. one-sentence product job
3. target user
4. evidence summary + inline source links + source/observation dates
5. evidence quality level
6. current alternatives and why they do/do not kill it
7. build-hour estimate + confidence
8. required surfaces + concrete implementation path
9. workaround friction and official/native workaround status
10. seller cash/runtime/support cost
11. portfolio role
12. suggested launch price (`FREE`, `$4.99`, `$9.99`, `$19+`, or justified alternative)
13. natural discovery channel + search keyword/slug
14. 30-second demo
15. measurable stop condition
16. copy/platform risk
17. if SHIP: minimal MVP specification suitable for a coding agent

Do not output 20 mediocre ideas.

## Launch hypothesis rule

A candidate is not ready for SHIP until you can state a compact launch hypothesis:

> **[Persona]** will discover **[slug/search phrase]** in **[channel]**, install/buy because **[immediate pain]**, and understand the value within **30 seconds** by seeing **[demo outcome]**.

If this sentence is vague, distribution is not validated.

## Local learning

When the host permits local files, users may keep a local-only structured history with:

`python scripts/local_ledger.py append record.json`

and inspect portfolio outcomes with:

`python scripts/local_ledger.py summary`

This script makes no network calls. The public Skill must not upload this private ledger.

## Competitive boundary

Opportunity Finder should be better at **finding a tiny window to ship now**, not better at owning a million-row complaint database.

If a mature product already owns data collection, revenue intelligence, or continuous crawling, treat it as an upstream intelligence source instead of rebuilding it.

## Definition of done

A scan is complete only when:

- a broad scan completed the configured minimum number of **traceable Winner Benchmarks**;
- winner/trend surfaces were checked;
- raw install signals were normalized for ambiguity;
- platform-only incidents were quarantined before product scoring;
- direct substitutes were searched and competition maturity was classified;
- evidence was collected from real sources and material claims are traceable to original URLs plus dates;
- broad scans covered enough distinct workflow domains before a zero-SHIP conclusion;
- required surfaces and implementation path were verified;
- workaround friction and official platform workaround/fix status were checked;
- finalists were attacked with market/feasibility/distribution/economics kill tests;
- seller costs and runtime owner were explicit;
- no more than 3 candidates survived;
- each survivor has a concrete launch hypothesis and stop condition;
- the final report contains a clickable Source Ledger with full URL schemes and does not rely on untraceable install, pricing, competitor, or platform-capability claims.
