# Tool abuse / excessive agency

**Class:** LLM06 (Excessive Agency) + LLM08 (Vector/tool misuse) · **ATLAS:** AML.T0053

## What / where
An agent with tools (HTTP, shell, DB, email, file I/O) can be steered — often via
[indirect prompt injection](prompt-injection.md) — into calling those tools in ways the
user never intended. The blast radius is whatever the tools can do.

## Preconditions
- The model can invoke tools with side effects (write, send, delete, spend, request URLs).
- Tool arguments are derived from model output without an independent policy check.
- Over-broad credentials/permissions on the tool backend.

## Test procedure (against your lab target)
1. Enumerate the tools the agent exposes and their real permissions.
2. For each side-effecting tool, test whether injected/data-channel text can reach its
   arguments. Use a **harmless sentinel action**: e.g. a tool that fetches a URL → see if
   you can make it fetch `http://127.0.0.1:LAB/canary?from=injection`.
3. Check for SSRF via the agent's HTTP tool (internal metadata endpoints, localhost).
4. Check confirmation gates: do destructive/outbound actions require explicit user OK?

## Signals
- Tool called with attacker-influenced arguments.
- Outbound request to a sentinel URL you planted.
- Side-effecting action fired without user confirmation.

## Mitigations / detections
- Least-privilege tool credentials; per-tool allow-lists for arguments/destinations.
- Human-in-the-loop confirmation for irreversible / outbound / spending actions.
- Deny-by-default egress; block link-local/metadata ranges (SSRF).
- Log every tool call with provenance of its arguments; alert on sentinel hits.

## References
- OWASP LLM06 Excessive Agency / LLM08.
- MITRE ATLAS case studies on agent tool misuse.
