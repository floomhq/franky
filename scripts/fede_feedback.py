#!/usr/bin/env python3
"""Create or prepare a Fede feedback issue.

The script never requires GitHub auth. With `gh` auth it creates an issue. Without
auth it prints a prefilled GitHub issue URL and a copy-paste packet.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import textwrap
import urllib.parse


REPO = "floomhq/fede"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def gh_ready() -> bool:
    if not shutil.which("gh"):
        return False
    result = run(["gh", "auth", "status"])
    return result.returncode == 0


def clean(value: str) -> str:
    return value.strip() or "not provided"


def body(args: argparse.Namespace) -> str:
    return textwrap.dedent(
        f"""\
        ## Summary

        {clean(args.summary)}

        ## What Happened

        {clean(args.actual)}

        ## Expected

        {clean(args.expected)}

        ## Context

        {clean(args.context)}

        ## User Friction

        {clean(args.friction)}

        ## Source

        {clean(args.source)}

        ## Privacy Check

        The reporter confirmed this issue contains no secrets, credentials,
        private customer data, or confidential names.
        """
    )


def issue_url(title: str, issue_body: str) -> str:
    query = urllib.parse.urlencode({"title": title, "body": issue_body})
    return f"https://github.com/{REPO}/issues/new?{query}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or prepare a Fede feedback issue.")
    parser.add_argument("--summary", required=True, help="Short feedback summary")
    parser.add_argument("--actual", default="", help="What happened")
    parser.add_argument("--expected", default="", help="Expected behavior")
    parser.add_argument("--context", default="", help="User context")
    parser.add_argument("--friction", default="", help="User frustration or blocker")
    parser.add_argument("--source", default="fede-coach", help="Feedback source")
    parser.add_argument("--dry-run", action="store_true", help="Print packet only")
    args = parser.parse_args()

    title = f"Feedback: {clean(args.summary)[:90]}"
    issue_body = body(args)

    if args.dry_run:
        print(title)
        print()
        print(issue_body)
        print(issue_url(title, issue_body))
        return 0

    if gh_ready():
        result = run(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", issue_body])
        if result.returncode == 0:
            print(result.stdout.strip())
            return 0
        print(result.stderr.strip(), file=sys.stderr)

    print("GitHub issue was not created locally.")
    print("Open this URL or copy the packet below:")
    print()
    print(issue_url(title, issue_body))
    print()
    print(title)
    print()
    print(issue_body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
