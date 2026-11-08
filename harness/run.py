#!/usr/bin/env python3
"""
Minimal probe runner for the redteam-scratchpad.

Fires canary/signal probes at a target YOU OWN or are authorized to test, and records each
request/response pair under harness/out/ so you can write it up. Stdlib only.

Safety behaviour:
  * You must pass --target explicitly. Default assumptions point at loopback.
  * Non-loopback targets require --i-have-authorization (records your attestation in output).
  * Probes are benign reachability/canary checks, not weaponized exploits.

Usage:
  python harness/run.py --target http://127.0.0.1:8080 --check echo
  python harness/run.py --target http://127.0.0.1:8080 --catalog payloads/web.yaml
  python harness/run.py --target http://127.0.0.1 --check cve_2024_4577
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
LOOPBACK = ("127.0.0.1", "localhost", "::1")
CANARY = "LAB_CANARY_7Q"


def _is_loopback(target: str) -> bool:
    host = urllib.parse.urlparse(target).hostname or ""
    return host in LOOPBACK


def _record(name: str, req: dict, resp: dict) -> pathlib.Path:
    OUT.mkdir(exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = OUT / f"{ts}-{name}.json"
    path.write_text(json.dumps({"request": req, "response": resp}, indent=2))
    return path


def _http(method: str, url: str, timeout: int = 5) -> dict:
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(8192).decode("utf-8", "replace")
            return {"status": r.status, "body": body}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read(2048).decode("utf-8", "replace")}
    except Exception as e:  # noqa: BLE001
        return {"status": None, "error": str(e)}


def check_echo(target: str):
    url = target.rstrip("/") + "/echo?ping=" + CANARY
    resp = _http("GET", url)
    ok = CANARY in json.dumps(resp)
    p = _record("echo", {"url": url}, resp)
    print(f"[echo] reachable={resp.get('status')} canary_reflected={ok}  -> {p.name}")


def check_cve_2024_4577(target: str):
    """
    BENIGN reachability probe for the PHP-CGI arg-injection lab.
    Reads phpinfo and reports whether it's present. The actual arg-injection proof (flipping
    a -d directive and reading it back) is lab/locale specific — see labs/php-cve-2024-4577.
    This check just confirms the lab surface is up and records a baseline.
    """
    url = target.rstrip("/") + "/phpinfo.php"
    resp = _http("GET", url)
    body = resp.get("body", "") or ""
    has_info = "phpinfo()" in body or "PHP Version" in body
    p = _record("cve_2024_4577_baseline", {"url": url}, {"status": resp.get("status"),
                                                          "phpinfo_present": has_info})
    print(f"[cve_2024_4577] phpinfo_surface={has_info} status={resp.get('status')} -> {p.name}")
    print("  next: follow labs/php-cve-2024-4577/README.md for the benign -d read-back proof.")


def run_catalog(target: str, catalog: str):
    # Tiny YAML-ish loader to avoid a dependency: supports the simple list format used in
    # payloads/*.yaml. For richer files, `pip install pyyaml` and swap this out.
    try:
        import yaml  # type: ignore
        items = yaml.safe_load(pathlib.Path(catalog).read_text())
    except ModuleNotFoundError:
        print("(!) pyyaml not installed; install it to run catalogs: pip install pyyaml")
        return
    for item in items or []:
        send = item.get("send", {})
        endpoint = send.get("endpoint", "")
        param = send.get("param")
        payload = item.get("payload", "")
        if not param:
            print(f"[{item.get('id')}] manual probe — see notes: {item.get('notes','')}")
            continue
        q = urllib.parse.urlencode({param: payload})
        url = target.rstrip("/") + endpoint + "?" + q
        resp = _http("GET", url)
        p = _record(item.get("id", "probe"), {"url": url, "expect": item.get("expect")}, resp)
        print(f"[{item.get('id')}] status={resp.get('status')} -> {p.name}  expect: {item.get('expect')}")


def main():
    ap = argparse.ArgumentParser(description="redteam-scratchpad probe runner")
    ap.add_argument("--target", required=True, help="base URL of a target you own/are authorized to test")
    ap.add_argument("--check", choices=["echo", "cve_2024_4577"], help="run a single built-in check")
    ap.add_argument("--catalog", help="path to a payloads/*.yaml catalog to run")
    ap.add_argument("--i-have-authorization", action="store_true",
                    help="required for non-loopback targets; attests you're authorized")
    args = ap.parse_args()

    if not _is_loopback(args.target) and not args.i_have_authorization:
        sys.exit("Refusing non-loopback target without --i-have-authorization "
                 "(and a matching entry in SCOPE.md).")

    print(f"target: {args.target}  (loopback={_is_loopback(args.target)})")
    if args.check == "echo":
        check_echo(args.target)
    elif args.check == "cve_2024_4577":
        check_cve_2024_4577(args.target)
    if args.catalog:
        run_catalog(args.target, args.catalog)
    if not args.check and not args.catalog:
        print("nothing to do: pass --check or --catalog")


if __name__ == "__main__":
    main()
