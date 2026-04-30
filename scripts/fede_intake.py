#!/usr/bin/env python3
"""Guided zero-to-first-workflow intake for Fede."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Workflow:
    name: str
    user: str
    trigger: str
    input: str
    output: str
    systems: str
    impact: int
    confidence: int
    effort: int
    version: str
    staging: str

    @property
    def ice(self) -> int:
        return self.impact * self.confidence * self.effort


@dataclass(frozen=True)
class Domain:
    name: str
    label: str
    workflows: tuple[Workflow, ...]
    prompt: str
    template: str
    success_metric: str
    first_task: str


DOMAINS: dict[str, Domain] = {
    "sales": Domain(
        name="sales",
        label="Sales",
        workflows=(
            Workflow("Discovery prep note", "sales", "meeting tomorrow", "pasted deal context", "Notion-ready prep note draft", "manual paste/export", 5, 4, 4, "v1", "no connector writes"),
            Workflow("Weekly update", "team", "Friday", "pasted CRM changes and notes", "Slack update draft", "manual paste/export", 4, 4, 4, "v1", "draft only"),
            Workflow("Email assistant", "sales", "inbound email", "pasted thread", "reply draft", "manual paste/export", 4, 3, 4, "v1", "no auto-send"),
            Workflow("CRM entry assistant", "sales", "new lead", "pasted email or notes", "CRM field draft", "manual paste/export", 5, 3, 3, "v1", "human copies fields"),
            Workflow("Live-call assistant", "sales", "live call", "transcript and references", "objection support", "call tool, CRM, knowledge base", 5, 2, 1, "v0 later", "no live assist until evals pass"),
        ),
        prompt="""You are helping me build one narrow sales workflow.

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

First, ask me for one real deal example. Then turn it into the output format.""",
        template="""# Discovery Prep: <Company>

## Account Summary
- 

## Current Signal
- 

## Discovery Questions
1. 
2. 
3. 

## Likely Objections
| Objection | Reply | Proof |
|---|---|---|
|  |  |  |

## Missing Fields
- 

## Next Step
- """,
        success_metric="One salesperson creates a useful discovery prep note from pasted deal context in under five minutes.",
        first_task="Paste one real deal context and generate a Notion-ready prep note draft.",
    ),
    "ops": Domain(
        name="ops",
        label="Ops",
        workflows=(
            Workflow("Weekly ops update", "ops lead", "Friday", "pasted notes, metrics, blockers", "Slack-ready update draft", "manual paste/export", 5, 4, 4, "v1", "draft only"),
            Workflow("Support reply draft", "support", "new ticket", "pasted ticket and account notes", "reply draft", "manual paste/export", 4, 4, 4, "v1", "no auto-send"),
            Workflow("Task cleanup", "ops", "end of day", "pasted Slack/Notion notes", "prioritized task list", "manual paste/export", 4, 3, 4, "v1", "no task writes"),
            Workflow("CRM hygiene", "sales ops", "stale deal", "pasted CRM fields", "proposed field updates", "CRM export", 4, 3, 3, "v1", "human copies fields"),
            Workflow("Automated notifications", "team", "status change", "CRM/Notion event", "Slack notification", "Slack, CRM, Notion", 4, 2, 2, "v2 later", "private test channel first"),
        ),
        prompt="""You are helping me build one narrow ops workflow.

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

First, ask me for one real weekly notes example. Then turn it into the output format.""",
        template="""Weekly Ops Update

Wins:
- 

Risks:
- 

Blockers:
- 

Owners / Next Actions:
- 

Missing Info:
- """,
        success_metric="One team update can be drafted from messy notes in under five minutes.",
        first_task="Paste one messy weekly notes dump and generate a Slack-ready draft.",
    ),
    "support": Domain(
        name="support",
        label="Support",
        workflows=(
            Workflow("Support reply draft", "support", "new ticket", "pasted ticket and account context", "reply draft", "manual paste/export", 5, 4, 4, "v1", "no auto-send"),
            Workflow("Account summary", "support", "escalation", "pasted account notes", "short context brief", "manual paste/export", 4, 4, 4, "v1", "draft only"),
            Workflow("Bug report cleanup", "support", "bug-like ticket", "pasted ticket", "structured bug report", "ticket export", 4, 3, 4, "v1", "human files issue"),
            Workflow("Help center gap finder", "support", "repeated question", "ticket cluster", "article outline", "manual paste/export", 3, 3, 4, "v1", "draft only"),
        ),
        prompt="""You are helping me build one narrow support workflow.

Goal: create a reply draft from a support ticket.

Input I will paste manually:
- customer question
- account context
- relevant policy or product notes
- previous replies

Output:
- short diagnosis
- reply draft
- missing information
- escalation flag

Rules:
- do not send the reply
- do not update the ticket
- produce a draft only

First, ask me for one real ticket example. Then turn it into the output format.""",
        template="""# Support Reply Draft

## Diagnosis
- 

## Reply Draft
Hi <name>,


## Missing Information
- 

## Escalation Flag
- """,
        success_metric="One support teammate gets a useful reply draft from one pasted ticket in under five minutes.",
        first_task="Paste one support ticket and generate a reply draft with missing information flagged.",
    ),
    "recruiting": Domain(
        name="recruiting",
        label="Recruiting",
        workflows=(
            Workflow("Candidate screen summary", "recruiter", "new candidate", "pasted resume and notes", "screen summary", "manual paste/export", 5, 4, 4, "v1", "draft only"),
            Workflow("Interview prep", "hiring manager", "interview tomorrow", "candidate profile", "interview plan", "manual paste/export", 4, 4, 4, "v1", "draft only"),
            Workflow("Follow-up draft", "recruiter", "after interview", "feedback notes", "candidate email draft", "manual paste/export", 4, 3, 4, "v1", "no auto-send"),
            Workflow("Scorecard cleanup", "recruiter", "feedback received", "raw interview notes", "structured scorecard", "ATS export", 4, 3, 3, "v1", "human copies fields"),
        ),
        prompt="""You are helping me build one narrow recruiting workflow.

Goal: create a candidate screen summary from pasted context.

Input I will paste manually:
- resume or LinkedIn summary
- role description
- recruiter notes
- must-have criteria

Output:
- candidate summary
- fit against must-have criteria
- risks or gaps
- suggested interview questions
- missing information

Rules:
- do not contact the candidate
- do not update ATS
- produce a draft only

First, ask me for one real candidate example. Then turn it into the output format.""",
        template="""# Candidate Screen: <Name>

## Summary
- 

## Must-Have Fit
| Criterion | Evidence | Gap |
|---|---|---|
|  |  |  |

## Risks
- 

## Interview Questions
1. 
2. 
3. 

## Missing Information
- """,
        success_metric="One recruiter gets a useful candidate screen summary from pasted context in under five minutes.",
        first_task="Paste one candidate profile and role description, then generate a screen summary.",
    ),
    "finance": Domain(
        name="finance",
        label="Finance",
        workflows=(
            Workflow("Expense categorization draft", "finance", "monthly close", "pasted expense lines", "category draft", "manual paste/export", 4, 4, 4, "v1", "human reviews"),
            Workflow("Invoice follow-up draft", "finance", "overdue invoice", "pasted invoice context", "email draft", "manual paste/export", 4, 3, 4, "v1", "no auto-send"),
            Workflow("Cash update", "founder", "weekly finance check", "pasted numbers", "short cash note", "manual paste/export", 5, 3, 3, "v1", "draft only"),
            Workflow("Vendor summary", "finance", "new vendor", "pasted contract notes", "vendor brief", "manual paste/export", 3, 3, 4, "v1", "draft only"),
        ),
        prompt="""You are helping me build one narrow finance workflow.

Goal: create an expense categorization draft.

Input I will paste manually:
- expense line
- vendor name
- amount
- memo or receipt text
- known categories

Output:
- suggested category
- confidence
- reason
- missing information

Rules:
- do not change accounting records
- do not send emails
- produce a draft only

First, ask me for 5 real expense lines. Then turn them into the output format.""",
        template="""# Expense Categorization Draft

| Vendor | Amount | Suggested Category | Confidence | Reason | Missing Info |
|---|---:|---|---|---|---|
|  |  |  |  |  |  |
""",
        success_metric="One finance pass produces useful draft categories for five pasted expenses in under five minutes.",
        first_task="Paste five expense lines and generate category drafts with confidence and reasons.",
    ),
    "admin": Domain(
        name="admin",
        label="Founder/admin",
        workflows=(
            Workflow("Meeting brief", "founder", "meeting tomorrow", "pasted calendar note and context", "meeting brief", "manual paste/export", 5, 4, 4, "v1", "draft only"),
            Workflow("Investor update draft", "founder", "monthly update", "pasted wins, metrics, asks", "update draft", "manual paste/export", 5, 3, 4, "v1", "no auto-send"),
            Workflow("Personal CRM note", "founder", "after call", "pasted notes", "relationship note", "manual paste/export", 3, 3, 4, "v1", "human copies fields"),
            Workflow("Follow-up checklist", "founder", "after meeting", "pasted notes", "task list", "manual paste/export", 4, 3, 4, "v1", "no task writes"),
        ),
        prompt="""You are helping me build one narrow founder/admin workflow.

Goal: create a meeting brief from pasted context.

Input I will paste manually:
- meeting title
- attendee names
- notes from previous interaction
- goals for the call
- open questions

Output:
- meeting summary
- goals
- questions to ask
- likely follow-ups
- missing information

Rules:
- do not send messages
- do not update the calendar
- produce a draft only

First, ask me for one real meeting example. Then turn it into the output format.""",
        template="""# Meeting Brief: <Meeting>

## Context
- 

## Goals
- 

## Questions
1. 
2. 
3. 

## Likely Follow-Ups
- 

## Missing Information
- """,
        success_metric="One founder gets a useful meeting brief from pasted context in under five minutes.",
        first_task="Paste one meeting context and generate a meeting brief draft.",
    ),
}


ALIASES = {
    "customer": "support",
    "customers": "support",
    "ticket": "support",
    "tickets": "support",
    "hire": "recruiting",
    "hiring": "recruiting",
    "candidate": "recruiting",
    "recruiter": "recruiting",
    "expense": "finance",
    "invoice": "finance",
    "cash": "finance",
    "money": "finance",
    "meeting": "admin",
    "calendar": "admin",
    "founder": "admin",
    "admin": "admin",
    "ops": "ops",
    "operations": "ops",
    "slack": "ops",
    "status": "ops",
    "update": "ops",
    "sales": "sales",
    "deal": "sales",
    "crm": "sales",
    "email": "sales",
    "discovery": "sales",
}


def choose_domain(raw: str) -> str | None:
    value = raw.strip().lower()
    if value in DOMAINS:
        return value
    for needle, domain in ALIASES.items():
        if needle in value:
            return domain
    return None


def starter_menu() -> str:
    lines = [
        "# Fede Zero-Input Intake",
        "",
        "Pick the closest domain and rerun with `--domain <name>`:",
        "",
        "| Domain | First useful workflow | Command |",
        "|---|---|---|",
    ]
    for domain in DOMAINS.values():
        top = max(domain.workflows, key=lambda w: w.ice)
        lines.append(f"| {domain.name} | {top.name} | `python3 scripts/fede_intake.py --domain {domain.name}` |")
    return "\n".join(lines)


def table(workflows: tuple[Workflow, ...]) -> str:
    lines = [
        "| Workflow | User | Trigger | Input | Output | Systems | Impact | Confidence | Effort | ICE | Version | Staging Rule |",
        "|---|---|---|---|---|---|---:|---:|---:|---:|---|---|",
    ]
    for item in sorted(workflows, key=lambda w: w.ice, reverse=True):
        lines.append(
            f"| {item.name} | {item.user} | {item.trigger} | {item.input} | {item.output} | {item.systems} | "
            f"{item.impact} | {item.confidence} | {item.effort} | {item.ice} | {item.version} | {item.staging} |"
        )
    return "\n".join(lines)


def build_report(domain: Domain, beginner_text: str) -> str:
    top = max(domain.workflows, key=lambda w: w.ice)
    return f"""# Fede First Workflow Plan

Source input: {beginner_text or domain.label}

## Verdict

Start with **{top.name}**.

## Why

It has the highest ICE score with the lowest live-risk. Build the draft first,
then add connectors only after the output works on real examples.

## ICE Matrix

{table(domain.workflows)}

## Version Plan

- v0: pasted input, copied output, no connectors.
- v1: one repeated workflow, one user, one trigger, one draft output.
- v2: one staged connector with test data, private page, or private channel.
- v3: live action only with approval, logging, monitoring, and rollback.

## First Build Task

{domain.first_task}

## First Output Template

```markdown
{domain.template}
```

## Success Metric

{domain.success_metric}

## 60-Minute Session

| Minute | Action | Output |
|---:|---|---|
| 0-10 | Pick one real example | raw input |
| 10-20 | Run the first prompt | draft output |
| 20-35 | Tighten the template | stable format |
| 35-45 | Add missing-field detection | quality check |
| 45-55 | Save prompt or tiny script | repeatable v0 |
| 55-60 | Define pass/fail | success metric |

## 2-Day Basics Plan

| Time | Goal | Output |
|---|---|---|
| Day 1, hour 1 | Understand the workflow | filled beginner bridge |
| Day 1, hour 2 | Make v0 work once | one good draft |
| Day 1, hour 3 | Turn output into a template | reusable markdown |
| Day 1, hour 4 | Add missing-field checks | quality checklist |
| Day 2, hour 1 | Make it repeatable | saved prompt, script, or tiny local form |
| Day 2, hour 2 | Test on 3 examples | pass/fail notes |
| Day 2, hour 3 | Pick first connector | export, test page, or test channel |
| Day 2, hour 4 | Stage v2 | private test destination and approval rule |

## First Prompt

```text
{domain.prompt}
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Fede beginner workflow plan.")
    parser.add_argument("--domain", default="", help="sales, ops, support, recruiting, finance, admin, or rough description")
    parser.add_argument("--text", default="", help="beginner's rough workflow description")
    args = parser.parse_args()

    selected = choose_domain(args.domain or args.text)
    if not selected:
        print(starter_menu())
        return 0
    print(build_report(DOMAINS[selected], args.text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
