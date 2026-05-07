#!/usr/bin/env python3
"""Regression checks for ClawHub Review verdict handling."""

from __future__ import annotations

from clawhub_live_status import (
    extract_page_scan_badge_status,
    extract_status_after_label,
    normalize_status,
)
from clawhub_suspicious_diagnosis import classify_rules


def main() -> None:
    assert normalize_status("Review") == "review"
    assert extract_page_scan_badge_status('<span class="scan-status-review">Review</span>') == "review"
    assert extract_status_after_label(["ClawScan", "Review"], "ClawScan") == "review"
    assert extract_status_after_label(["Scan Metadata", "Verdict", "Review"], "Verdict") == "review"

    item = {
        "scan_status": "review",
        "clawscan_verdict": "review",
        "suspicious": True,
        "pending": False,
    }
    assert "review_scan" in classify_rules(item)
    print("ClawHub Review verdict checks passed.")


if __name__ == "__main__":
    main()
