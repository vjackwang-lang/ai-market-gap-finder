# Winner Benchmark Protocol V1.6

Study winners to discover **validated behavior and adjacent unfinished jobs**, not to manufacture clones.

For a broad Opportunity Finder scan, Winner Benchmark is mandatory rather than optional background reading.

## Snapshot fields

For each high-install/high-growth Skill, plugin, MCP tool or adjacent product record:

1. `product_name`;
2. `source_reference`: original live URL;
3. `observation_date`;
4. `source_date` when available;
5. raw install/rating/growth signal;
6. signal-quality notes: standalone vs whole-repo/Pack, official/curated advantage, duplicate/fork flag, independent usage evidence;
7. primary job-to-be-done;
8. target user and agent/platform;
9. search/name keywords that make discovery obvious;
10. 30–60 second killer demo;
11. why users install instead of just prompting the base model;
12. hard gates, persistent artifacts or concrete automation behavior that make the Skill reliable;
13. complaints/issues/discussions with original source links;
14. manual step immediately before/after use;
15. recent platform change that expands/shrinks the window;
16. `adjacent_unresolved_job`: at least one job the winner does not already solve;
17. whether this belongs to a coherent product cluster.

## Mandatory install-signal normalization

Never convert raw installs directly into demand quality.

Check when possible:

- Was it installed as part of a repository or Pack?
- Is it official/curated and therefore advantaged in distribution?
- Is it marked as a duplicate/fork?
- Is growth sudden without matching stars/issues/community use?
- Is there independent evidence the Skill is invoked or discussed?
- Is the number all-time, trending or hot?

If material ambiguity remains, set `ambiguous_install_signal=true` and lower evidence quality.

## Adjacent-opportunity lenses

Look one step beyond the winner for:

- verification / QA / regression;
- professional or niche adaptation;
- migration / compatibility / repair;
- state / memory / handoff;
- cost / usage / support reduction;
- physical-world or external-system validation;
- missing output packaging / distribution;
- event-driven fixes caused by a recent change;
- a free category anchor with a clear downstream problem chain.

## Broad-scan gate

Before a broad scan can conclude `0 SHIP`, it must contain at least the configured minimum number of traceable Winner Benchmarks.

A benchmark counts only when it has:

- original `http://` or `https://` source;
- observation date;
- job-to-be-done;
- signal-quality note;
- adjacent unresolved job.

## Rejection rule

Never recommend a clone solely because a winner has large installs. The output must name what is **still unsolved**, why the base model/winner does not already solve it, and why the proposed product has a natural discovery path.
