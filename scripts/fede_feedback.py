#!/usr/bin/env python3
"""Create, relay, or store a Fede feedback event.

Remote relay:
  FEDE_AUTO_FEEDBACK_URL=https://... python3 scripts/fede_feedback.py ...

Fallbacks:
  - GitHub CLI auth creates an issue.
  - No remote/auth writes .fede-feedback.jsonl locally.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import time
import urllib.parse
import urllib.request


REPO = "floomhq/fede"
MAX_FIELD_CHARS = 1000


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def gh_ready() -> bool:
    if not shutil.which("gh"):
        return False
    result = run(["gh", "auth", "status"])
    return result.returncode == 0


def clean(value: str) -> str:
    trimmed = value.strip()[:MAX_FIELD_CHARS]
    return trimmed or "not provided"


def payload(args: argparse.Namespace) -> dict[str, object]:
    return {
        "summary": clean(args.summary),
        "actual": clean(args.actual),
        "expected": clean(args.expected),
        "context": clean(args.context),
        "friction": clean(args.friction),
        "source": clean(args.source),
        "created_at": int(time.time()),
        "privacy": "sanitized_no_secrets_no_private_customer_data",
    }


def body(args: argparse.Namespace) -> str:
    event = payload(args)
    return textwrap.dedent(
        f"""\
        ## Summary

        {event["summary"]}

        ## What Happened

        {event["actual"]}

        ## Expected

        {event["expected"]}

        ## Context

        {event["context"]}

        ## User Friction

        {event["friction"]}

        ## Source

        {event["source"]}

        ## Privacy Check

        The reporter confirmed this issue contains no secrets, credentials,
        private customer data, or confidential names.
        """
    )


def issue_url(title: str, issue_body: str) -> str:
    query = urllib.parse.urlencode({"title": title, "body": issue_body})
    return f"https://github.com/{REPO}/issues/new?{query}"


def post_relay(url: str, event: dict[str, object]) -> str | None:
    data = json.dumps(event, sort_keys=True).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"content-type": "application/json", "user-agent": "fede-feedback/1"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            body_text = response.read().decode("utf-8", errors="replace").strip()
            if 200 <= response.status < 300:
                return body_text or f"feedback relayed: HTTP {response.status}"
            return None
    except Exception:
        return None


def write_local(event: dict[str, object], path: Path) -> Path:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or prepare a Fede feedback issue.")
    parser.add_argument("--summary", required=True, help="Short feedback summary")
    parser.add_argument("--actual", default="", help="What happened")
    parser.add_argument("--expected", default="", help="Expected behavior")
    parser.add_argument("--context", default="", help="User context")
    parser.add_argument("--friction", default="", help="User frustration or blocker")
    parser.add_argument("--source", default="fede-coach", help="Feedback source")
    parser.add_argument("--dry-run", action="store_true", help="Print packet only")
    parser.add_argument("--local-file", default=".fede-feedback.jsonl", help="Local fallback path")
    args = parser.parse_args()

    title = f"Feedback: {clean(args.summary)[:90]}"
    issue_body = body(args)
    event = payload(args)

    if args.dry_run:
        print(title)
        print()
        print(issue_body)
        print(issue_url(title, issue_body))
        return 0

    relay_url = os.environ.get("FEDE_AUTO_FEEDBACK_URL", "").strip()
    if relay_url:
        result = post_relay(relay_url, event)
        if result:
            print(result)
            return 0

    if gh_ready():
        result = run(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", issue_body])
        if result.returncode == 0:
            print(result.stdout.strip())
            return 0
        print(result.stderr.strip(), file=sys.stderr)

    path = write_local(event, Path(args.local_file))
    print(f"feedback stored locally: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
