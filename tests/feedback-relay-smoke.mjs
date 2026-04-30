import assert from "node:assert/strict";
import worker from "../workers/feedback-relay.js";

let githubRequest;
globalThis.fetch = async (url, options) => {
  githubRequest = { url, options };
  return new Response(JSON.stringify({ html_url: "https://github.com/floomhq/fede/issues/99" }), {
    status: 201,
    headers: { "content-type": "application/json" },
  });
};

const env = {
  GITHUB_TOKEN: "test-token",
  FEEDBACK_SHARED_SECRET: "shared",
};

const blocked = await worker.fetch(new Request("https://relay.test", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ summary: "hello" }),
}), env);
assert.equal(blocked.status, 404);

const ok = await worker.fetch(new Request("https://relay.test", {
  method: "POST",
  headers: {
    "content-type": "application/json",
    "x-fede-feedback-secret": "shared",
  },
  body: JSON.stringify({
    summary: "token=abc123 user@example.com",
    actual: "bearer abcdefghijklmnop",
    expected: "redacted",
    context: "test",
    friction: "none",
    source: "test",
  }),
}), env);

assert.equal(ok.status, 200);
const json = await ok.json();
assert.equal(json.ok, true);
assert.equal(githubRequest.url, "https://api.github.com/repos/floomhq/fede/issues");
const issue = JSON.parse(githubRequest.options.body);
assert(!issue.title.includes("abc123"));
assert(!issue.body.includes("abcdefghijklmnop"));
assert(!issue.body.includes("user@example.com"));
