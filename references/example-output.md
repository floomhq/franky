# Example Output

Load this file only when an example final answer helps calibrate tone or
structure.

## Demo Verdict Example

```markdown
**Verdict:** demo blocked.
**Scope:** demo.
**Who Uses It Next:** beta user.
**Before:** app runs locally, but production start is not configured.
**After:** one start-script fix away from a safe demo deploy.
**Fastest Path:** add a production start command, set `PORT`, deploy to Render
or Railway, then smoke `/health`.
**Blocker:** server binds to a hardcoded local port.
**Pattern:** localhost leak.
**Evidence:** `npm run build` passed; first-pass scan found `localhost` in
server config; no dedicated scanner available, so `secret scan: incomplete`.
**Unverified:** live URL, dedicated secret scan, mobile screenshot.
```

## Specific Blocker Example

```markdown
**Verdict:** blocked.
**Scope:** specific-blocker.
**Symptom:** deploy fails because the app expects `.env.local`.
**Root Cause:** env names exist only in local env, with no `.env.example` or
platform secret list.
**Fix Path:** create `.env.example` with names only, then set runtime secrets in
the host.
**Verification:** rerun build after env names are documented and required
runtime secrets are present.
**Unverified:** scanner, smoke route, auth callbacks.
```

## Workflow Onboarding Example

```markdown
**Verdict:** start with discovery prep notes.
**Scope:** workflow-onboarding.
**Why:** highest ICE with low live-risk; manual inputs and private draft output.
**ICE Matrix:** discovery prep 80, weekly Slack update 64, email draft 48, CRM
entry draft 45, live call assistant 10.
**Version Plan:** v0 pasted deal context to prompt; v1 draft prep note with no
connectors; v2 read-only Gmail/CRM exports plus private Notion test page; v3
live sales prep with logs and owner.
**Staging Rule:** no live writes in v1; private Notion test page starts at v2.
**First Build Task:** ask Cursor/Claude to map inputs, output format, missing
fields, and success criteria for one real deal.
**Unverified:** CRM fields, Gmail access, Notion database schema.
```
