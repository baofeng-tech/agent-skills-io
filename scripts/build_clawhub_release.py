#!/usr/bin/env python3
"""Build a ClawHub-ready release tree from targetSkills/."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import build_claude_release as base


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "clawhub-release"


def detect_domain(name: str, description: str) -> str:
    lower = f"{name} {description}".lower()
    if "last30days" in lower:
        return "search"
    if "twitter" in lower or lower.startswith("x-"):
        return "twitter"
    if "youtube" in lower:
        return "youtube"
    if any(token in lower for token in ("search", "tavily", "perplexity", "scholar", "web-search", "multi-search")):
        return "search"
    if any(token in lower for token in ("stock", "market", "portfolio", "dividend", "prediction", "finance")):
        return "finance"
    if any(token in lower for token in ("media", "image", "video")):
        return "media"
    if any(token in lower for token in ("llm", "provider", "router", "model", "qwen", "deepseek")):
        return "ai"
    return "automation"


def is_zh_variant(name: str) -> bool:
    return name.endswith("-zh") or re.search(r"[\u4e00-\u9fff]", name) is not None


def infer_emoji(domain: str) -> str:
    return {
        "twitter": "🐦",
        "youtube": "▶️",
        "search": "🔎",
        "finance": "📊",
        "media": "🎬",
        "ai": "🤖",
        "automation": "🛠",
    }.get(domain, "🛠")


def needs_aisa_key(skill_dir: Path) -> bool:
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "AISA_API_KEY" in text:
            return True
    return False


def infer_required_bins(skill_dir: Path) -> list[str]:
    suffixes = {path.suffix.lower() for path in skill_dir.rglob("*") if path.is_file()}
    bins: list[str] = []
    if ".py" in suffixes:
        bins.append("python3")
    if ".sh" in suffixes:
        bins.append("bash")
    if {".js", ".mjs", ".cjs", ".ts"} & suffixes:
        bins.append("node")
    return bins


def infer_entrypoints(skill_dir: Path) -> list[str]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return []
    commands: list[str] = []
    for path in sorted(scripts_dir.iterdir()):
        if not path.is_file():
            continue
        if re.match(r"^(compare|dev-python|evaluate|generate|sync|test-|verify)", path.name):
            continue
        rel = path.relative_to(skill_dir).as_posix()
        if path.suffix == ".py":
            commands.append(f"python3 {rel} --help")
        elif path.suffix == ".sh":
            commands.append(f"bash {rel} --help")
        if len(commands) >= 3:
            break
    return commands


def resolve_clawhub_slug(skill_dir: Path, frontmatter: dict[str, Any]) -> str:
    metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
    candidates: list[Any] = [
        frontmatter.get("clawhub-slug"),
        frontmatter.get("clawhub_slug"),
    ]
    for scope in ("clawhub", "openclaw", "aisa"):
        scoped = metadata.get(scope) if isinstance(metadata, dict) else None
        if not isinstance(scoped, dict):
            continue
        candidates.extend(
            [
                scoped.get("slug"),
                scoped.get("clawhubSlug"),
                scoped.get("clawhub_slug"),
            ]
        )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return skill_dir.name


def build_description(name: str, domain: str, zh: bool) -> str:
    if zh:
        templates = {
            "twitter": "通过 AIsa 搜索 X/Twitter 账号、推文、趋势与经 OAuth 授权的发布流程。触发条件：当用户需要 Twitter 研究、监控或互动操作时使用。支持搜索、监控与授权发布。",
            "youtube": "通过 AIsa 搜索 YouTube 视频、频道、趋势与排名结果。触发条件：当用户需要选题研究、竞品分析或频道检索时使用。支持视频发现与趋势分析。",
            "search": "通过 AIsa 执行网页、多源或近 30 天研究检索。触发条件：当用户需要搜索、研究、比对或趋势归纳时使用。支持多源检索与结构化输出。",
            "finance": "通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。",
            "media": "通过 AIsa 生成图片或视频素材。触发条件：当用户需要 AI 媒体生成或创意资产产出时使用。支持图像与视频工作流。",
            "ai": "通过 AIsa 使用模型路由、Provider 配置或中文大模型能力。触发条件：当用户需要模型接入、路由或 Provider 设置时使用。支持统一模型工作流。",
            "automation": f"使用 {name} 提供的自动化工作流。触发条件：当用户需要该领域的专用自动化能力时使用。支持公开发布的运行时能力。",
        }
        return templates[domain]

    templates = {
        "twitter": "Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.",
        "youtube": "Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.",
        "search": "Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.",
        "finance": "Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.",
        "media": "Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.",
        "ai": "Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.",
        "automation": f"Use {name} for domain-specific automation. Use when: the user needs this workflow's specialized runtime behavior. Supports the packaged public workflow only.",
    }
    return templates[domain]


def domain_sections(domain: str, zh: bool) -> tuple[list[str], list[str], list[str], list[str]]:
    if zh:
        mapping = {
            "twitter": (
                ["用户需要做 Twitter/X 研究、监控、发帖或互动。", "用户需要查看账号、时间线、趋势、列表、社区或 Spaces。", "用户需要在不提供密码的前提下完成授权发布。"] ,
                ["研究某个账号近期动态。", "监控热点关键词或趋势。", "完成 OAuth 授权后发帖或互动。"] ,
                ["研究马斯克最近 30 天关于 AI 的推文趋势", "搜索某个产品在 X 上的讨论反馈", "授权后发一条产品更新推文"] ,
                ["不要请求密码、Cookie 或浏览器凭据。", "不要在未确认 API 成功前声称已发布。", "公开包默认返回授权链接，而不是自动打开浏览器。"] ,
            ),
            "youtube": (
                ["用户需要搜索 YouTube 视频、频道或趋势。", "用户需要做选题、竞品或 SERP 排名研究。", "用户需要快速拿到公开视频结果。"] ,
                ["查找某个关键词下的热门视频。", "分析竞品频道最近的内容方向。", "观察趋势话题下的视频分布。"] ,
                ["搜索 OpenAI Agents 相关热门 YouTube 视频", "看看某个频道最近都在发什么内容", "找出 AI coding 主题下排名靠前的视频"] ,
                ["不要伪造视频标题、链接或观看量。", "只基于返回结果做总结。", "如果上游返回空结果，要明确说明。"] ,
            ),
            "search": (
                ["用户需要网页、多源或近 30 天研究检索。", "用户需要竞品研究、趋势扫描或结构化搜索结果。", "用户希望用一个技能覆盖多来源检索。"] ,
                ["先搜索再归纳最近动态。", "对两个产品做近期对比研究。", "把多来源结果整理成结构化输出。"] ,
                ["研究 OpenAI Agents SDK 最近 30 天讨论", "比较 OpenClaw 和 Codex 最近的反馈", "搜索某个品牌最近一周的社区反应"] ,
                ["不要把开发测试脚本当成公开功能。", "不要承诺未实际返回的来源。", "如果某些来源超时，要按真实情况说明。"] ,
            ),
            "finance": (
                ["用户需要股票、加密、预测市场或投资研究数据。", "用户需要价格、筛选、估值、组合或事件分析。", "用户需要结构化金融输出用于进一步分析。"] ,
                ["查看价格走势与市场波动。", "筛选符合条件的股票或币种。", "研究组合、分红或预测市场机会。"] ,
                ["查询 NVDA 最近价格与分析师预期", "找出符合某些财务条件的股票", "查看 BTC 和 ETH 的最新市场数据"] ,
                ["不要给出虚构价格或财务数字。", "不要把示例请求当成投资建议。", "如果接口受限，要直接说明。"] ,
            ),
            "media": (
                ["用户需要生成图片或视频。", "用户需要快速得到创意草稿或媒体素材。", "用户需要通过一个 API key 完成媒体生成。"] ,
                ["生成图像草稿。", "生成视频概念片段。", "把创意需求转成媒体素材。"] ,
                ["生成一张未来城市风格海报", "生成一个产品演示短视频脚本素材", "把某个场景描述转成图片草稿"] ,
                ["不要承诺未生成成功的媒体结果。", "不要引用不存在的本地文件。", "如上游限流，要直接说明。"] ,
            ),
            "ai": (
                ["用户需要模型路由、Provider 配置或中文大模型接入。", "用户需要统一模型入口或 Provider 设置说明。", "用户需要对模型与成本进行快速判断。"] ,
                ["配置 AIsa Provider。", "查看模型路由或支持列表。", "为中文大模型接入准备环境。"] ,
                ["如何配置 AIsa Provider 使用 Qwen", "列出当前支持的模型", "帮我选择适合中文任务的模型"] ,
                ["不要请求密码或多余凭据。", "不要把未 shipped 的配置方式写成公开主路径。", "优先描述公开发布包真正支持的运行方式。"] ,
            ),
            "automation": (
                ["用户需要这个技能提供的专用自动化能力。", "用户需要公开发布包里的主工作流。", "用户希望使用打包后的运行时入口。"] ,
                ["运行公开主工作流。", "检查运行时入口是否可用。", "按公开说明执行自动化任务。"] ,
                ["帮我执行这个技能的主要自动化工作", "告诉我这个包最适合处理什么任务", "给我公开包支持的示例请求"] ,
                ["不要引用未发布的开发工具。", "不要声称未 shipped 的能力。", "保持说明与实际运行时一致。"] ,
            ),
        }
        return mapping[domain]

    mapping = {
        "twitter": (
            ["The user needs Twitter/X research, monitoring, posting, or engagement workflows.", "The user wants profiles, timelines, trends, lists, communities, or Spaces.", "The user wants approved posting without sharing passwords."],
            ["Research an account or conversation thread.", "Monitor a keyword, trend, or competitor.", "Authorize and publish a post after explicit approval."],
            ["Research recent AI agent conversations on X", "Search how users are reacting to a product launch on Twitter", "Authorize and publish a short product update post"],
            ["Do not ask for passwords, cookies, or browser credentials.", "Do not claim posting succeeded until the API confirms it.", "Return authorization links instead of relying on auto-open behavior."],
        ),
        "youtube": (
            ["The user needs YouTube video, channel, or trend discovery.", "The user wants content research, SERP scouting, or competitor review.", "The user wants public YouTube results quickly."],
            ["Find top-ranking videos for a topic.", "Inspect a competitor channel's recent content direction.", "Scan trend-heavy queries for content opportunities."],
            ["Search top YouTube videos about OpenAI Agents", "Review a competitor channel's recent uploads", "Find high-ranking videos for AI coding tutorials"],
            ["Do not invent video titles, URLs, or metrics.", "Summaries should stay grounded in returned results.", "If the upstream returns no results, say so clearly."],
        ),
        "search": (
            ["The user needs web, multi-source, or last-30-days research.", "The user wants competitor scans, trend discovery, or structured search output.", "The user wants one skill to cover multiple retrieval surfaces."],
            ["Search and summarize recent evidence.", "Compare two tools or companies using recent signals.", "Turn multi-source retrieval into a research brief."],
            ["Research OpenAI Agents SDK over the last 30 days", "Compare OpenClaw and Codex using recent public discussion", "Search recent sentiment around a product launch"],
            ["Do not present test-only helpers as public features.", "Do not claim sources that were not actually queried.", "If some providers time out, report that honestly."],
        ),
        "finance": (
            ["The user needs stocks, crypto, prediction market, or portfolio research.", "The user wants prices, screening, valuation, or event-driven analysis.", "The user wants structured financial output for downstream analysis."],
            ["Check price action and market movement.", "Screen assets or equities that match filters.", "Research portfolios, dividends, or market opportunities."],
            ["Query NVDA price history and analyst expectations", "Find stocks matching a screening rule", "Check BTC and ETH market data for a portfolio view"],
            ["Do not invent prices or financial metrics.", "Do not turn examples into financial advice.", "If an upstream endpoint is limited, say so directly."],
        ),
        "media": (
            ["The user needs image or video generation.", "The user wants creative drafts or media assets from one API key.", "The user wants quick generation workflows."],
            ["Generate an image draft.", "Generate a short video concept.", "Turn a creative brief into media output."],
            ["Generate a futuristic city poster", "Create a short product-demo video concept", "Turn a scene description into an image draft"],
            ["Do not promise media output that was not returned.", "Do not reference local files that were not provided.", "If the upstream is rate-limited, say so."],
        ),
        "ai": (
            ["The user needs model routing, provider setup, or Chinese LLM access.", "The user wants one place for provider configuration or model selection.", "The user wants setup guidance for AIsa-hosted model workflows."],
            ["Configure an AIsa provider path.", "Inspect supported models or routing options.", "Prepare a runtime for Chinese-model access."],
            ["Help me configure AIsa for Qwen", "List the supported routed models", "Choose a model for Chinese long-form analysis"],
            ["Do not ask for extra credentials beyond the shipped flow.", "Do not advertise setup paths that the public bundle does not ship.", "Keep setup instructions aligned with the actual runtime."],
        ),
        "automation": (
            ["The user needs the skill's packaged automation workflow.", "The user wants the public runtime entrypoint, not the developer bundle.", "The user needs domain-specific automation guidance."],
            ["Run the main public workflow.", "Confirm the packaged entrypoint is usable.", "Guide the user through the released runtime path."],
            ["Help me use this skill's main automation path", "What is this public package best for?", "Show me example requests for the shipped runtime"],
            ["Do not reference unpublished developer tools.", "Do not claim functionality outside the shipped bundle.", "Keep instructions aligned with the packaged runtime."],
        ),
    }
    return mapping[domain]


def build_body(skill_dir: Path, skill_name: str, description: str, domain: str, zh: bool) -> str:
    when_to_use, workflows, example_requests, guardrails = domain_sections(domain, zh)
    quick_reference = infer_entrypoints(skill_dir)
    setup_lines = [
        "- `AISA_API_KEY` is required for AIsa-backed API access.",
        "- Use repo-relative `scripts/` paths from the shipped package.",
        "- Prefer explicit CLI auth flags when a script exposes them.",
    ]
    if zh:
        setup_lines = [
            "- 需要 `AISA_API_KEY` 才能访问 AIsa API。",
            "- 使用公开包里的相对 `scripts/` 路径。",
            "- 如果脚本提供显式鉴权参数，优先使用该参数。",
        ]

    lines = [f"# {base.prettify_skill_name(skill_name)}", "", description]

    lines.extend(["", "## When to use" if not zh else "## 适用场景", ""])
    for item in when_to_use:
        lines.append(f"- {item}")

    lines.extend(["", "## High-Intent Workflows" if not zh else "## 高意图工作流", ""])
    for item in workflows:
        lines.append(f"- {item}")

    if quick_reference:
        lines.extend(["", "## Quick Reference" if not zh else "## 快速命令", ""])
        for item in quick_reference:
            lines.append(f"- `{item}`")

    lines.extend(["", "## Setup" if not zh else "## 配置", ""])
    for item in setup_lines:
        lines.append(item)

    lines.extend(["", "## Example Requests" if not zh else "## 示例请求", ""])
    for item in example_requests:
        lines.append(f"- {item}")

    lines.extend(["", "## Guardrails" if not zh else "## 边界说明", ""])
    for item in guardrails:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def clean_frontmatter(skill_dir: Path, frontmatter: dict[str, Any], publish_name: str) -> dict[str, Any]:
    canonical_name = str(frontmatter.get("name") or skill_dir.name).strip()
    name = publish_name.strip() or canonical_name
    domain = detect_domain(canonical_name, str(frontmatter.get("description") or ""))
    description = build_description(name, domain, is_zh_variant(name))
    bins = infer_required_bins(skill_dir)
    envs = ["AISA_API_KEY"] if needs_aisa_key(skill_dir) else []
    version = frontmatter.get("version") or "1.0.0"
    license_value = frontmatter.get("license") or "Apache-2.0"
    cleaned: dict[str, Any] = {
        "name": name,
        "description": description,
        "author": "AIsa",
        "version": str(version),
        "license": license_value,
        "user-invocable": True,
    }
    if envs:
        cleaned["primaryEnv"] = "AISA_API_KEY"
    if bins or envs:
        cleaned["requires"] = {}
        if bins:
            cleaned["requires"]["bins"] = bins
        if envs:
            cleaned["requires"]["env"] = envs
    cleaned["metadata"] = {
        "aisa": {
            "emoji": infer_emoji(domain),
            "requires": {
                "bins": bins,
                "env": envs,
            },
            "primaryEnv": "AISA_API_KEY" if envs else None,
            "compatibility": ["openclaw", "claude-code", "hermes"],
        },
        "openclaw": {
            "emoji": infer_emoji(domain),
            "requires": {
                "bins": bins,
                "env": envs,
            },
            "primaryEnv": "AISA_API_KEY" if envs else None,
        },
    }

    def compact(data: Any) -> Any:
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                compacted = compact(value)
                if compacted in (None, "", [], {}):
                    continue
                result[key] = compacted
            return result
        if isinstance(data, list):
            return [compact(item) for item in data if compact(item) not in (None, "", [], {})]
        return data

    return compact(cleaned)


def build_skill(src_dir: Path) -> base.SkillAudit:
    frontmatter, _body = base.load_frontmatter(src_dir / "SKILL.md")
    publish_name = resolve_clawhub_slug(src_dir, frontmatter)
    out_dir = OUTPUT_ROOT / publish_name
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    kept = base.copy_tree(src_dir, out_dir)
    cleaned_frontmatter = clean_frontmatter(src_dir, frontmatter, publish_name)
    domain = detect_domain(publish_name, str(frontmatter.get("description") or cleaned_frontmatter["description"]))
    zh = is_zh_variant(src_dir.name)

    audit = base.SkillAudit(
        name=publish_name,
        source_path=str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=cleaned_frontmatter["description"],
    )

    base.prune_release_tree(out_dir, audit)
    base.patch_runtime_files(out_dir, audit)
    (out_dir / "SKILL.md").write_text(
        base.dump_skill(
            cleaned_frontmatter,
            build_body(out_dir, publish_name, cleaned_frontmatter["description"], domain, zh),
        ),
        encoding="utf-8",
    )
    base.write_skill_readme(out_dir, cleaned_frontmatter, "clawhub")
    audit.changes.append("generated a ClawHub-oriented SKILL.md with high-intent workflows and example requests")
    audit.changes.append("normalized frontmatter for ClawHub upload compatibility while keeping canonical metadata.aisa")
    if any(name in kept for name in ("scripts", "references")):
        audit.changes.append("copied runtime scripts and essential references only")
    return audit


def write_docs(audits: list[base.SkillAudit]) -> None:
    readme = [
        "# ClawHub Release",
        "",
        "ClawHub-oriented packaged copy of all `targetSkills/` mother skills.",
        "",
        "## Principles",
        "",
        "- Keep `targetSkills/` as the mother-skill source layer.",
        "- Generate `clawhub-release/` as the upload-focused runtime layer.",
        "- Keep canonical `metadata.aisa`, then duplicate the minimal `metadata.openclaw` hints only where helpful for upload compatibility.",
        "- Prefer runtime-only files, repo-local defaults, and explicit auth flows.",
        "",
        "## Skills",
        "",
    ]
    for audit in audits:
        readme.append(f"- `{audit.name}`")
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    index_lines = ["# ClawHub Release Index", ""]
    for audit in audits:
        index_lines.append(f"- `{audit.name}`: {audit.description}")
    (OUTPUT_ROOT / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    audit_doc = ["# ClawHub Release Audit", ""]
    for audit in audits:
        audit_doc.extend(
            [
                f"## {audit.name}",
                "",
                f"- Source: `{audit.source_path}`",
                f"- Output: `{audit.output_path}`",
                f"- Description: {audit.description}",
            ]
        )
        for change in audit.changes:
            audit_doc.append(f"- Change: {change}")
        for risk in audit.residual_risks:
            audit_doc.append(f"- Residual risk: {risk}")
        audit_doc.append("")
    (OUTPUT_ROOT / "AUDIT.md").write_text("\n".join(audit_doc), encoding="utf-8")

    index = {
        "generated_at": "2026-04-20",
        "source": "targetSkills",
        "skills": [
            {
                "name": audit.name,
                "path": audit.output_path,
                "description": audit.description,
                "changes": audit.changes,
                "residual_risks": audit.residual_risks,
            }
            for audit in audits
        ],
    }
    (OUTPUT_ROOT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    audits = [build_skill(path.parent) for path in sorted(SOURCE_ROOT.glob("*/SKILL.md"))]
    write_docs(audits)
    print(f"Built {len(audits)} ClawHub-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
