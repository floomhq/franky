# Report Templates

Load this file only when drafting the final response.

## Demo Report

```markdown
**Verdict:** demo-ready / demo blocked / URL live / incomplete.
**Scope:** demo.
**Who Uses It Next:** teammate / investor / beta user / client / public.
**Before:** trapped on localhost because <verified reason>.
**After:** shareable via <path> with <accepted risk>.
**Fastest Path:** exact platform, commands, and env names.
**Blocker:** one blocker, if any.
**Pattern:** localhost leak / secret exposure / platform mismatch / evidence gap / scope mismatch / none.
**Evidence:** commands run, URL or local route tested, scanner status, smoke status.
**Unverified:** incomplete checks.
```

## Staging Report

```markdown
**Verdict**
**Scope**
**Who Uses It Next**
**Stop-Work Risks**
**Fastest Sane Path**
**Pattern**
**Env And Data Plan**
**Staging Rules**
**Next 24 Hours**
**Evidence**
**Unverified**
```

## Production Report

Use the staging report plus:

```markdown
**Owners And Runbooks**
**Rollback**
**Monitoring**
**Backup And Restore**
**Privacy And AI Spend**
**Residual Risk**
```

## Specific Blocker Report

```markdown
**Verdict:** fixed / blocked / incomplete.
**Scope:** specific-blocker.
**Symptom:** exact error or missing credential/config.
**Root Cause:** verified cause.
**Fix Path:** one concrete fix.
**Verification:** command or route that proves the fix.
**Unverified:** remaining checks.
```

## Workflow Onboarding Report

```markdown
**Verdict:** start with <workflow>.
**Scope:** workflow-onboarding.
**Why:** highest ICE with lowest live-risk.
**ICE Matrix:** workflow, user, trigger, input, output, systems, impact,
confidence, effort, ICE, version, staging rule.
**Version Plan:** v0 manual, v1 narrow, v2 staged connector, v3 live.
**Staging Rule:** read-only, draft, test channel/page/account before live writes.
**First Build Task:** exact first prompt, file, or connector step.
**Unverified:** missing systems, permissions, data, or success criteria.
```
