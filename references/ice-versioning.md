# ICE And Versioning

Load this file for `workflow-onboarding` or when a user has several automation
ideas and needs a starting point.

## Consultant Move

Do not answer with a generic course list. Anchor the user in one real work
domain and guide them into building.

Flow:

1. Pick a domain: sales, ops, recruiting, finance, support, research, personal
   admin, or another concrete area.
2. Map workflows in that domain.
3. Score each workflow with ICE.
4. Pick the highest practical v1.
5. Define versions and staging.
6. Build workflow 1 together.

## ICE Matrix

Score 1-5.

- Impact: value if this works for the next real user.
- Confidence: clarity of inputs, outputs, permissions, and success criteria.
- Effort: build and integration difficulty; lower effort scores higher.

Formula:

```text
ICE = impact * confidence * effort
```

Use this table:

| Workflow | User | Trigger | Input | Output | Systems | Impact | Confidence | Effort | ICE | Version | Staging Rule |
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|

Effort scoring:

- 5: prompt/manual, no connector
- 4: read-only connector
- 3: write to one low-risk system
- 2: multiple systems, approvals, or schema changes
- 1: money, customer data, live messages, destructive writes, or complex auth

## Version Ladder

- v0: manual prompt or script with copied input and copied output.
- v1: one narrow workflow, one user, one trigger, one output, dry-run by default.
- v2: staged connector flow with test accounts, fixture data, logs, and approval
  before writes.
- v3: live workflow with monitoring, rollback, ownership, and budget guard.

Every workflow gets a version label before implementation.

## Staging Rules

Any workflow with Gmail, Slack, Notion, CRM, payments, customer data, or external
writes starts in staged mode:

- read-only first
- draft outputs before sending or writing
- test channel, test database, test page, or sandbox account
- explicit approval before live writes
- logs for inputs, outputs, errors, and owner action

For email and Slack:

- v0: generate a draft from pasted context
- v1: read selected inputs and produce a draft only
- v2: write to a test label, test channel, or private Notion page
- v3: send or post live only after approval and logging

## Beginner Example

User asks for basics and lists:

- automate emails
- CRM entries
- deal notes and discovery prep in Notion
- weekly updates, reports, and Slack notifications
- later: live call sales assistant

Map:

| Workflow | User | Trigger | Input | Output | Systems | Impact | Confidence | Effort | ICE | Version | Staging Rule |
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|
| Discovery prep note | sales | meeting tomorrow | pasted deal context | prep note draft | manual paste/export | 5 | 4 | 4 | 80 | v1 | no connector writes |
| Weekly update | team | Friday | pasted CRM changes, notes | Slack update draft | manual paste/export | 4 | 4 | 4 | 64 | v1 | draft only, no channel post |
| Email assistant | sales | inbound email | pasted thread | reply draft | manual paste/export | 4 | 3 | 4 | 48 | v1 | draft only, no auto-send |
| CRM entry assistant | sales | new lead | pasted email/thread | CRM field draft | manual paste/export | 5 | 3 | 3 | 45 | v1 | draft fields, human copies |
| Live call assistant | sales | live call | transcript, CRM, references | objection support | call tool, CRM, knowledge base | 5 | 2 | 1 | 10 | v0 later | no live deployment until retrieval quality is proven |

Recommended first build:

```text
v1: Discovery prep note.
Why: high impact, manual inputs, private draft output, clear success criteria.
First task: paste one real deal context into Cursor/Claude and ask it to map
inputs, output format, and missing fields. Then build a draft generator before
connecting Gmail, CRM, or Notion.
v2: add read-only Gmail/CRM exports and write to a private Notion test page.
```

Exact first prompt:

```text
You are helping me build one narrow sales workflow.

Goal: create a discovery prep note draft before a sales call.

Input I will paste manually:
- company name
- contact name and role
- CRM notes or deal notes
- email thread summary
- meeting goal
- known objections
- reference customers or proof points I can use

Output:
- 5-bullet account summary
- likely pain points
- 5 discovery questions
- likely objections and suggested replies
- missing fields I need before the call
- Notion-ready markdown

Rules:
- do not send emails
- do not write to CRM
- do not post to Slack
- produce a draft only

First, ask me for one real deal example. Then turn it into the output format.
```

Notion-ready output template:

```markdown
# Discovery Prep: <Company>

## Account Summary
- 

## Current Signal
- 

## Discovery Questions
1. 
2. 
3. 
4. 
5. 

## Likely Objections
| Objection | Reply | Proof |
|---|---|---|
|  |  |  |

## Missing Fields
- 

## Next Step
- 
```

Slack draft template for later:

```markdown
Weekly Sales Update

Wins:
- 

Risks:
- 

Deals Needing Help:
- 

Next Week:
- 
```

Plain-language staging explanation:

```text
Staging Gmail, Slack, Notion, and CRM safely means Franky starts with copies and
drafts, not live actions. Gmail is read-only or pasted manually. Slack output is
posted to a private test channel or kept as a draft. Notion writes go to a test
page. CRM updates are proposed as fields for a human to copy. Live writes happen
only after the draft output is reliable, logs exist, and a human approves the
action.
```

## Output Format

```markdown
**Verdict:** start with <workflow>.
**Why:** highest ICE with lowest live-risk.
**ICE Matrix:** table.
**Version Plan:** v0, v1, v2, v3.
**Staging Rule:** read-only/draft/test-channel/private-page before live writes.
**First Prompt:** exact prompt to paste into Cursor, Claude, Codex, or ChatGPT.
**First Output Template:** the artifact the workflow produces.
**Task 1:** collect one real example.
**Task 2:** build v0 with pasted inputs.
**Task 3:** build v2 with one staged connector or export.
```
