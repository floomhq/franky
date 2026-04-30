---
date:
slug:
repo_path:
consult_type:
segment:
outcome:
blocker:
urgency:
traction_level:
technical_proficiency:
existing_infra:
decision_maker:
checks_run:
evidence_status:
scanner_used:
smoke_result:
time_to_url:
pattern_match:
ice_top_workflow:
version_plan:
staging_rule:
---

# Fede Consult Note

## Raw Pain

## Context

- Source builder:
- Who needs it next:
- Why now:
- What breaks if it stays localhost:

## Workflow Map

| Workflow | User | Trigger | Input | Output | Systems | Impact | Confidence | Effort | ICE | Version | Staging Rule |
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|

## Blocker Taxonomy

- Env/secrets:
- Localhost leak:
- Auth callback:
- Database:
- File storage:
- AI cost:
- Webhook:
- Background jobs:
- Deployment platform:
- Fear of breaking things:
- Other:

## What They Tried

## Evidence

- Commands run:
- Build/start result:
- Smoke result:
- Screenshot or route:
- Blockers left open:

## Traction Signal

- Exact pain quote:
- Who said it:
- Trigger event:
- Current workaround:
- Would share/pay/introduce:
- Time-to-value:
- Pattern match:

## Consult Outcome

## Final Recommendation

## Evidence

## Insight

## Copy Seed

- headline_candidate:
- problem_phrase:
- proof_phrase:
- outcome_phrase:

## Next Outreach Angle

## Publishable Snippet

One anonymized paragraph suitable for a case study, launch post, or outreach.
Do not include names, companies, or direct quotes without explicit approval.

## Why This Note Matters

## Filled Example Shape

Use this density, replacing placeholders with verified facts:

```markdown
## Evidence
- Commands run: npm run build, rg localhost, gitleaks detect
- Build/start result: build passed, production start blocked by missing PORT
- Smoke result: public route not tested because start blocked
- Screenshot or route: not available
- Blockers left open: production start script ignores platform PORT

## Traction Signal
- Exact pain quote: "I can demo it on Zoom, but I cannot send a link."
- Who said it: solo founder, anonymized
- Trigger event: investor demo tomorrow
- Current workaround: screen-share from local dev server
- Would share/pay/introduce: would share repo for review
- Time-to-value: verdict in 12 minutes
- Pattern match: evidence gap

## Copy Seed
- headline_candidate: Local works. Sharing is the hard part.
- problem_phrase: cannot send a link
- proof_phrase: build passed, production start blocked by PORT
- outcome_phrase: one config fix away from demo URL
```
