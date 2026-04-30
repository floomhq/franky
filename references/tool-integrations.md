# Tool Integrations

Load this file when scanner or check execution details are needed.

## First-Pass Scanner

```bash
python3 ~/.codex/skills/fede-coach/scripts/fede_scan.py .
python3 ~/.codex/skills/fede-coach/scripts/fede_scan.py . --json
```

These commands assume Fede is installed at `~/.codex/skills/fede-coach`. From a
fresh repo clone, use `python3 scripts/fede_scan.py . --json`.

The first-pass scanner detects stack metadata, localhost references, secret-like
keywords, git status, and scanner tool availability. It redacts matched values
by printing file paths and line numbers only.

## Beginner Intake CLI

Use when the user has no repo, no clear workflow, or needs a generated first
plan:

```bash
python3 scripts/fede_intake.py --text "I am a beginner and want to automate CRM, Slack, Notion, and emails"
python3 scripts/fede_intake.py --domain ops --text "I need weekly updates and support replies"
```

The output is a deterministic Markdown starter plan with ICE, versions, staging,
a 60-minute session, a 2-day basics plan, and a first prompt.

## Dedicated Secret Scanners

Run at least one dedicated scanner for staging or production readiness:

```bash
gitleaks detect --no-banner --redact
trufflehog filesystem --no-update .
```

Or run available scanners through the bundled first-pass scanner:

```bash
python3 ~/.codex/skills/fede-coach/scripts/fede_scan.py . --run-scanners --json
```

If scanners are missing:

```text
secret scan: incomplete
```

Demo consults can continue with that caveat. Staging and production readiness
remain blocked.

## Check Matrix Validation

The deterministic check matrix is valid only when the final report includes:

- command or blocker evidence for the relevant stack
- scanner status
- smoke status
- unverified checks

Use this evidence shape:

```markdown
**Evidence**
- stack: JS/TS
- install: passed via `npm ci`
- build: passed via `npm run build`
- production start: blocked, app expects local `.env.local`
- scanner: incomplete, no dedicated scanner available
- smoke: not run because production start blocked
- unverified: live URL, auth callback, mobile layout
```
