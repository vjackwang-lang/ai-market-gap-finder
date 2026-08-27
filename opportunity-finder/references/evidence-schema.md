# Evidence Schema V1.6

For each raw market signal, capture only what is needed to judge the opportunity and make the final decision auditable.

Required fields:

- `claim_type`: demand | competition | platform | pricing | winner | implementation | other
- `source_type`: reddit | github_issue | github_repo | marketplace | official_docs | forum | hn | product_hunt | youtube | x | other
- `source_reference`: original public URL (`http://` or `https://`) when the claim comes from the public web
- `source_date`: ISO date when the source/event date is available; otherwise null
- `observed_at`: ISO date when the scan checked the source
- `persona`: precise user type
- `agent_stack`: Claude Code / Codex / Cursor / OpenClaw / WorkBuddy / MCP / other
- `workflow`: what the user was actually doing
- `pain`: concrete failure, friction, request, workaround, or claim supported by the source
- `workaround`: what the user does now
- `workaround_minutes`: approximate time for the current workaround when inferable
- `workaround_repeats`: how often the workaround repeats when inferable
- `second_order`: true/false
- `event_linked`: true/false; whether a recent release/change created or amplified it
- `cost_signal`: time | money | rework | risk | embarrassment | compute | unknown
- `install_or_buy_signal`: observed install/payment/tool-shopping behavior if any; otherwise unknown
- `required_surface`: local file | documented_api | browser_ui | public_web | private_cloud_state | local_database | other
- `implementation_path`: concrete library/API/interface that could power the product, if known
- `platform_fix_status`: none | documented_workaround | fix_in_progress | native_feature_present | unknown

Material facts such as install counts, prices, stars, release dates, vote counts, competitor coverage, and platform capability must be supported by the exact evidence record that contains the original source URL.

Do not infer revenue, install counts, payment intent, or platform capabilities without evidence.

For public telemetry, do **not** upload this evidence record. Evidence may contain URLs or user content and stays in the active research session unless the user explicitly opts into a separate sharing flow.
