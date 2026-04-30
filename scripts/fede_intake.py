#!/usr/bin/env python3
"""Guided zero-to-first-workflow intake for Fede.

The script has no external dependencies. It turns a vague beginner answer into a
draft-first workflow plan with ICE, versions, staging, and a first prompt.
"""

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


PRESETS: dict[str, list[Workflow]] = {
    "sales": [
        Workflow("Discovery prep note", "sales", "meeting tomorrow", "pasted deal context", "Notion-ready prep note draft", "manual paste/export", 5, 4, 4, "v1", "no connector writes"),
        Workflow("Weekly update", "team", "Friday", "pasted CRM changes and notes", "Slack update draft", "manual paste/export", 4, 4, 4, "v1", "draft only"),
        Workflow("Email assistant", "sales", "inbound email", "pasted thread", "reply draft", "manual paste/export", 4, 3, 4, "v1", "no auto-send"),
        Workflow("CRM entry assistant", "sales", "new lead", "pasted email or notes", "CRM field draft", "manual paste/export", 5, 3, 3, "v1", "human copies fields"),
        Workflow("Live-call assistant", "sales", "live call", "transcript and references", "objection support", "call tool, CRM, knowledge base", 5, 2, 1, "v0 later", "no live assist until evals pass"),
    ],
    "ops": [
        Workflow("Weekly ops update", "ops lead", "Friday", "pasted notes, metrics, blockers", "Slack-ready update draft", "manual paste/export", 5, 4, 4, "v1", "draft only"),
        Workflow("Support reply draft", "support", "new ticket", "pasted ticket and account notes", "reply draft", "manual paste/export", 4, 4, 4, "v1", "no auto-send"),
        Workflow("Task cleanup", "ops", "end of day", "pasted Slack/Notion notes", "prioritized task list", "manual paste/export", 4, 3, 4, "v1", "no task writes"),
        Workflow("CRM hygiene", "sales ops", "stale deal", "pasted CRM fields", "proposed field updates", "CRM export", 4, 3, 3, "v1", "human copies fields"),
        Workflow("Automated notifications", "team", "status change", "CRM/Notion event", "Slack notification", "Slack, CRM, Notion", 4, 2, 2, "v2 later", "private test channel first"),
    ],
}


def choose_domain(raw: str) -> str:
    value = raw.strip().lower()
    if value in PRESETS:
        return value
    if any(word in value for word in ["deal", "crm", "sales", "email", "discovery"]):
        return "sales"
    return "ops"


def table(workflows: list[Workflow]) -> str:
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


def first_prompt(top: Workflow) -> str:
    if "ops" in top.name.lower():
        return """You are helping me build one narrow ops workflow.

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

First, ask me for one real weekly notes example. Then turn it into the output format."""
    return """You are helping me build one narrow sales workflow.

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

First, ask me for one real deal example. Then turn it into the output format."""


def build_report(domain: str, beginner_text: str) -> str:
    workflows = PRESETS[domain]
    top = max(workflows, key=lambda w: w.ice)
    return f"""# Fede First Workflow Plan

Source input: {beginner_text or "blank beginner intake"}

## Verdict

Start with **{top.name}**.

## Why

It has the highest ICE score with the lowest live-risk. Build the draft first,
then add connectors only after the output works on real examples.

## ICE Matrix

{table(workflows)}

## Version Plan

- v0: pasted input, copied output, no connectors.
- v1: one repeated workflow, one user, one trigger, one draft output.
- v2: one staged connector with test data, private page, or private channel.
- v3: live action only with approval, logging, monitoring, and rollback.

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
{first_prompt(top)}
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Fede beginner workflow plan.")
    parser.add_argument("--domain", default="", help="sales, ops, or a rough description")
    parser.add_argument("--text", default="", help="beginner's rough workflow description")
    args = parser.parse_args()

    domain = choose_domain(args.domain or args.text)
    print(build_report(domain, args.text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
