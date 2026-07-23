#!/usr/bin/env python3
"""Small UTF-8-safe client for the local Kimi WebBridge daemon."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ENDPOINT = "http://127.0.0.1:10086/command"


def start_daemon() -> None:
    if os.name == "nt":
        executable = Path.home() / ".kimi-webbridge" / "bin" / "kimi-webbridge.exe"
    else:
        executable = Path.home() / ".kimi-webbridge" / "bin" / "kimi-webbridge"
    if not executable.exists():
        raise FileNotFoundError(f"Kimi WebBridge executable not found: {executable}")
    subprocess.run(
        [str(executable), "start"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def request(payload: dict[str, Any], timeout: float) -> Any:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, help="Stable task session name")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--no-auto-start", action="store_true")
    parser.add_argument(
        "action",
        choices=[
            "navigate",
            "find_tab",
            "snapshot",
            "click",
            "fill",
            "evaluate",
            "screenshot",
            "network",
            "upload",
            "save_as_pdf",
            "list_tabs",
            "close_tab",
            "close_session",
        ],
    )
    parser.add_argument("--args-json", default="{}", help="JSON object passed as args")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        action_args = json.loads(args.args_json)
    except json.JSONDecodeError as exc:
        print(f"Invalid --args-json: {exc}", file=sys.stderr)
        return 2
    if not isinstance(action_args, dict):
        print("--args-json must decode to an object", file=sys.stderr)
        return 2

    payload = {"action": args.action, "args": action_args, "session": args.session}
    try:
        result = request(payload, args.timeout)
    except (urllib.error.URLError, ConnectionError, TimeoutError) as first_error:
        if args.no_auto_start:
            print(f"WebBridge request failed: {first_error}", file=sys.stderr)
            return 1
        try:
            start_daemon()
            result = request(payload, args.timeout)
        except Exception as retry_error:
            print(
                "Kimi WebBridge is unavailable after one start attempt. "
                f"Initial error: {first_error}; retry error: {retry_error}",
                file=sys.stderr,
            )
            return 1

    json.dump(result, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
