# Installing OpenClaw Safely

A vetted, security-first guide to installing **OpenClaw** (the self-hosted personal
AI agent / gateway — formerly *Moltbot* / *Clawdbot*).

> Verified against the canonical project on **2026-06-30**:
> npm package `openclaw@2026.6.11`, MIT licensed, repo
> `https://github.com/openclaw/openclaw`, maintainers `steipete`
> (Peter Steinberger) + `vincentkoc`. A trial install was run in an isolated
> sandbox and `openclaw doctor` confirmed the real tool.

---

## ⚠️ Read this first — the threat landscape

OpenClaw itself is a legitimate open-source project, but its *ecosystem* is
currently a popular malware target. Treat the following as hard rules:

1. **Install only from the canonical sources** — the npm package `openclaw`
   (or `github.com/openclaw/openclaw`). Nothing else.
2. **Never run a `curl … | bash` one-liner from a blog, gist, or "setup guide
   I wish I had."** Security vendors (McAfee, Kaspersky) have documented the
   *ClickFix* technique: fake install guides that get you to paste a malicious
   command yourself. The official install is a plain `npm install` — if a guide
   tells you to pipe a script from a random domain, it is not the official one.
3. **Install zero third-party plugins/skills during setup.** 230+ credential-
   and crypto-stealing plugins were published to "ClawHub" and GitHub in a
   single week. Get the bare gateway working first; add plugins later, one at a
   time, only after reading their source.
4. **Never expose the gateway to the public internet unauthenticated.**
   ~1,000 OpenClaw instances were found publicly reachable with no auth. Keep it
   on localhost/your private network and turn token auth on.
5. **Beware impersonation.** There is a hijacked-handle `$CLAWD` crypto scam and
   fake OpenClaw websites. OpenClaw has **no token and asks for no payment** to
   install. Ignore anything that does.

---

## Prerequisites

- **Node.js 24 (recommended) or 22.19+** and a package manager (`npm` or `pnpm`).
  Check: `node --version`.
- macOS, Linux, or Windows.
- An LLM provider API key (e.g. Anthropic/OpenAI) when you reach onboarding —
  have it ready but don't paste it anywhere except OpenClaw's own prompts.

---

## Step 1 — Install from the official npm package

```bash
npm install -g openclaw@latest
# or, with pnpm:
# pnpm add -g openclaw@latest

openclaw --version    # expect: OpenClaw 2026.x.x (…)
```

Before trusting it, confirm the package points back to the real repo:

```bash
npm view openclaw repository.url license maintainers
# repository.url should be git+https://github.com/openclaw/openclaw.git
# license should be MIT
```

> **From-source alternative** (only if you specifically want to build it):
> ```bash
> git clone https://github.com/openclaw/openclaw.git
> cd openclaw && pnpm install && pnpm openclaw setup
> ```

## Step 2 — Run the doctor before anything else

```bash
openclaw doctor
```

On a fresh install it will (correctly) flag the items you must fix in Step 3:
- `gateway.mode` is unset → gateway start is blocked until you set it.
- **Gateway auth is off** → token auth is the recommended default, *even on
  loopback*.
- **No command owner** is configured → nobody is authorized for owner-only
  commands yet.

## Step 3 — Harden before you connect anything

Do these **before** adding any messaging channel or starting the gateway.

```bash
# 3a. Keep the gateway local (do NOT use remote unless you've read the
#     security runbook and put it behind a VPN/Tailscale + auth).
openclaw config set gateway.mode local

# 3b. Designate yourself as the command owner. DM pairing alone does NOT make
#     someone an owner — owner-only commands (/config, /diagnostics, exec
#     approvals) require this. Use your own channel user id.
openclaw config set commands.ownerAllowFrom '["telegram:<your-user-id>"]'

# 3c. Sandbox non-main sessions so untrusted senders can't run tools on your host.
openclaw config set agents.defaults.sandbox.mode non-main
```

Then run the guided setup, which turns on gateway **token auth** for you:

```bash
openclaw onboard      # or: openclaw configure
```

> Skip `--install-daemon` until you've finished hardening and tested manually.
> The daemon registers a background service; you don't want a misconfigured
> gateway auto-starting.

## Step 4 — Connect a channel, with pairing left ON

```bash
openclaw channels --help     # see supported channels (Telegram, Discord, etc.)
```

OpenClaw's default is safe: an **unknown sender gets a pairing code and their
message is NOT processed** until you approve it. Keep that default. Approve only
people you intend to:

```bash
openclaw pairing approve <channel> <code>
```

Treat **every inbound DM as untrusted input** — it can contain prompt-injection
attempts aimed at your agent.

## Step 5 — Start it and re-check

```bash
openclaw gateway start
openclaw doctor          # should now be clean
openclaw logs            # watch what it's actually doing
```

---

## Ongoing safety checklist

- [ ] Gateway bound to localhost / private network — **never** raw public internet.
- [ ] Token auth ON (verify with `openclaw doctor`).
- [ ] Command owner set to *only* your own ids.
- [ ] `sandbox.mode = non-main` so untrusted sessions are isolated.
- [ ] Pairing left ON; approve senders deliberately.
- [ ] Zero plugins beyond what you've read the source of.
- [ ] Re-run `openclaw doctor` after any config change.
- [ ] Before *ever* exposing remotely, read the official Security runbook:
      <https://docs.openclaw.ai/gateway/security>

## Canonical sources (bookmark these, ignore everything else)

- Repo: <https://github.com/openclaw/openclaw>
- npm: <https://www.npmjs.com/package/openclaw>
- Docs: <https://docs.openclaw.ai>
