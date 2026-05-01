#!/usr/bin/env python3
"""Resolve ClawHub detail pages and extract live security scan status."""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACCOUNTS_FILE = REPO_ROOT / "example" / "accounts"
DEFAULT_STATE_FILE = REPO_ROOT / "targets" / "clawhub-publish-state.json"
DEFAULT_OUTPUT_FILE = REPO_ROOT / "targets" / "clawhub-live-status.json"
DEFAULT_CONFIG_ROOT = REPO_ROOT / ".tmp-clawhub-auth"
USER_AGENT = "Mozilla/5.0 (compatible; agent-skills-io/1.0; ClawHub live status scanner)"
STATUS_WORDS = {"benign", "clean", "pending", "suspicious", "malicious", "warning", "safe", "unknown"}
TOKEN_KEY_PATTERN = re.compile(r"^clawhubapitoken(?P<index>\d*)$")
DEFAULT_SKILL_OWNER_CANDIDATES = ("baofeng-tech", "bibaofeng", "aisadocs", "aisapay")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", raw.lower())


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_owner_candidates(values: list[str] | tuple[str, ...] | None) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for raw in values or []:
        for piece in re.split(r"[,\s]+", str(raw or "").strip()):
            owner = clean_text(piece).lstrip("@")
            if not owner or owner in seen:
                continue
            seen.add(owner)
            candidates.append(owner)
    return candidates


def parse_accounts_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        separator = "=" if "=" in line else ":" if ":" in line else None
        if not separator:
            continue
        key, value = line.split(separator, 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            values[normalize_key(key)] = value
    return values


def token_sort_key(key: str) -> tuple[int, str]:
    match = TOKEN_KEY_PATTERN.match(key)
    if not match:
        return (sys.maxsize, key)
    raw_index = match.group("index")
    return (int(raw_index) if raw_index else 1, key)


def extract_account_tokens(account_values: dict[str, str]) -> list[str]:
    return [
        account_values[key]
        for key in sorted(account_values, key=token_sort_key)
        if TOKEN_KEY_PATTERN.match(key)
    ]


def resolve_tokens(
    accounts_file: Path | None,
    explicit_tokens: list[str] | None = None,
) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()

    def add(token: str | None) -> None:
        if not token:
            return
        token = token.strip()
        if not token or token in seen:
            return
        seen.add(token)
        tokens.append(token)

    for token in explicit_tokens or []:
        add(token)

    env_tokens: list[tuple[int, str]] = []
    for env_name, value in os.environ.items():
        if not value:
            continue
        if env_name == "CLAWHUB_TOKEN":
            env_tokens.append((1, value))
            continue
        match = re.fullmatch(r"CLAWHUB_TOKEN_(\d+)", env_name)
        if match:
            env_tokens.append((int(match.group(1)), value))
    for _index, value in sorted(env_tokens, key=lambda item: item[0]):
        add(value)

    if accounts_file:
        for token in extract_account_tokens(parse_accounts_file(accounts_file)):
            add(token)
    return tokens


def run_command(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path = REPO_ROOT,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    if args and args[0] == "clawhub":
        clawhub_bin = (
            os.environ.get("CLAWHUB_BIN", "").strip()
            or shutil.which("clawhub")
            or shutil.which("clawhub.cmd")
            or shutil.which("clawhub.exe")
        )
        if clawhub_bin:
            if os.name == "nt" and clawhub_bin.lower().endswith((".cmd", ".bat")):
                args = ["cmd.exe", "/c", clawhub_bin, *args[1:]]
            else:
                args = [clawhub_bin, *args[1:]]
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=merged_env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def try_parse_json(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def normalize_status(value: str | None) -> str | None:
    if not value:
        return None
    lowered = clean_text(value).lower()
    if lowered not in STATUS_WORDS:
        return None
    if lowered == "safe":
        return "benign"
    return lowered


def extract_clawhub_slug_from_url(url: str | None, kind: str) -> str | None:
    if not url:
        return None
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return None
    segments = [clean_text(piece) for piece in parsed.path.split("/") if clean_text(piece)]
    if not segments:
        return None
    if kind == "plugin":
        if segments and segments[0] == "plugins" and len(segments) >= 2:
            return segments[1]
        return None
    if segments[0] == "plugins":
        return None
    if len(segments) >= 2:
        return segments[1]
    return None


def detail_url_matches_artifact(url: str | None, kind: str, expected_name: str) -> bool:
    slug = extract_clawhub_slug_from_url(url, kind)
    return bool(slug and slug == expected_name)


def extract_canonical_url(page_html: str) -> str | None:
    patterns = [
        r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"',
        r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            return html.unescape(match.group(1))
    return None


def extract_text_lines(page_html: str) -> list[str]:
    stripped = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", "\n", page_html)
    stripped = re.sub(r"(?is)<[^>]+>", "\n", stripped)
    stripped = html.unescape(stripped)
    return [clean_text(line) for line in stripped.splitlines() if clean_text(line)]


def strip_html_fragment(fragment: str) -> str:
    stripped = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", fragment)
    stripped = re.sub(r"(?is)<[^>]+>", " ", stripped)
    return clean_text(html.unescape(stripped))


def extract_definition_value_from_html(page_html: str, labels: tuple[str, ...]) -> str | None:
    for label in labels:
        pattern = rf"<dt[^>]*>\s*{re.escape(label)}\s*</dt>\s*<dd[^>]*>(.*?)</dd>"
        match = re.search(pattern, page_html, re.IGNORECASE | re.DOTALL)
        if match:
            value = strip_html_fragment(match.group(1))
            if value:
                return value
    return None


def extract_page_scan_badge_status(page_html: str) -> str | None:
    match = re.search(
        r"scan-status-(benign|clean|pending|suspicious|malicious|warning|safe|unknown)",
        page_html,
        re.IGNORECASE,
    )
    if match:
        return normalize_status(match.group(1))
    return None


def extract_structured_scan_field(page_html: str, object_names: tuple[str, ...], field: str) -> str | None:
    for object_name in object_names:
        pattern = (
            rf"{re.escape(object_name)}\s*:\s*\$R\[\d+\]\s*=\s*{{[\s\S]{{0,8000}}?"
            rf"{re.escape(field)}\s*:\s*\"((?:[^\"\\]|\\.)*)\""
        )
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            value = clean_text(decode_js_string(match.group(1)))
            if value:
                return value
    return None


def extract_block(lines: list[str], headings: list[str]) -> str:
    stops = {
        "verification",
        "tags",
        "browse",
        "publish",
        "platform",
        "community",
        "compatibility",
        "capabilities",
        "what it ships",
        "why this format",
        "notes",
    }
    lowered = [line.lower() for line in lines]
    for heading in headings:
        heading_lower = heading.lower()
        if heading_lower not in lowered:
            continue
        start = lowered.index(heading_lower) + 1
        collected: list[str] = []
        for line in lines[start:]:
            line_lower = line.lower()
            if line_lower in stops:
                break
            if re.fullmatch(r"[✓✗ℹ⚠]", line):
                continue
            collected.append(line)
            if len(collected) >= 8:
                break
        if collected:
            return clean_text(" ".join(collected))
    return ""


def extract_status_after_label(lines: list[str], label: str) -> str | None:
    text = "\n".join(lines)
    patterns = [
        rf"{re.escape(label)}(?:\s+{re.escape(label)})?\s+(Benign|Clean|Pending|Suspicious|Malicious|Warning|Safe|Unknown)",
        rf"{re.escape(label)}\s*\n\s*(Benign|Clean|Pending|Suspicious|Malicious|Warning|Safe|Unknown)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return normalize_status(match.group(1))
    return None


def extract_scan_status(lines: list[str]) -> str | None:
    text = "\n".join(lines)
    match = re.search(r"Scan status\s+(clean|pending|suspicious|malicious|warning|unknown)", text, re.IGNORECASE)
    if match:
        return normalize_status(match.group(1))
    if re.search(r"flagged\s+[—-]\s+suspicious patterns detected", text, re.IGNORECASE):
        return "suspicious"
    return None


def extract_clawscan_confidence(lines: list[str]) -> str | None:
    text = "\n".join(lines)
    match = re.search(r"\b(low|medium|high)\s+confidence\b", text, re.IGNORECASE)
    return clean_text(match.group(0)).lower() if match else None


def extract_static_analysis_status(lines: list[str]) -> str | None:
    direct = extract_status_after_label(lines, "Static analysis")
    if direct:
        return direct

    text = "\n".join(lines)
    match = re.search(r"Static analysis:\s*(\d+)\s+pattern(?:s)?\s+detected", text, re.IGNORECASE)
    if match:
        return "benign" if int(match.group(1)) == 0 else "suspicious"
    if re.search(r"Static analysis:\s*no\s+patterns\s+detected", text, re.IGNORECASE):
        return "benign"
    return None


def extract_prefixed_section(lines: list[str], prefixes: tuple[str, ...], *, max_lines: int = 5) -> str:
    stops = {
        "verification",
        "tags",
        "browse",
        "publish",
        "platform",
        "community",
        "compatibility",
        "capabilities",
        "what it ships",
        "why this format",
        "notes",
        "filescompareversions",
        "files",
        "compare",
        "versions",
    }
    normalized_prefixes = tuple(prefix.lower() for prefix in prefixes)
    for index, line in enumerate(lines):
        lowered = line.lower()
        if not any(lowered.startswith(prefix) for prefix in normalized_prefixes):
            continue
        collected = [line]
        for extra in lines[index + 1 :]:
            extra_lower = extra.lower()
            if extra_lower in stops or extra.startswith("## "):
                break
            if re.fullmatch(r"[✓✗ℹ⚠!]", extra):
                continue
            collected.append(extra)
            if len(collected) >= max_lines:
                break
        return clean_text(" ".join(collected))
    return ""


def extract_static_analysis_summary(lines: list[str]) -> str | None:
    summary = extract_prefixed_section(lines, ("Static analysis:",), max_lines=5)
    return summary or None


def extract_heading_value(lines: list[str], headings: tuple[str, ...], *, min_length: int = 12) -> str | None:
    stops = {
        "guidance",
        "findings (",
        "findings",
        "reason codes",
        "engine",
        "artifact",
        "hash",
        "browse",
        "publish",
        "platform",
        "community",
        "scan metadata",
    }
    lowered = [line.lower() for line in lines]
    for heading in headings:
        heading_lower = heading.lower()
        if heading_lower not in lowered:
            continue
        start = lowered.index(heading_lower) + 1
        for line in lines[start : start + 5]:
            line_lower = line.lower()
            if any(line_lower.startswith(stop) for stop in stops):
                break
            if len(line) >= min_length:
                return line
    return None


def extract_security_detail_summary(lines: list[str]) -> str | None:
    skip_exact = {
        "clawscan",
        "openclaw",
        "static analysis",
        "virustotal",
        "suspicious",
        "pending",
        "benign",
        "clean",
        "warning",
        "malicious",
        "unknown",
        "safe",
        "stale",
        "assessment",
        "what to consider before installing",
    }
    skip_prefixes = (
        "clawhub's context-aware review",
        "deterministic local checks",
        "this page records",
        "clawscan verdict",
        "scanner verdict",
        "review compatibility and verification",
    )

    heading_summary = extract_heading_value(lines, ("Summary", "Analysis"), min_length=10)
    if heading_summary:
        return heading_summary

    verdict_seen = False
    for line in lines:
        lowered = line.lower()
        if lowered.startswith("detected:"):
            return line
        if lowered in skip_exact:
            verdict_seen = verdict_seen or lowered in {"suspicious", "pending", "benign", "clean", "warning", "malicious"}
            continue
        if lowered.startswith(skip_prefixes):
            continue
        if not verdict_seen:
            continue
        if len(line) >= 40:
            return line

    for heading in ("What to consider before installing", "Assessment"):
        block = extract_block(lines, [heading])
        if block:
            return block
    return None


def decode_js_string(value: str) -> str:
    return (
        value.replace(r"\"", '"')
        .replace(r"\n", "\n")
        .replace(r"\r", "\r")
        .replace(r"\t", "\t")
        .replace(r"\\", "\\")
    )


def extract_suspicious_reason(page_html: str, lines: list[str]) -> str:
    patterns = [
        r'status:"(?:suspicious|malicious)".{0,1200}?summary:"((?:[^"\\]|\\.)*)"',
        r"scan-status-suspicious[\s\S]{0,1200}?analysis-summary-text\">([^<]+)",
        r"scan-status-malicious[\s\S]{0,1200}?analysis-summary-text\">([^<]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            return clean_text(decode_js_string(match.group(1)))
    block = extract_block(lines, ["What to consider before installing", "Assessment"])
    if block:
        return block
    return ""


def has_security_signals(lines: list[str]) -> bool:
    text = "\n".join(lines)
    return any(
        token in text
        for token in (
            "VirusTotal",
            "ClawScan",
            "OpenClaw",
            "Static analysis",
            "Scan status",
            "What to consider before installing",
            "Assessment",
        )
    )


def needs_render(kind: str, lines: list[str], page_html: str) -> bool:
    joined = "\n".join(lines)
    if "Loading skill" in joined or "Loading plugin" in joined:
        return True
    if kind == "skill" and not has_security_signals(lines):
        return True
    return "Powered by Convex" in page_html and not has_security_signals(lines)


def fetch_html(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_page_html(
    url: str,
    *,
    render_mode: str,
    request_timeout: int,
    render_timeout_ms: int,
    render_wait_ms: int,
) -> tuple[str | None, str, str | None]:
    try:
        return fetch_html(url, request_timeout), "http", None
    except urllib.error.HTTPError as exc:
        warning = f"HTTP {exc.code} while fetching detail page."
    except Exception as exc:  # noqa: BLE001
        warning = clean_text(str(exc)) or "Failed to fetch detail page."

    if render_mode == "off":
        return None, "http", warning

    rendered_html, render_error = render_html(
        url,
        timeout_ms=render_timeout_ms,
        wait_ms=render_wait_ms,
    )
    if rendered_html:
        return rendered_html, "rendered", warning
    if render_error:
        warning = f"{warning or 'Fetch failed.'} Render fallback failed: {render_error}"
    return None, "http", warning


def build_security_detail_url(detail_url: str, scan_name: str) -> str:
    return f"{detail_url.rstrip('/')}/security/{scan_name}"


async def wait_for_dynamic_html(page: Any, *, max_wait_ms: int, interval_ms: int = 400) -> str:
    try:
        await page.wait_for_load_state("networkidle", timeout=min(max_wait_ms, 2500))
    except Exception:  # noqa: BLE001
        pass

    last_len = -1
    stable_rounds = 0
    elapsed = 0
    latest_html = ""
    while elapsed <= max_wait_ms:
        latest_html = await page.content()
        current_len = len(latest_html)
        if current_len == last_len:
            stable_rounds += 1
            if stable_rounds >= 2:
                return latest_html
        else:
            stable_rounds = 0
            last_len = current_len
        await page.wait_for_timeout(interval_ms)
        elapsed += interval_ms
    return latest_html


async def render_html_async(url: str, *, timeout_ms: int, wait_ms: int) -> str:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            return await wait_for_dynamic_html(page, max_wait_ms=wait_ms)
        finally:
            await browser.close()


def render_html(url: str, *, timeout_ms: int, wait_ms: int) -> tuple[str | None, str | None]:
    try:
        rendered = asyncio.run(render_html_async(url, timeout_ms=timeout_ms, wait_ms=wait_ms))
    except Exception as exc:  # noqa: BLE001
        return None, clean_text(str(exc)) or "render failed"
    return rendered, None


def choose_clawhub_url(payload: Any, kind: str, name: str) -> str | None:
    urls: list[str] = []
    owners: list[str] = []
    slugs: list[str] = []

    def visit(value: Any, *, key: str | None = None) -> None:
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                normalized = normalize_key(str(inner_key))
                if normalized in {"owner", "username", "publisher", "author"} and isinstance(inner_value, str):
                    owners.append(clean_text(inner_value).lstrip("@"))
                if normalized in {"slug", "name", "runtimid", "runtimeid"} and isinstance(inner_value, str):
                    slugs.append(clean_text(inner_value))
                visit(inner_value, key=normalized)
            return
        if isinstance(value, list):
            for item in value:
                visit(item, key=key)
            return
        if isinstance(value, str):
            cleaned = clean_text(value)
            if cleaned.startswith("http") and "clawhub.ai" in cleaned:
                urls.append(cleaned)

    visit(payload)
    for url in urls:
        if kind == "plugin" and "/plugins/" in url:
            return url
        if kind == "skill" and "/plugins/" not in url:
            return url

    if kind == "plugin":
        slug = slugs[0] if slugs else name
        return f"https://clawhub.ai/plugins/{slug}"
    if owners and slugs:
        return f"https://clawhub.ai/{owners[0]}/{slugs[0]}"
    return None


@dataclass
class ArtifactRef:
    key: str
    kind: str
    name: str
    requested_name: str | None = None
    version: str | None = None
    path: str | None = None
    release_ref: str | None = None
    detail_url: str | None = None
    skill_owner_candidates: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    key: str
    kind: str
    name: str
    requested_name: str | None
    version: str | None
    detail_url: str | None
    resolved_slug: str | None
    page_found: bool
    fetch_mode: str
    scan_status: str | None = None
    virus_total: str | None = None
    virus_total_report_url: str | None = None
    clawscan_verdict: str | None = None
    clawscan_confidence: str | None = None
    openclaw_verdict: str | None = None
    openclaw_confidence: str | None = None
    static_analysis_status: str | None = None
    static_analysis_summary: str | None = None
    publisher_handle: str | None = None
    suspicious: bool = False
    suspicious_reason: str | None = None
    pending: bool = False
    warnings: list[str] = field(default_factory=list)
    checked_at: str = field(default_factory=iso_now)


def extract_virustotal_report_url(page_html: str) -> str | None:
    patterns = [
        r'href="([^"]*virustotal\.com[^"]*)"\s*[^>]*>\s*View report',
        r'href="([^"]*virustotal\.com[^"]*)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            return html.unescape(match.group(1))
    return None


def extract_publisher_handle(lines: list[str]) -> str | None:
    text = "\n".join(lines)
    match = re.search(r"by\s*@?\s*([A-Za-z0-9][A-Za-z0-9_-]*)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r"@([A-Za-z0-9][A-Za-z0-9_-]*)", text)
    return match.group(1) if match else None


def extract_publisher_handle_from_html(page_html: str) -> str | None:
    patterns = [
        r'href="/u/([A-Za-z0-9][A-Za-z0-9_-]*)"',
        r'class="user-handle"[^>]*>@?([A-Za-z0-9][A-Za-z0-9_-]*)<',
        r'by\s*@<!-- -->\s*([A-Za-z0-9][A-Za-z0-9_-]*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def candidate_detail_urls(
    artifact: ArtifactRef,
    payload: Any | None,
    skill_owner_candidates: list[str],
) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()

    def add(url: str | None) -> None:
        if not url:
            return
        cleaned = clean_text(url)
        if not cleaned or cleaned in seen:
            return
        seen.add(cleaned)
        candidates.append(cleaned)

    add(artifact.detail_url)
    add(choose_clawhub_url(payload, artifact.kind, artifact.name) if payload is not None else None)

    if artifact.kind == "plugin":
        add(f"https://clawhub.ai/plugins/{artifact.name}")
    else:
        for owner in skill_owner_candidates:
            add(f"https://clawhub.ai/{owner}/{artifact.name}")
    return candidates


def scan_needs_retry(result: ScanResult) -> bool:
    return result.pending and result.page_found


def scan_artifact_status(
    artifact: ArtifactRef,
    *,
    inspect_payload_getter: Callable[[ArtifactRef], Any | None] | None = None,
    skill_owner_candidates: list[str] | None = None,
    render_mode: str = "auto",
    request_timeout: int = 20,
    render_timeout_ms: int = 20000,
    render_wait_ms: int = 5000,
) -> ScanResult:
    warnings: list[str] = []
    if artifact.detail_url and not detail_url_matches_artifact(artifact.detail_url, artifact.kind, artifact.name):
        warnings.append(
            f"Cached detail URL did not match current published slug {artifact.name}; refreshing live lookup."
        )
        artifact.detail_url = None

    payload: Any | None = None
    if artifact.detail_url is None and inspect_payload_getter is not None:
        payload = inspect_payload_getter(artifact)
    owner_candidates = normalize_owner_candidates(artifact.skill_owner_candidates)
    owner_candidates.extend(
        owner for owner in normalize_owner_candidates(skill_owner_candidates) if owner not in owner_candidates
    )
    if artifact.kind == "skill" and not owner_candidates:
        owner_candidates = list(DEFAULT_SKILL_OWNER_CANDIDATES)

    candidate_urls = candidate_detail_urls(artifact, payload, owner_candidates)
    if not candidate_urls:
        return ScanResult(
            key=artifact.key,
            kind=artifact.kind,
            name=artifact.name,
            requested_name=artifact.requested_name,
            version=artifact.version,
            detail_url=None,
            resolved_slug=None,
            page_found=False,
            fetch_mode="unresolved",
            scan_status="unresolved",
            pending=True,
            warnings=["Could not resolve a ClawHub detail URL for this artifact."],
        )

    detail_url: str | None = None
    page_html = ""
    fetch_mode = "http"
    last_fetch_warning: str | None = None
    for candidate_url in candidate_urls:
        fetched_html, fetched_mode, fetch_warning = fetch_page_html(
            candidate_url,
            render_mode=render_mode,
            request_timeout=request_timeout,
            render_timeout_ms=render_timeout_ms,
            render_wait_ms=render_wait_ms,
        )
        if fetched_html:
            page_html = fetched_html
            detail_url = candidate_url
            fetch_mode = fetched_mode
            break
        last_fetch_warning = fetch_warning
        if last_fetch_warning and "HTTP 404" in last_fetch_warning:
            continue

    if detail_url is None:
        return ScanResult(
            key=artifact.key,
            kind=artifact.kind,
            name=artifact.name,
            requested_name=artifact.requested_name,
            version=artifact.version,
            detail_url=candidate_urls[0],
            resolved_slug=extract_clawhub_slug_from_url(candidate_urls[0], artifact.kind),
            page_found=False,
            fetch_mode="http",
            scan_status="unresolved",
            pending=True,
            warnings=[last_fetch_warning or "Failed to fetch detail page."],
        )

    canonical_url = extract_canonical_url(page_html)
    if canonical_url and detail_url_matches_artifact(canonical_url, artifact.kind, artifact.name):
        detail_url = canonical_url

    artifact.detail_url = detail_url
    lines = extract_text_lines(page_html)
    if (
        fetch_mode != "rendered"
        and render_mode != "off"
        and (render_mode == "always" or needs_render(artifact.kind, lines, page_html))
    ):
        rendered_html, render_error = render_html(
            detail_url,
            timeout_ms=render_timeout_ms,
            wait_ms=render_wait_ms,
        )
        if rendered_html:
            page_html = rendered_html
            lines = extract_text_lines(page_html)
            fetch_mode = "rendered"
        elif render_error:
            warnings.append(f"Render fallback failed: {render_error}")

    virus_total = (
        normalize_status(extract_structured_scan_field(page_html, ("vtAnalysis",), "status"))
        or extract_status_after_label(lines, "VirusTotal")
    )
    virus_total_report_url = extract_virustotal_report_url(page_html)
    clawscan_verdict = (
        normalize_status(extract_structured_scan_field(page_html, ("llmAnalysis",), "status"))
        or extract_status_after_label(lines, "ClawScan")
        or extract_status_after_label(lines, "OpenClaw")
    )
    clawscan_confidence = extract_clawscan_confidence(lines)
    openclaw_verdict = clawscan_verdict
    openclaw_confidence = clawscan_confidence
    static_analysis_status = (
        normalize_status(extract_structured_scan_field(page_html, ("staticScan",), "status"))
        or extract_static_analysis_status(lines)
    )
    static_analysis_summary = (
        extract_definition_value_from_html(page_html, ("Summary", "Analysis"))
        or extract_structured_scan_field(page_html, ("staticScan",), "summary")
        or extract_static_analysis_summary(lines)
    )
    scan_status = extract_scan_status(lines)
    suspicious_reason = extract_suspicious_reason(page_html, lines) or None
    publisher_handle = extract_publisher_handle_from_html(page_html) or extract_publisher_handle(lines)

    if detail_url and (clawscan_verdict in {None, "pending", "warning", "suspicious", "malicious"} or not suspicious_reason):
        openclaw_url = build_security_detail_url(detail_url, "openclaw")
        security_html, _security_mode, security_warning = fetch_page_html(
            openclaw_url,
            render_mode=render_mode,
            request_timeout=request_timeout,
            render_timeout_ms=render_timeout_ms,
            render_wait_ms=render_wait_ms,
        )
        if security_html:
            security_lines = extract_text_lines(security_html)
            clawscan_verdict = (
                normalize_status(extract_structured_scan_field(security_html, ("llmAnalysis",), "status"))
                or extract_page_scan_badge_status(security_html)
                or extract_status_after_label(security_lines, "ClawScan")
                or extract_status_after_label(security_lines, "OpenClaw")
                or clawscan_verdict
            )
            suspicious_reason = (
                extract_definition_value_from_html(security_html, ("Summary", "Analysis"))
                or extract_structured_scan_field(security_html, ("llmAnalysis",), "summary")
                or extract_structured_scan_field(security_html, ("llmAnalysis",), "analysis")
                or extract_security_detail_summary(security_lines)
                or suspicious_reason
            )
            publisher_handle = (
                publisher_handle
                or extract_publisher_handle_from_html(security_html)
                or extract_publisher_handle(security_lines)
            )
        elif security_warning:
            warnings.append(f"OpenClaw detail lookup failed: {security_warning}")

    if detail_url and (
        static_analysis_status in {None, "pending", "warning", "suspicious", "malicious"}
        or not static_analysis_summary
    ):
        static_url = build_security_detail_url(detail_url, "static-analysis")
        static_html, _static_mode, static_warning = fetch_page_html(
            static_url,
            render_mode=render_mode,
            request_timeout=request_timeout,
            render_timeout_ms=render_timeout_ms,
            render_wait_ms=render_wait_ms,
        )
        if static_html:
            static_lines = extract_text_lines(static_html)
            static_analysis_status = (
                normalize_status(extract_structured_scan_field(static_html, ("staticScan",), "status"))
                or extract_page_scan_badge_status(static_html)
                or extract_status_after_label(static_lines, "Static analysis")
                or static_analysis_status
            )
            static_analysis_summary = (
                extract_definition_value_from_html(static_html, ("Summary", "Analysis"))
                or extract_structured_scan_field(static_html, ("staticScan",), "summary")
                or extract_security_detail_summary(static_lines)
                or extract_static_analysis_summary(static_lines)
                or static_analysis_summary
            )
        elif static_warning:
            warnings.append(f"Static analysis detail lookup failed: {static_warning}")

    if static_analysis_status in {"suspicious", "malicious", "warning"} and clawscan_verdict not in {"suspicious", "malicious", "warning"}:
        suspicious_reason = static_analysis_summary or suspicious_reason

    suspicious = any(
        status in {"suspicious", "malicious", "warning"}
        for status in (virus_total, clawscan_verdict, static_analysis_status, scan_status)
    )
    explicit_pending_scan = scan_status in {"pending", "unresolved"}
    explicit_final_scan = scan_status in {"clean", "suspicious", "malicious", "warning"}
    pending = explicit_pending_scan or (
        not suspicious
        and not explicit_final_scan
        and (
            not has_security_signals(lines)
            or virus_total in {None, "pending"}
            or clawscan_verdict in {None, "pending"}
        )
    )
    if scan_status is None:
        if pending:
            scan_status = "pending"
        elif suspicious:
            scan_status = "suspicious"
        elif (
            virus_total in {"benign", "clean", "safe"}
            and clawscan_verdict in {"benign", "clean", "safe"}
            and static_analysis_status not in {"suspicious", "malicious", "warning"}
        ):
            scan_status = "clean"
    if pending and not suspicious_reason:
        warnings.append("Security scan output is still incomplete or pending.")

    return ScanResult(
        key=artifact.key,
        kind=artifact.kind,
        name=artifact.name,
        requested_name=artifact.requested_name,
        version=artifact.version,
        detail_url=detail_url,
        resolved_slug=extract_clawhub_slug_from_url(detail_url, artifact.kind),
        page_found=True,
        fetch_mode=fetch_mode,
        scan_status=scan_status,
        virus_total=virus_total,
        virus_total_report_url=virus_total_report_url,
        clawscan_verdict=clawscan_verdict,
        clawscan_confidence=clawscan_confidence,
        openclaw_verdict=openclaw_verdict,
        openclaw_confidence=openclaw_confidence,
        static_analysis_status=static_analysis_status,
        static_analysis_summary=static_analysis_summary,
        publisher_handle=publisher_handle,
        suspicious=suspicious,
        suspicious_reason=suspicious_reason,
        pending=pending,
        warnings=warnings,
    )


def scan_result_to_state(result: ScanResult) -> dict[str, Any]:
    return asdict(result)


class ClawHubSession:
    def __init__(
        self,
        *,
        config_path: Path,
        token: str,
        inspect_timeout: int = 25,
        login_timeout: int = 20,
    ) -> None:
        self.config_path = config_path
        self.token = token
        self.inspect_timeout = inspect_timeout
        self.login_timeout = login_timeout
        self.logged_in = False

    def clawhub(self, args: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
        return run_command(
            ["clawhub", *args],
            env={"CLAWHUB_CONFIG_PATH": str(self.config_path)},
            timeout=timeout,
        )

    def login(self) -> None:
        if self.logged_in:
            return
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            result = self.clawhub(["login", "--token", self.token, "--no-browser"], timeout=self.login_timeout)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("ClawHub login timed out during live status scan.") from exc
        if result.returncode != 0:
            message = clean_text(result.stderr or result.stdout) or "ClawHub login failed."
            raise RuntimeError(message)
        self.logged_in = True

    def inspect_payload(self, artifact: ArtifactRef) -> Any | None:
        try:
            self.login()
        except RuntimeError:
            return None
        command = ["inspect", artifact.name, "--json"] if artifact.kind == "skill" else ["package", "inspect", artifact.name, "--json"]
        try:
            result = self.clawhub(command, timeout=self.inspect_timeout)
        except subprocess.TimeoutExpired:
            return None
        if result.returncode != 0:
            return None
        return try_parse_json(result.stdout)


def load_artifacts_from_state(
    path: Path,
    *,
    targets: str,
    artifact_keys: set[str] | None = None,
    statuses: set[str] | None = None,
) -> list[ArtifactRef]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    artifacts: list[ArtifactRef] = []
    status_filter = statuses or {"published"}
    for key, meta in sorted((payload.get("artifacts") or {}).items()):
        if artifact_keys and key not in artifact_keys:
            continue
        kind = str(meta.get("kind") or "")
        if targets != "both" and kind != targets:
            continue
        if status_filter and str(meta.get("status") or "") not in status_filter:
            continue
        live_scan = meta.get("live_scan") or {}
        published_name = str(meta.get("published_name") or meta.get("name") or "")
        cached_detail_url = str(live_scan.get("detail_url") or "") or None
        if cached_detail_url and not detail_url_matches_artifact(cached_detail_url, kind, published_name):
            cached_detail_url = None
        artifacts.append(
            ArtifactRef(
                key=key,
                kind=kind,
                name=published_name,
                requested_name=str(meta.get("name") or "") or None,
                version=str(meta.get("version") or "") or None,
                path=str(meta.get("path") or "") or None,
                release_ref=str(meta.get("release_ref") or "") or None,
                detail_url=cached_detail_url,
                skill_owner_candidates=normalize_owner_candidates(
                    [
                        str(meta.get("owner_handle") or ""),
                        str(live_scan.get("publisher_handle") or ""),
                    ]
                ),
            )
        )
    return artifacts


def write_output(path: Path, results: list[ScanResult]) -> None:
    existing_artifacts: dict[str, dict[str, Any]] = {}
    if path.exists():
        try:
            existing_payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing_payload = {}
        if isinstance(existing_payload, dict):
            for item in existing_payload.get("artifacts", []):
                if isinstance(item, dict):
                    key = clean_text(str(item.get("key") or ""))
                    if key:
                        existing_artifacts[key] = item

    for result in results:
        item = scan_result_to_state(result)
        key = clean_text(str(item.get("key") or ""))
        if key:
            existing_artifacts[key] = item

    merged_results = [existing_artifacts[key] for key in sorted(existing_artifacts)]
    payload = {
        "generated_at": iso_now(),
        "summary": {
            "total": len(merged_results),
            "suspicious": sum(1 for item in merged_results if item.get("suspicious")),
            "pending": sum(1 for item in merged_results if item.get("pending")),
            "resolved_urls": sum(1 for item in merged_results if item.get("detail_url")),
        },
        "artifacts": merged_results,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check live ClawHub VirusTotal / ClawScan / Static analysis status for published artifacts.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Publish state JSON to read artifacts from and write back scan results into.",
    )
    parser.add_argument(
        "--output-file",
        default=str(DEFAULT_OUTPUT_FILE),
        help="Standalone JSON report output path.",
    )
    parser.add_argument(
        "--targets",
        choices=("skill", "plugin", "both"),
        default="both",
        help="Which artifact kinds to scan.",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Optional artifact key(s) such as skill:search or plugin:twitter-plugin.",
    )
    parser.add_argument(
        "--include-status",
        action="append",
        default=["published"],
        help="State statuses to include. Repeat to include more than one.",
    )
    parser.add_argument(
        "--accounts-file",
        default=str(DEFAULT_ACCOUNTS_FILE),
        help="Optional credentials file containing clawhub_ApI_token* entries for skill URL resolution.",
    )
    parser.add_argument(
        "--token",
        action="append",
        default=[],
        help="Optional explicit ClawHub token used for inspect-based skill URL resolution.",
    )
    parser.add_argument(
        "--skill-owner",
        action="append",
        default=[],
        help="Optional skill owner handle(s) used to guess skill detail URLs when inspect does not resolve them.",
    )
    parser.add_argument(
        "--config-root",
        default=str(DEFAULT_CONFIG_ROOT),
        help="Directory for the scanner's temporary ClawHub CLI auth config.",
    )
    parser.add_argument(
        "--render-mode",
        choices=("off", "auto", "always"),
        default="auto",
        help="Whether to use Playwright rendering for dynamic ClawHub pages.",
    )
    parser.add_argument(
        "--request-timeout",
        type=int,
        default=20,
        help="HTTP fetch timeout in seconds.",
    )
    parser.add_argument(
        "--render-timeout-ms",
        type=int,
        default=20000,
        help="Navigation timeout for Playwright rendering.",
    )
    parser.add_argument(
        "--render-wait-ms",
        type=int,
        default=5000,
        help="Extra wait window for dynamic page HTML to stabilize.",
    )
    parser.add_argument(
        "--inspect-timeout",
        type=int,
        default=25,
        help="Timeout in seconds for `clawhub inspect` / `clawhub package inspect` during skill URL resolution.",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    state_path = Path(args.state_file)
    output_path = Path(args.output_file)
    artifact_keys = set(args.artifact or [])
    statuses = {item for item in args.include_status if item}
    artifacts = load_artifacts_from_state(
        state_path,
        targets=args.targets,
        artifact_keys=artifact_keys or None,
        statuses=statuses,
    )
    if not artifacts:
        print("No matching artifacts found in state.", flush=True)
        return 0

    tokens = resolve_tokens(Path(args.accounts_file), args.token)
    session: ClawHubSession | None = None
    if any(artifact.kind == "skill" and not artifact.detail_url for artifact in artifacts):
        if tokens:
            session = ClawHubSession(
                config_path=Path(args.config_root) / "scanner.json",
                token=tokens[0],
                inspect_timeout=args.inspect_timeout,
            )
        else:
            print(
                "Warning: no ClawHub token resolved; skill detail URLs may remain unresolved.",
                flush=True,
            )

    payload = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"artifacts": {}}
    skill_owner_candidates = normalize_owner_candidates(args.skill_owner) or list(DEFAULT_SKILL_OWNER_CANDIDATES)
    results: list[ScanResult] = []
    for artifact in artifacts:
        result = scan_artifact_status(
            artifact,
            inspect_payload_getter=session.inspect_payload if session else None,
            skill_owner_candidates=skill_owner_candidates,
            render_mode=args.render_mode,
            request_timeout=args.request_timeout,
            render_timeout_ms=args.render_timeout_ms,
            render_wait_ms=args.render_wait_ms,
        )
        results.append(result)
        if artifact.key in payload.get("artifacts", {}):
            payload["artifacts"][artifact.key]["live_scan"] = scan_result_to_state(result)
        status_label = "suspicious" if result.suspicious else "pending" if result.pending else "ok"
        url_label = result.detail_url or "unresolved"
        print(
            f"{artifact.key}: {status_label} | vt={result.virus_total or '-'} | "
            f"clawscan={result.clawscan_verdict or result.openclaw_verdict or '-'} | "
            f"static={result.static_analysis_status or '-'} | {url_label}",
            flush=True,
        )

    if state_path.exists():
        state_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_output(output_path, results)

    suspicious = sum(1 for item in results if item.suspicious)
    pending = sum(1 for item in results if item.pending)
    print("", flush=True)
    print("ClawHub live status summary", flush=True)
    print(f"  total:      {len(results)}", flush=True)
    print(f"  suspicious: {suspicious}", flush=True)
    print(f"  pending:    {pending}", flush=True)
    print(f"  output:     {output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
