# Methodology

A loop that keeps the scratchpad honest:

1. **Scope** — add the target to [../SCOPE.md](../SCOPE.md). No row, no testing.
2. **Stand up a target you control** — a `labs/*` container or the `lambda/` vuln-api in a
   sandbox account. Never test third-party/production without written authorization.
3. **Probe with canaries** — use `harness/run.py` + a `payloads/*` catalog. Prefer signals
   (canary tokens, discard-port reachability) over anything destructive.
4. **Capture** — request/response lands in `harness/out/` (gitignored).
5. **Write up the payoff** — in the matching `techniques/` or `labs/` note, record the
   **detection + mitigation**, not just "it worked".
6. **Tear down** — kill the container / `sam delete`. Confirm nothing is left listening on a
   routable interface.
7. **Commit** — small, frequent. Rewrite history freely; never commit captures or secrets.

## Keeping it defensible
Everything here should make a defender better: a detection signature, a WAF/egress rule, a
guardrail regression test, a least-privilege change. If a note ends at the exploit, it's not
done.

## References
- OWASP LLM Top 10 · MITRE ATLAS · NIST AI 100-2
- OWASP Web Security Testing Guide (WSTG) for the web-side methodology
