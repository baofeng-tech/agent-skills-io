#!/usr/bin/env python3
"""Regression checks for ClawHub batch publish exit-code semantics."""

from __future__ import annotations

from publish_clawhub_batch import (
    SharedQueue,
    WorkerResult,
    batch_exit_code,
    conflict_fallback_suffix,
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
    assert conflict_fallback_suffix(1, "suffix-by-aisa") == "aisa"
    assert conflict_fallback_suffix(2, "suffix-by-aisa") == "aisa-api"
    assert conflict_fallback_suffix(3, "suffix-by-aisa") == "aisa-one"
    assert suffix_publish_name("stock-dividend-plugin", "aisa") == "stock-dividend-aisa-plugin"
    queue = SharedQueue([], valid_slots={"token-1"})
    assert queue.slot_unavailable("token-2")
    assert not queue.slot_unavailable("token-1")
    print("ClawHub batch publish exit-code checks passed.")


if __name__ == "__main__":
    main()
