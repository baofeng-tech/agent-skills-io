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
BREAKOUT_VARIANTS_PATH = REPO_ROOT / "targets" / "clawhub-breakout-variants.json"
TWITTER_PROFILES = {
    "twitter",
    "twitter_api",
    "twitter_watchlist",
    "twitter_engagement",
    "twitter_post_engage",
}
OPTIONAL_ENV_ALLOWLIST = {
    "AISA_BASE_URL",
    "AISA_MODEL",
    "LAST30DAYS_FUN_MODEL",
    "LAST30DAYS_PLANNER_MODEL",
    "LAST30DAYS_RERANK_MODEL",
    "TWITTER_RELAY_BASE_URL",
    "TWITTER_RELAY_TIMEOUT",
    "XIAOHONGSHU_API_BASE",
}
OPTIONAL_ENV_IGNORE = {
    "AISA_API_KEY",
    "CLAUDE_PLUGIN_ROOT",
}


def parse_version_parts(value: Any) -> tuple[int, ...]:
    if value is None:
        return ()
    parts: list[int] = []
    for raw in str(value).split("."):
        raw = raw.strip()
        if not raw or not raw.isdigit():
            return ()
        parts.append(int(raw))
    return tuple(parts)


def choose_release_version(source_version: Any, existing_version: Any) -> str:
    source_text = str(source_version).strip() if source_version not in (None, "") else ""
    existing_text = str(existing_version).strip() if existing_version not in (None, "") else ""
    source_parts = parse_version_parts(source_text)
    existing_parts = parse_version_parts(existing_text)
    if source_parts and existing_parts:
        return existing_text if existing_parts > source_parts else source_text
    if source_text:
        return source_text
    if existing_text:
        return existing_text
    return "1.0.0"


def detect_domain(name: str, description: str) -> str:
    lower_name = name.lower()
    lower = f"{name} {description}".lower()
    if "last30days" in lower_name or "last30days" in lower:
        return "search"
    if "youtube" in lower_name:
        return "youtube"
    if "twitter" in lower_name or lower_name.startswith("x-"):
        return "twitter"
    if any(token in lower_name for token in ("search", "tavily", "perplexity", "scholar", "web-search", "multi-search")):
        return "search"
    if any(token in lower_name for token in ("stock", "market", "portfolio", "dividend", "prediction", "finance")):
        return "finance"
    if any(token in lower_name for token in ("media", "image", "video")):
        return "media"
    if any(token in lower_name for token in ("llm", "provider", "router", "model", "qwen", "deepseek")):
        return "ai"
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


def load_breakout_variants() -> dict[str, list[dict[str, str]]]:
    if not BREAKOUT_VARIANTS_PATH.exists():
        return {}
    try:
        payload = json.loads(BREAKOUT_VARIANTS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    variants: dict[str, list[dict[str, str]]] = {}
    for raw in payload.get("variants") or []:
        if not isinstance(raw, dict):
            continue
        source = str(raw.get("source") or "").strip()
        slug = str(raw.get("slug") or raw.get("name") or "").strip()
        if not source or not slug:
            continue
        entry = {
            "source": source,
            "slug": slug,
            "profile": str(raw.get("profile") or "").strip(),
            "version": str(raw.get("version") or "").strip(),
        }
        variants.setdefault(source, []).append(entry)
    return variants


def release_profile(name: str, domain: str, profile_override: str | None = None) -> str:
    if profile_override and profile_override.strip():
        return profile_override.strip()
    return domain


def release_heading(name: str, domain: str, profile_override: str | None = None) -> str:
    profile = release_profile(name, domain, profile_override)
    headings = {
        "twitter_api": "AIsa Twitter API Command Center",
        "twitter_watchlist": "AIsa Twitter Watchlist Desk",
        "twitter_engagement": "AIsa Twitter Engagement Suite",
        "twitter_post_engage": "AIsa Twitter Post-Launch Follow-Through",
        "search_flagship": "AIsa Search Command Center",
        "search_multi_engine": "AIsa Multi-Engine Search Hub",
        "search_verification": "Multi-Source Search Verification Engine",
        "youtube_scout": "AIsa YouTube SERP Scout",
        "youtube_lookup": "AIsa YouTube Search Relay",
        "market_flagship": "AIsa Market Command Center",
        "market_equities": "MarketPulse Equity Research Desk",
        "market_prediction": "AIsa Prediction Market Probability Desk",
        "market_crypto": "Crypto Market Data Terminal",
        "market_stock_analyst": "US Stock Analyst Workbench",
    }
    return headings.get(profile, base.prettify_skill_name(name))


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


def infer_optional_envs(skill_dir: Path, profile: str) -> list[str]:
    optional_envs: list[str] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for env_name in re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text):
            if env_name in OPTIONAL_ENV_IGNORE or env_name not in OPTIONAL_ENV_ALLOWLIST:
                continue
            if env_name not in optional_envs:
                optional_envs.append(env_name)
    return optional_envs


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


def build_description(name: str, domain: str, zh: bool, profile_override: str | None = None) -> str:
    profile = release_profile(name, domain, profile_override)
    if zh:
        templates = {
            "twitter": "通过 AIsa 搜索 X/Twitter 账号、推文、趋势与经 OAuth 授权的发布流程。触发条件：当用户需要 Twitter 研究、监控或互动操作时使用。支持搜索、监控与授权发布。",
            "twitter_api": "通过 AIsa 执行 Twitter/X 研究、监控、观察列表与经 OAuth 授权的发布。触发条件：当用户需要一个旗舰 Twitter 技能来跟踪趋势、竞品或发布内容时使用。支持搜索、监控与授权发布。",
            "twitter_watchlist": "通过 AIsa 把 X/Twitter 作为观察列表与趋势监控工作台来使用。触发条件：当用户需要竞品追踪、观察列表、趋势扫描或账号巡检时使用。支持监控、搜索与经授权的跟进发布。",
            "twitter_engagement": "通过 AIsa 执行 X/Twitter 的点赞、关注、回复与经授权发布。触发条件：当用户已经知道要互动的账号或推文，并需要显式授权的互动动作时使用。支持研究上下文、互动与授权发布。",
            "twitter_post_engage": "通过 AIsa 执行 X/Twitter 发帖后的跟进动作。触发条件：当用户已经有草稿、活动或发帖目标，并需要发布后继续处理早期互动时使用。支持发帖、回复上下文与轻量互动。",
            "youtube": "通过 AIsa 搜索 YouTube 视频、频道、趋势与排名结果。触发条件：当用户需要选题研究、竞品分析或频道检索时使用。支持视频发现与趋势分析。",
            "search": "通过 AIsa 执行网页、多源或近 30 天研究检索。触发条件：当用户需要搜索、研究、比对或趋势归纳时使用。支持多源检索与结构化输出。",
            "search_flagship": "通过 AIsa 执行网页、学术、Tavily 与深度研究检索。触发条件：当用户需要一个旗舰搜索技能来做实时查询、来源发现或引用型研究时使用。支持快速检索、答案生成与深度研究。",
            "search_multi_engine": "通过 AIsa 提供一个一键多引擎检索工作台。触发条件：当用户想在网页、学术、Tavily 与 Perplexity 检索面之间显式切换并比较结果时使用。支持多工具并排检索与研究启动。",
            "search_verification": "通过 AIsa 做多来源对比检索与置信度判断。触发条件：当用户需要交叉验证、共识检查或一份比较多个检索面的研究输出时使用。支持并行检索、置信度评分与结构化综合。",
            "youtube_scout": "通过 AIsa 执行 YouTube 排名侦察、内容研究与竞品频道巡检。触发条件：当用户需要 YouTube 选题研究、竞品追踪或趋势发现时使用。支持 SERP 观察、频道研究与趋势扫描。",
            "youtube_lookup": "通过 AIsa 执行轻量 YouTube 搜索与筛选。触发条件：当用户只需要快速查询视频、频道、播放列表或地区/语言过滤时使用。支持 curl-first 查询与结构化结果返回。",
            "finance": "通过 AIsa 查询股票、加密、预测市场与投资分析数据。触发条件：当用户需要市场研究、筛选、价格走势或组合分析时使用。支持研究与分析输出。",
            "market_flagship": "通过 AIsa 执行股票、加密与宏观利率的跨资产市场查询。触发条件：当用户需要一个旗舰市场技能来查看报价、走势、观察列表或跨资产报告时使用。支持股票、加密、筛选与宏观上下文。",
            "market_equities": "通过 AIsa 执行股票、财报、分析师预期与 SEC 文件研究。触发条件：当用户需要股票基本面、财报、研报上下文或筛选，而不是广义跨资产数据时使用。支持股权研究与公司层分析。",
            "market_prediction": "通过 AIsa 执行 Polymarket 与 Kalshi 概率市场查询。触发条件：当用户需要事件合约赔率、预测市场情绪或头寸视图时使用。支持市场查找、价格历史与组合视角。",
            "market_crypto": "通过 AIsa 执行加密货币价格、图表、交易所与合约地址查询。触发条件：当用户需要 crypto 专用市场数据、合约地址价格或分类研究时使用。支持现货价格、图表与交易所研究。",
            "market_stock_analyst": "通过 AIsa 执行更深的美股 thesis 分析。触发条件：当用户需要把财务、新闻、社交情绪和 AI 分析组合成一份美股研究结论时使用。支持 thesis 构建、对比研究与报告生成。",
            "media": "通过 AIsa 生成图片或视频素材。触发条件：当用户需要 AI 媒体生成或创意资产产出时使用。支持图像与视频工作流。",
            "ai": "通过 AIsa 使用模型路由、Provider 配置或中文大模型能力。触发条件：当用户需要模型接入、路由或 Provider 设置时使用。支持统一模型工作流。",
            "automation": f"使用 {name} 提供的自动化工作流。触发条件：当用户需要该领域的专用自动化能力时使用。支持公开发布的运行时能力。",
        }
        return templates[profile]

    templates = {
        "twitter": "Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. Use when: the user needs Twitter research, monitoring, or engagement workflows. Supports search, monitoring, and approved posting.",
        "twitter_api": "Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.",
        "twitter_watchlist": "Run Twitter/X watchlists, competitor monitoring, trend scans, and OAuth-gated follow-through through AIsa. Use when: the user needs a monitoring-first Twitter desk for recurring account sweeps, launch reactions, or trend tracking. Supports search, monitoring, and approved posting after review.",
        "twitter_engagement": "Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.",
        "twitter_post_engage": "Run Twitter/X post-launch follow-through through AIsa. Use when: the user already has a draft, launch tweet, or reply target and needs one skill to publish and then manage early interactions. Supports posting, reply context, and lightweight engagement.",
        "youtube": "Search YouTube videos, channels, rankings, and trends through AIsa. Use when: the user needs YouTube research, competitor scouting, or content discovery. Supports video discovery and SERP-style analysis.",
        "search": "Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.",
        "search_flagship": "Run web, scholar, Tavily, and deep research through one AIsa search command center. Use when: the user needs one flagship skill for live search, source discovery, or citation-ready research. Supports fast lookup, answer generation, and deep research reports.",
        "search_multi_engine": "Run web, scholar, Tavily, and Perplexity-backed research through one explicit multi-engine AIsa hub. Use when: the user wants a one-key package with tool-by-tool control across several search surfaces. Supports multi-engine lookup, extraction, and research kickoff.",
        "search_verification": "Run confidence-scored multi-source retrieval through AIsa. Use when: the user needs cross-source verification, consensus checks, or one report that compares multiple search surfaces. Supports parallel retrieval, confidence scoring, and synthesis-ready outputs.",
        "youtube_scout": "Run ranking-aware YouTube research through AIsa. Use when: the user needs YouTube content discovery, competitor scouting, or repeated SERP-style channel research. Supports top-video discovery, channel sweeps, and trend scouting.",
        "youtube_lookup": "Run lightweight YouTube lookup through AIsa. Use when: the user needs fast video, channel, playlist, locale, or pagination queries without the broader research workflow. Supports curl-first discovery and structured YouTube search results.",
        "finance": "Query stocks, crypto, prediction markets, and portfolio research through AIsa. Use when: the user needs market data, screening, price history, or investment analysis. Supports research and analysis-ready outputs.",
        "market_flagship": "Run cross-asset market research through AIsa. Use when: the user needs one flagship finance skill for equities, crypto, macro rates, watchlists, or broad market reporting. Supports stocks, crypto, screening, and macro context.",
        "market_equities": "Run equity research through AIsa. Use when: the user needs prices, filings, analyst estimates, earnings context, or stock screening rather than broad cross-asset coverage. Supports public-company analysis and equity workflows.",
        "market_prediction": "Run prediction-market probability research through AIsa. Use when: the user needs Polymarket or Kalshi odds, market sentiment, or event-contract history instead of traditional equity or crypto coverage. Supports market lookup, price history, and position views.",
        "market_crypto": "Run crypto-specific market data research through AIsa. Use when: the user needs prices, charts, contract-address lookup, exchange data, or category research rather than broad equities workflows. Supports spot prices, charts, and crypto screening.",
        "market_stock_analyst": "Run deeper US-stock thesis analysis through AIsa. Use when: the user needs financial data, news, social sentiment, and AI-assisted report generation for one or more US equities. Supports stock research, comparison, and report workflows.",
        "media": "Generate AI images or videos through AIsa. Use when: the user needs creative generation, asset drafts, or media workflows. Supports image and video generation.",
        "ai": "Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.",
        "automation": f"Use {name} for domain-specific automation. Use when: the user needs this workflow's specialized runtime behavior. Supports the packaged public workflow only.",
    }
    return templates[profile]


def domain_sections(
    skill_name: str,
    domain: str,
    zh: bool,
    profile_override: str | None = None,
) -> tuple[list[str], list[str], list[str], list[str]]:
    profile = release_profile(skill_name, domain, profile_override)
    if zh:
        mapping = {
            "twitter": (
                ["用户需要做 Twitter/X 研究、监控、发帖或互动。", "用户需要查看账号、时间线、趋势、列表、社区或 Spaces。", "用户需要在不提供密码的前提下完成授权发布。"] ,
                ["研究某个账号近期动态。", "监控热点关键词或趋势。", "完成 OAuth 授权后发帖或互动。"] ,
                ["研究马斯克最近 30 天关于 AI 的推文趋势", "搜索某个产品在 X 上的讨论反馈", "授权后发一条产品更新推文"] ,
                ["不要请求密码、Cookie 或浏览器凭据。", "不要在未确认 API 成功前声称已发布。", "公开包默认返回授权链接，而不是自动打开浏览器。"] ,
            ),
            "twitter_api": (
                ["用户需要一个旗舰 Twitter/X 技能做研究、监控、观察列表或发布。", "用户想在搜索、监控与发帖之间切换，而不更换技能。", "用户需要在不提供密码的前提下完成授权发布。"] ,
                ["研究创作者、竞品或叙事变化。", "监控关键词、账号列表或产品发布反应。", "在完成 OAuth 授权后发出一条确认过的帖子。"] ,
                ["研究 AI agent 创作者最近一周在 X 上的讨论", "跟踪竞品账号列表今天发生了什么变化", "授权后发布一条带图片的产品更新"] ,
                ["不要请求密码、Cookie 或浏览器凭据。", "不要把互动增长动作写成这个包的主职责。", "不要在未确认 API 成功前声称已发布。"] ,
            ),
            "twitter_watchlist": (
                ["用户需要用 X/Twitter 做观察列表、竞品追踪或趋势巡检。", "用户要定期查看账号、时间线、趋势、列表、社区或 Spaces。", "用户可能会在监控后执行一条经授权的跟进发布。"] ,
                ["跟踪竞品账号列表今天发生了什么变化。", "监控某个关键词、主题或产品发布反应。", "先完成观察，再决定是否经授权发帖。"] ,
                ["跟踪一组竞品账号今天的新动态", "监控某个产品发布在 X 上的趋势变化", "看完观察列表后再决定是否发一条跟进帖"] ,
                ["不要把它写成通用旗舰入口。", "不要把点赞、关注等互动动作当成这个包的主职责。", "不要在未确认 API 成功前声称已发布。"] ,
            ),
            "twitter_engagement": (
                ["用户已经知道要点赞、关注、回复或互动的目标。", "用户需要显式授权的互动工作流，而不是只做监控。", "用户需要在不提供密码的前提下完成互动或发帖。"] ,
                ["对一条已确认的推文执行点赞或关注动作。", "在研究上下文后执行回复、互动或发帖。", "把账号级互动动作串到一个经授权流程里。"] ,
                ["先研究目标账号，再点赞最近一条推文", "对一条发帖结果做跟进互动", "授权后回复或关注某个目标账号"] ,
                ["不要请求密码、Cookie 或浏览器凭据。", "不要把互动写成静默自动执行。", "不要在未确认 API 成功前声称互动已完成。"] ,
            ),
            "twitter_post_engage": (
                ["用户已经有草稿、活动、发帖目标或回复目标。", "用户需要一个发帖后继续跟进早期互动的工作流。", "用户需要在不提供密码的前提下完成经授权的发帖与轻量互动。"] ,
                ["先完成一条发帖，再跟进最早的互动动作。", "围绕某个 launch tweet 做发帖后的回复与轻量互动。", "在已有上下文下完成发帖、回复与跟进。"] ,
                ["授权后发布一条产品更新并继续跟进第一波反馈", "围绕某条 launch tweet 做发帖后回复与轻量互动", "先发帖再关注与话题相关的目标账号"] ,
                ["不要把它写成长期运营或重度互动总控台。", "不要请求密码、Cookie 或浏览器凭据。", "不要在未确认 API 成功前声称发帖或互动已完成。"] ,
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
            "search_flagship": (
                ["用户需要一个旗舰搜索技能来做实时查询、来源发现或引用型研究。", "用户想在网页检索、学术检索、Tavily 与深度研究之间切换，而不更换技能。", "用户需要从快速查询扩展到长篇研究输出。"] ,
                ["先快速检索，再扩展成带引用的答案。", "补学术或页面提取证据来强化第一轮结论。", "把短查询升级为深度研究报告。"] ,
                ["搜索最新的 AI coding agent 发布并给我最相关的来源", "找过去 18 个月多模态推理的论文与引用分析", "生成一份 browser-use agents 的深度研究报告"] ,
                ["不要把开发测试脚本当成公开功能。", "不要把多来源共识验证说成这个包的主职责。", "如果某些来源超时，要按真实情况说明。"] ,
            ),
            "search_multi_engine": (
                ["用户想用一个 API key 在多个检索面之间显式切换。", "用户需要把网页、学术、Tavily 或 Perplexity 结果并排看。", "用户更看重工具级控制，而不是一个总控式旗舰入口。"] ,
                ["先分别跑多个检索面，再决定往哪个方向深入。", "用显式工具选择对比不同 provider 的返回差异。", "把一轮多引擎查询作为更大研究任务的起点。"] ,
                ["先分别搜索 web、scholar 和 Tavily，再比较哪组结果更适合写报告", "给我一个一键多引擎搜索包来重复做竞品研究", "把几个搜索工具的结果并排整理出来"] ,
                ["不要把它写成唯一旗舰搜索入口。", "不要把跨来源置信度评分说成它的主职责。", "如果某个检索面超时，要明确说明是哪一路失败。"] ,
            ),
            "search_verification": (
                ["用户需要对同一主题做多来源交叉验证，而不是只查一个来源。", "用户需要置信度评分、共识检查或比较多个搜索面。", "用户需要一份适合进一步综合的验证型研究输出。"] ,
                ["并行检索多个来源并比较结果。", "验证某个结论是否在不同搜索面都出现。", "把多来源检索结果整理成一份带置信度的研究摘要。"] ,
                ["比较三个搜索面如何描述 browser-use agent 产品", "验证一个市场观点是否同时出现在 web、scholar 和 cited answer 结果里", "对 multi-agent IDE 做一轮带置信度评分的研究"] ,
                ["不要把它写成通用单一搜索入口。", "不要承诺未实际返回的共识结论。", "如果某些来源超时，要明确说明评分会受影响。"] ,
            ),
            "youtube_scout": (
                ["用户需要做 YouTube 选题研究、竞品追踪或 SERP 侦察。", "用户会反复查看频道、视频排名或趋势结果。", "用户想把 YouTube 当作研究面，而不是只做一次轻量查询。"] ,
                ["查看某个主题下排名靠前的视频与频道。", "巡检竞品频道最近的内容方向。", "围绕某个内容话题做趋势发现。"] ,
                ["研究 AI coding 主题下最近排名靠前的视频", "看看竞品频道这一周都在发什么内容", "做一轮 YouTube 竞品和趋势侦察"] ,
                ["不要把它写成只做简单查询的轻量入口。", "不要伪造视频标题、链接或排名变化。", "如果上游返回空结果，要明确说明。"] ,
            ),
            "youtube_lookup": (
                ["用户只需要快速查询 YouTube 视频、频道、播放列表或 locale 过滤。", "用户更需要 curl-first 的轻量调用，而不是重复研究工作流。", "任务集中在快速检索、分页或地区/语言参数。"] ,
                ["查一个关键词下的视频或频道结果。", "按地区和语言过滤一次 YouTube 查询。", "用 `sp` 参数继续翻页或缩小结果面。"] ,
                ["搜索美国市场里的 AI 新闻视频", "查一个频道名是否有对应 YouTube 结果", "给我一个可以带 locale 和分页参数的轻量 YouTube 查询"] ,
                ["不要把它写成竞品追踪或内容研究总控台。", "不要伪造过滤参数或返回字段。", "如果结果为空，要直接说明。"] ,
            ),
            "finance": (
                ["用户需要股票、加密、预测市场或投资研究数据。", "用户需要价格、筛选、估值、组合或事件分析。", "用户需要结构化金融输出用于进一步分析。"] ,
                ["查看价格走势与市场波动。", "筛选符合条件的股票或币种。", "研究组合、分红或预测市场机会。"] ,
                ["查询 NVDA 最近价格与分析师预期", "找出符合某些财务条件的股票", "查看 BTC 和 ETH 的最新市场数据"] ,
                ["不要给出虚构价格或财务数字。", "不要把示例请求当成投资建议。", "如果接口受限，要直接说明。"] ,
            ),
            "market_flagship": (
                ["用户需要一个广义市场入口来查看股票、加密和宏观利率。", "用户需要跨资产观察列表、报价、走势或筛选。", "用户想先用一个旗舰技能收集市场全景，再决定是否下钻。"] ,
                ["做一轮跨资产 watchlist 或市场快照。", "先看价格、走势和筛选，再决定是否深入研究。", "把股票、加密和宏观背景合并到一个报告里。"] ,
                ["做一个包含 NVDA、BTC 和美联储利率的市场快照", "给我一轮股票加密混合 watchlist 监控", "先筛选市场机会再决定下钻哪条资产线"] ,
                ["不要把它写成 filing-heavy 的股票研究包。", "不要把 prediction market 或 crypto 专用深度工作流写成它的主职责。", "如果某个上游端点受限，要如实说明。"] ,
            ),
            "market_equities": (
                ["用户需要股票价格之外的财报、分析师预期、SEC 文件和 earnings 上下文。", "用户要做 public-company 基本面研究或股票筛选。", "任务聚焦 equities，而不是跨资产全景。"] ,
                ["围绕一个 ticker 做价格、财报和分析师预期研究。", "先筛选，再下钻到 filings 或 segmented revenues。", "围绕 earnings 做公司层分析。"] ,
                ["研究 NVDA 的价格、财报、分析师预期和 filings", "给我一轮 public-company equity screening", "围绕某只股票做 earnings 上下文研究"] ,
                ["不要把它写成跨资产总控入口。", "不要把 crypto 或 prediction market 当成这个包的主线。", "不要把示例请求包装成投资建议。"] ,
            ),
            "market_prediction": (
                ["用户需要 Polymarket 或 Kalshi 赔率、价格历史或持仓视图。", "任务是事件合约、市场概率或预测市场情绪。", "用户需要 prediction-market 专用工作流，而不是传统股票研究。"] ,
                ["先找市场，再取 token_id 或 market_ticker 做价格查询。", "围绕某个事件合约查看历史价格和订单簿。", "查看 prediction-market 头寸或市场情绪。"] ,
                ["查美国大选相关 prediction market 的当前概率", "先找 Kalshi 市场再查价格历史", "围绕一个事件合约做概率与情绪研究"] ,
                ["不要把它写成广义股票/加密市场包。", "不要假装 market ID、token_id 或 ticker 已经知道。", "如果需要先查 markets，要明确告诉用户。"] ,
            ),
            "market_crypto": (
                ["用户需要加密货币价格、图表、交易所、分类或合约地址价格。", "任务是 crypto 专用研究，而不是股票或预测市场。", "用户要做交易所、category 或 trending 类的 crypto 查询。"] ,
                ["查询币价和图表。", "按合约地址查 token 价格。", "看交易所、分类或 trending coin。"] ,
                ["给我 BTC、ETH 的最近 30 天图表", "按合约地址查某个 token 的价格", "看看现在最热的 crypto category 和 trending coin"] ,
                ["不要把它写成 broad market 或 equity 研究总入口。", "不要把链上钱包、转账或节点 RPC 说成这个包支持。", "如果上游不支持某个 token 或 platform，要直接说明。"] ,
            ),
            "market_stock_analyst": (
                ["用户需要一条更深的美股 thesis 工作流。", "任务要把财务、新闻、社交情绪和 AI 分析拼成一份研究输出。", "用户想比较一组美国股票或生成报告。"] ,
                ["对一只美股做 thesis 分析。", "比较两只股票的基本面、情绪和叙事。", "生成一份带 AI synthesis 的美股研究报告。"] ,
                ["给我一份 NVDA 的 thesis 研究", "比较 AMD 和 NVDA 的财务与市场情绪", "把一组美国股票整理成研究报告"] ,
                ["不要把它写成 broad market data 包。", "不要把 filing-only 数据提取当成它唯一职责。", "不要把示例请求包装成投资建议。"] ,
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
        return mapping[profile]

    mapping = {
            "twitter": (
                ["The user needs Twitter/X research, monitoring, posting, or engagement workflows.", "The user wants profiles, timelines, trends, lists, communities, or Spaces.", "The user wants approved posting without sharing passwords."],
                ["Research an account or conversation thread.", "Monitor a keyword, trend, or competitor.", "Authorize and publish a post after explicit approval."],
                ["Research recent AI agent conversations on X", "Search how users are reacting to a product launch on Twitter", "Authorize and publish a short product update post"],
                ["Do not ask for passwords, cookies, or browser credentials.", "Do not claim posting succeeded until the API confirms it.", "Return authorization links instead of relying on auto-open behavior."],
            ),
            "twitter_api": (
                ["The user needs one flagship Twitter/X skill for research, monitoring, watchlists, or posting.", "The user wants to move between search, monitoring, and publish-ready workflows without switching skills.", "The user wants approved posting without sharing passwords."],
                ["Research a creator, competitor, or narrative shift.", "Monitor a keyword, watchlist, or launch reaction.", "Authorize and publish a post only after explicit approval."],
                ["Research what AI agent builders are saying on X this week", "Track what changed across a competitor watchlist today", "Authorize and publish a short product update with an image"],
                ["Do not ask for passwords, cookies, or browser credentials.", "Do not market growth actions as this package's primary lane.", "Do not claim posting succeeded until the API confirms it."],
            ),
            "twitter_watchlist": (
                ["The user needs recurring Twitter/X monitoring, watchlists, competitor sweeps, or trend scans.", "The user wants profiles, timelines, trends, lists, communities, or Spaces checked on a repeated basis.", "The user may follow the monitoring pass with an approved post, but monitoring stays primary."],
                ["Track what changed across a competitor watchlist today.", "Monitor reactions to a launch, narrative, or keyword over time.", "Review a monitoring pass before deciding whether to publish."],
                ["Track a competitor watchlist and summarize what changed today", "Monitor how X is reacting to our launch this week", "Review a trend desk before publishing a follow-up post"],
                ["Do not market this package as the flagship general-purpose Twitter lane.", "Do not treat likes, follows, or replies as the core job of this package.", "Do not claim posting succeeded until the API confirms it."],
            ),
            "twitter_engagement": (
                ["The user already knows which tweet, account, or campaign needs action.", "The user needs explicit likes, follows, replies, or other engagement workflows after review.", "The user wants approved posting and engagement without sharing passwords."],
                ["Research the target, then like or follow with explicit approval.", "Use engagement actions as follow-through after a post or campaign review.", "Combine read context, posting, and engagement in one approved workflow."],
                ["Research a target account and like its latest tweet", "Authorize a reply or follow-up action after a launch post", "Run a reply, like, or follow workflow on a confirmed target"],
                ["Do not ask for passwords, cookies, or browser credentials.", "Do not make likes, follows, replies, or uploads sound silent or automatic.", "Do not claim an engagement action succeeded until the API confirms it."],
            ),
            "twitter_post_engage": (
                ["The user already has a draft, launch tweet, campaign, or reply target.", "The user needs one workflow to publish first and then handle the earliest follow-through actions.", "The user wants approved posting and lightweight engagement without sharing passwords."],
                ["Publish a confirmed update and handle the first wave of reactions.", "Move from a draft or launch tweet into reply and follow-through actions.", "Use one workflow for post-launch context, posting, and lightweight engagement."],
                ["Authorize a product update post and handle the first follow-up actions", "Publish a launch tweet and then review or reply to early reactions", "Start from a draft and move into post-launch engagement"],
                ["Do not market this package as a long-running social-growth control tower.", "Do not ask for passwords, cookies, or browser credentials.", "Do not claim posting or engagement succeeded until the API confirms it."],
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
            "search_flagship": (
                ["The user needs one flagship search skill for live lookup, source discovery, or citation-ready research.", "The user wants to move between web search, scholar search, Tavily, and deep research without switching packages.", "The user wants a search lane that can expand from fast lookup into broader synthesis."],
                ["Search quickly, then expand into cited answers.", "Pull academic or extracted-page evidence when the first pass needs stronger support.", "Turn a short query into a deep research report."],
                ["Search the latest AI agent launches and show the most relevant sources first", "Find papers and cited analysis on multimodal reasoning from the last 18 months", "Build a deep research report on browser-use agents with sources and tradeoffs"],
                ["Do not present test-only helpers as public features.", "Do not market cross-source consensus scoring as this package's primary lane.", "If some providers time out, report that honestly."],
            ),
            "search_multi_engine": (
                ["The user wants one API key with explicit control across several search surfaces.", "The user wants web, scholar, Tavily, or Perplexity results compared side by side.", "The user values tool-level choice more than one flagship command-center entrypoint."],
                ["Run several search tools separately, then decide where to go deeper.", "Compare how different providers respond before writing or recommending.", "Use one multi-engine package as the kickoff surface for a larger research task."],
                ["Run web, scholar, and Tavily separately and compare which results are strongest", "Give me a one-key multi-engine search package for repeated competitor research", "Lay out several search-tool results side by side before we synthesize them"],
                ["Do not market this package as the flagship one-search entry point.", "Do not market confidence-scored consensus as the core job of this package.", "If one search surface times out, say which lane failed."],
            ),
            "search_verification": (
                ["The user wants the same topic checked across multiple search surfaces instead of trusting one provider.", "The user needs confidence scoring, consensus checks, or a comparison across multiple search lanes.", "The user wants synthesis-ready validation before making a recommendation."],
                ["Run parallel retrieval and compare the returned signals.", "Check whether a claim appears across multiple search surfaces.", "Turn multi-source retrieval into a confidence-scored research brief."],
                ["Compare how three search surfaces describe the latest browser-use agent products", "Verify whether a market claim appears in web, scholar, and cited answer results", "Run a confidence-scored research pass on multi-agent IDEs before writing a recommendation"],
                ["Do not market this package as the generic one-search entry point.", "Do not claim consensus that the returned results do not support.", "If some providers time out, explain how that affects the score."],
            ),
            "youtube_scout": (
                ["The user needs YouTube content discovery, competitor scouting, or repeated SERP-style research.", "The workflow will inspect rankings, channels, or trend patterns more than once.", "The user wants YouTube treated as a research surface, not just a quick lookup."],
                ["Review top-ranking videos and channels for a topic.", "Sweep a competitor channel's recent content direction.", "Use YouTube results to scout trends or content opportunities."],
                ["Research top-ranking YouTube videos on AI coding agents", "Review what a competitor channel has published this week", "Run a YouTube trend and competitor scout before planning content"],
                ["Do not market this package as a lightweight one-off lookup lane.", "Do not invent video titles, URLs, or ranking changes.", "If the upstream returns no results, say so clearly."],
            ),
            "youtube_lookup": (
                ["The user only needs fast YouTube video, channel, playlist, or locale-filtered lookup.", "The workflow values curl-first speed more than a repeated research surface.", "The request focuses on quick retrieval, pagination, or locale parameters."],
                ["Search one keyword for videos or channels.", "Filter one YouTube query by region and language.", "Continue or narrow a result set with pagination parameters."],
                ["Search US YouTube results for AI news", "Check whether a channel name resolves in YouTube search", "Give me a lightweight YouTube query with locale and pagination controls"],
                ["Do not market this package as a competitor-tracking or research desk.", "Do not fabricate missing filters or returned fields.", "If the result set is empty, say so directly."],
            ),
            "finance": (
                ["The user needs stocks, crypto, prediction market, or portfolio research.", "The user wants prices, screening, valuation, or event-driven analysis.", "The user wants structured financial output for downstream analysis."],
                ["Check price action and market movement.", "Screen assets or equities that match filters.", "Research portfolios, dividends, or market opportunities."],
                ["Query NVDA price history and analyst expectations", "Find stocks matching a screening rule", "Check BTC and ETH market data for a portfolio view"],
                ["Do not invent prices or financial metrics.", "Do not turn examples into financial advice.", "If an upstream endpoint is limited, say so directly."],
            ),
            "market_flagship": (
                ["The user needs one broad market entry point across equities, crypto, and macro rates.", "The task is watchlists, quotes, charts, screeners, or cross-asset market reporting.", "The user wants to gather the whole market picture before deciding which narrower lane to use."],
                ["Build a cross-asset watchlist or market snapshot.", "Check prices, charts, or screeners before going deeper.", "Combine stocks, crypto, and macro context into one report."],
                ["Build a market snapshot with NVDA, BTC, and Fed rates", "Run a mixed stock-and-crypto watchlist update", "Screen the market first, then decide which asset lane to investigate"],
                ["Do not market this package as a filing-heavy equity-research desk.", "Do not make prediction-market or crypto-specialist workflows sound like its main lane.", "If one upstream endpoint is limited, report that honestly."],
            ),
            "market_equities": (
                ["The user needs filings, analyst estimates, SEC context, or equity screening beyond simple quotes.", "The workflow is public-company analysis rather than a cross-asset market overview.", "The user wants an equities specialist that goes deeper than the broad `market` flagship."],
                ["Research a ticker across prices, filings, and analyst estimates.", "Screen public companies and then drill into filings or segmented revenues.", "Use earnings context to frame one company-level analysis."],
                ["Research NVDA across prices, filings, and analyst estimates", "Run a public-company equity screen before we choose candidates", "Build an earnings-context brief for one stock"],
                ["Do not market this package as the cross-asset flagship lane.", "Do not make crypto or prediction-market workflows sound central here.", "Do not turn examples into investment advice."],
            ),
            "market_prediction": (
                ["The user needs Polymarket or Kalshi odds, price history, or position views.", "The task is event contracts, market probabilities, or prediction-market sentiment.", "The workflow needs a prediction-market specialist rather than traditional equity or crypto coverage."],
                ["Find a market, then pull the right token_id or market_ticker for price lookup.", "Inspect one event contract's probability history or order flow.", "Review prediction-market positions or sentiment around an event."],
                ["Check current prediction-market odds for the US election", "Find a Kalshi market first and then pull its price history", "Research event-contract probabilities and market sentiment around one outcome"],
                ["Do not market this package as a broad stock or crypto market desk.", "Do not pretend the required market identifiers are already known.", "If the user must query markets first, say that clearly."],
            ),
            "market_crypto": (
                ["The user needs cryptocurrency prices, charts, exchange data, categories, or contract-address lookup.", "The task is crypto-specific rather than public-company or prediction-market analysis.", "The user wants a crypto specialist rather than a broad cross-asset overview."],
                ["Check coin prices and historical charts.", "Resolve a token by contract address.", "Inspect exchanges, categories, or trending-coin signals."],
                ["Pull the last 30 days of BTC and ETH charts", "Look up a token price by contract address", "Review the hottest crypto categories and trending coins right now"],
                ["Do not market this package as a broad market or equity desk.", "Do not claim wallet balances, transfers, or node-RPC behavior.", "If a token or platform is unsupported, say so directly."],
            ),
            "market_stock_analyst": (
                ["The user wants a deeper US-stock thesis workflow.", "The task combines financial data, news, social sentiment, and AI-assisted synthesis.", "The user wants report-style research on one or more US equities rather than generic market quotes."],
                ["Build a thesis on one US stock.", "Compare two equities across fundamentals, sentiment, and narrative.", "Generate a report-style stock research output with AI synthesis."],
                ["Build a thesis on NVDA", "Compare AMD and NVDA across fundamentals and market sentiment", "Generate a report-style brief on a basket of US equities"],
                ["Do not market this package as the broad market-data flagship.", "Do not reduce it to filing-only extraction work.", "Do not turn examples into investment advice."],
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
    return mapping[profile]


def build_body(
    skill_dir: Path,
    skill_name: str,
    description: str,
    domain: str,
    zh: bool,
    profile_override: str | None = None,
) -> str:
    when_to_use, workflows, example_requests, guardrails = domain_sections(
        skill_name,
        domain,
        zh,
        profile_override,
    )
    profile = release_profile(skill_name, domain, profile_override)
    quick_reference = infer_entrypoints(skill_dir)
    setup_lines = [
        "- `AISA_API_KEY` is required for AIsa-backed API access.",
        "- Use repo-relative `scripts/` paths from the shipped package.",
    ]
    if zh:
        setup_lines = [
            "- 需要 `AISA_API_KEY` 才能访问 AIsa API。",
            "- 使用公开包里的相对 `scripts/` 路径。",
        ]
    if profile in TWITTER_PROFILES:
        if zh:
            setup_lines.extend(
                [
                    "- Twitter/X 读取、OAuth 请求与经用户批准的媒体上传都使用固定的 AIsa API 端点 `https://api.aisa.one/apis/v1/twitter`。",
                    "- 只需要提供 `AISA_API_KEY`，不要使用密码、Cookie 或浏览器凭据导出。",
                ]
            )
            guardrails.append("只在用户明确附加本地文件时上传媒体，且要说明这些文件会发送到 AIsa 的 Twitter/X API 端点。")
        else:
            setup_lines.extend(
                [
                    "- Twitter/X reads, OAuth requests, and user-approved media uploads use the fixed AIsa API endpoint `https://api.aisa.one/apis/v1/twitter`.",
                    "- Provide only `AISA_API_KEY`; do not use passwords, cookies, or browser credential export.",
                ]
            )
            guardrails.append(
                "Only upload local files the user explicitly attached, and make it clear those files are sent to AIsa's Twitter/X API endpoint."
            )

    lines = [f"# {release_heading(skill_name, domain, profile_override)}", "", description]

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


def normalize_source_description(name: str, description: str, zh: bool) -> str:
    cleaned = " ".join((description or "").split())
    if cleaned:
        return cleaned
    return build_description(name, detect_domain(name, description), zh)


def clean_frontmatter(
    skill_dir: Path,
    frontmatter: dict[str, Any],
    publish_name: str,
    *,
    existing_version: str | None = None,
    mode: str = "original",
    profile_override: str | None = None,
    version_override: str | None = None,
) -> dict[str, Any]:
    canonical_name = str(frontmatter.get("name") or skill_dir.name).strip()
    name = publish_name.strip() or canonical_name
    domain = detect_domain(canonical_name, str(frontmatter.get("description") or ""))
    profile = release_profile(name, domain, profile_override)
    zh = is_zh_variant(name)
    if mode == "breakout":
        description = build_description(name, domain, zh, profile_override)
    else:
        description = normalize_source_description(name, str(frontmatter.get("description") or ""), zh)
    bins = infer_required_bins(skill_dir)
    envs = ["AISA_API_KEY"] if needs_aisa_key(skill_dir) else []
    optional_envs = infer_optional_envs(skill_dir, profile)
    version_source = version_override or frontmatter.get("version")
    version = choose_release_version(version_source, existing_version)
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
            "optionalEnv": optional_envs,
            "primaryEnv": "AISA_API_KEY" if envs else None,
            "compatibility": ["openclaw", "claude-code", "hermes"],
        },
        "openclaw": {
            "emoji": infer_emoji(domain),
            "requires": {
                "bins": bins,
                "env": envs,
            },
            "optionalEnv": optional_envs,
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


def build_skill(
    src_dir: Path,
    *,
    publish_name: str | None = None,
    mode: str = "original",
    profile_override: str | None = None,
    version_override: str | None = None,
    existing_root: Path | None = None,
    source_label: str | None = None,
) -> base.SkillAudit:
    frontmatter, source_body = base.load_frontmatter(src_dir / "SKILL.md")
    publish_name = publish_name or resolve_clawhub_slug(src_dir, frontmatter)
    out_dir = OUTPUT_ROOT / publish_name
    existing_frontmatter: dict[str, Any] = {}
    existing_skill_md = (existing_root or OUTPUT_ROOT) / publish_name / "SKILL.md"
    if existing_skill_md.exists():
        existing_frontmatter, _existing_body = base.load_frontmatter(existing_skill_md)
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    kept = base.copy_tree(src_dir, out_dir)
    cleaned_frontmatter = clean_frontmatter(
        src_dir,
        frontmatter,
        publish_name,
        existing_version=str(existing_frontmatter.get("version") or "") or None,
        mode=mode,
        profile_override=profile_override,
        version_override=version_override or None,
    )
    domain = detect_domain(publish_name, str(frontmatter.get("description") or cleaned_frontmatter["description"]))
    zh = is_zh_variant(src_dir.name)
    if mode == "breakout":
        rendered_body = build_body(
            out_dir,
            publish_name,
            cleaned_frontmatter["description"],
            domain,
            zh,
            profile_override,
        )
    else:
        rendered_body = base.rewrite_user_facing_markdown(source_body, "clawhub", publish_name)

    audit = base.SkillAudit(
        name=publish_name,
        source_path=source_label or str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=cleaned_frontmatter["description"],
    )

    base.prune_release_tree(out_dir, audit)
    base.patch_runtime_files(out_dir, audit)
    (out_dir / "SKILL.md").write_text(
        base.dump_skill(cleaned_frontmatter, rendered_body),
        encoding="utf-8",
    )
    base.write_skill_readme(out_dir, cleaned_frontmatter, "clawhub")
    if mode == "breakout":
        audit.changes.append("generated a ClawHub-only breakout SKILL.md with family-specific JTBD copy")
    else:
        audit.changes.append("kept the mother-skill body while normalizing ClawHub upload frontmatter")
    audit.changes.append("normalized frontmatter for ClawHub upload compatibility while keeping canonical metadata.aisa")
    if any(name in kept for name in ("scripts", "references")):
        audit.changes.append("copied runtime scripts and essential references only")
    return audit


def audit_source_skill_name(audit: base.SkillAudit) -> str:
    source_label = str(audit.source_path or "")
    base_label = source_label.split(" -> ", 1)[0]
    return Path(base_label).name or audit.name


def write_docs(audits: list[base.SkillAudit], variants: dict[str, list[dict[str, str]]]) -> None:
    breakout_lookup = {
        str(entry.get("slug") or "").strip(): entry
        for entries in variants.values()
        for entry in entries
        if str(entry.get("slug") or "").strip()
    }
    original_audits = [audit for audit in audits if audit.name not in breakout_lookup]
    breakout_audits = [audit for audit in audits if audit.name in breakout_lookup]

    readme = [
        "# ClawHub Release",
        "",
        "ClawHub-oriented packaged copy of all `targetSkills/` mother skills.",
        "",
        "## Principles",
        "",
        "- Keep `targetSkills/` as the mother-skill source layer.",
        "- Generate `clawhub-release/` as the upload-focused runtime layer.",
        "- Keep original ClawHub slugs separate from ClawHub-only breakout siblings declared in `targets/clawhub-breakout-variants.json`.",
        "- Keep canonical `metadata.aisa`, then duplicate the minimal `metadata.openclaw` hints only where helpful for upload compatibility.",
        "- Prefer runtime-only files, repo-local defaults, and explicit auth flows.",
        "",
        "## Directory Layout",
        "",
        "- The root stays flat because the current publish/test/live-status scripts discover `clawhub-release/*` directly.",
        "- Read `slug-groups.json` or the grouped lists below when you need the human-friendly split between original and breakout slugs.",
        "",
        f"## Original Slugs ({len(original_audits)})",
        "",
    ]
    for audit in original_audits:
        readme.append(f"- `{audit.name}` <- source `{audit_source_skill_name(audit)}`")
    readme.extend(["", f"## Breakout Slugs ({len(breakout_audits)})", ""])
    for audit in breakout_audits:
        variant = breakout_lookup[audit.name]
        profile = str(variant.get("profile") or "").strip()
        suffix = f" (`{profile}`)" if profile else ""
        readme.append(f"- `{audit.name}` <- source `{audit_source_skill_name(audit)}`{suffix}")
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    index_lines = [
        "# ClawHub Release Index",
        "",
        "## Original Slugs",
        "",
    ]
    for audit in original_audits:
        index_lines.append(f"- `{audit.name}`: {audit.description}")
    index_lines.extend(["", "## Breakout Slugs", ""])
    for audit in breakout_audits:
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

    grouped_index = {
        "original": [
            {
                "slug": audit.name,
                "source_skill": audit_source_skill_name(audit),
                "path": audit.output_path,
                "description": audit.description,
            }
            for audit in original_audits
        ],
        "breakout": [
            {
                "slug": audit.name,
                "source_skill": audit_source_skill_name(audit),
                "profile": str(breakout_lookup[audit.name].get("profile") or ""),
                "path": audit.output_path,
                "description": audit.description,
            }
            for audit in breakout_audits
        ],
    }
    (OUTPUT_ROOT / "slug-groups.json").write_text(
        json.dumps(grouped_index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    index = {
        "generated_at": "2026-04-20",
        "source": "targetSkills",
        "groups": grouped_index,
        "skills": [
            {
                "name": audit.name,
                "group": "breakout" if audit.name in breakout_lookup else "original",
                "source_skill": audit_source_skill_name(audit),
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
    previous_root = REPO_ROOT / ".tmp-clawhub-release-prev"
    shutil.rmtree(previous_root, ignore_errors=True)
    if OUTPUT_ROOT.exists():
        OUTPUT_ROOT.replace(previous_root)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    variants = load_breakout_variants()
    audits: list[base.SkillAudit] = []
    for skill_file in sorted(SOURCE_ROOT.glob("*/SKILL.md")):
        src_dir = skill_file.parent
        audits.append(build_skill(src_dir, existing_root=previous_root))
        for variant in variants.get(src_dir.name, []):
            audits.append(
                build_skill(
                    src_dir,
                    publish_name=variant["slug"],
                    mode="breakout",
                    profile_override=variant.get("profile") or None,
                    version_override=variant.get("version") or None,
                    existing_root=previous_root,
                    source_label=f"{src_dir.relative_to(REPO_ROOT)} -> {variant['slug']}",
                )
            )
    write_docs(audits, variants)
    shutil.rmtree(previous_root, ignore_errors=True)
    print(f"Built {len(audits)} ClawHub-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
