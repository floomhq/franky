# Franky

Franky is a vendor-neutral AI building coach for beginners, operators, and
builders with AI-made prototypes.

It helps a user go from "I have workflow ideas" or "this works on localhost" to
one concrete next build step: workflow map, ICE ranking, v0/v1/v2/v3 plan,
staging rules, live-URL path, and evidence-based blockers.

## TL;DR

Franky answers:

- What do I build first?
- Which workflow has the best impact, confidence, and effort profile?
- What is v0, v1, v2, and v3?
- What needs staging before live writes?
- Can this localhost prototype become a shareable URL?
- What blocks demo, staging, or production readiness?

## Example Prompt

```text
I am a beginner.

I want to automate:
- emails
- CRM entries
- deal notes and discovery prep in Notion
- weekly updates and notifications in Slack

Later I want a live-call sales assistant for objections and reference customer
data.

Help me map workflows, score ICE, pick the first v1, define staging, and give me
the first build task.
```

## What Franky Does

Franky has two modes:

- `workflow-onboarding`: no repo yet. It maps workflows, creates an ICE matrix,
  picks the first v1, defines version stages, and gives a first build task.
- `prototype-to-live`: repo exists. It inspects the app, scans for localhost
  leaks, env gaps, secrets risk, staging gaps, deployment fit, and smoke-test
  evidence.

Franky always thinks in:

- ICE: impact, confidence, effort
- versions: v0 manual proof, v1 narrow workflow, v2 staged connector flow, v3
  monitored live workflow
- staging: separate test data, sandbox accounts, preview deploys, dry-runs, and
  rollback before real users or live side effects

## Public-Safe Launch Copy

Launch copy lives in:

- `references/public-launch-copy.md`
- `references/evidence-ledger.md`

The public proof spine:

```text
16 discovery calls reviewed, 9 strong ICP fits, 5 repeated blockers extracted,
and a scanner-backed consult workflow created from those patterns.
```

Do not publish interviewee names, company names, or direct quotes.

## Install As A Codex Skill

Clone or copy this repository into the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/floomhq/franky.git ~/.codex/skills/franky
```

Then use:

```text
Use $franky to map workflows, score ICE, plan versions and staging, inspect the
repo if one exists, and return the next concrete build step with evidence.
```

Commands in `SKILL.md` assume Franky is installed at `~/.codex/skills/franky`.
From a fresh clone, use repo-local commands such as `python3
scripts/franky_scan.py . --json`.

## Scanner

Franky includes a first-pass scanner:

```bash
python3 scripts/franky_scan.py . --json
```

The scanner finds common prototype-to-live blockers:

- localhost and tunnel references
- env file and env schema signals
- suspicious secret patterns
- framework and platform config hints
- package scripts
- git status
- optional scanner availability

The scanner is not a replacement for `gitleaks`, `trufflehog`, package audits,
browser QA, or live smoke tests.

The heuristic findings are intentionally noisy because the scanner flags
keywords and localhost references by file and line only. Treat the dedicated
scanner pass, such as `gitleaks dir --no-banner --redact .`, as the real leak
signal.

## Field Hacks

Franky includes practical hacks in `references/field-hacks.md`:

- temporary URLs with Vercel previews, Cloudflare Tunnel, ngrok, localtunnel, or
  Tailscale Funnel
- Dynadot bulk domain search
- Vercel GitHub auto-deploy setup
- curl smoke checks
- browser QA prompts
- custom-domain DNS checks
- common beginner mistakes

## Repo Layout

```text
SKILL.md
agents/openai.yaml
scripts/franky_scan.py
templates/consult-note.md
references/
```

## License

MIT
