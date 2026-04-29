# Field Hacks

Load this file when the user needs a fast practical move: temporary URL,
domain search, preview deploy, smoke checks, screenshots, or a quick staged
demo path.

## Rule

Label every hack as one of:

- `demo-only`: useful for a call, not stable enough for users.
- `staging`: safe enough for testers with isolated data.
- `production`: requires normal release gates.

Never let a `demo-only` hack become production by accident.

## Temporary URL

Use when the app runs locally and the user needs a quick link for one call.

### Cloudflare Tunnel

Use Cloudflare Tunnel for a temporary URL from a local service.

```bash
cloudflared tunnel --url http://localhost:PORT
```

Classification: `demo-only`.

Rules:

- Use for a live demo or webhook test.
- Keep secrets out of query strings and logs.
- Do not use for customer data, payments, live email, or production auth.
- Replace with staging or production host after the call.

### Ngrok Or Localtunnel

Use only when installed and when Cloudflare Tunnel is unavailable.

```bash
ngrok http PORT
npx localtunnel --port PORT
```

Classification: `demo-only`.

Same safety rules as Cloudflare Tunnel.

### Browser-Use Tunnel

Verified local skill docs include `browser-use tunnel <port>` as a Cloudflare
Tunnel wrapper.

```bash
browser-use tunnel PORT
```

Classification: `demo-only`.

Use when the user needs a public browser-accessible URL from a local port and
the browser-use tooling is available.

## Domain Search

Use when the builder needs a real name quickly.

### Dynadot Bulk Search

Verified from Dynadot official bulk search page on 2026-04-29:
`https://www.dynadot.com/domain/bulk-search`

Dynadot supports pasting many domain names, filtering TLDs, seeing availability,
adding available names to cart, and downloading results.

Flow:

1. Generate 50-200 candidate names.
2. Keep names short, pronounceable, and easy to spell.
3. Paste candidates into Dynadot Bulk Search.
4. Filter to relevant TLDs such as `.com`, `.ai`, `.dev`, `.app`, `.io`.
5. Download results.
6. Shortlist 3 names: safest, clearest, weirdest.
7. Buy only after checking trademarks, obvious confusion, and renewal pricing.

Classification: `staging` for naming; not a launch claim until bought and DNS
is configured.

## Preview Deploys

Use a preview branch when the repo already has CI/deploy wiring.

Verified local deploy notes use:

```bash
git push origin preview
git push origin production
```

Classification: preview branch is `staging`; production branch is `production`.

Rules:

- Preview gets test data and preview secrets.
- Production gets production secrets.
- Do not reuse live provider keys in preview unless explicitly approved.

## Vercel GitHub Auto-Deploy

Use when the project is a static site, Next.js app, or frontend-heavy app and the
user has a GitHub repo.

Verified from Vercel official docs on 2026-04-29:

- Importing a Git repository into Vercel enables automatic deployments.
- Every branch push can create a deployment.
- Pull requests get preview URLs.
- Merges or pushes to the production branch create production deployments.
- Vercel supports changing the production branch and using preview branches or
  custom environments.

Flow:

1. Push repo to GitHub.
2. In Vercel, create New Project from that GitHub repo.
3. Confirm framework preset, root directory, build command, output directory,
   and install command.
4. Add env vars with correct scope: Local, Preview, Production.
5. Deploy once.
6. Open a branch and PR.
7. Verify the preview URL from the PR comment or Vercel dashboard.
8. Merge only after preview smoke checks pass.

Classification: `staging` for preview branches, `production` for production
branch/domain.

Common misses:

- wrong root directory in a monorepo
- missing env vars in Preview scope
- production secrets reused in Preview
- production branch accidentally set to the wrong branch
- app works in dev but no production build command exists
- API base URL points to localhost
- auth callback URL still points to localhost or old preview URL
- database migrations not run before production deploy
- custom domain attached before smoke checks pass
- PR from fork blocked because deployment authorization is required

## Private Publish Ladder

Use when turning a local script or prototype into something others can run:

1. spec first
2. build locally
3. verify locally
4. publish privately
5. verify public staging
6. promote only after staging evidence passes

Classification: `staging`.

Use this for agent-built utilities, internal tools, and demos that need a real
link but not public launch pressure.

## Deploy Dry Run

When `.deploy-stack.yaml` exists, use the deploy-stack pattern:

```bash
python3 ~/.codex/skills/deploy-stack/scripts/deploy_stack.py plan --repo /path/to/repo --environment preview
python3 ~/.codex/skills/deploy-stack/scripts/deploy_stack.py check --repo /path/to/repo --environment preview
python3 ~/.codex/skills/deploy-stack/scripts/deploy_stack.py deploy --repo /path/to/repo --environment preview
python3 ~/.codex/skills/deploy-stack/scripts/deploy_stack.py deploy --repo /path/to/repo --environment preview --apply
```

Classification: `staging`.

Rule: plan, check, dry-run, then apply.

## Vercel Static Page

Use for a quick static landing page or waitlist page.

Verified local launch notes used a temp deploy folder plus:

```bash
vercel --prod --yes
```

Classification: `demo-only` for throwaway pages, `staging` when linked to a
real preview project, `production` only after domain, analytics, and smoke pass.

## Smoke Checks

Use after any deploy, rollback, or tunnel demo.

Verified local rollback runbooks use this shape:

```bash
curl -fsS http://127.0.0.1:PORT/api/health && echo OK_LOCAL || echo FAIL_LOCAL
curl -fsS https://preview.example.com/api/health && echo OK_PUBLIC || echo FAIL_PUBLIC
curl -fsS -o /dev/null -w "%{http_code}\n" https://preview.example.com/ | grep -q "^200$" && echo OK_HOME || echo FAIL_HOME
```

Add one safe canary route:

```bash
curl -fsS -o /dev/null -w "%{http_code}\n" https://preview.example.com/safe-canary | grep -q "^200$" && echo OK_CANARY || echo FAIL_CANARY
```

Classification: `staging` or `production`, depending on target.

## Browser QA Proof

Use when the page is part of the deliverable:

1. run in a real browser
2. test desktop and mobile
3. reach the completed result state
4. save screenshots
5. record console or network errors

Classification: `staging`.

Evidence is a screenshot of the completed state, not a loading screen.

## Screenshot Checks

Use when the output is visual or shared with non-technical users.

Verified local UX/product audit skills capture full-page desktop and mobile
screenshots. Minimum manual version:

- desktop page loaded
- mobile page loaded
- no loading skeleton as final evidence
- primary CTA visible
- no obvious overlap or clipped text

Classification: `staging`.

## DNS And Custom Domain

Use after a preview URL is stable and the user wants a real domain.

Verified local DNS skill uses IONOS API flow:

```bash
# list zones
# list records
# add/update/delete A, CNAME, TXT, MX records
# verify with dig
dig example.com
dig www.example.com
```

Classification: `production` for customer-facing domains, `staging` for
preview subdomains.

Rule: verify DNS with `dig` and verify HTTPS after records propagate.

## Common Beginner Mistakes

Use this as a diagnostic checklist before picking a platform:

- Building five workflows before one manual v0 works.
- Connecting Gmail, Slack, Notion, or CRM before the draft output is useful.
- Letting AI send or write live data before staged approval exists.
- No `.env.example`; only `.env.local` on the builder's machine.
- Secrets pasted into code, screenshots, prompts, logs, or frontend env vars.
- Hardcoded `localhost` in API URLs, auth callbacks, CORS, webhooks, or
  WebSockets.
- Picking Vercel for an app that needs local files, WebSockets, SQLite, workers,
  or long AI calls.
- Picking a VPS before testing a managed preview deploy.
- No health route, no canary route, and no smoke command.
- No distinction between demo, staging, and production.
- No rollback story before a customer-facing launch.
- Buying a domain before checking spelling, renewal price, trademark risk, and
  whether the app is even shareable.
- Treating a tunnel URL as deployment.
- Treating a successful build as proof that the workflow works.

## Local Script To Shareable Tool

Use for simple AI utilities and internal tools:

1. local script
2. hosted web app
3. HTTP API
4. MCP/tool interface when useful
5. shareable run page

Classification: starts as `staging`; becomes `production` only after normal
release gates.

This is useful when the builder has a Python script, CLI, or agent workflow and
a non-technical teammate needs to run it.

## Laptop Demo Fallback

Use only for a live call when no hosting path is available.

Verified local research noted `caffeinate -d` as a Mac keep-awake workaround for
scripts that only run while the laptop is open.

```bash
caffeinate -d
```

Classification: `demo-only`.

Rule: this is a stopgap, not deployment.
