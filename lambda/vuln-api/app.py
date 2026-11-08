"""
Deliberately-vulnerable test API for AUTHORIZED LAB USE ONLY.

Deploy to a dedicated sandbox AWS account, locked to your own CIDR (see template.yaml).
Every weak endpoint is OFF unless its env flag is "true". Turn one on only while you are
actively testing it, then turn it back off and tear the stack down.

This exists so you can practice finding and *detecting* these classes against a target you
control. Do not point it at, or reuse it against, anything you don't own.
"""
import json
import os
import urllib.request


def _enabled(flag: str) -> bool:
    return os.environ.get(flag, "false").lower() == "true"


def _resp(status: int, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _qs(event) -> dict:
    return event.get("queryStringParameters") or {}


# A tiny in-memory "dataset" so the injection demo needs no real database.
_RECORDS = {
    "1": {"id": "1", "name": "alice", "role": "user"},
    "2": {"id": "2", "name": "bob", "role": "user"},
    "9": {"id": "9", "name": "root", "role": "admin", "secret": "LAB_CANARY_7Q"},
}


def handler(event, context):
    path = (event.get("rawPath") or event.get("path") or "/").rstrip("/") or "/"
    qs = _qs(event)

    # --- /echo : safe reflection baseline (always on) --------------------------
    if path.endswith("/echo"):
        return _resp(200, {"echo": qs})

    # --- /fetch : SSRF (gated) -------------------------------------------------
    # VULN: fetches an attacker-supplied URL with no allow-list. In Lambda this can
    # reach 169.254.169.254 and leak the function's role creds — which is exactly why
    # the role is least-privilege and the stack is disposable. Detection/mitigation:
    # egress allow-list, block link-local/metadata, never fetch unvalidated URLs.
    if path.endswith("/fetch"):
        if not _enabled("ENABLE_SSRF"):
            return _resp(403, {"error": "endpoint disabled", "flag": "ENABLE_SSRF"})
        url = qs.get("url")
        if not url:
            return _resp(400, {"error": "missing url"})
        try:
            with urllib.request.urlopen(url, timeout=3) as r:  # noqa: S310 (intentional)
                data = r.read(2048)
            return _resp(200, {"fetched": url, "body": data.decode("utf-8", "replace")})
        except Exception as e:  # noqa: BLE001
            return _resp(502, {"error": str(e), "fetched": url})

    # --- /render : template/format-string injection (gated) --------------------
    # VULN: user input used as a format string against internal objects, which can leak
    # attributes/config (SSTI class). Detection/mitigation: never use untrusted input as
    # a format/template string; render with a sandboxed engine and an explicit context.
    if path.endswith("/render"):
        if not _enabled("ENABLE_TEMPLATE"):
            return _resp(403, {"error": "endpoint disabled", "flag": "ENABLE_TEMPLATE"})
        tmpl = qs.get("tmpl", "")
        ctx = {"app": "vuln-api", "records": _RECORDS}
        try:
            rendered = tmpl.format(**ctx)  # intentional format-string injection surface
            return _resp(200, {"rendered": rendered})
        except Exception as e:  # noqa: BLE001
            return _resp(400, {"error": str(e)})

    # --- /lookup : injection-style input handling (gated) ----------------------
    # VULN: naive "query" that trusts input shape; malformed input leaks more than one
    # record (stand-in for SQL/NoSQL injection). Detection/mitigation: parameterized
    # queries, strict input validation, least-privilege data access.
    if path.endswith("/lookup"):
        if not _enabled("ENABLE_INJECTION"):
            return _resp(403, {"error": "endpoint disabled", "flag": "ENABLE_INJECTION"})
        rec_id = qs.get("id", "")
        # Broken "filter": an input like "*" or "' OR '1'='1" returns everything.
        if rec_id in ("*", "' OR '1'='1", '" OR "1"="1'):
            return _resp(200, {"records": list(_RECORDS.values())})
        rec = _RECORDS.get(rec_id)
        return _resp(200, {"record": rec} if rec else {"record": None})

    return _resp(404, {"error": "no such endpoint", "path": path})
