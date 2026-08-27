# Public Publish Checklist

## Required before first public install

- [ ] Create the final GitHub repository and choose the permanent owner/repo coordinates.
- [ ] Put the `opportunity-finder/` folder in the repository without renaming it.
- [ ] Confirm `SKILL.md` frontmatter `name: opportunity-finder` still matches the parent directory.
- [ ] Run `skills-ref validate ./opportunity-finder`.
- [ ] Run the full offline test suite.
- [ ] Run `python scripts/score_opportunities.py examples/candidates.example.json --pretty`.
- [ ] Run `python scripts/validate_scan.py examples/candidates.example.json examples/scored_output.json --pretty` or regenerate scored output first if needed.
- [ ] Review `PRIVACY.md`; verify first-run consent asks once and No preserves full functionality.
- [ ] Verify bundled PostHog Project token uses US ingestion and no Personal API key is present.
- [ ] Test the exact GitHub install command from a clean temp Agent environment.
- [ ] Import the release ZIP once in WorkBuddy and verify natural-language activation.
- [ ] Publish the GitHub release and use `MARKETPLACE_LISTING.md` for listing copy.

## After launch

- [ ] Verify the first real `npx skills add` install is visible to skills.sh telemetry/ranking surfaces.
- [ ] Check that public Source Ledgers preserve clickable `https://` links.
- [ ] Verify one opt-in QA event reaches PostHog and can be read back.
- [ ] Record installs, feedback and optional telemetry separately from private portfolio/revenue data.
- [ ] Do not add features until real user feedback identifies a repeated failure or missing job.
