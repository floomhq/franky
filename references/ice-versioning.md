# ICE And Versioning

Load this file for `workflow-onboarding` or when a user has several automation
ideas and needs a starting point.

## Consultant Move

Do not answer with a generic course list. Anchor the user in one real work
domain and guide them into building.

If the user asks for a 1-2 day course or says they need the basics, use this
move:

```text
Pick a real workflow from your job. I will guide you through that. The basics
make sense faster once they are attached to something you already do.
```

Then give a tiny learning path:

```text
Day 1: learn by building v0 manually.
Day 2: turn v0 into v1 with one repeatable input, one output, and one pass/fail
test.
Only after that: add one staged connector.
```

Flow:

1. Pick a domain: sales, ops, recruiting, finance, support, research, personal
   admin, or another concrete area.
2. Map workflows in that domain.
3. Score each workflow with ICE.
4. Pick the highest practical v1.
5. Define versions and staging.
6. Give a 60-minute first session plan.
7. Give a 2-day basics plan.
8. Build workflow 1 together.

## Beginner Bridge

If the user is too vague to paste a real example, bridge them with fill-in
questions instead of stopping:

```text
Fill this in with rough words:

1. Role: I work in <sales/ops/support/recruiting/finance/other>.
2. Repeated task: every <day/week/event>, I have to <task>.
3. Input: I usually look at <email/CRM/Slack/Notion/sheet/call notes>.
4. Output: I need to create <reply/update/note/report/task>.
5. Risk: it would be bad if AI <sent/wrote/deleted/shared> this without review.
```

If the user cannot answer, offer these starting domains:

| Domain | Beginner-safe first v1 |
|---|---|
| Sales | discovery prep note from pasted deal context |
| Ops | weekly status summary from pasted notes |
| Support | support reply draft from pasted ticket |
| Recruiting | candidate screen summary from pasted resume and notes |
| Finance | invoice or expense categorization draft from pasted line items |
| Founder/admin | meeting brief from pasted calendar note and context |

Use the user's language. For German/English users, mirror the mixed style:

```text
ok, lass gemeinsam bauen. Kein Kurs zuerst. Such dir ein echtes Workflow-Thema
aus deinem Job, dann bauen wir v0 in 60 Minuten.
```

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

## Connector Ladder

Use this ladder before any live integration:

| System | v0 | v1 | v2 staging | v3 live |
|---|---|---|---|---|
| Gmail | paste thread manually | read selected exported thread | read-only OAuth with test label | draft replies only, send after human approval |
| CRM | paste deal fields | import CSV/export | write to test pipeline or sandbox object | propose field updates with approval log |
| Notion | paste output manually | copy markdown into private page | write to private test page/database | write to shared database after schema lock |
| Slack | paste update manually | generate Slack-ready draft | post to private test channel | post to live channel after approval |
| Calls | paste transcript | summarize one transcript | retrieve from test knowledge base | live assist only after evals and fallback |

Beginner implementation ladder:

```text
Step 1: prompt only.
Step 2: saved prompt or tiny script.
Step 3: simple local page or CLI form.
Step 4: one read-only connector.
Step 5: one staged write.
Step 6: live write with approval, logging, and rollback.
```

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

## Non-Sales Example

User asks for basics but works in ops, support, or internal coordination:

| Workflow | User | Trigger | Input | Output | Systems | Impact | Confidence | Effort | ICE | Version | Staging Rule |
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|
| Weekly ops update | ops/team lead | Friday | pasted notes, metrics, blockers | Slack-ready update draft | manual paste/export | 5 | 4 | 4 | 80 | v1 | draft only, no channel post |
| Support reply draft | support | new ticket | pasted ticket and account notes | reply draft | manual paste/export | 4 | 4 | 4 | 64 | v1 | no auto-send |
| Task cleanup | ops | end of day | pasted Slack/Notion notes | prioritized task list | manual paste/export | 4 | 3 | 4 | 48 | v1 | no task writes |
| CRM hygiene | sales ops | stale deal | pasted CRM fields | proposed field updates | CRM export | 4 | 3 | 3 | 36 | v1 | human copies fields |
| Automated notifications | team | status change | CRM/Notion event | Slack notification | Slack, CRM, Notion | 4 | 2 | 2 | 16 | v2 later | private test channel first |

Recommended first build:

```text
v1: Weekly ops update.
Why: high impact, easy manual input, private draft output, clear pass/fail.
First task: paste last week's messy notes and ask the AI tool to turn them into
a Slack-ready update with wins, risks, blockers, and next actions.
v2: read from a Notion test page or exported sheet and post only to a private
Slack test channel.
```

Ops first prompt:

```text
You are helping me build one narrow ops workflow.

Goal: create a weekly Slack update draft from messy notes.

Input I will paste manually:
- completed work
- open blockers
- customer or team risks
- metrics or numbers
- next actions

Output:
- 3 wins
- 3 risks or blockers
- owner for each next action
- Slack-ready markdown
- missing information to ask the team for

Rules:
- do not post to Slack
- do not write to Notion or CRM
- produce a draft only

First, ask me for one real weekly notes example. Then turn it into the output
format.
```

60-minute first session:

| Minute | Action | Output |
|---:|---|---|
| 0-10 | Pick one real deal and paste raw context | one example input |
| 10-20 | Run the first prompt | first draft output |
| 20-35 | Tighten the output template | stable Notion format |
| 35-45 | Add missing-field detection | quality check |
| 45-55 | Save as reusable prompt or tiny script | repeatable v0 |
| 55-60 | Decide v1 success metric | pass/fail rule |

Success metric:

```text
The workflow wins when one salesperson can create a useful discovery prep note
from one pasted deal context in under five minutes, with no Gmail, CRM, Notion,
or Slack live writes.
```

2-day basics plan:

| Time | Goal | Output |
|---|---|---|
| Day 1, hour 1 | Understand the workflow | filled beginner bridge |
| Day 1, hour 2 | Make v0 prompt work once | one good discovery prep note |
| Day 1, hour 3 | Turn output into a template | reusable Notion markdown |
| Day 1, hour 4 | Add missing-field checks | quality checklist |
| Day 2, hour 1 | Make it repeatable | saved prompt, script, or tiny local form |
| Day 2, hour 2 | Test on 3 examples | pass/fail notes |
| Day 2, hour 3 | Pick first connector | Gmail export, CRM CSV, or Notion test page |
| Day 2, hour 4 | Stage v2 | private test page/channel and approval rule |

First files for a tiny local implementation:

```text
README.md: explains the workflow and test examples.
examples/deal-1.txt: pasted raw deal context.
templates/discovery-prep.md: desired output format.
prompt.md: reusable prompt.
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
Staging Gmail, Slack, Notion, and CRM safely means Fede starts with copies and
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
**60-Minute Session:** minute-by-minute plan.
**2-Day Basics Plan:** short learning-by-building plan.
**Connector Ladder:** Gmail/CRM/Notion/Slack staged path.
**Task 1:** collect one real example.
**Task 2:** build v0 with pasted inputs.
**Task 3:** build v2 with one staged connector or export.
```
