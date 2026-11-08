# harness

Small stdlib runner that fires canary/signal probes at a target **you own** and saves each
request/response under `out/` (gitignored).

```bash
# built-in checks
python harness/run.py --target http://127.0.0.1:8080 --check echo
python harness/run.py --target http://127.0.0.1 --check cve_2024_4577

# run a payload catalog (needs pyyaml: pip install pyyaml)
python harness/run.py --target http://127.0.0.1:8080 --catalog payloads/web.yaml
```

Rules baked in:
- Non-loopback targets require `--i-have-authorization` **and** a matching row in
  [../SCOPE.md](../SCOPE.md).
- Probes are benign (canaries, discard-port reachability), not weaponized exploits.
- Output in `out/` can contain target responses — it's gitignored; don't commit captures.
