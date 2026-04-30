#!/usr/bin/env python3
"""First-pass Fede repo scanner.

This script is intentionally conservative. It reports file paths, line numbers,
and categories, but never prints matched secret-like values.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from shutil import which


SKIP_DIRS = {
    ".git",
    ".next",
    ".turbo",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "node_modules",
    "vendor",
}

TEXT_SUFFIXES = {
    ".cjs",
    ".css",
    ".env",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".mjs",
    ".md",
    ".py",
    ".rb",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

LOCALHOST_RE = re.compile(r"(localhost|127\.0\.0\.1|::1|ngrok|localtunnel)", re.I)
SECRET_RE = re.compile(
    r"(password|secret|token|api[_-]?key|private[_-]?key|database_url|stripe|openai|anthropic|resend|sendgrid)",
    re.I,
)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def run(cmd: list[str], cwd: Path) -> dict[str, object]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=30)
    except Exception as exc:  # noqa: BLE001
        return {"cmd": cmd, "ok": False, "error": str(exc)}
    return {
        "cmd": cmd,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        base = Path(dirpath)
        for name in filenames:
            path = base / name
            if path.suffix.lower() in TEXT_SUFFIXES or name.startswith(".env"):
                out.append(path)
    return out


def scan_file(path: Path, root: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return findings
    for idx, line in enumerate(text.splitlines(), 1):
        categories = []
        if LOCALHOST_RE.search(line):
            categories.append("localhost")
        if SECRET_RE.search(line):
            categories.append("secret_keyword")
        for category in categories:
            findings.append({"file": rel(path, root), "line": idx, "category": category})
    return findings


def detect_metadata(root: Path) -> dict[str, object]:
    names = {p.name for p in root.iterdir()} if root.exists() else set()
    return {
        "package_json": "package.json" in names,
        "lockfiles": sorted(n for n in names if n in {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"}),
        "python": sorted(n for n in names if n in {"pyproject.toml", "requirements.txt", "uv.lock", "Pipfile"}),
        "dockerfile": "Dockerfile" in names,
        "platform_config": sorted(
            n
            for n in names
            if n in {"vercel.json", "netlify.toml", "render.yaml", "railway.json", "fly.toml", "Procfile"}
        ),
        "env_schema": sorted(n for n in names if n in {".env.example", ".env.template", "env.sample", ".env.sample"}),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--run-scanners", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo).expanduser().resolve()
    if not root.exists():
        print(f"repo not found: {root}", file=sys.stderr)
        return 2

    findings: list[dict[str, object]] = []
    for path in iter_files(root):
        findings.extend(scan_file(path, root))

    scanner_tools = {name: bool(which(name)) for name in ["gitleaks", "trufflehog"]}
    scanner_results = {}
    dedicated_ran = False
    dedicated_passed = False
    if args.run_scanners:
        if scanner_tools["gitleaks"]:
            dedicated_ran = True
            result = run(["gitleaks", "dir", "--no-banner", "--redact", "."], root)
            scanner_results["gitleaks"] = result
            dedicated_passed = dedicated_passed or bool(result.get("ok"))
        if scanner_tools["trufflehog"]:
            dedicated_ran = True
            result = run(["trufflehog", "filesystem", "--no-update", "."], root)
            scanner_results["trufflehog"] = result
            dedicated_passed = dedicated_passed or bool(result.get("ok"))
    if dedicated_passed:
        secret_scan_status = "dedicated_passed"
    elif dedicated_ran:
        secret_scan_status = "dedicated_failed"
    else:
        secret_scan_status = "keyword_only_incomplete"
    result = {
        "repo": str(root),
        "metadata": detect_metadata(root),
        "git_status": run(["git", "status", "--short", "--branch"], root),
        "scanner_tools": scanner_tools,
        "scanner_results": scanner_results,
        "secret_scan_status": secret_scan_status,
        "findings": findings[:500],
        "finding_count": len(findings),
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"repo: {result['repo']}")
        print(f"secret_scan_status: {result['secret_scan_status']}")
        print(f"finding_count: {result['finding_count']}")
        print("metadata:")
        for key, value in result["metadata"].items():
            print(f"  {key}: {value}")
        print("scanner_tools:")
        for key, value in scanner_tools.items():
            print(f"  {key}: {value}")
        if scanner_results:
            print("scanner_results:")
            for key, value in scanner_results.items():
                print(f"  {key}: ok={value.get('ok')} returncode={value.get('returncode')}")
        print("findings:")
        for item in findings[:50]:
            print(f"  {item['category']}: {item['file']}:{item['line']}")
        if len(findings) > 50:
            print(f"  ... {len(findings) - 50} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
