# Advanced Gates

Use this file only for `staging` and `production` consults, or when a demo has
auth, durable data, external side effects, uploads, background jobs, or AI spend.
Assess each gate as `pass`, `blocked`, `partial`, or `not applicable`; include
evidence for any `pass`.

## Status Rules

- `pass`: evidence is attached.
- `partial`: the control exists, but coverage is incomplete.
- `blocked`: a required control is missing or unverifiable.
- `not applicable`: the app has no path that can trigger this gate.

Use this table format for staging and production review:

| Gate | Status | Evidence | Next Action |
|---|---|---|---|
| Auth and authorization | pass/blocked/partial/not applicable | command, route, screenshot, config, or test | next concrete action |
| Data, storage, and migrations | pass/blocked/partial/not applicable | migration output, schema file, backup proof, or config | next concrete action |
| AI and external providers | pass/blocked/partial/not applicable | sandbox config, timeout, budget, eval, or log redaction proof | next concrete action |
| Release and staging | pass/blocked/partial/not applicable | CI output, deploy log, release note, or rollback proof | next concrete action |
| Observability and operations | pass/blocked/partial/not applicable | health URL, log location, alert, metric, or owner | next concrete action |
| Security and supply chain | pass/blocked/partial/not applicable | scanner output, audit output, header check, or CORS config | next concrete action |
| Privacy and compliance | pass/blocked/partial/not applicable | data map, retention rule, approval, or provider setting | next concrete action |

## Auth And Authorization

- Server-side authorization protects private data and privileged actions.
- Cookie auth uses `HttpOnly`, `Secure`, and appropriate `SameSite`.
- Cookie-authenticated writes have CSRF protection.
- OAuth callback, logout, and redirect URLs match the intended environment.
- Admin and support paths have explicit role checks and audit logs.
- User-controlled HTML, Markdown, files, URLs, and callback targets are validated
  or sanitized before use.

## Data, Storage, And Migrations

- Production and staging use separate databases, buckets, auth tenants, webhook
  endpoints, and secrets.
- Migrations are versioned, repeatable, and part of release.
- Every schema change has rollback or forward-fix notes.
- Durable uploads use object storage, not ephemeral local disk.
- Backups, retention, restore command, RPO, and RTO are documented before live
  customer data.
- Seed or fixture data exists for staging smoke tests without production data.

## AI And External Providers

- AI calls have timeouts, retry boundaries, budget limits, and user-visible
  failure states.
- Prompt-injection risk is reviewed for tools, browsing, file access, and
  retrieval-augmented generation.
- Tool permissions are least-privilege and environment-scoped.
- Prompt and output logs redact secrets, PII, credentials, and customer data.
- A golden-path AI test, eval, fixture, or manual smoke case exists.
- Provider fallback, quota exhaustion, and billing-limit behavior are documented.
- Payment, email, webhook, and AI-spend tests use sandbox providers or explicit
  approval.

## Release And Staging Rules

- Main branch or PR previews deploy to staging when the repo supports it.
- Production deploys from a tagged release, approved promotion, or documented
  release branch.
- CI runs install, build, lint or typecheck, tests, secret scan, and smoke checks
  before staging or production deploys.
- Release notes list schema changes, env changes, provider changes, and rollback
  steps.
- Rollback covers app version, migrations, workers, cron, provider config, and
  feature flags.
- Staging exercises migrations, worker startup, scheduled jobs, webhooks, and
  rollback before production promotion.

## Observability And Operations

- Health checks or uptime checks cover the public URL and core API.
- Runtime exceptions go to error tracking or accessible deploy logs.
- Logs include request IDs or correlation IDs for key workflows.
- Metrics cover request rate, latency, error rate, job failures, queue depth,
  provider failures, and AI spend where applicable.
- Alerts cover downtime, elevated errors, failed jobs, exhausted budgets, and
  failed deploys.
- Owners are named for deploys, incidents, secrets, providers, backups, and
  billing.

## Security And Supply Chain

- A dedicated secret scanner such as `gitleaks`, `trufflehog`, or repo-native
  equivalent passes for staging and production verdicts.
- Any discovered secret is treated as compromised and rotated before sharing.
- Dependency audit runs through the project package manager or configured
  scanner.
- Container images run as non-root, expose a health check, and are scanned when
  Docker tooling is present.
- CORS is restricted for public APIs.
- Security headers are configured for web apps: CSP, HSTS, frame controls,
  `X-Content-Type-Options`, and `Referrer-Policy`.
- SSRF protections exist for URL fetchers, importers, crawlers, webhooks, and AI
  browsing or tool calls.

## Privacy And Compliance Triage

- Sensitive data types are listed: PII, customer data, financial data,
  health data, children data, secrets, uploaded files, logs, and prompts.
- Regulated or compliance-sensitive data has explicit approval before staging or
  production advice.
- Data residency, retention, deletion, and access controls are documented when
  customers or regulated data are in scope.
- Analytics, logging, and AI providers avoid storing sensitive data unless the
  user has approved that risk.

## Smoke Recipes

Use only safe, environment-appropriate data.

### Login And Session

1. Visit login page.
2. Complete sandbox or test login when credentials are available.
3. Confirm session persists after refresh.
4. Confirm logout clears session.
5. Confirm private route rejects anonymous access.

### Upload Flow

1. Upload a tiny benign fixture to staging storage.
2. Confirm file appears in the expected bucket or storage path.
3. Confirm generated URL or processing result works.
4. Delete the fixture or confirm lifecycle cleanup.

### Webhook Delivery

1. Use sandbox provider event or local replay tool.
2. Verify signature check passes.
3. Verify duplicate delivery is idempotent.
4. Verify failure logs are findable.

### Background Job Startup

1. Start worker or scheduled job process in staging.
2. Enqueue a harmless fixture job.
3. Verify completion, logs, retries, and failure visibility.
4. Confirm HTTP requests do not block on long-running work.

### Rollback Rehearsal

1. Identify current release artifact or tag.
2. Identify prior known-good artifact or tag.
3. Confirm app rollback command.
4. Confirm migration rollback or forward-fix path.
5. Confirm provider config and feature-flag rollback path.

## Production Report Additions

Add these sections to the staging report:

```markdown
**Owners And Runbooks**
Deploy, incident, secrets, providers, backups, billing, and log locations.

**Rollback**
Exact app, migration, job, provider, and feature-flag rollback path.

**Monitoring**
Health checks, logs, metrics, alerts, and known blind spots.

**Backup And Restore**
Backup schedule, retention, restore command, RPO, RTO, and last tested restore.

**Privacy And AI Spend**
Sensitive data flows, prompt/output logging policy, model/provider limits, and
budget guardrails.

**Residual Risks**
Accepted risks, why they are accepted, and the trigger for revisiting them.
```
