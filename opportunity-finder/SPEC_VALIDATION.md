# Agent Skills Specification Validation

Date: 2026-08-26
Status: PASS (equivalent local checks)

Validated against the published Agent Skills specification constraints used by this package:

- parent directory is `opportunity-finder` and matches frontmatter `name`;
- `name` uses lowercase alphanumeric/hyphen syntax and is within 64 characters;
- `description` is non-empty and below 1024 characters;
- `compatibility` is below 500 characters;
- only supported top-level frontmatter fields are used;
- metadata values are strings;
- `SKILL.md` remains below the recommended 500-line limit;
- referenced scripts/references/assets exist at the Skill root structure;
- Python scripts are self-contained and use standard library only.

The official `skills-ref` executable was not preinstalled in this execution environment, so the final GitHub publish checklist retains an explicit `skills-ref validate ./opportunity-finder` gate before public launch.
