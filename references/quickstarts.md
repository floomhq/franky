# Quickstarts

Load this file when the user is a total beginner, asks for basics, cannot name a
workflow, or resembles the Andres/Joshio profile.

## Zero-Input Intake

If the user has no clear idea yet, start here:

```text
Pick one:

1. Sales: emails, CRM, discovery prep, Slack updates, call prep.
2. Ops: weekly updates, task cleanup, support replies, reports.
3. Support: tickets, account summaries, reply drafts.
4. Recruiting: candidate summaries, interview prep, follow-ups.
5. Founder/admin: meeting briefs, investor updates, personal CRM.

If you are unsure, pick sales or ops. We will build a draft-first v0 in one
hour, then decide whether it deserves a connector.
```

## Andres Quickstart

Use for a German/English sales or ops beginner.

```text
ok, lass gemeinsam bauen.

Kein Kurs zuerst. Wir nehmen einen echten Workflow von dir, bauen v0 manuell,
und danach verstehst du die Basics schneller.

Dein erstes Projekt:
Discovery prep note fuer einen echten Deal.

Warum:
- hoher Impact
- kein Risiko durch live writes
- du siehst sofort, ob AI dir wirklich Zeit spart
- Gmail, CRM, Notion und Slack koennen spaeter staged dazukommen

Heute:
1. Nimm einen echten Deal.
2. Paste CRM notes, email summary, meeting goal, objections.
3. Lass Fede daraus eine Notion-ready discovery prep machen.
4. Teste es an 3 Deals.
5. Erst danach verbinden wir Gmail/CRM/Notion.
```

## Joshio Quickstart

Use for a smart but vague beginner who wants to start building with AI.

```text
You do not need the perfect idea.

Start with one repeated task from this week:

- something you copied from one tool to another
- something you summarized for someone
- something you forgot to follow up on
- something you turned into a status update
- something you searched for before a meeting

Fede will turn that into:

- one v0 prompt
- one output template
- one success metric
- one 60-minute build plan
- one staged connector path
```

## Generated Sample Output

```markdown
**Verdict:** start with weekly ops update.

**Why:** it has high impact, clear input, draft-only output, and no risky live
write.

**ICE Matrix**

| Workflow | Impact | Confidence | Effort | ICE | Version |
|---|---:|---:|---:|---:|---|
| Weekly ops update | 5 | 4 | 4 | 80 | v1 |
| Support reply draft | 4 | 4 | 4 | 64 | v1 |
| Task cleanup | 4 | 3 | 4 | 48 | v1 |

**First Prompt**

Turn these messy weekly notes into a Slack-ready update with wins, risks,
blockers, owners, and missing info. Do not post to Slack. Produce a draft only.

**60-Minute Plan**

0-10: paste one real notes dump.
10-20: generate first draft.
20-35: tighten the template.
35-45: add missing-field checks.
45-55: save reusable prompt.
55-60: define pass/fail.

**Connector Ladder**

v0 paste notes manually.
v1 saved prompt or tiny local form.
v2 read from Notion test page and post to private Slack test channel.
v3 post to live channel after approval and logging.
```

## CLI

For a deterministic starter plan:

```bash
python3 scripts/fede_intake.py --text "I am a beginner and want to automate CRM, Slack, Notion, and emails"
python3 scripts/fede_intake.py --domain ops --text "I need weekly updates and support replies"
```
