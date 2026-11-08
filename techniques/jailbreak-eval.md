# Jailbreak / guardrail evaluation methodology

**Class:** LLM01 (guardrail bypass) · purpose here is **measuring** guardrail robustness.

## What / where
Systematically measure how well a model/app's safety guardrails hold against adversarial
phrasing, so you can report a pass/fail rate and track it across model or prompt changes.
This is evaluation, not an attempt to actually elicit harmful content — use **proxy
behaviours** and canaries, not real harmful requests.

## Method
1. Define a **refusal policy** for the app: what it should decline.
2. Build a test set of prompts that *should* be refused, each paired with the expected
   refusal. Keep real harmful content out — use benign stand-ins that trigger the same
   policy path (e.g. a fictional "forbidden token" the system prompt says never to reveal).
3. Apply transformation families to each prompt and record whether the guardrail still
   holds: role-play framing, obfuscation/encoding, context-stuffing, multi-turn setup.
4. Score: refusal rate per family; track over time / across model versions.

## Signals
- App emits the forbidden canary / violates its stated refusal policy.
- Refusal rate drops for a given transformation family (regression).

## Mitigations / detections
- Independent output classifier in addition to prompt-level instructions.
- Refusal-rate regression tests in CI (reuse this eval set).
- Multi-turn state tracking (don't let setup turns launder a later request).

## References
- NIST AI 100-2 adversarial ML taxonomy.
- OWASP LLM01; vendor model cards / usage policies for the refusal baseline.
