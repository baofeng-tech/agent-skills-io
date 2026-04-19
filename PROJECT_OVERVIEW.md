# Project Overview

## 0. AI Working Rule

Any AI working in this repository should:

1. Read this file before doing substantial work
2. Treat this file as the high-level map of the project
3. Update this file before finishing if the project structure, outputs, workflow, or current status changed

## 1. 项目一句话目的

这个仓库是一个 **AIsa Skills 迁移与发布工作台**。  
它的目标不是直接作为正式发布仓库长期维护，而是用于：

- 收集已有的 OpenClaw / ClawPub skill 包
- 分析多平台 skill 规范
- 产出跨平台母版 skill
- 再进一步产出适合 ClawHub 上传的保守发布变体
- 再进一步产出适合 Claude / skills.sh / GitHub 分发的保守发布变体
- 再进一步产出适合 Hermes Hub / GitHub / tap 分发的保守发布变体
- 沉淀一套让人类和 AI 都能快速复用的迁移、包装、发布方法

正式发布目标仓库不是这里，而是：

- `https://github.com/AIsa-team/agent-skills`
- 分支：`agentskills`

当前工作区里的外部发布仓库包括：

- `D:\workplace\agent-skills-own`
  - 承接 `targetSkills/` 的平铺母 skill 副本
- `D:\workplace\Aisa-One-Skills-Claude`
  - 承接 `claude-release/`
- `D:\workplace\Aisa-One-Plugins-Claude`
  - 承接 `claude-marketplace/`
- `D:\workplace\Aisa-One-Skills-Hermes`
  - 承接 `hermes-release/`

## 2. 这个项目现在能做什么

当前仓库已经可以支撑下面这些工作：

### A. 作为技能迁移工作台

- 从 `sources/` 中读取历史 zip 包
- 提取 skill 的 `SKILL.md`、`scripts/`、`references/`
- 重组为新的跨平台 skill 目录

### B. 作为跨平台 skill 设计工作区

- 以 `AgentSkills` 规范为母版
- 对比 `OpenClaw / ClawHub`、`Hermes`、`Claude Code`
- 生成统一的 `SKILL.md` 骨架、目录结构和发布索引

### C. 作为 ClawHub 发布预处理层

- 保留跨平台母版在 `targetSkills/`
- 生成更保守的 ClawHub 上传变体在 `clawhub-release/`
- 收敛 frontmatter
- 收敛高敏感文案和本地副作用入口

### D. 作为技能包装方法库

- 提供迁移手册
- 提供平台差异对照表
- 提供索引与发布说明
- 提供 Claude 市场结构分析与发布预处理层
- 提供 Hermes 市场结构分析与发布预处理层
- 提供 2 个面向 ClawHub 的辅助 skill：
  - `clawhub-skill-optimizer`
  - `clawhub-security-auditor`

## 3. 当前已经做了什么

### 已完成的核心产物

#### 1. 规范与策略文档

位于 `targets/` 和 `platformDesc/`：

- `targets/clawpub-to-agentskillsso-manual.md`
  - ClawPub / OpenClaw skill 向 AgentSkills.so 的迁移手册
- `targets/platform-spec-compare.md`
  - AgentSkills、OpenClaw、Hermes、Claude Code 的规范对照
- `targets/platform-reference-links.md`
  - 官方文档链接索引
- `targets/aisa-universal-skill-template.md`
  - AIsa 通用 skill 模板
- `targets/skill-modification-rules-2026-04-19.md`
  - 新增的 skill 修改硬规则，约束零依赖、`metadata.aisa`、运行时文件范围和 Hermes 发布层收敛方式
- `targets/openclaw-twitter-cross-platform-example.md`
  - 真实 skill 的跨平台改造示例
- `targets/targetSkills-test-matrix-2026-04-17.md`
  - `targetSkills/` 母版 skill 的阶段性全量测试矩阵与阻塞项记录
- `targets/targetSkills-test-summary-2026-04-17.md`
  - 面向汇报的简版测试结论与优先级摘要
- `targets/aisa-api-endpoint-failures-2026-04-17.md`
  - 本次测试中已复核的 AISA 上游失效接口与状态码清单
- `targets/claude-market-structure-and-upload-plan-2026-04-17.md`
  - Claude Market / Claude Code / skills.sh 当前结构、搜索优化和低风险发布方案
- `targets/hermes-market-structure-and-upload-plan-2026-04-17.md`
  - Hermes Agent 当前 skill 规范、分类结构、搜索优化和低风险发布方案
- `targets/release-layer-test-report-2026-04-17.json`
  - Claude / Hermes 发布层的结构校验与 smoke test 结果
- `targets/release-layer-real-test-report-2026-04-17.md`
  - 使用真实账号、真实 AISA 数据、真实 Python 3.12 环境的发布层测试报告
- `targets/release-generation-rules-and-runbook-2026-04-17.md`
  - Claude / Claude marketplace / Hermes 三类发布层的生成规则与执行顺序
- `targets/release-accounts-and-environment-reference-2026-04-17.md`
  - 说明账号、环境路径、凭据入口统一从 `example/accounts` 查找
- `targets/claude-and-hermes-upload-guide-2026-04-17.md`
  - Claude 与 Hermes 的详细上传 / 发布步骤
- `platformDesc/Skills Platform平台.md`
  - 平台研究草稿
- `platformDesc/AIsa Skills 如何跨平台兼容.md`
  - 跨平台兼容思路草稿

#### 2. 跨平台母版技能

位于 `targetSkills/`：

- `aisa-twitter-command-center`
- `aisa-twitter-api`
- `aisa-twitter-post-engage`
- `aisa-twitter-engagement-suite`
- `x-intelligence-automation`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`
- `market`
- `marketpulse`
- `media-gen`
- `openclaw-media-gen`
- `perplexity-search`
- `aisa-tavily`
- `llm-router`
- `aisa-provider`
- `cn-llm`
- `last30days`
- `last30days-zh`
- `openclaw-search`
- `openclaw-twitter`
- `openclaw-twitter-post-engage`
- `twitter-command-center-search-post`
- `twitter-command-center-search-post-interact`
- `openclaw-youtube`
- `youtube-search`
- `openclaw-aisa-youtube-aisa`
- `us-stock-analyst`
- `prediction-market`
- `prediction-market-data`
- `prediction-market-arbitrage`
- `prediction-market-arbitrage-api`
- `prediction-market-data-zh`
- `prediction-market-arbitrage-zh`
- `search`
- `twitter`
- `youtube`
- `twitter-autopilot`
- `aisa-multi-search-engine`
- `multi-search`
- `perplexity-research`
- `scholar-search`
- `smart-search`
- `tavily-extract`
- `tavily-search`
- `web-search`
- `stock-analysis`
- `stock-dividend`
- `stock-hot`
- `stock-portfolio`
- `stock-rumors`
- `stock-watchlist`

这些 skill 的特点：

- 保留原始运行脚本
- 使用相对路径
- 面向 GitHub / AgentSkills / Hermes / Claude Code 的母版结构
- 已经配好 README、SKILL、索引文件

#### 3. ClawHub 发布变体

位于 `clawhub-release/`：

- `aisa-twitter-command-center`
- `aisa-twitter-post-engage`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`

这些目录不是母版，而是：

- 专门给 ClawHub 上传准备的保守版本
- frontmatter 更扁平
- `metadata` 收敛到 `metadata.openclaw`
- 去掉部分跨平台字段
- Twitter 变体中已去掉本地浏览器自动打开入口

#### 3.1 Claude 发布变体

位于 `claude-release/`：

- 当前包含 `targetSkills/` 下全部 51 个 skill 的 Claude-oriented 发布副本
- 由 `scripts/build_claude_release.py` 自动生成

这些目录不是母版，而是：

- 面向 Claude Code / skills.sh / GitHub 公共分发的保守版本
- `SKILL.md` frontmatter 收敛为 Claude 更友好的字段
- 尽量移除 `__pycache__`、测试脚本、同步脚本等非运行时文件
- 对部分高风险默认行为做了收敛，例如 OAuth 浏览器自动打开、home 目录默认持久化路径

#### 3.2 Claude Plugin Marketplace 包装层

位于 `claude-marketplace/`：

- 当前包含 51 个独立 plugin 包装后的 Claude skill
- 由 `scripts/build_claude_marketplace.py` 自动生成

这些目录的作用：

- 作为 Claude Code `/plugin marketplace add` 的 Git 仓库骨架
- 为每个 skill 单独生成 `.claude-plugin/plugin.json`
- 在根部生成 `.claude-plugin/marketplace.json`
- 当前工作区里的对应外部仓库是 `D:\workplace\Aisa-One-Plugins-Claude`

#### 3.3 Hermes 发布变体

位于 `hermes-release/`：

- 当前包含 `targetSkills/` 下全部 51 个 skill 的 Hermes-oriented 发布副本
- 由 `scripts/build_hermes_release.py` 自动生成

这些目录不是母版，而是：

- 按 `communication/`、`research/`、`finance/`、`ai/`、`creative/` 等分类组织
- `SKILL.md` frontmatter 现在同时收敛到 `metadata.aisa` 和 `metadata.hermes`
- 发布层默认做 runtime-only 包装，尽量移除 `references/`、测试脚本、评估脚本和高风险命令示例
- 对常见 AISA Python 客户端做显式 `--api-key` / repo-local state 的 Hermes 安全补丁
- 当前 Hermes 官方复扫结果为：51 个 `safe`
- `last30days` / `last30days-zh` 已经从 Guard 阻塞项降为 `SAFE`
- 当前剩余阻塞不再是技能内容，而是 Hermes CLI 侧缺少 GitHub API 凭证（`GITHUB_TOKEN` / `gh auth login`）

#### 4. 发布索引

位于 `targetSkills/`：

- `index.md`
- `index.json`
- `well-known-skills-index.json`
- `PUBLISHING.md`

这些文件的作用：

- 面向正式仓库 `AIsa-team/agent-skills/tree/agentskills`
- 说明 skill 列表、发布顺序、索引方式、well-known 方向

#### 4.1 发布辅助脚本

位于 `scripts/`：

- `publish-targetSkills-to-agent-skills.ps1`
- `publish-targetSkills-to-agent-skills.sh`
- `import-agent-skills-own-to-targetSkills.ps1`
- `import-agent-skills-own-to-targetSkills.sh`
- `import-clawhub-downloads-to-targetSkills.ps1`
- `import-clawhub-downloads-to-targetSkills.sh`
- `import-clawhub-downloads-to-targetSkills.py`
- `import-github-downloads-to-targetSkills.ps1`
- `import-github-downloads-to-targetSkills.sh`
- `import-github-downloads-to-targetSkills.py`
- `build_claude_release.py`
- `build_claude_marketplace.py`
- `build_hermes_release.py`
- `publish-claude-release.sh`
- `publish-hermes-release.sh`
- `test_release_layers.py`

这些脚本的作用：

- `build_claude_release.py`
  - 从 `targetSkills/` 生成 `claude-release/`
- `build_claude_marketplace.py`
  - 从 `claude-release/` 生成 `claude-marketplace/`
- `build_hermes_release.py`
  - 从 `targetSkills/` 生成 `hermes-release/`
- `publish-claude-release.sh`
  - 一键构建并同步 `claude-release/`（可选同时同步 `claude-marketplace/`）到外部发布仓库
- `publish-hermes-release.sh`
  - 一键构建并同步 `hermes-release/` 到外部发布仓库
- `test_release_layers.py`
  - 对 Claude / Hermes 发布层做结构校验与 smoke test
- 其余 `publish-*` / `import-*` 脚本
  - 用于 `targetSkills/` 与外部仓库、下载目录之间的导入导出同步

发布层常用命令：

```bash
python3 scripts/build_claude_release.py
python3 scripts/build_claude_marketplace.py
python3 scripts/build_hermes_release.py
PYTHON_EXE=/usr/local/python3.12/bin/python3.12 python3 scripts/test_release_layers.py
```

- 将 `targetSkills/` 下的内容同步到相邻的正式仓库目录 `../agent-skills/`
- 保留目标仓库中的其它无关文件
- 只替换同名 skill 目录和根层索引文件
- 默认排除 `PUBLISHING.md`
- 支持从相邻的 `../agent-skills-own/` 导入 skill 到 `targetSkills/`
- 导入脚本默认只补充缺失 skill，避免覆盖本仓库已改造的母版目录
- 支持从相邻的 `../skillGet/public/downloads/clawHub/` 递归导入 zip 包到 `targetSkills/`
- ClawHub 导入脚本按“压缩包名”或 `SKILL.md` 中的 `name` 是否重名来去重，并保留原有功能脚本不变
- 支持从相邻的 `../skillGet/public/downloads/github/` 递归导入 `.tar.gz`、`.tgz`、`.zip` skill 包到 `targetSkills/`
- GitHub 导入脚本按“源目录名（归档根目录名）”和 `SKILL.md` 中的 `name` 两个维度去重，只导入未做过的 skill
- Claude 发布构建脚本从 `targetSkills/` 生成 `claude-release/`，并同时输出 `README.md`、`index.json`、`AUDIT.md`
- Claude marketplace 构建脚本从 `claude-release/` 生成 `claude-marketplace/`
- Hermes 发布构建脚本从 `targetSkills/` 生成 `hermes-release/`，并额外做 runtime-only 文档收缩、显式 API key 补丁、repo-local state 收敛
- 发布层测试脚本对 Claude / Hermes 目录执行结构校验与代表性 smoke test
- 发布层真实测试现在明确支持读取 `example/accounts` 中的账号与 Python 3.12 路径

#### 5. ClawHub 辅助技能

位于 `.agents/skills/`：

- `clawhub-skill-optimizer`
  - 负责搜索优化、frontmatter 优化、双模式输出
  - 现在已经明确区分：
    - `cross-platform mode`
    - `clawhub publish mode`
- `clawhub-security-auditor`
  - 负责 Suspicious 风险分析
  - 现在已经支持：
    - `blocker`
    - `warning`
    - `note`
    - `ready to upload / uploadable with low residual risk / uploadable with residual risk / not ready`
- `clawhub-plugin-packager`
  - 用于 plugin 方向的打包与校验

## 4. 仓库结构怎么理解

### `sources/`

输入层。  
这里放的是历史 skill zip 包，是“原始资产”。

你可以把它理解成：

- 原材料仓
- 待迁移、待清洗的历史技能包来源

### `targetSkills/`

跨平台母版输出层。  
这里放的是已经整理成新结构的 skill，是之后要复制到正式仓库 `AIsa-team/agent-skills` 的主要候选内容。

用途：

- 作为正式 skill 仓库的候选源
- 作为跨平台主版本
- 作为 GitHub / AgentSkills / Hermes / Claude Code 的基础版本

### `clawhub-release/`

ClawHub 专用发布层。  
这是从母版再往前收敛一层后的发布变体。

用途：

- 减少 Suspicious 风险
- 减少 parser / frontmatter 兼容风险

### `claude-release/`

Claude / skills.sh / GitHub 分发层。  
这是从母版再收敛一层后的 Claude-oriented 发布副本。

用途：

- 提高 `SKILL.md` 在 Claude 生态中的可读性与可触发性
- 作为后续单独公开 GitHub 仓库的候选源
- 作为 `claudemarketplaces.com` / `skills.sh` 方向的预发布层
- 降低非运行时文件和本地副作用默认值带来的信任风险
- 作为 ClawHub 上传候选包

### `claude-marketplace/`

Claude plugin marketplace 包装层。  
这是在 `claude-release/` 之上再包一层、面向 Claude Code plugin marketplace 的分发壳。

用途：

- 支持 `/plugin marketplace add`
- 为每个 skill 生成独立 plugin 目录
- 在一个仓库里集中分发多 skill plugin

### `hermes-release/`

Hermes / GitHub / tap 分发层。  
这是从母版再收敛一层后的 Hermes-oriented 发布副本。

用途：

- 按 Hermes 习惯使用分类目录组织 skills
- 提高 `SKILL.md` 在 Hermes 生态中的可发现性
- 为后续 GitHub 安装、tap、optional-skills 候选 PR 做准备
- 降低非运行时文件和本地副作用默认值带来的信任风险

### `targets/`

方法论与说明文档层。  
这里不是 skill 运行目录，而是沉淀出来的：

- 规范研究
- 模板
- 教程
- 对照表
- 改造示例

用途：

- 给人看
- 给 AI 看
- 给后续批量迁移复用

### `platformDesc/`

研究草稿层。  
这里保存的是面向平台兼容、平台生态的研究记录。

用途：

- 保存分析过程
- 为正式手册提供来源和上下文

### `.agents/skills/`

AI 工作辅助层。  
这里不是业务 skill 本身，而是“帮助 AI 做 skill 优化/审计/打包”的辅助 skill。

用途：

- 让 AI 在这个项目里更稳定地分析、包装、审计 AIsa skills

### `scripts/`

发布辅助脚本层。  
这里放的是工作台到正式仓库的复制/同步脚本。

用途：

- 将 `targetSkills/` 发布到相邻的 `../agent-skills/`
- 降低手工复制时误删其它仓库文件的风险

### `examp/`

参考示例层。  
这里目前主要放一个由 Claude 产出的示例版本，用来对照好的 agentskills 风格。

用途：

- 参考，不是当前主输出目录

### `example/`

账号与环境入口层。  
这里当前最重要的是 `example/accounts`。

用途：

- 查找真实测试用的 AISA key
- 查找 X/Twitter 测试账号
- 查找 Python 3.12 路径
- 作为发布层真实测试的统一凭据入口

### `src/`

当前基本空置。  
不是这个项目的主工作目录，可以视为预留目录。

## 5. 当前推荐工作流

如果后续由其他 AI 或新账号接手，建议按这个流程工作：

1. 先读 `PROJECT_OVERVIEW.md`
2. 再读：
   - `targets/clawpub-to-agentskillsso-manual.md`
   - `targets/platform-spec-compare.md`
   - `targetSkills/PUBLISHING.md`
3. 如果要继续做 skill 迁移：
   - 从 `sources/` 找原始 zip
   - 先整理到 `targetSkills/`
   - 如果来源是相邻仓库 `../agent-skills-own/`，优先使用 `scripts/import-agent-skills-own-to-targetSkills.ps1` 或 `.sh`
   - 如果来源是相邻目录 `../skillGet/public/downloads/clawHub/`，优先使用 `scripts/import-clawhub-downloads-to-targetSkills.py` 或对应的 `.ps1` / `.sh`
4. 如果目标是 ClawHub 上传：
   - 优先从 `clawhub-release/` 继续收敛
   - 不要直接拿 `targetSkills/` 原样上传
5. 如果要优化搜索或审计 Suspicious：
   - 使用 `.agents/skills/clawhub-skill-optimizer`
   - 使用 `.agents/skills/clawhub-security-auditor`
6. 如果目标是 Claude plugin marketplace：
   - 先生成 `claude-release/`
   - 再生成 `claude-marketplace/`
   - 再同步到 `D:\workplace\Aisa-One-Plugins-Claude`
7. 如果目标是 Hermes 分发：
   - 先从 `targetSkills/` 生成 `hermes-release/`
   - 再使用 `scripts/test_release_layers.py` 做结构校验和 smoke test
   - 再用 Hermes Guard 复扫，优先确认哪些 skill 已达 `safe`
   - 最后同步到 `D:\workplace\Aisa-One-Skills-Hermes` 并执行 `skill -> fork -> PR`
8. 如果要跑真实发布测试：
   - 先查看 `example/accounts`
   - 再查看 `targets/release-accounts-and-environment-reference-2026-04-17.md`
   - 最后查看 `targets/release-layer-real-test-report-2026-04-17.md`

## 6. 目前项目的阶段判断

这个项目现在不再是“纯研究阶段”，已经进入：

**迁移方法已建立 + 首批技能已产出 + 发布变体已开始成形**

更具体地说：

- 平台研究：已完成第一轮
- 模板设计：已完成
- 示例 skill 改造：已完成
- 第一批目标 skill 生成：已完成
- 第二批从 `agent-skills-own` 回收的通用 AIsa skills：已并入 `targetSkills/`
- 第三批从 `clawHub` 下载目录回收的未重复 skills：已并入 `targetSkills/`
- ClawHub 专用发布层：已开始，首批 4 个已生成
- Claude 发布层：已完成，51 个已生成
- Claude plugin marketplace 包装层：已完成，51 个 plugin 包装已生成
- Hermes 发布层：已完成，51 个已生成
- Hermes Guard 批量降风险：已完成一轮，51 个 skill 已进入 `safe`
- Claude / Hermes 发布层测试：已完成一轮结构校验与 smoke test
- Claude / Hermes 发布层真实测试：已完成一轮基于真实账号、真实 Python 3.12、真实上游数据的验证
- Claude 外部发布仓库同步：已完成并推到最新
- Claude marketplace 外部发布仓库同步：已完成并推到最新
- Hermes 外部发布仓库同步：已完成并推到最新
- Claude marketplace 真安装验证：`last30days` / `last30days-zh` 已从 `aisa-claude-marketplace` 安装成功
- 中文镜像 / EN-ZH 双版本发布：尚未系统化完成

## 7. 现在最重要的下一步

如果继续推进，这个项目最有价值的下一步是：

### 优先级 1

把 `targetSkills/` 中主推 skill 同步到正式仓库：

- `aisa-twitter-command-center`
- `aisa-twitter-post-engage`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`

### 优先级 1.5

把 `claude-release/`、`claude-marketplace/`、`hermes-release/` 分别推到对应公开仓库或分支，形成真正可安装的外部入口

当前 Hermes 方向已经进一步细化为：

- 保持 `hermes-release/` 的 Guard 结果维持在 `safe`
- 对 51 个 `safe` skill 继续执行 Hermes `skills publish` 的 `fork -> PR` 批处理
- 当前 `last30days` / `last30days-zh` 已不再是 Guard 阻塞项，但仍建议长期保持“无状态研究主链”形态，避免重新膨胀回研究应用

### 优先级 1.6

继续扩大 Python 3.12 + 真实账号的运行时覆盖面：

- 视需要把更多高价值 skill 纳入 Python 3.12 真实回归

### 优先级 2

对 `clawhub-release/` 做逐个上传前审计：

- frontmatter 兼容性
- 高敏关键词
- 非运行时文件
- 本地副作用能力
- `metadata.openclaw` 一致性

### 优先级 3

补 EN / ZH 双版本策略：

- 特别是针对 `clawhub.ai` 和 `cn.clawhub-mirror.com`
- 目前这部分主要停留在规则层，尚未批量生成真实 ZH skill 目录

## 8. 给 AI 的一句话理解

如果你是第一次接手这个仓库，可以把它理解成：

**这是一个把历史 OpenClaw / ClawPub 技能资产，重构成 AIsa 官方跨平台 skill 仓库和 ClawHub 上传变体的中间工厂。**
