#!/usr/bin/env python3
"""Regression checks for the public-write Twitter OAuth client."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENT_PATH = REPO_ROOT / "targetSkills" / "openclaw-twitter-post-engage" / "scripts" / "twitter_oauth_client.py"
TEST_SECRET = "test_secret_must_not_be_printed"


def load_client() -> Any:
    spec = importlib.util.spec_from_file_location("openclaw_twitter_oauth_client_under_test", CLIENT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load {CLIENT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_secret_not_present(payload: Any) -> None:
    rendered = json.dumps(payload, ensure_ascii=False)
    if TEST_SECRET in rendered:
        raise AssertionError("AISA_API_KEY value leaked into public command output")


def test_publish_chunks_hides_secret_and_threads_replies(client: Any) -> None:
    counter = {"value": 0}
    calls: list[dict[str, Any]] = []

    def fake_post_single_tweet(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        counter["value"] += 1
        calls.append(kwargs)
        return {"ok": True, "code": 200, "data": {"tweet_id": f"tweet-{counter['value']}"}}

    client.post_single_tweet = fake_post_single_tweet
    config = {"base_url": "https://api.aisa.one/apis/v1/twitter", "aisa_api_key": TEST_SECRET, "timeout": 1}
    result = client.publish_chunks(config, ["first", "second"], post_type="reply")

    assert_secret_not_present(result)
    if result["results"][0]["relationship"] != "standalone":
        raise AssertionError("first chunk of a normal thread should be standalone")
    if result["results"][1]["relationship"] != "reply":
        raise AssertionError("second chunk should continue as a reply")
    if calls[1]["parent_tweet_id"] != "tweet-1":
        raise AssertionError("reply continuation should target the previous published tweet")


def test_quote_post_requires_explicit_url_and_replies_after_first_chunk(client: Any) -> None:
    counter = {"value": 0}
    calls: list[dict[str, Any]] = []

    def fake_post_single_tweet(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        counter["value"] += 1
        calls.append(kwargs)
        return {"ok": True, "code": 200, "data": {"tweet_id": f"quote-{counter['value']}"}}

    client.post_single_tweet = fake_post_single_tweet
    config = {"base_url": "https://api.aisa.one/apis/v1/twitter", "aisa_api_key": TEST_SECRET, "timeout": 1}
    result = client.publish_chunks(
        config,
        ["quote", "continuation"],
        initial_parent_tweet_id="1888888888888888888",
        post_type="quote",
    )

    assert_secret_not_present(result)
    if calls[0]["post_type"] != "quote" or calls[0]["parent_tweet_id"] != "1888888888888888888":
        raise AssertionError("quote mode should quote only the explicit external target on the first chunk")
    if calls[1]["post_type"] != "reply" or calls[1]["parent_tweet_id"] != "quote-1":
        raise AssertionError("quote continuations should reply to the first published chunk")

    args = client.build_parser().parse_args(["post", "--text", "missing target", "--type", "quote", "--confirm-public-write"])
    os.environ["AISA_API_KEY"] = TEST_SECRET
    try:
        args.func(args)
    except client.RelayConfigError:
        pass
    else:
        raise AssertionError("--type quote must require --quote-tweet-url")


def test_authorize_output_hides_secret(client: Any) -> None:
    def fake_send_json_request(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return {"code": 200, "data": {"auth_url": "https://example.test/oauth"}}

    client.send_json_request = fake_send_json_request
    os.environ["AISA_API_KEY"] = TEST_SECRET
    args = client.build_parser().parse_args(["authorize"])
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        args.func(args)
    output = json.loads(stream.getvalue())
    assert_secret_not_present(output)
    if output.get("aisa_api_key_present") is not True:
        raise AssertionError("authorize output should report key presence without exposing the value")


def main() -> int:
    client = load_client()
    test_publish_chunks_hides_secret_and_threads_replies(client)
    test_quote_post_requires_explicit_url_and_replies_after_first_chunk(client)
    test_authorize_output_hides_secret(client)
    print("Twitter OAuth client safety checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"twitter oauth safety check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
