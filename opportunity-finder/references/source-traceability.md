# Source Traceability Gate V1.6

Opportunity Finder is a decision tool, not a confidence generator. A material market claim must be traceable before it can support `SHIP`.

## What counts as a material claim

Always trace claims about:

- install counts, stars, ratings, votes, growth, or ranking;
- price, plan, marketplace fee, payment model, or paid workaround;
- launch/release/change dates;
- platform capability, limitation, bug status, workaround, or native feature;
- competitor existence, maturity, or claimed feature coverage;
- demand frequency, repeated complaints, or explicit willingness to pay;
- implementation availability such as API, file format, extension surface, or documented integration.

## Preferred source order

Use the closest original source available:

1. official documentation / release note / marketplace listing;
2. original GitHub repository, issue, discussion, or changelog;
3. original community post or forum thread;
4. first-party pricing/product page;
5. reputable secondary report when the original is unavailable.

Do not use an AI summary or search-result snippet as the final support when an original URL exists.

## Required evidence fields

Each evidence record should contain:

- `claim_type`: demand | competition | platform | pricing | winner | implementation | other
- `source_type`
- `source_reference`: original `http://` or `https://` URL
- `source_date`: source publication/event date when available
- `observed_at`: date the scan checked the source
- `persona`
- `workflow`
- `pain` or supported claim

If the source has no publication date, leave `source_date` null but `observed_at` is mandatory.

## Final report rule

The final report must include a compact **Source Ledger**. Each material claim in finalist reasoning should point to one or more ledger items.

Minimum Source Ledger columns:

| ID | Claim type | Source | Source date | Observed | Supports |
|---|---|---|---|---|---|

For public Markdown output, render `Source` as a clickable Markdown link using the complete `http://` or `https://` URL. Never shorten `https://example.com/path` to `example.com/path`, because some hosts will no longer make it clickable. If scan JSON is available, use `scripts/render_source_ledger.py` to generate this section deterministically.

## Unverified rule

If a claim cannot be traced:

- label it `unverified`;
- do not use it to increase evidence quality, competition confidence, pricing confidence, or winner status;
- do not allow it to be the deciding reason for `SHIP`.

Traceability is a quality gate, not a citation-volume contest. Prefer a few strong original sources over many weak summaries.
