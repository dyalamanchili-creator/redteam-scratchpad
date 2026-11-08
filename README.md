# redteam-scratchpad

A working-copy, scratchpad-style knowledge base for **AI red-team techniques** and
**application security testing**, with reusable (and clearly-labelled) **vulnerable test
targets** and payload catalogs for use in isolated, authorized lab environments.

This is a living notebook, not a polished framework. Add messy notes, drop in payloads,
spin up a lab, tear it down. The structure below just keeps it from becoming a junk drawer.

---

## ⚠️ Authorized use only

Everything here is for:

- security testing against systems **you own or are explicitly authorized to test**,
- CTF / lab / coursework, and
- defensive research (detections, filters, model-side guardrail evaluation).

The "vulnerable" code in `labs/` and `lambda/` is **deliberately broken**. Never expose it
to the public internet, never deploy it into a shared/production account, and never point
any payload at a system you don't have written permission to test. See [SCOPE.md](SCOPE.md).

---

## Layout

```
techniques/   AI red-team technique notes (prompt injection, tool-abuse, jailbreak eval, ...)
labs/         Self-contained deliberately-vulnerable targets to practice against
  php-cve-2024-4577/   Lab writeup for the PHP CGI argument-injection RCE class
lambda/       Deployable vulnerable API (AWS Lambda) — your throwaway test target
payloads/     Catalogued test inputs (web + LLM), tagged by class and expected behaviour
harness/      Small scripts to fire payloads at a target and record results
docs/         Cross-cutting notes, methodology, references
```

## How I use this

1. Spin up a disposable target (`lambda/` or a `labs/*` container).
2. Grab or write payloads in `payloads/`, tag them.
3. Run `harness/run.py` against the target, capture request/response pairs.
4. Write up what worked in the matching `techniques/` or `labs/` note.
5. Commit. It's a scratchpad — commit often, rewrite history freely, never push the lab
   targets anywhere reachable.

## Quick start

- Read [SCOPE.md](SCOPE.md) first.
- Start with [labs/php-cve-2024-4577/README.md](labs/php-cve-2024-4577/README.md).
- Deploy a test target: [lambda/README.md](lambda/README.md).
