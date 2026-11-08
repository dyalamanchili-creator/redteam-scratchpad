# Deployable vulnerable test API (AWS Lambda)

A throwaway target you deploy into **your own sandbox AWS account** to practice against.
It's a small HTTP API behind API Gateway → Lambda, with individual weak endpoints you can
turn on one at a time. Everything is **off by default** and gated behind env flags so you
never accidentally ship an open target.

> **Rules (non-negotiable):**
> - Deploy only to a **dedicated sandbox account** you own. Never a shared/prod account.
> - Keep it private: API Gateway resource policy locks it to **your IP** (`ALLOWED_CIDR`).
> - The Lambda role is **least-privilege** (logs only). Don't attach broad policies.
> - No real data. Tear it down after each session (`sam delete`).
> - This is for testing *your own* detections and the harness — not third parties.

## Endpoints (each behind a flag)

| Path | Vuln class | Flag (env) | Default |
|------|-----------|------------|---------|
| `/echo` | reflection baseline (safe) | — | on |
| `/fetch?url=` | SSRF | `ENABLE_SSRF` | off |
| `/render?tmpl=` | template/eval surface | `ENABLE_TEMPLATE` | off |
| `/lookup?id=` | injection-style input handling | `ENABLE_INJECTION` | off |

Turn one on only while you're actively testing it, then turn it back off.

## Deploy

Prereqs: AWS SAM CLI, creds for your **sandbox** account, your current public IP.

```bash
cd lambda/vuln-api
export ALLOWED_CIDR="$(curl -s https://checkip.amazonaws.com)/32"
sam build
sam deploy --guided \
  --parameter-overrides AllowedCidr="$ALLOWED_CIDR" EnableSsrf=false EnableTemplate=false EnableInjection=false
```

SAM prints the API URL. Point the harness at it:

```bash
python ../../harness/run.py --target "https://<api-id>.execute-api.<region>.amazonaws.com/Prod" --check echo
```

## Tear down

```bash
sam delete
```

Then confirm in the console that the stack, API, and log group are gone.

## Why gated / IP-locked
A "vulnerable API" with SSRF on a public URL is a liability the moment it's reachable —
bots find it fast and it can be pivoted into the rest of the account. Flags + resource
policy + least-privilege role keep the blast radius to a single disposable function.
See `template.yaml` and `app.py`.
