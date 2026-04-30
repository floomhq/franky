export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("not found", { status: 404 });
    }

    const contentType = request.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      return new Response("json required", { status: 415 });
    }

    if (env.FEEDBACK_SHARED_SECRET) {
      const provided = request.headers.get("x-fede-feedback-secret") || "";
      if (provided !== env.FEEDBACK_SHARED_SECRET) {
        return new Response("not found", { status: 404 });
      }
    }

    const raw = await request.text();
    if (raw.length > 12000) {
      return new Response("payload too large", { status: 413 });
    }

    let event;
    try {
      event = JSON.parse(raw);
    } catch {
      return new Response("invalid json", { status: 400 });
    }

    const summary = truncate(redact(event.summary || "unknown friction"), 120);
    const body = [
      "## Summary",
      "",
      text(event.summary),
      "",
      "## What Happened",
      "",
      text(event.actual),
      "",
      "## Expected",
      "",
      text(event.expected),
      "",
      "## Context",
      "",
      text(event.context),
      "",
      "## User Friction",
      "",
      text(event.friction),
      "",
      "## Source",
      "",
      text(event.source || "fede-coach"),
      "",
      "## Privacy",
      "",
      "Client sent sanitized feedback. Do not include secrets or private customer data.",
    ].join("\n");

    const response = await fetch("https://api.github.com/repos/floomhq/fede/issues", {
      method: "POST",
      headers: {
        "authorization": `Bearer ${env.GITHUB_TOKEN}`,
        "accept": "application/vnd.github+json",
        "content-type": "application/json",
        "user-agent": "fede-feedback-relay",
      },
      body: JSON.stringify({
        title: `Feedback: ${summary}`,
        body,
      }),
    });

    const json = await response.json().catch(() => ({}));
    if (!response.ok) {
      return new Response(JSON.stringify({ ok: false }), {
        status: 502,
        headers: { "content-type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ ok: true, url: json.html_url }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  },
};

function text(value) {
  return truncate(redact(String(value || "not provided")), 1000);
}

function truncate(value, max) {
  return value.length > max ? value.slice(0, max) : value;
}

function redact(value) {
  return String(value)
    .replace(/(api[_-]?key|token|secret|password)\s*[:=]\s*['"]?[^\s,'"]+/gi, "[redacted]")
    .replace(/bearer\s+[a-z0-9._-]{12,}/gi, "[redacted]")
    .replace(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g, "[redacted]");
}
