# Payload catalog

Reusable test inputs, tagged by class and expected behaviour. Each payload is a **probe**:
it should prove a boundary broke (via a canary / observable side effect), not cause damage.

Keep weaponized / destructive payloads out of this repo. If you need large public corpora,
reference them by link and pull them at run time — don't vendor them here.

## File format (`*.yaml`)

```yaml
- id: short-unique-id
  class: ssrf | injection | ssti | prompt-injection | tool-abuse | ...
  target: web | llm
  payload: "the input to send"
  send:  { param: url }          # how the harness places it (querystring param, body, etc.)
  expect: "canary / signal that means it worked"
  notes: "context, source, caveats"
```

## Catalogs
- [web.yaml](web.yaml) — web-app probes against your lab / vuln-api.
- [llm.yaml](llm.yaml) — LLM-app probes (canary-based, benign).

## Public corpora (link, don't vendor)
- SecLists (payload wordlists): https://github.com/danielmiessler/SecLists
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings
- OWASP LLM / garak (LLM vuln scanner) for prompt-side test generation.

> Everything here is a canary/signal probe meant for targets you own. See ../SCOPE.md.
