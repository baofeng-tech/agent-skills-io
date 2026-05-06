#!/usr/bin/env python3
"""Regression checks for ClawHub batch publish exit-code semantics."""

from __future__ import annotations

from publish_clawhub_batch import WorkerResult, batch_exit_code


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
    print("ClawHub batch publish exit-code checks passed.")


if __name__ == "__main__":
    main()
