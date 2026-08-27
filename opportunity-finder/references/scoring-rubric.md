# Quick-Commerce Scoring Rubric V1.4

Score each dimension from 0 to 10. Deterministic weights are frozen in `config/criteria.json` and sum to 100.

## Freshness — 10
10 = demand visibly appeared or accelerated in the last 24h–7d; 7 = strong 30-day growth; 5 = recent but stable; 0 = old evergreen idea with no current window.

## AI power-user density — 7
10 = target users already install/use Agent Skills, MCP, Claude Code, Codex, Cursor, OpenClaw or adjacent AI extensions; 0 = the market needs substantial education.

## Evidence quality — 11
10 = payment/paid workaround/repeated active use; 8 = costly recurring workaround or strong behavioral demand; 6 = repeated complaints plus install/search intent; 4 = mainly stars/upvotes/raw installs; 0 = generated speculation. Raw installs alone are not strong evidence.

## Repeated evidence — 7
10 = many independent recent signals across sources; 7 = 3–5 strong independent signals; 5 = two usable independent signals; 0 = one speculative comment.

## Natural distribution — 10
10 = obvious slug/keyword + concentrated community/marketplace + users already install this product type; 6 = one credible organic path; 0 = paid ads/audience building are required.

## Build speed — 12
10 = 2–4 hours; 8 = one workday; 5 = 2–3 days; 0 = above the 24-hour hard limit. Never give a high score without an implementation sketch.

## Seller economics — 13
10 = user-owned model/API/BYOK/local compute, negligible variable seller cost, low support; 6 = modest bounded cost; 0 = unbounded seller runtime or support dominates likely revenue.

## Technical feasibility — 12
10 = required surfaces are accessible through stable documented/local interfaces, fixture-based test path exists, permissions are clear; 6 = feasible but one material dependency is uncertain; 0 = core value requires inaccessible private cloud state or an undefined implementation path. See `feasibility-gates.md`.

## Workaround friction — 7
10 = repeated fragile/manual workaround or meaningful failure cost; 6 = 10–30 minutes of recurring friction; 3 = a few manual steps; 0 = a documented toggle or <2 minute fix.

## Portfolio value — 5
10 = strong cash SKU or free anchor with explicit measurable asset; 0 = neither revenue nor strategic asset.

## Competition window — 3
10 = 0–1 weak focused solution; 6 = market forming; 0 = mature strong free incumbent/commodity.

## Event tailwind — 3
10 = new release/regression/API change creates immediate demand; 5 = recent structural adoption tailwind; 0 = no timing catalyst.

## Penalties
- generic wrapper: -15
- mature free incumbent: -20
- emerging free alternatives: -6
- paid-ad dependency: -20
- high support debt: -15
- seller-paid runtime: -10
- platform capture soon: -5
- high liability: -20
- ambiguous install signal: -5
- free without measurable asset: -15
- trivial workaround: -20
- platform fix in progress: -10
- unstable private API dependency: -15
- low build-estimate confidence: -10

## Hard skip conditions
- no current demand evidence;
- build time above 24 hours;
- unbounded seller runtime cost;
- no legal distribution path;
- required product surface is inaccessible;
- no concrete implementation path;
- platform incident only, with no stable user-controlled repair surface.

## Decision bands
- 80–100: SHIP only when evidence count >= 2, evidence quality >= 6, technical feasibility >= 7, workaround friction >= 6, and build-estimate confidence >= 0.7.
- 68–79.99: TEST
- 58–67.99: WATCH
- below 58: SKIP
- any hard reject: SKIP

A high score cannot bypass weak evidence, weak productizability, or a trivial workaround.

## Competition maturity
Use `competition.maturity` = `none`, `emerging`, or `mature`. Reserve the -20 penalty for a functionally complete adopted free incumbent. Emerging alternatives get -6 and may validate a young market. See `competition-maturity.md`.
