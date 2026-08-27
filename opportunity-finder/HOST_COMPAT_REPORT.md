# Host Compatibility Report — V1.6

Date: 2026-08-26

Local host-layout smoke tests were executed from installed copies, not only from the build directory.

## Layouts tested

- `.agents/skills/opportunity-finder/`
- `.codebuddy/skills/opportunity-finder/`

## Checks

- parent folder matches `name: opportunity-finder`;
- `SKILL.md` frontmatter parses under package tests;
- all Python scripts import/execute from the installed path;
- deterministic scorer executes from both installed layouts;
- full offline unit-test suite passes in both installed layouts;
- publisher PostHog ingestion defaults are packaged, but no consent state is packaged; telemetry remains fail-closed until explicit opt-in.

## Result

PASS for both local host directory conventions.

This does **not** claim that a live WorkBuddy/Claude/Codex model has re-run V1.6 yet. V1.6 still requires one final live-host scan to verify that the model obeys the new Source Ledger and mandatory Winner Benchmark rules during real web research.
