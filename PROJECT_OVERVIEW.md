# Project Overview

## 0. AI Working Rule

Any AI working in this repository should:

1. Read this file before doing substantial work
2. Treat this file as the high-level map of the project
3. Update this file before finishing if the project structure, outputs, workflow, or current status changed
4. Review the previous task first, and check whether any unfinished issue or obvious optimization should be handled before starting the new task
5. Assume repo-working permission is already granted unless the user explicitly narrows it, then make the best plan and execute it
6. When upstream changes are large, treat `AIsa-team/agent-skills` as the authoritative source first, then reshape into mother skills and platform release layers here
7. Do not use the local `D:\workplace\agent-skills` checkout as this repo's automation source; it is reserved for manual company-skill authoring and upload work
8. Because GitHub Actions may commit directly to `main`, pull the latest remote changes before starting edits and reconcile workflow-generated commits first

## 1. 项目一句话目的

这个仓库是一个 **AIsa Skills 迁移与发布工作台**。  
它的目标不是直接作为正式发布仓库长期维护，而是用于：

- 收集已有的 OpenClaw / ClawPub skill 包
- 分析多平台 skill 规范
- 产出跨平台母版 skill
- 再进一步产出适合 ClawHub 上传的保守发布变体
- 再进一步产出适合 ClawHub plugin catalog 的 native-first plugin 发布变体
- 再进一步产出适合 Claude / skills.sh / GitHub 分发的保守发布变体
- 再进一步产出适合 Agent Skills / agentskills.so 生态分发的标准公开变体
- 再进一步产出适合 agentskill.sh 目录导入的标准公开变体
- 再进一步产出适合 Hermes Hub / GitHub / tap 分发的保守发布变体
- 沉淀一套让人类和 AI 都能快速复用的迁移、包装、发布方法

正式发布目标仓库不是这里，而是：

- `https://github.com/AIsa-team/agent-skills`
- 分支：`main`

当前工作区里的外部发布仓库包括：

- `D:\workplace\agent-skills`
  - 承接 `targetSkills/` 的正式发布副本
  - 默认推送到 `AIsa-team/agent-skills` 的 `main` 分支
  - 仅作为发布目标与人工工作区，不作为本仓库自动化同步输入源
- `D:\workplace\agent-skills-own`
  - 承接 `agentskill-sh-release/` 的 GitHub 导入层副本
- `D:\workplace\agent-skills-so`
  - 承接 `agentskills-so-release/` 的公开分发层副本
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

- 当上游改动较大时，先以 `AIsa-team/agent-skills` 为准做能力与结构对齐
- 对已存在于 `AIsa-team/agent-skills@main` 的 skill，默认先以该上游版本为运行时基线，再做本仓库的母版/发布层收敛
- 以 `AgentSkills` 规范为母版
- 对比 `OpenClaw / ClawHub`、`Hermes`、`Claude Code`
- 生成统一的 `SKILL.md` 骨架、目录结构和发布索引

### C. 作为 ClawHub 发布预处理层

- 保留跨平台母版在 `targetSkills/`
- 生成更保守的 ClawHub 上传变体在 `clawhub-release/`
- 生成可直接走 `clawhub package publish` 的 native-first plugin 包在 `clawhub-plugin-release/`
- 收敛 frontmatter
- 收敛高敏感文案和本地副作用入口
- 支持在发布后回查 ClawHub 详情页的 `VirusTotal`、`OpenClaw verdict` 与 `Suspicious` 原因
- 支持把 live scan 状态写回 `targets/clawhub-publish-state.json` 并输出独立状态报告

### D. 作为 Agent Skills 标准公开层

- 从 `targetSkills/` 生成更标准、更中立的公开层 `agentskills-so-release/`
- 面向 `agentskills.so`、`agentskill.sh`、GitHub 公开仓库与手工 ZIP 导入
- 把母版中的平台私有嵌套元数据收敛成更扁平的公开 frontmatter

### E. 作为 agentskill.sh 导入层

- 从 `targetSkills/` 生成单独的 `agentskill-sh-release/`
- 维持 root-level skill 目录，以适配 agentskill.sh 的 GitHub 仓库扫描与 `Analyze & Import`
- 保持与 `agentskills-so-release/` 共源但文档与发布说明独立

### F. 作为技能包装方法库

- 提供迁移手册
- 提供平台差异对照表
- 提供索引与发布说明
- 提供 Claude 市场结构分析与发布预处理层
- 提供 Hermes 市场结构分析与发布预处理层
- 提供 3 个面向 ClawHub 的辅助 skill：
  - `clawhub-skill-optimizer`
  - `clawhub-security-auditor`
  - `clawhub-plugin-packager`

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
- `targets/targetskills-agentskills-compliance-audit-2026-04-20.md`
  - `targetSkills/` 面向 `agentskills.io` 母版规范的审查与修复结果
- `targets/clawhub-plugin-structure-and-upload-plan-2026-04-20.md`
  - ClawHub plugin catalog 的 native-first / bundle-compatible 双格式结构、发布路径与爆款策略
- `targets/agentskills-so-structure-and-upload-plan-2026-04-20.md`
  - `agentskills.so` / `agentskill.sh` 当前观察、标准公开层设计与发布顺序
- `targets/current-context-compression-2026-04-20.md`
  - 当前阶段核心结论压缩版，方便后续快速接续
- `targets/project-capability-internalization-2026-04-20.md`
  - 把近期对话中形成的方法、脚本和流程沉淀为本项目能力
- `targets/chat-history-daily-summary-2026-04-20.md`
  - 近期工作按日总结与阶段性成果汇总
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
- `targets/claude-hermes-inclusion-and-install-checks-2026-04-21.md`
  - Claude standalone / Claude marketplace / Hermes tap / Hermes publish 的收录判断、可安装验证命令与当前状态快照
- `targets/repo-runbook-and-script-reference.md`
  - 仓库执行流、脚本用途、参数与常用命令的统一参考
- `targets/clawhub-resume-and-breakout-plan-2026-04-24.md`
  - 当前 ClawHub 续跑、版本收口、爆款改造与 skillGet 证据接入的执行计划
- `targets/aisa-api-breakout-rollout-plan-2026-04-28.md`
  - AISA API skill 的家族分层、旗舰/增长/支撑位矩阵，以及本轮 Twitter 家族爆款收口计划
- `targets/clawhub-suspicious-causes-and-fixes-2026-04-25.md`
  - 已上线 skill/plugin 的 `Suspicious` 原因、对应修改方式，以及沉淀进全局优化/打包/审计 skill 的能力摘要
- `targets/platform-layer-and-rule-split-audit-2026-04-28.md`
  - 本轮对母版污染、多平台结构差异、`.agents/skills` 规则混用、ClawHub breakout slug 并存方式的专项复核
- `targets/clawhub-account-status-2026-04-28.md`
  - 基于本轮重新 live scan 的三个 ClawHub token 发布账号状态总表、`suspicious` 汇总和版本漂移记录
- `targets/breakout-skill-plugin-registry-2026-04-28.md`
  - 记录 breakout skill/plugin 名称、对应母版、live 状态和观察到的发布账号句柄
- `targets/platform-skill-plugin-methodology.md`
  - 本项目如何使用全局优化/打包/审计 skill 来约束母版和各平台 skill/plugin
- `targets/unified-pipeline-and-github-actions.md`
  - 新增统一调度脚本与 GitHub Actions 定时执行方案
- `targets/hermes-guard-and-publish-followup-2026-04-20.md`
  - `last30days` 系列收敛、Hermes Guard 状态与后续批量发布跟踪
- `targets/hermes-fork-pr-batch-report-2026-04-20.json`
  - 当前 25 个 Hermes 缺口 skill 的远端分支批处理结果
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
- `crypto-market-data`
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
- `multi-source-search`
- `multi-search`
- `perplexity-research`
- `scholar-search`
- `smart-search`
- `tavily-extract`
- `tavily-search`
- `web-search`
- `youtube-serp`
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

新增的 ClawHub 发布辅助脚本：

- `scripts/clawhub_live_status.py`
  - 可独立扫描已发布 skill/plugin 的 ClawHub live status，提取 `VirusTotal`、`OpenClaw` 与 `Suspicious` 原因
  - 现在会把 `pending` / `unresolved` 写成显式 `scan_status`，并支持在 skill 页 URL 不稳定时传入 owner hint
- `scripts/publish_clawhub_batch.py`
  - 现在支持可选 `--post-publish-scan`，在发布或探测到远端已存在后立即做 live scan
  - 现在支持为 post-publish scan 传入 skill owner hint，并可在 Windows 侧 `py -3` 环境下直接续发

#### 3. ClawHub 发布变体

位于 `clawhub-release/`：

- 当前包含 `targetSkills/` 下全部 54 个 skill 的 ClawHub-oriented 发布副本
- 由 `scripts/build_clawhub_release.py` 自动生成

这些目录不是母版，而是：

- 专门给 ClawHub 上传准备的保守版本
- frontmatter 更扁平，并保留 canonical `metadata.aisa`
- 同时补最小 `metadata.openclaw` 兼容提示
- 支持从母版 `SKILL.md` 读取仅对 ClawHub 生效的 `clawhub-slug` 发布别名，用来绕开站内已占用 slug，而不影响 Claude / Hermes / AgentSkills 的母版命名
- 去掉部分跨平台噪音字段
- 对 OAuth 自动打开与本地副作用默认值做收敛

#### 3.0 ClawHub Plugin 发布变体

位于 `clawhub-plugin-release/`：

- 当前包含 54 个独立的 ClawHub bundle plugin 包
- 由 `scripts/build_clawhub_plugin_release.py` 自动生成

这些目录的作用：

- 把 `clawhub-release/` 中的单 skill 包装成 `.claude-plugin/plugin.json` + `package.json` + `skills/<skill>/` 的 bundle plugin
- 为每个 plugin 同时生成 root-flat zip
- 作为 `clawhub package publish` 的实际输入层

#### 3.1 Claude 发布变体

位于 `claude-release/`：

- 当前包含 `targetSkills/` 下全部 54 个 skill 的 Claude-oriented 发布副本
- 由 `scripts/build_claude_release.py` 自动生成

这些目录不是母版，而是：

- 面向 Claude Code / skills.sh / GitHub 公共分发的保守版本
- `SKILL.md` frontmatter 收敛为 Claude 更友好的字段
- 尽量移除 `__pycache__`、测试脚本、同步脚本等非运行时文件
- 对部分高风险默认行为做了收敛，例如 OAuth 浏览器自动打开、home 目录默认持久化路径

#### 3.2 Claude Plugin Marketplace 包装层

位于 `claude-marketplace/`：

- 当前包含 54 个独立 plugin 包装后的 Claude skill
- 由 `scripts/build_claude_marketplace.py` 自动生成

这些目录的作用：

- 作为 Claude Code `/plugin marketplace add` 的 Git 仓库骨架
- 为每个 skill 单独生成 `.claude-plugin/plugin.json`
- 在根部生成 `.claude-plugin/marketplace.json`
- 当前工作区里的对应外部仓库是 `D:\workplace\Aisa-One-Plugins-Claude`

#### 3.3 Hermes 发布变体

位于 `hermes-release/`：

- 当前包含 `targetSkills/` 下全部 54 个 skill 的 Hermes-oriented 发布副本
- 由 `scripts/build_hermes_release.py` 自动生成

这些目录不是母版，而是：

- 按 `communication/`、`research/`、`finance/`、`ai/`、`creative/` 等分类组织
- `SKILL.md` frontmatter 现在同时收敛到 `metadata.aisa` 和 `metadata.hermes`
- 发布层默认做 runtime-only 包装，尽量移除 `references/`、测试脚本、评估脚本和高风险命令示例
- 对常见 AISA Python 客户端做显式 `--api-key` / repo-local state 的 Hermes 安全补丁
- 历史 Hermes Guard 复扫基线为：旧 51-skill 集合达到 `51 safe`
- `last30days` / `last30days-zh` 已经从 Guard 阻塞项降为 `SAFE`
- 当前剩余阻塞不再是技能内容，而是 GitHub PR 创建权限
- 仓库内已新增批量脚本，可把缺口 skill 推成远端 `add-skill-*` 分支
- 2026-04-23 新增 3 个上游 skill 并扩充到 54-skill 集合后，需要对 Hermes 新集合重新跑一轮 Guard / 安装验证

#### 3.4 AgentSkills.so 发布变体

位于 `agentskills-so-release/`：

- 当前包含 `targetSkills/` 下全部 54 个 skill 的 Agent Skills 标准公开副本
- 由 `scripts/build_agentskills_so_release.py` 自动生成

这些目录不是母版，而是：

- 面向 `agentskills.so` / GitHub 标准技能目录的公开层
- frontmatter 收敛为更接近 `agentskills.io` 开放规范的 `name`、`description`、`license`、`compatibility`、flat `metadata`
- 默认把 `repository` 指向 `https://github.com/baofeng-tech/agent-skills-so`
- 默认把 `platforms` 收敛为 `agentskills.io,agentskills.so,github`
- 每个 skill 生成单独 README
- 每个 skill 同时生成 root-flat zip 以应对手工导入场景
- 根目录额外生成 `README.md`、`PUBLISHING.md`、`AUDIT.md`、`index.json`、`index.md`、`well-known-skills-index.json`、`LICENSE`
- 会移除标准 skill 分发层里不需要的 plugin 包装文件，例如 `package.json`、`index.ts`

#### 3.5 agentskill.sh 发布变体

位于 `agentskill-sh-release/`：

- 当前包含 `targetSkills/` 下全部 54 个 skill 的 agentskill.sh-oriented 公开副本
- 由 `scripts/build_agentskill_sh_release.py` 自动生成

这些目录不是母版，而是：

- 面向 agentskill.sh 的 GitHub repo 扫描与 `Analyze & Import`
- 保持 root-level skill 目录与扁平 frontmatter
- 默认把 `repository` 指向 `https://github.com/baofeng-tech/agent-skills`
- 默认把 `platforms` 收敛为 `agentskills.io,agentskill.sh,github`
- 每个 skill 同时生成 root-flat zip，兼容 direct URL / 手工更新路径
- 根目录额外生成 `README.md`、`PUBLISHING.md`、`AUDIT.md`、`index.json`、`index.md`、`well-known-skills-index.json`、`LICENSE`
- 会移除标准 skill 分发层里不需要的 plugin 包装文件，例如 `package.json`、`index.ts`

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
- `build_targetskills_catalog.py`
- `build_claude_release.py`
- `build_claude_marketplace.py`
- `build_clawhub_release.py`
- `build_clawhub_plugin_release.py`
- `build_hermes_release.py`
- `build_agentskills_so_release.py`
- `build_agentskill_sh_release.py`
- `batch_publish_hermes_prs.py`
- `publish-claude-release.sh`
- `publish-clawhub-release.sh`
- `publish-clawhub-plugin-release.sh`
- `publish_clawhub_batch.py`
- `publish-hermes-release.sh`
- `publish-agentskills-so-release.sh`
- `publish-agentskill-sh-release.sh`
- `unified_skill_pipeline.py`
- `one_click_distribute_all.sh`
- `test_release_layers.py`

这些脚本的作用：

- `build_targetskills_catalog.py`
  - 从 `targetSkills/` 重建 `index.json`、`index.md`、`well-known-skills-index.json`
- `build_claude_release.py`
  - 从 `targetSkills/` 生成 `claude-release/`
- `build_claude_marketplace.py`
  - 从 `claude-release/` 生成 `claude-marketplace/`
- `build_clawhub_release.py`
  - 从 `targetSkills/` 生成 `clawhub-release/`
- `build_clawhub_plugin_release.py`
  - 从 `clawhub-release/` 生成 `clawhub-plugin-release/`
- `build_hermes_release.py`
  - 从 `targetSkills/` 生成 `hermes-release/`
- `build_agentskills_so_release.py`
  - 从 `targetSkills/` 生成 `agentskills-so-release/`
- `build_agentskill_sh_release.py`
  - 从 `targetSkills/` 生成 `agentskill-sh-release/`
- `batch_publish_hermes_prs.py`
  - 对 Hermes 缺口 skill 批量补推 `add-skill-*` 远端分支，并尝试创建 PR
- `publish-targetSkills-to-agent-skills.sh`
  - 一键把 `targetSkills/` 同步到目标 Git 仓库
  - 支持通过 `PUBLISH_AGENT_SKILLS_DEST` 给 CI / self-hosted workflow 注入目标路径
- `publish-claude-release.sh`
  - 一键构建并同步 `claude-release/`（可选同时同步 `claude-marketplace/`）到外部发布仓库
  - 支持通过 `PUBLISH_CLAUDE_DEST`、`PUBLISH_CLAUDE_MARKETPLACE_DEST` 给 CI / self-hosted workflow 注入目标路径
- `publish-clawhub-release.sh`
  - 一键规范化并生成 `clawhub-release/`
- `publish-clawhub-plugin-release.sh`
  - 一键规范化、生成 `clawhub-release/`，并继续生成 `clawhub-plugin-release/`
- `publish_clawhub_batch.py`
  - 用 1-N 个 ClawHub API token 批量续传 `clawhub-release/` skill 与 `clawhub-plugin-release/plugins/` plugin
  - 支持 `example/accounts` 中 `clawhub_ApI_token3+`、错峰启动、远端版本探测、按 artifact 落盘状态、跨 rerun 记住每 token 近一小时真实 publish 次数，以及 dry-run 续跑
- `publish-hermes-release.sh`
  - 一键构建并同步 `hermes-release/` 到外部发布仓库
  - 支持通过 `PUBLISH_HERMES_DEST` 给 CI / self-hosted workflow 注入目标路径
- `publish-agentskills-so-release.sh`
  - 一键规范化、生成 `agentskills-so-release/`，并同步到外部发布仓库
  - 支持通过 `PUBLISH_AGENTSKILLS_SO_DEST` 给 CI / self-hosted workflow 注入目标路径
- `publish-agentskill-sh-release.sh`
  - 一键规范化、生成 `agentskill-sh-release/`，并同步到外部发布仓库
  - 支持通过 `PUBLISH_AGENTSKILL_SH_DEST` 给 CI / self-hosted workflow 注入目标路径
- `unified_skill_pipeline.py`
  - 统一调度“上游 diff 检测 -> 母版同步 -> catalog 重建 -> 各平台构建 -> 校验 -> 可选发布续跑”
  - 支持本地上游仓库路径、Git clone/fetch、仅变更 skill、显式 skill 列表、人工审核 hold 持续追踪、ClawHub dry-run 续接
  - 现已与 GitHub Actions 的 hosted 校验轨 + optional / auto self-hosted 真发布轨配套
- `one_click_distribute_all.sh`
  - 旧的一键全量构建脚本，保留为本地快速重建入口
- `test_release_layers.py`
  - 对 Claude / ClawHub / ClawHub plugin / Hermes / AgentSkills.so 发布层做结构校验，并对代表性 skill 做 smoke test
- 其余 `publish-*` / `import-*` 脚本
  - 用于 `targetSkills/` 与外部仓库、下载目录之间的导入导出同步

发布层常用命令：

```bash
python3 scripts/build_claude_release.py
python3 scripts/build_claude_marketplace.py
python3 scripts/build_clawhub_release.py
python3 scripts/build_clawhub_plugin_release.py
python3 scripts/build_hermes_release.py
python3 scripts/build_agentskills_so_release.py
python3 scripts/build_agentskill_sh_release.py
python3 scripts/build_targetskills_catalog.py
python3 scripts/unified_skill_pipeline.py --dry-run
python3 scripts/publish_clawhub_batch.py --targets both --dry-run
python3 scripts/test_release_layers.py
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
- ClawHub 发布构建脚本从 `targetSkills/` 生成 `clawhub-release/`
- ClawHub plugin 构建脚本从 `clawhub-release/` 生成 `clawhub-plugin-release/`，并输出每个 plugin 的 root-flat zip
- Hermes 发布构建脚本从 `targetSkills/` 生成 `hermes-release/`，并额外做 runtime-only 文档收缩、显式 API key 补丁、repo-local state 收敛
- AgentSkills.so 发布构建脚本从 `targetSkills/` 生成 `agentskills-so-release/`，并把 frontmatter 收敛为更扁平的公开层
- AgentSkills.so 发布层会补齐根目录 catalog 文件：`index.json`、`index.md`、`well-known-skills-index.json`、`LICENSE`
- agentskill.sh 发布构建脚本从 `targetSkills/` 生成 `agentskill-sh-release/`，并保持适合 GitHub 仓库扫描的根目录结构
- agentskill.sh 发布层也会补齐根目录 catalog 文件：`index.json`、`index.md`、`well-known-skills-index.json`、`LICENSE`
- 发布层测试脚本对 Claude / ClawHub / ClawHub plugin / Hermes / AgentSkills.so / agentskill.sh 目录执行结构校验，并对代表性旧三层做 smoke test
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

### `clawhub-plugin-release/`

ClawHub plugin 分发层。  
这是在 `clawhub-release/` 之上再包一层后的 bundle plugin 发布壳。

用途：

- 进入 ClawHub plugin catalog
- 使用 `clawhub package publish` 发布
- 保持 skill-first 的 bundle plugin 形态，而不是强行改写成 native code plugin
- 同时产出 root-flat zip 以便审计和归档

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

### `agentskills-so-release/`

Agent Skills 标准生态分发层。  
这是从母版再收敛一层后的 standards-first 公开副本。

用途：

- 面向 `agentskills.so`、GitHub 公开仓库
- 使用更接近开放规范的 flat frontmatter
- 为手工上传/导入保留单 skill zip
- 作为比 `claude-release/` 更中立的公开技能目录
- 根目录保留 crawler 友好的公开索引文件和 license
- 对应外部 public repo：`baofeng-tech/agent-skills-so`

### `agentskill-sh-release/`

agentskill.sh 分发层。  
这是从母版再收敛一层后的 agentskill.sh 专用公开副本。

用途：

- 面向 agentskill.sh 的 GitHub repo 导入与 direct URL 更新
- 保持一 skill 一目录的 root-level 结构
- 将平台说明明确写成 agentskill.sh 的提交与 webhook 语境
- 根目录保留 crawler 友好的公开索引文件和 license
- 对应外部 public repo：`baofeng-tech/agent-skills`

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

### `.github/`

GitHub Actions 工作流层。  
这里不是 skill 运行目录，而是仓库自动化入口。

用途：

- 承载定时或手动执行的统一调度流程
- 在 CI 环境里自动完成 upstream sync、release rebuild、smoke test、artifact 上传与自动提交

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
5. 如果目标是 ClawHub plugin 发布：
   - 先生成 `clawhub-release/`
   - 再生成 `clawhub-plugin-release/`
   - 用 `clawhub package publish` 发布 `plugins/<skill>-plugin`
6. 如果要优化搜索或审计 Suspicious：
   - 使用 `.agents/skills/clawhub-skill-optimizer`
   - 使用 `.agents/skills/clawhub-security-auditor`
7. 如果目标是 Claude plugin marketplace：
   - 先生成 `claude-release/`
   - 再生成 `claude-marketplace/`
   - 再同步到 `D:\workplace\Aisa-One-Plugins-Claude`
   - 再按 `targets/claude-hermes-inclusion-and-install-checks-2026-04-21.md` 里的 `marketplace list` / `plugin install` 做真实安装验证
8. 如果目标是 Hermes 分发：
   - 先从 `targetSkills/` 生成 `hermes-release/`
   - 再按 `targets/claude-hermes-inclusion-and-install-checks-2026-04-21.md` 里的 `tap list` / `inspect` / `install` 区分“tap 可安装”和“官方 publish 收录”
9. 如果目标是 Agent Skills 标准生态分发：
   - 如果目标是 `agentskills.so`，优先生成 `agentskills-so-release/`
   - 如果目标是 `agentskill.sh`，优先生成 `agentskill-sh-release/`
   - 如果只是沿用旧的 Claude / skills.sh / GitHub 线，仍可继续使用 `claude-release/`
   - 再使用 `scripts/test_release_layers.py` 做结构校验和 smoke test
   - 再用 Hermes Guard 复扫，优先确认哪些 skill 已达 `safe`
   - 最后同步到 `D:\workplace\Aisa-One-Skills-Hermes`
   - 若官方 `skills publish` 的 fork 链路不稳定，则改用 `scripts/batch_publish_hermes_prs.py` 先批量推远端 `add-skill-*` 分支，再用具备写权限的 GitHub 凭据补开 PR
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
- 第四批从 `D:\workplace\agent-skills` 上游工作树回灌的 skill 更新：已通过统一调度脚本并入，当前母版总数扩展到 54
- ClawHub 专用发布层：已开始，首批 4 个已生成
- Claude 发布层：已完成，54 个已生成
- Claude plugin marketplace 包装层：已完成，54 个 plugin 包装已生成
- Hermes 发布层：已完成，54 个已生成
- Hermes Guard 批量降风险：历史旧 51-skill 集合已完成一轮，新增到 54-skill 集合后需要补跑
- Claude / Hermes 发布层测试：已完成一轮结构校验与 smoke test
- 2026-04-23 新一轮 release-layer 结构校验：`claude/hermes/clawhub/clawhub-plugin/agentskills-so/agentskill-sh` 六类结构错误均为 `0`；18 个 smoke tests 中有 5 个命中上游 `NETWORK_ERROR: timed out`，当前更像外部接口波动而非目录或脚本缺失
- Claude / Hermes 发布层真实测试：已完成一轮基于真实账号、真实 Python 3.12、真实上游数据的验证
- Claude / Claude marketplace / Hermes / agent-skills 外部发布仓库同步：2026-04-22 复核时四个外部仓库均已与 `origin/main` 对齐，不再存在“领先 1 个 commit 尚未 push”的当前阻塞
- Claude marketplace 外部发布仓库同步：`Aisa-One-Plugins-Claude` 已与 `origin/main` 对齐
- Hermes 外部发布仓库同步：已完成并推到最新
- Claude marketplace 真安装验证：历史基线为本地目录源 `./claude-marketplace` 的 51/51 plugin 全部安装成功；在 2026-04-23 扩展到 54-plugin 集合后，需要对新增 3 个 plugin 重新跑安装验证
- ClawHub plugin 真发布环境：已接通，`clawhub` CLI 已登录并完成首批 7 个 plugin 真实发布
- ClawHub plugin registry 识别验证：首批已发布 plugin 已可通过 `clawhub package inspect` 查到
- ClawHub 批量续传：`scripts/publish_clawhub_batch.py` 已升级为 3+ token、版本感知 probe、错峰起跑，并会跨多次 rerun 记住每个 token 近一小时内的真实 publish 次数
- ClawHub 2026-04-23 真实发布推进：新增上线 `aisa-search`、`aisa-tavily-search`，并确认 `aisa-twitter` 已由自有账号 `bibaofeng` 持有且同版本存在；新增 plugin 上线 `aisa-search-plugin`、`aisa-tavily-search-plugin`、`prediction-market-arbitrage-plugin`、`prediction-market-arbitrage-zh-plugin`、`prediction-market-data-plugin`、`prediction-market-data-zh-plugin`、`prediction-market-plugin`、`smart-search-plugin`、`stock-analysis-plugin`
- ClawHub 当前活跃发布状态：历史发布进度仍对应旧 51-skill 基线；在 2026-04-23 扩展到 54-skill / 54-plugin 生成集后，需要按新集合重新对账待补发清单
- ClawHub 当前剩余显式阻塞：原 `perplexity-search` slug 被系统锁给 deleted / banned account；第一次改名后的 `aisa-perplexity-search` 已确认归属外部账号 `renning22`，因此母版现已改为新的 ClawHub 专用 slug `aisa-perplexity-sonar-search`，待下一轮配额窗口补发；另外少量 plugin 失败主要表现为 `fetch failed` / `package inspect` 超时，更像平台侧瞬时波动
- Claude / Hermes / ClawHub timeout 复测：上一轮结构报告里残留的 4 个超时端点已在 2026-04-22 定向复测中全部成功返回，说明它们当前更像外部接口波动，不是稳定可复现的构建缺陷
- Hermes 缺口 skill 分支级批量补推：已完成，25 个 `add-skill-*` 远端分支已存在
- Hermes 当前最后阻塞：GitHub PAT 无 PR 创建权限，不能自动补开 Pull Request
- 统一调度与自动化：已新增 `scripts/unified_skill_pipeline.py`、`scripts/build_targetskills_catalog.py` 与 `.github/workflows/unified-skill-pipeline.yml`
- `last30days` 上游跟随策略：已从 2026-04-26 起取消统一调度层的人工 hold，改为直接跟随 `AIsa-team/agent-skills@main`，保守收敛放到发布层与 suspicious 诊断 / 修复链路中处理
- GitHub Actions 真发布模式：已扩展为 hosted 同步/构建/校验 + self-hosted 下游仓库 push / ClawHub publish 双轨；当前下游 GitHub 目标已覆盖 `AIsa-team/agent-skills@main`、`baofeng-tech/agent-skills-so`、`baofeng-tech/agent-skills`、Claude、Claude marketplace、Hermes
- 触发策略已收敛：本仓库统一流水线默认采用 GitHub Actions 的 `schedule + workflow_dispatch`，不再依赖上游仓库 push 触发；当前 hosted cron 为每 4 小时一次（`21 */4 * * *`）
- GitHub Actions checkout 后置失败修复：hosted lane 已改为 `persist-credentials: false` + explicit token push，避免此前的 post-job `exit code 128`
- GitHub Actions suspicious 修复闭环：workflow dispatch 仍支持显式 LLM 精修（`run_llm_step` / `llm_apply` / `sync_repo_skills`），但默认关闭，避免把当前仅面向 ClawHub 的 breakout/diagnosis 文案误带到全平台重建；repo-local 精修 helper 现只走共享 `AISA_API_KEY` 固定端点；self-hosted 的 targeted suspicious remediation 也已收口为只重建 ClawHub 层，并要求显式传入可发布的自有 artifact key
- repo-local 精修规则拆层：本轮已把默认母版精修和 ClawHub breakout / suspicious 修复精修拆成两个 profile，避免继续把平台私有规则混入 `targetSkills/`
- GitHub Actions self-hosted 与 hosted 衔接：self-hosted lane 在准备下游发布前会先 fast-forward 到远端最新 `main`，避免 hosted lane 先行 auto-commit 后造成后续 non-fast-forward push 失败
- GitHub Actions self-hosted 凭据回退：当 `DOWNSTREAM_REPO_TOKEN` 与 ClawHub tokens 等 CI secrets 未配置时，当前 runner 会回退读取本机 `/mnt/d/workplace/agent-skills-io/example/accounts`，并优先使用公开 HTTPS clone 准备下游仓库，避免 SSH 超时卡死在发布前置阶段
- `normalize_target_skills.py` 现已保留母 skill frontmatter 的 `version` 字段，不再在规范化时把版本号吞掉；这样 `targetSkills/` 的升版现在可以稳定传递到 ClawHub / Claude / Hermes / AgentSkills 各发布层，并支撑 targeted ClawHub 续发
- ClawHub 2026-04-25 真实续发：已通过 Windows 侧 `py -3` + `clawhub` 继续完成一轮真实 skill/plugin 续发，并把 live scan 状态回写主 publish state
- ClawHub `twitter` 历史测试结论：新 ClawHub 专用 slug `aisa-twitter-research-engage-relay` 曾真实发布到 `1.0.5`；当时的扫描修复主要围绕 relay disclosure、plugin 顶层 metadata 与 summary description requirement 展开。当前公开发布面已收口，不再把 `TWITTER_RELAY_*` 当作默认对外入口
- AISA API 爆款改造进入“家族分层 + 发布层同步”阶段：已新增 `targets/aisa-api-breakout-rollout-plan-2026-04-28.md`，不再把“所有 AISA API skill 都改成同一套旗舰文案”当默认策略；当前除了 Twitter 家族拆成 `aisa-twitter-api` 旗舰位、`aisa-twitter-command-center` 监控盘、`aisa-twitter-engagement-suite` 互动盘、`aisa-twitter-post-engage` 发帖后跟进盘之外，还已继续把 Search / YouTube / Market / Finance 的核心位同步拆成 `search` 旗舰、`aisa-multi-search-engine` 多引擎盘、`multi-source-search` 验证盘、`aisa-youtube-serp-scout` 侦察盘、`aisa-youtube-search` 轻量查询盘，以及 `market` / `marketpulse` / `prediction-market` / `crypto-market-data` / `us-stock-analyst` 的分层位，并同步修正 `build_clawhub_release.py`，避免 ClawHub 发布层把兄弟 skill 再次压回同一套泛化文案
- ClawHub 2026-04-28 Twitter 续发边界：本轮已成功真实发布 `skill:aisa-twitter-post-engage@1.0.2` 与 `plugin:aisa-twitter-api-plugin@1.0.4`，并完成 live scan 回查；`plugin:aisa-twitter-command-center-plugin` 继续保持 `vt=benign/openclaw=benign`，`skill:aisa-twitter-post-engage` 与 `plugin:aisa-twitter-api-plugin` 当前仍是 `pending`，而 `plugin:aisa-twitter-engagement-suite-plugin`、`plugin:aisa-twitter-post-engage-plugin` 仍停留在外部 publisher 旧包导致的 registry metadata / trust drift suspicious；`skill:aisa-twitter-api`、`skill:aisa-twitter-command-center`、`skill:aisa-twitter-engagement-suite` 目前的直接阻塞则是 slug ownership，不是本地构建内容
- `last30days` 当前策略：不再通过 `MANUAL_REVIEW_RULES` 跳过统一同步；如果上游扩大了公开发布面，应在 release layer、诊断规则或 targeted remediation 里显式收口，而不是停留在母版同步入口
- `agentskills.so` 人工入口：已确认公开邮箱 `support@agentskills.so` 与 Discord 邀请链接
- `claudemarketplaces.com` 当前检索：2026-04-21 以 `baofeng-tech/Aisa-One-Plugins-Claude`、`Aisa-One-Skills-Claude`、`aisa-claude-marketplace` 为关键词做公开检索，暂未搜到收录页；结合站点公开说明，marketplace 仍需等待 crawler 周期，standalone skills 仍依赖 GitHub / skills.sh 分发与安装量信号
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
- 对已经推好的 `baofeng-tech:add-skill-*` 远端分支继续补开 PR
- 当前主要不是内容整改问题，而是需要具备 PR 写权限的 GitHub 凭据
- 当前 `last30days` / `last30days-zh` 已不再是 Guard 阻塞项，但仍建议长期保持“无状态研究主链”形态，避免重新膨胀回研究应用

### 优先级 1.6

继续扩大 Python 3.12 + 真实账号的运行时覆盖面：

- 视需要把更多高价值 skill 纳入 Python 3.12 真实回归

### 优先级 1.7

继续扩大 ClawHub plugin 首发矩阵并跟进站内扫描状态：

- 优先继续发布 `aisa-youtube-search-plugin`
- 优先继续发布 `aisa-youtube-serp-scout-plugin`
- 优先继续发布 `aisa-twitter-post-engage-plugin`
- 观察已发布首批 7 个 plugin 的 `Scan`、展示页与安装体验

### 优先级 1.8

推动 `agentskills.so` 收录：

- 先观察 `baofeng-tech/agent-skills-so` 是否在 crawler 周期中自然出现
- 若仍未收录，则通过 `support@agentskills.so` 与 Discord 做人工触达

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
