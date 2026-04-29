# Franky Evidence Ledger

Purpose: public-safe source map for launch copy.

## Privacy Rule

Use aggregate facts publicly. Do not publish interviewee names, company names,
direct quotes, LinkedIn URLs, or sensitive business context.

## Public-Safe Claims

| Public claim | Verified source fact | Public use | Private boundary |
|---|---|---|---|
| I reviewed 16 discovery calls. | Interview synthesis covers 16 calls from April 2-8, 2026. | Safe as aggregate count. | Do not list roster. |
| Strong ICP fit appeared in 9 of 16 calls. | Interview synthesis scorecard marks 9 strong ICP fits. | Safe as aggregate ratio. | Do not name the 9. |
| Builders repeatedly care more about reliability than speed. | Interview synthesis marks reliability over speed as a high-confidence finding across all calls. | Safe as pattern. | Do not quote individuals. |
| Staging/prod separation came up repeatedly. | Interview synthesis lists staging/prod as high-confidence across technical and ops profiles. | Safe as pattern. | Do not attach to named users. |
| Observability was a repeated missing layer. | Interview synthesis identifies observability as a high-confidence missing feature. | Safe as pattern. | Do not expose specific company workflows. |
| Some teams use Google Sheets as operational data storage. | Interview synthesis lists Google Sheets as database across multiple calls. | Safe as aggregate pattern. | Do not name teams. |
| n8n frustration appeared repeatedly. | Interview synthesis lists n8n frustration as high confidence across multiple users. | Safe as aggregate pattern. | Do not use direct quotes. |
| The core gap is local prototype to team/client-facing use. | Interview synthesis identifies local tools and client-facing UI as a key recurring gap. | Safe as positioning. | Do not expose paid-client details. |

## Visible Proof Spine

Use this in launch materials when space permits:

```text
Proof spine: 16 discovery calls reviewed, 9 strong ICP fits, 5 repeated blockers
extracted, and a scanner-backed consult workflow created from those patterns.
```

The 5 repeated blockers:

| Blocker | Evidence basis | Public-safe phrasing |
|---|---|---|
| localhost leak | Discovery notes and repo-audit pattern: local callbacks, API bases, CORS, and routes often fail when the URL changes. | Production paths still point at local-only addresses. |
| secret exposure | Consult workflow and readiness gates repeatedly treat keys, tokens, and env handling as stop-work risk. | Sharing is blocked until secrets are scanned and rotated if exposed. |
| platform mismatch | Interview synthesis and deploy audits show host choice depends on SQLite, workers, WebSockets, long AI calls, and files. | The host has to match the app shape. |
| evidence gap | Interview synthesis emphasizes reliability, staging/prod, observability, and proof over speed. | The app may run, but it is not shareable until checks are visible. |
| scope mismatch | Interview synthesis separates demo, staging, and production needs across technical and ops profiles. | A requested demo can become a staging problem when data or side effects are live. |

## Launch Copy Claim Map

| Copy line | Evidence ledger row |
|---|---|
| "I reviewed 16 discovery calls..." | 16 discovery calls |
| "local is easy now, shareable is still hard" | core gap |
| "env vars, secrets, auth callbacks, deploy targets, staging, smoke tests, and rollback" | staging/prod, reliability, observability, core gap |
| "No platform pitch" | skill contract and vendor-neutral scope |
| "not safe to share yet verdict" | evidence floor and advanced gates |

## Claims Not Cleared

- Any named customer, company, or role-specific quote.
- Any paid conversion, revenue, waitlist, signup, or retention claim.
- Any claim that the consult guarantees deployment.
- Any claim that production readiness was verified for a real customer app.
