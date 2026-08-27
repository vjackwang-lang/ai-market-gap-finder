# Signal Hierarchy — Do Not Confuse Attention With Demand

Opportunity Finder must rank evidence by how close it is to real economic behavior.

## Strongest to weakest

1. **Actual payment / purchase / paid workaround**
2. **Repeated active use / installs with independent usage evidence**
3. **Time or money spent on a workaround**
4. **Repeated recent complaints across independent sources**
5. **Explicit willingness-to-pay language**
6. **Search/install intent**
7. **Upvotes, stars, likes, comments**
8. **AI-generated scores or market-size estimates**

A lower-level signal can support a decision but should not overrule a contradictory higher-level signal.

## Install-count caution

A Skill install is useful behavioral evidence, but not proof of active usage or payment.

Before treating install count as a winner signal, check:

- Is the Skill an original or a detected duplicate/fork?
- Was it installed individually, or could it have arrived through a repository collection or Pack?
- Is the source official/curated, which may have a distribution advantage unrelated to product quality?
- Is the install count supported by current Trending/Hot velocity?
- Is there independent GitHub/community evidence that people actually use the capability?
- Is the first-seen date consistent with plausible organic growth?
- Are there reviews/issues/discussions describing real outcomes?

If raw installs are impressive but these checks are weak, mark `ambiguous_install_signal=true` and do not use installs as the primary demand proof.

## Free-product caution

Free installs prove acquisition, not monetization. A free opportunity can still be excellent when its assigned role is `FREE_ANCHOR`, but its value must be measured as a concrete asset: ranking, reviews, opt-in demand data, author trust, or conversion into a related paid product.
