#!/usr/bin/env python3
"""Regression checks for ClawHub batch publish exit-code semantics."""

from __future__ import annotations

import tempfile
from pathlib import Path

from publish_clawhub_batch import (
    Artifact,
    NON_RETRYABLE_STATUSES,
    SharedQueue,
    StateStore,
    WorkerResult,
    batch_exit_code,
    conflict_fallback_suffix,
    extract_existing_owner,
    filter_pending,
    next_patch_version,
    owner_slot_for_error,
    should_preserve_state_version,
    suffix_publish_name,
)


def main() -> None:
    assert (
        batch_exit_code(
            [
                WorkerResult(slot="token-1", published=1),
                WorkerResult(slot="token-2", login_failed=True, notes=["whoami timed out"]),
            ],
            pending_after=0,
        )
        == 0
    )
    assert batch_exit_code([WorkerResult(slot="token-1", login_failed=True)], pending_after=1) == 1
    assert batch_exit_code([WorkerResult(slot="token-1", failed=1)], pending_after=0) == 1
    assert batch_exit_code([WorkerResult(slot="token-1", blocked=2)], pending_after=0) == 0
    assert conflict_fallback_suffix(1, "suffix-by-aisa") == "aisa"
    assert conflict_fallback_suffix(2, "suffix-by-aisa") == "aisa-api"
    assert conflict_fallback_suffix(3, "suffix-by-aisa") == "aisa-one"
    assert suffix_publish_name("stock-dividend-plugin", "aisa") == "stock-dividend-aisa-plugin"
    assert next_patch_version("1.0.9") == "1.0.10"
    assert should_preserve_state_version("1.0.10", "1.0.9")
    conflict = "Slug is already taken. Existing skill: /bibaofeng/aisa-twitter-api"
    assert extract_existing_owner(conflict) == "bibaofeng"
    assert owner_slot_for_error(conflict) == "token-2"
    queue = SharedQueue([], valid_slots={"token-1"})
    assert queue.slot_unavailable("token-2")
    assert not queue.slot_unavailable("token-1")
    with tempfile.TemporaryDirectory() as raw_tmp:
        state = StateStore(Path(raw_tmp) / "state.json")
        artifact = Artifact(
            key="skill:blocked",
            kind="skill",
            name="blocked",
            version="1.0.0",
            path="clawhub-release/blocked",
            display_name="Blocked",
        )
        state.upsert_artifact(artifact)
        state.mark(
            artifact,
            status=next(iter(NON_RETRYABLE_STATUSES)),
            version="1.0.0",
            last_error="external owner conflict",
        )
        assert filter_pending([artifact], state, force=False) == []
        newer = Artifact(
            key=artifact.key,
            kind=artifact.kind,
            name=artifact.name,
            version="1.0.1",
            path=artifact.path,
            display_name=artifact.display_name,
        )
        assert filter_pending([newer], state, force=False) == [newer]
    print("ClawHub batch publish exit-code checks passed.")


if __name__ == "__main__":
    main()
