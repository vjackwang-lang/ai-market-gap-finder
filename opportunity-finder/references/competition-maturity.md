# Competition Maturity — V1.4

Do not treat every free alternative as a mature incumbent.

## none

Use when no directly usable substitute was found after a reasonable search.

No automatic competition penalty.

## emerging

Use when one or a few fresh alternatives exist, but the category is still forming. Typical evidence:

- new repositories or Skills with limited adoption history;
- partial solutions that cover only part of the job;
- recent entrants without clear category dominance;
- multiple competing approaches with no obvious standard.

This is **demand validation plus a small competition cost**, not an automatic rejection. The deterministic scorer applies `emerging_free_alternatives`.

A candidate still needs a concrete reason to be materially better or narrower. “Same thing but ours is prettier” is not enough.

## mature

Reserve this label for a free solution that materially closes the opportunity. Typical evidence:

- meaningful independent adoption or repeated recommendations;
- functionally complete coverage of the proposed job;
- active maintenance and easy installation;
- strong marketplace/search position;
- no clear missing job that justifies a new product.

The scorer applies the larger `mature_free_incumbent` penalty.

## Why this matters for Quick Commerce

A traditional SaaS investor may avoid any early free competition. A high-turnover micro-product portfolio should not. A newly forming category can still be worth entering if:

- the product ships in hours;
- seller runtime cost is near zero;
- natural discovery is strong;
- the implementation is materially better or narrower;
- the exit cost is tiny.

But do not relabel a dominant free incumbent as “emerging” merely to force a favorite idea through the gate.
