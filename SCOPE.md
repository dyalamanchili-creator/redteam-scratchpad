# Scope & rules of engagement

Fill this in **before** each engagement or lab session. If a target isn't listed here with
authorization, it's out of scope — full stop.

## Authorization checklist

- [ ] I own the target, or I hold **written** authorization to test it.
- [ ] Testing window and allowed techniques are agreed (no DoS unless explicitly permitted).
- [ ] Vulnerable labs run **only** in an isolated network / throwaway cloud account.
- [ ] No real user data is loaded into any lab target.
- [ ] Findings are handled per the disclosure policy below.

## In-scope targets (this session)

| Target | Owner / auth ref | Window | Allowed | Notes |
|--------|------------------|--------|---------|-------|
| local `labs/*` containers | me (localhost) | always | all | isolated |
| my AWS sandbox acct `xxxx` | me | always | all | tear down after |
|        |                  |        |         |       |

## Hard limits (never, regardless of scope)

- No destructive techniques, DoS, or data-destruction against anything shared/production.
- No mass/untargeted scanning or exploitation.
- No testing third-party or production systems without written authorization.
- No real credentials, PII, or secrets in this repo (see `.gitignore` / `payloads/`).

## Disclosure

If a technique here maps to a real third-party product, follow coordinated disclosure:
report to the vendor, give them a remediation window, don't publish working exploit chains
against unpatched production systems.
