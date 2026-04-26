#!/usr/bin/env python3
"""Run an explicit AISA-backed LLM pass over AIsa API skills in targetSkills/."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_ROOT = REPO_ROOT / "targetSkills"
PROPOSAL_ROOT = REPO_ROOT / "targets" / "llm-skill-refinement"
DEFAULT_BASE_URL = "https://api.aisa.one/v1"
DEFAULT_MODEL = "gpt-4.1"
DEFAULT_SKILLS = (
    REPO_ROOT / ".agents" / "skills" / "clawhub-skill-optimizer-all" / "SKILL.md",
    REPO_ROOT / ".agents" / "skills" / "clawhub-security-auditor-all" / "SKILL.md",
)
REFERENCE_FILES = (
    REPO_ROOT / ".agents" / "skills" / "clawhub-skill-optimizer-all" / "references" / "frontmatter-rules.md",
    REPO_ROOT / ".agents" / "skills" / "clawhub-skill-optimizer-all" / "references" / "body-structure.md",
    REPO_ROOT / ".agents" / "skills" / "clawhub-skill-optimizer-all" / "references" / "bilingual-rules.md",
    REPO_ROOT / "targets" / "clawhub-suspicious-causes-and-fixes-2026-04-25.md",
)
ENV_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
ALLOWED_ENV_NAMES = {
    "AISA_API_KEY",
    "AI_BASE_URL",
    "AI_API_KEY",
    "AI_MODEL",
    "TWITTER_RELAY_BASE_URL",
}


@dataclass
class ClientConfig:
    mode: str
    base_url: str
    api_key: str
    model: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use an AISA/OpenAI-compatible LLM to refine AIsa-backed SKILL.md and README files.",
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Comma-separated skill names under targetSkills/. Defaults to all detected AIsa-backed skills.",
    )
    parser.add_argument(
        "--target-root",
        default=str(TARGET_ROOT),
        help="Root directory containing mother skills.",
    )
    parser.add_argument(
        "--proposal-root",
        default=str(PROPOSAL_ROOT),
        help="Where JSON proposals and raw model responses are written.",
    )
    parser.add_argument(
        "--mode",
        choices=("chat-completions", "messages", "generate-content"),
        default="chat-completions",
        help="API surface to use against the configured provider.",
    )
    parser.add_argument("--base-url", default="", help="Override the API base URL.")
    parser.add_argument("--api-key", default="", help="Override the API key.")
    parser.add_argument("--model", default="", help="Override the model name.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the returned SKILL.md / README.md back into targetSkills/.",
    )
    parser.add_argument(
        "--if-available",
        action="store_true",
        help="Exit successfully when credentials are unavailable.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Only print which skills would be processed.",
    )
    parser.add_argument(
        "--max-skills",
        type=int,
        default=0,
        help="Optional cap on the number of skills to process.",
    )
    return parser


def normalize_base_url(base_url: str, mode: str, model: str) -> str:
    base = base_url.rstrip("/")
    if mode == "chat-completions":
        if base.endswith("/chat/completions"):
            return base
        if base.endswith("/v1"):
            return f"{base}/chat/completions"
        return f"{base}/v1/chat/completions"
    if mode == "messages":
        if base.endswith("/messages"):
            return base
        if base.endswith("/v1"):
            return f"{base}/messages"
        return f"{base}/v1/messages"
    model_id = urllib.parse.quote(model, safe="")
    if base.endswith(":generateContent"):
        return base
    if base.endswith("/v1"):
        return f"{base}/models/{model_id}:generateContent"
    return f"{base}/v1/models/{model_id}:generateContent"


def resolve_client_config(args: argparse.Namespace) -> ClientConfig | None:
    api_key = (
        args.api_key.strip()
        or os.environ.get("AISA_API_KEY", "").strip()
        or os.environ.get("AI_API_KEY", "").strip()
    )
    if not api_key:
        return None
    base_url = (
        args.base_url.strip()
        or os.environ.get("AISA_BASE_URL", "").strip()
        or os.environ.get("AI_BASE_URL", "").strip()
        or DEFAULT_BASE_URL
    )
    model = (
        args.model.strip()
        or os.environ.get("AISA_LLM_MODEL", "").strip()
        or os.environ.get("AI_MODEL", "").strip()
        or DEFAULT_MODEL
    )
    return ClientConfig(
        mode=args.mode,
        base_url=normalize_base_url(base_url, args.mode, model),
        api_key=api_key,
        model=model,
    )


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def is_aisa_backed(skill_dir: Path) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    text = load_text(skill_md)
    if skill_dir.name.startswith("aisa-"):
        return True
    return any(token in text for token in ("AISA_API_KEY", "api.aisa.one", "AIsa"))


def discover_skill_dirs(target_root: Path, explicit_names: list[str]) -> list[Path]:
    if explicit_names:
        return [target_root / name for name in explicit_names if (target_root / name / "SKILL.md").exists()]
    return [
        skill_dir
        for skill_dir in sorted(path for path in target_root.iterdir() if path.is_dir())
        if is_aisa_backed(skill_dir)
    ]


def load_context() -> str:
    blocks: list[str] = []
    for path in DEFAULT_SKILLS:
        if path.exists():
            blocks.append(f"# {path.relative_to(REPO_ROOT)}\n\n{load_text(path).strip()}")
    for path in REFERENCE_FILES:
        if path.exists():
            blocks.append(f"# {path.relative_to(REPO_ROOT)}\n\n{load_text(path).strip()}")
    return "\n\n".join(blocks).strip()


def required_env_names(text: str) -> list[str]:
    return sorted({token for token in ENV_PATTERN.findall(text) if token in ALLOWED_ENV_NAMES})


def build_messages(skill_dir: Path, context: str) -> list[dict[str, str]]:
    skill_md = load_text(skill_dir / "SKILL.md")
    readme_md = load_text(skill_dir / "README.md")
    required_envs = required_env_names(skill_md + "\n" + readme_md)
    prompt = (
        "Refine this existing AIsa-backed skill for publish quality.\n\n"
        "Hard constraints:\n"
        "- Preserve runtime behavior, command paths, filenames, relative paths, and code examples unless they are obviously inconsistent.\n"
        "- Do not invent new APIs, new dependencies, or new environment variables.\n"
        "- Keep the skill aligned with repo-local optimizer and auditor rules.\n"
        "- Improve clarity around AISA_API_KEY, relay targets, OAuth/upload side effects, and breakout positioning when relevant.\n"
        "- Return strict JSON with keys: summary, skill_md, readme_md, notes.\n"
        "- skill_md must be the full replacement content for SKILL.md.\n"
        "- readme_md must be the full replacement README.md content, or null if no README update is needed.\n"
        f"- Preserve these required env names if they already exist: {required_envs or ['AISA_API_KEY']}.\n\n"
        f"Repo rules context:\n{context}\n\n"
        f"Target skill directory: {skill_dir.name}\n\n"
        "Current SKILL.md:\n"
        f"{skill_md}\n\n"
        "Current README.md:\n"
        f"{readme_md or '(missing)'}\n"
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a careful release-copy editor working inside a multi-platform skill repo. "
                "Keep functionality intact and only improve publish-surface clarity, metadata, and positioning."
            ),
        },
        {"role": "user", "content": prompt},
    ]


def request_payload(config: ClientConfig, messages: list[dict[str, str]]) -> dict[str, Any]:
    if config.mode == "chat-completions":
        return {
            "model": config.model,
            "temperature": 0.2,
            "messages": messages,
        }
    if config.mode == "messages":
        anthropic_messages = [{"role": item["role"], "content": item["content"]} for item in messages if item["role"] != "system"]
        system = "\n\n".join(item["content"] for item in messages if item["role"] == "system")
        payload: dict[str, Any] = {
            "model": config.model,
            "max_tokens": 8192,
            "messages": anthropic_messages,
        }
        if system:
            payload["system"] = system
        return payload
    flattened = "\n\n".join(f"{item['role'].upper()}:\n{item['content']}" for item in messages)
    return {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": flattened}],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
        },
    }


def extract_response_text(config: ClientConfig, payload: dict[str, Any]) -> str:
    request = urllib.request.Request(
        config.base_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM request failed ({exc.code}): {detail}") from exc

    data = json.loads(body)
    if config.mode == "chat-completions":
        choice = ((data.get("choices") or [{}])[0]).get("message") or {}
        content = choice.get("content")
        if isinstance(content, list):
            return "\n".join(str(item.get("text") or item.get("content") or "").strip() for item in content).strip()
        return str(content or "").strip()
    if config.mode == "messages":
        content_items = data.get("content") or []
        return "\n".join(str(item.get("text") or "").strip() for item in content_items if isinstance(item, dict)).strip()
    candidates = data.get("candidates") or []
    if not candidates:
        return ""
    parts = (((candidates[0] or {}).get("content") or {}).get("parts") or [])
    return "\n".join(str(part.get("text") or "").strip() for part in parts if isinstance(part, dict)).strip()


def iter_balanced_json_objects(text: str) -> list[str]:
    objects: list[str] = []
    seen: set[str] = set()
    in_string = False
    escaped = False
    depth = 0
    start: int | None = None

    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
            continue
        if char == "}" and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                candidate = text[start : index + 1].strip()
                if candidate and candidate not in seen:
                    seen.add(candidate)
                    objects.append(candidate)
                start = None
    return objects


def extract_json(text: str) -> dict[str, Any]:
    candidates: list[str] = []

    def add_candidate(value: str) -> None:
        cleaned = value.strip().lstrip("\ufeff")
        if cleaned and cleaned not in candidates:
            candidates.append(cleaned)

    add_candidate(text)
    for fenced in re.findall(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE):
        add_candidate(fenced)
    for candidate in iter_balanced_json_objects(text):
        add_candidate(candidate)

    for candidate in candidates:
        if not candidate:
            continue
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise RuntimeError("Model output was not valid JSON.")


def coerce_json_response(config: ClientConfig, raw_response: str) -> str:
    repair_messages = [
        {
            "role": "system",
            "content": (
                "You convert prior model output into strict JSON only. "
                "Return a single JSON object with keys summary, skill_md, readme_md, notes and no surrounding prose."
            ),
        },
        {
            "role": "user",
            "content": (
                "Reformat the following output into strict JSON only. "
                "Do not change the meaning of the fields.\n\n"
                f"{raw_response}"
            ),
        },
    ]
    return extract_response_text(config, request_payload(config, repair_messages))


def validate_proposal(skill_dir: Path, proposal: dict[str, Any]) -> None:
    original = load_text(skill_dir / "SKILL.md") + "\n" + load_text(skill_dir / "README.md")
    required = required_env_names(original)
    skill_md = str(proposal.get("skill_md") or "").strip()
    if not skill_md:
        raise RuntimeError(f"{skill_dir.name}: proposal missing skill_md")
    for env_name in required:
        if env_name not in skill_md and env_name not in str(proposal.get("readme_md") or ""):
            raise RuntimeError(f"{skill_dir.name}: proposal dropped required env reference {env_name}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    target_root = Path(args.target_root).resolve()
    proposal_root = Path(args.proposal_root).resolve()
    explicit_names = [item.strip() for item in args.skills.split(",") if item.strip()]
    skill_dirs = discover_skill_dirs(target_root, explicit_names)

    if args.max_skills > 0:
        skill_dirs = skill_dirs[: args.max_skills]

    if not skill_dirs:
        print("No matching AIsa-backed skills found.")
        return 0

    print("LLM refinement targets:")
    for skill_dir in skill_dirs:
        print(f"  - {skill_dir.name}")
    if args.plan:
        return 0

    config = resolve_client_config(args)
    if config is None:
        if args.if_available:
            print("Skip LLM refinement: no API credentials found.")
            return 0
        raise SystemExit("Missing AISA/AI API credentials for the LLM refinement step.")

    context = load_context()
    if not context:
        raise SystemExit("Missing repo-local optimizer/auditor skill context under .agents/skills.")

    proposal_root.mkdir(parents=True, exist_ok=True)
    for skill_dir in skill_dirs:
        messages = build_messages(skill_dir, context)
        raw_response = extract_response_text(config, request_payload(config, messages))
        try:
            proposal = extract_json(raw_response)
        except RuntimeError:
            raw_response = coerce_json_response(config, raw_response)
            proposal = extract_json(raw_response)
        validate_proposal(skill_dir, proposal)

        proposal_path = proposal_root / f"{skill_dir.name}.json"
        proposal_payload = {
            "skill": skill_dir.name,
            "summary": proposal.get("summary"),
            "notes": proposal.get("notes") or [],
            "skill_md": proposal.get("skill_md"),
            "readme_md": proposal.get("readme_md"),
            "raw_response": raw_response,
        }
        write_text(proposal_path, json.dumps(proposal_payload, indent=2, ensure_ascii=False))

        if args.apply:
            write_text(skill_dir / "SKILL.md", str(proposal.get("skill_md") or ""))
            readme_md = proposal.get("readme_md")
            if isinstance(readme_md, str) and readme_md.strip():
                write_text(skill_dir / "README.md", readme_md)
            print(f"applied: {skill_dir.name}")
        else:
            print(f"proposed: {skill_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
