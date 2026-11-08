# AI red-team techniques

Notes on techniques for probing LLM-backed applications. The goal is to find where an app's
trust boundaries break down so they can be fixed — the useful output of each note is the
**detection / mitigation**, not just the attack.

Anchored to public taxonomies so notes stay comparable:

- **OWASP Top 10 for LLM Applications** — https://genai.owasp.org/llm-top-10/
- **MITRE ATLAS** (adversarial ML tactics/techniques) — https://atlas.mitre.org/
- **NIST AI 100-2 / AML taxonomy** — adversarial ML attacks & mitigations

## Index

| Note | Class | OWASP LLM | Status |
|------|-------|-----------|--------|
| [prompt-injection.md](prompt-injection.md) | Direct / indirect injection | LLM01 | seed |
| [tool-abuse.md](tool-abuse.md) | Excessive agency / tool misuse | LLM06 / LLM08 | seed |
| [jailbreak-eval.md](jailbreak-eval.md) | Guardrail evaluation methodology | LLM01 | seed |
| _data-exfil.md_ | Sensitive info disclosure | LLM02 | todo |
| _supply-chain.md_ | Model/plugin supply chain | LLM03 / LLM05 | todo |

## Note template

Each note follows:

1. **What / where** — the trust boundary being tested.
2. **Preconditions** — what the app must do for this to apply.
3. **Test procedure** — how to probe it (against *your* lab target).
4. **Signals** — how to tell it worked.
5. **Mitigations / detections** — the payoff.
6. **References**.
