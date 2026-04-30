import importlib.util
import os
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fede_feedback", ROOT / "scripts" / "fede_feedback.py")
fede_feedback = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["fede_feedback"] = fede_feedback
SPEC.loader.exec_module(fede_feedback)


def args(**overrides):
    defaults = {
        "summary": "token=abc123 and user@example.com",
        "actual": "bearer abcdefghijklmnop",
        "expected": "redacted output",
        "context": "verification",
        "friction": "none",
        "source": "test",
    }
    defaults.update(overrides)
    return Namespace(**defaults)


def test_clean_redacts_secret_like_values():
    assert fede_feedback.clean("token=abc123 user@example.com") == "[redacted] [redacted]"


def test_payload_is_redacted():
    payload = fede_feedback.payload(args())
    assert "abc123" not in payload["summary"]
    assert "user@example.com" not in payload["summary"]
    assert "abcdefghijklmnop" not in payload["actual"]


def test_write_local_jsonl(tmp_path):
    path = tmp_path / "feedback.jsonl"
    event = fede_feedback.payload(args(summary="hello"))
    fede_feedback.write_local(event, path)
    assert path.read_text(encoding="utf-8").count("\n") == 1
    assert "hello" in path.read_text(encoding="utf-8")


def test_relay_secret_header(monkeypatch):
    captured = {}

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b"ok"

    def fake_urlopen(request, timeout):
        captured["secret"] = request.headers.get("X-fede-feedback-secret")
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setenv("FEDE_FEEDBACK_SECRET", "shared")
    monkeypatch.setattr(fede_feedback.urllib.request, "urlopen", fake_urlopen)

    assert fede_feedback.post_relay("https://example.com", {"summary": "hi"}) == "ok"
    assert captured["secret"] == "shared"
    assert captured["timeout"] == 8
