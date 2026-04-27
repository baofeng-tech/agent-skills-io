#!/usr/bin/env python3
"""Local proxy that injects AISA_API_KEY for Codex custom-provider requests."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


LISTEN_HOST = os.environ.get("CODEX_AISA_PROXY_HOST", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("CODEX_AISA_PROXY_PORT", "8787"))
UPSTREAM_BASE_URL = os.environ.get("CODEX_AISA_PROXY_UPSTREAM", "https://api.aisa.one").rstrip("/")
AISA_API_KEY = os.environ.get("AISA_API_KEY", "").strip()


def json_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/healthz":
            body = json_bytes({"ok": True, "upstream": UPSTREAM_BASE_URL})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._send_json(405, {"error": "Use POST for model requests."})

    def do_POST(self) -> None:  # noqa: N802
        if not AISA_API_KEY:
            self._send_json(500, {"error": "AISA_API_KEY is required."})
            return

        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        upstream_url = f"{UPSTREAM_BASE_URL}{self.path}"
        content_type = self.headers.get("Content-Type", "application/json")

        with tempfile.TemporaryDirectory(prefix="codex-aisa-proxy-") as tmp_dir:
            tmp_path = Path(tmp_dir)
            request_path = tmp_path / "request.bin"
            headers_path = tmp_path / "headers.txt"
            response_path = tmp_path / "response.bin"
            request_path.write_bytes(body)

            result = subprocess.run(
                [
                    "curl",
                    "--http1.1",
                    "-sS",
                    "-D",
                    str(headers_path),
                    "-o",
                    str(response_path),
                    "-X",
                    "POST",
                    upstream_url,
                    "-H",
                    f"Authorization: Bearer {AISA_API_KEY}",
                    "-H",
                    f"Content-Type: {content_type}",
                    "--data-binary",
                    f"@{request_path}",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                self._send_json(
                    502,
                    {
                        "error": "Upstream curl relay failed.",
                        "details": (result.stderr or result.stdout).strip(),
                    },
                )
                return

            status_code, header_map = parse_headers(headers_path.read_text(encoding="utf-8", errors="replace"))
            response_body = response_path.read_bytes()

        self.send_response(status_code)
        self.send_header("Content-Type", header_map.get("content-type", "application/json"))
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, fmt: str, *args: object) -> None:
        print(fmt % args, flush=True)

    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_headers(text: str) -> tuple[int, dict[str, str]]:
    blocks = [block for block in text.split("\r\n\r\n") if block.strip()]
    header_block = blocks[-1] if blocks else text
    lines = [line for line in header_block.splitlines() if line.strip()]
    if not lines:
        return 502, {}

    status = 502
    first_line = lines[0]
    parts = first_line.split()
    if len(parts) >= 2 and parts[1].isdigit():
        status = int(parts[1])

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return status, headers


def main() -> int:
    if not AISA_API_KEY:
        print("AISA_API_KEY is required.", flush=True)
        return 1

    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), ProxyHandler)
    print(f"Codex AISA proxy listening on http://{LISTEN_HOST}:{LISTEN_PORT}", flush=True)
    print(f"Forwarding to {UPSTREAM_BASE_URL}", flush=True)
    print("Health check: GET /healthz", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
