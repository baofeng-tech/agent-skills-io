#!/usr/bin/env python3
"""Run the repo-local skill refinement helper over AISA API skills in targetSkills/."""

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

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_ROOT = REPO_ROOT / "targetSkills"
PROPOSAL_ROOT = REPO_ROOT / "targets" / "llm-skill-refinement"
DEFAULT_BASE_URL = "https://api.aisa.one/v1"
DEFAULT_MODEL = "gpt-4.1"
REPO_SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
PROFILE_CONTEXT = {
    "source": {
        "skills": (
            REPO_SKILLS_ROOT / "aisa-source-skill-editor" / "SKILL.md",
        ),
        "references": (
            REPO_ROOT / "targets" / "platform-skill-plugin-methodology.md",
            REPO_ROOT / "targets" / "skill-modification-rules-2026-04-19.md",
            REPO_ROOT / "targets" / "targetskills-agentskills-compliance-audit-2026-04-20.md",
        ),
    },
    "clawhub_breakout": {
        "skills": (
            REPO_SKILLS_ROOT / "aisa-clawhub-breakout-editor" / "SKILL.md",
            REPO_SKILLS_ROOT / "clawhub-skill-optimizer-all" / "SKILL.md",
            REPO_SKILLS_ROOT / "clawhub-security-auditor-all" / "SKILL.md",
        ),
        "references": (
            REPO_SKILLS_ROOT / "clawhub-skill-optimizer-all" / "references" / "frontmatter-rules.md",
            REPO_SKILLS_ROOT / "clawhub-skill-optimizer-all" / "references" / "body-structure.md",
            REPO_SKILLS_ROOT / "clawhub-skill-optimizer-all" / "references" / "bilingual-rules.md",
            REPO_ROOT / "targets" / "aisa-api-breakout-rollout-plan-2026-04-28.md",
            REPO_ROOT / "targets" / "clawhub-breakout-variants.json",
        ),
    },
    "clawhub_suspicious": {
        "skills": (
            REPO_SKILLS_ROOT / "aisa-clawhub-suspicious-remediation-editor" / "SKILL.md",
            REPO_SKILLS_ROOT / "clawhub-security-auditor-all" / "SKILL.md",
        ),
        "references": (
            REPO_ROOT / "targets" / "clawhub-suspicious-causes-and-fixes-2026-04-25.md",
            REPO_ROOT / "targets" / "platform-skill-plugin-methodology.md",
            REPO_ROOT / "targets" / "platform-layer-and-rule-split-audit-2026-04-28.md",
        ),
    },
}
DEFAULT_PROFILE = "source"
PROFILE_PROMPTS = {
    "source": (
        "- Keep this as a neutral mother skill for targetSkills/.\n"
        "- Do not introduce ClawHub-only breakout slugs, plugin wrapper details, or platform-specific release sections.\n"
        "- Keep sibling positioning portable so downstream build scripts can regenerate platform-specific layers cleanly.\n"
    ),
    "clawhub_breakout": (
        "- This refinement is for ClawHub breakout work feeding later release layers.\n"
        "- You may strengthen task-first breakout positioning when the runtime truly supports it.\n"
        "- Make relay, OAuth, upload, and env requirements explicit across public copy.\n"
    ),
    "clawhub_suspicious": (
        "- This refinement is for diagnosis-driven ClawHub suspicious remediation only.\n"
        "- Start from the selected diagnosis reasons and remove scanner ambiguity with the smallest safe change.\n"
        "- Do not widen scope or add breakout/growth copy unless the diagnosis context explicitly requires it.\n"
        "- Make relay, OAuth, upload, external execution, and env requirements explicit across public copy.\n"
    ),
}
ENV_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
ALLOWED_ENV_NAMES = {
    "AISA_API_KEY",
    "AISA_LLM_MODEL",
}


@dataclass
class ClientConfig:
    mode: str
    base_url: str
    api_key: str
    model: str
    source: str


def split_skill_document(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None, text
    if not isinstance(frontmatter, dict):
        return None, text
    return frontmatter, parts[2].lstrip("\r\n")


def render_skill_document(frontmatter: dict[str, Any], body: str) -> str:
    frontmatter_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    body_text = body.lstrip("\r\n").rstrip()
    return f"---\n{frontmatter_text}\n---\n\n{body_text}\n"


def stabilize_skill_md(skill_dir: Path, proposal_skill_md: str) -> str:
    original_frontmatter, original_body = split_skill_document(load_text(skill_dir / "SKILL.md"))
    proposal_frontmatter, proposal_body = split_skill_document(proposal_skill_md)
    if original_frontmatter is None or proposal_frontmatter is None:
        return proposal_skill_md

    # Keep release/runtime frontmatter stable and only allow the LLM to refresh
    # user-facing copy such as the description and markdown body.
    merged_frontmatter = dict(original_frontmatter)
    proposed_description = proposal_frontmatter.get("description")
    if isinstance(proposed_description, str) and proposed_description.strip():
        merged_frontmatter["description"] = proposed_description.strip()

    return render_skill_document(merged_frontmatter, proposal_body or original_body)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use the repo-local skill refinement helper to refine AISA API SKILL.md and README files.",
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Comma-separated skill names under targetSkills/. Defaults to all detected AISA API skills.",
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
        choices=("chat-completions", "messages", "generate-content", "responses"),
        default="chat-completions",
        help="API surface to use against the configured provider.",
    )
    parser.add_argument("--model", default="", help="Override the model name.")
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILE_CONTEXT),
        default=DEFAULT_PROFILE,
        help=(
            "Rule profile to load. Use source for neutral mother-skill refinement, "
            "clawhub_breakout for breakout-only refinement, and clawhub_suspicious for diagnosis-driven suspicious remediation."
        ),
    )
    parser.add_argument(
        "--extra-context-file",
        action="append",
        default=[],
        help="Optional extra context file(s) appended to the repo rules context, such as a remediation report JSON.",
    )
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
    if mode == "responses":
        if base.endswith("/responses"):
            return base
        if base.endswith("/v1"):
            return f"{base}/responses"
        return f"{base}/v1/responses"
    model_id = urllib.parse.quote(model, safe="")
    if base.endswith(":generateContent"):
        return base
    if base.endswith("/v1"):
        return f"{base}/models/{model_id}:generateContent"
    return f"{base}/v1/models/{model_id}:generateContent"


def first_nonempty(*values: str) -> str:
    for value in values:
        stripped = value.strip()
        if stripped:
            return stripped
    return ""


def resolve_client_config(args: argparse.Namespace) -> ClientConfig | None:
    explicit_model = args.model.strip()

    aisa_api_key = os.environ.get("AISA_API_KEY", "").strip()
    aisa_model = os.environ.get("AISA_LLM_MODEL", "").strip()

    if not aisa_api_key:
        return None
    model = first_nonempty(explicit_model, aisa_model, DEFAULT_MODEL)
    return ClientConfig(
        mode=args.mode,
        base_url=normalize_base_url(DEFAULT_BASE_URL, args.mode, model),
        api_key=aisa_api_key,
        model=model,
        source="AISA_API_KEY",
    )


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_first_heading(text: str) -> str:
    _frontmatter, body = split_skill_document(text)
    candidate_body = body if body is not None else text
    for line in candidate_body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def all_context_skill_paths() -> tuple[Path, ...]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for bundle in PROFILE_CONTEXT.values():
        for path in bundle["skills"]:
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return tuple(paths)


def helper_skill_headings() -> set[str]:
    headings: set[str] = set()
    for path in all_context_skill_paths():
        if not path.exists():
            continue
        heading = extract_first_heading(load_text(path))
        if heading:
            headings.add(heading)
    return headings


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


def load_context(profile: str, extra_context_files: list[str]) -> str:
    bundle = PROFILE_CONTEXT[profile]
    blocks: list[str] = []
    for path in bundle["skills"]:
        if path.exists():
            blocks.append(f"# {path.relative_to(REPO_ROOT)}\n\n{load_text(path).strip()}")
    for path in bundle["references"]:
        if path.exists():
            blocks.append(f"# {path.relative_to(REPO_ROOT)}\n\n{load_text(path).strip()}")
    for raw_path in extra_context_files:
        path = Path(raw_path).resolve()
        if path.exists():
            label = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
            blocks.append(f"# {label}\n\n{load_text(path).strip()}")
    return "\n\n".join(blocks).strip()


def required_env_names(text: str) -> list[str]:
    return sorted({token for token in ENV_PATTERN.findall(text) if token in ALLOWED_ENV_NAMES})


def build_messages(skill_dir: Path, context: str, profile: str) -> list[dict[str, str]]:
    skill_md = load_text(skill_dir / "SKILL.md")
    readme_md = load_text(skill_dir / "README.md")
    required_envs = required_env_names(skill_md + "\n" + readme_md)
    profile_prompt = PROFILE_PROMPTS.get(profile, PROFILE_PROMPTS[DEFAULT_PROFILE])
    prompt = (
        "Refine this existing AISA API skill for publish quality.\n\n"
        "Hard constraints:\n"
        "- Preserve runtime behavior, command paths, filenames, relative paths, and code examples unless they are obviously inconsistent.\n"
        "- Do not invent new APIs, new dependencies, or new environment variables.\n"
        "- Keep the skill aligned with repo-local optimizer and auditor rules.\n"
        f"{profile_prompt}"
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
    if config.mode == "responses":
        instructions = "\n\n".join(item["content"] for item in messages if item["role"] == "system").strip()
        response_input = [
            {
                "role": item["role"] if item["role"] in {"user", "assistant"} else "user",
                "content": [{"type": "input_text", "text": item["content"]}],
            }
            for item in messages
            if item["role"] != "system"
        ]
        payload = {
            "model": config.model,
            "input": response_input,
        }
        if instructions:
            payload["instructions"] = instructions
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
    if config.mode == "responses":
        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()
        lines: list[str] = []
        for item in data.get("output") or []:
            if not isinstance(item, dict):
                continue
            for content_item in item.get("content") or []:
                if not isinstance(content_item, dict):
                    continue
                if str(content_item.get("type") or "") not in {"output_text", "text"}:
                    continue
                text = str(content_item.get("text") or "").strip()
                if text:
                    lines.append(text)
        return "\n\n".join(lines).strip()
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


def validate_raw_skill_md(skill_dir: Path, raw_skill_md: str) -> None:
    frontmatter, _body = split_skill_document(raw_skill_md)
    if frontmatter is None:
        raise RuntimeError(f"{skill_dir.name}: proposal missing SKILL.md frontmatter")
    proposed_name = str(frontmatter.get("name") or "").strip()
    if proposed_name != skill_dir.name:
        raise RuntimeError(
            f"{skill_dir.name}: proposal targeted unexpected skill name {proposed_name or '(missing)'}"
        )
    proposed_heading = extract_first_heading(raw_skill_md)
    if proposed_heading and proposed_heading in helper_skill_headings():
        raise RuntimeError(
            f"{skill_dir.name}: proposal body matched repo helper skill content ({proposed_heading})"
        )


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
        print("No matching AISA API skills found.")
        return 0

    print("Skill refinement targets:")
    for skill_dir in skill_dirs:
        print(f"  - {skill_dir.name}")
    if args.plan:
        return 0

    config = resolve_client_config(args)
    if config is None:
        if args.if_available:
            print("Skip LLM refinement: no API credentials found.")
            return 0
        raise SystemExit(
            "Missing AISA_API_KEY for the repo-local skill-refinement helper."
        )

    print(
        "Refinement helper config: "
        f"source={config.source}, mode={config.mode}, model={config.model}, base_url={config.base_url}"
    )
    print(f"Refinement profile: {args.profile}")

    context = load_context(args.profile, args.extra_context_file)
    if not context:
        raise SystemExit(
            f"Missing repo-local refinement context for profile {args.profile} under .agents/skills or targets/."
        )

    proposal_root.mkdir(parents=True, exist_ok=True)
    for skill_dir in skill_dirs:
        messages = build_messages(skill_dir, context, args.profile)
        raw_response = ""
        proposal: dict[str, Any] = {}
        try:
            raw_response = extract_response_text(config, request_payload(config, messages))
            try:
                proposal = extract_json(raw_response)
            except RuntimeError:
                raw_response = coerce_json_response(config, raw_response)
                proposal = extract_json(raw_response)

            raw_skill_md = str(proposal.get("skill_md") or "")
            validate_raw_skill_md(skill_dir, raw_skill_md)
            proposal["skill_md"] = stabilize_skill_md(skill_dir, raw_skill_md)
            validate_proposal(skill_dir, proposal)
        except Exception as exc:
            proposal_path = proposal_root / f"{skill_dir.name}.json"
            error_payload = {
                "skill": skill_dir.name,
                "error": str(exc),
                "summary": proposal.get("summary"),
                "notes": proposal.get("notes") or [],
                "skill_md": proposal.get("skill_md"),
                "readme_md": proposal.get("readme_md"),
                "raw_response": raw_response,
            }
            write_text(proposal_path, json.dumps(error_payload, indent=2, ensure_ascii=False))
            if args.if_available:
                print(f"skipped: {skill_dir.name} ({exc})")
                continue
            raise

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
