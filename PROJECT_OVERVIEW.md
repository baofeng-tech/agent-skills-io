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
- 沉淀一套让人类和 AI 都能快速复用的迁移、包装、发布方法

正式发布目标仓库不是这里，而是：

- `https://github.com/AIsa-team/agent-skills`
- 分支：`agentskills`

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
- `targets/openclaw-twitter-cross-platform-example.md`
  - 真实 skill 的跨平台改造示例
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

#### 4. 发布索引

位于 `targetSkills/`：

- `index.md`
- `index.json`
- `well-known-skills-index.json`
- `PUBLISHING.md`

这些文件的作用：

- 面向正式仓库 `AIsa-team/agent-skills/tree/agentskills`
- 说明 skill 列表、发布顺序、索引方式、well-known 方向

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
- 作为 ClawHub 上传候选包

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

### `examp/`

参考示例层。  
这里目前主要放一个由 Claude 产出的示例版本，用来对照好的 agentskills 风格。

用途：

- 参考，不是当前主输出目录

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
4. 如果目标是 ClawHub 上传：
   - 优先从 `clawhub-release/` 继续收敛
   - 不要直接拿 `targetSkills/` 原样上传
5. 如果要优化搜索或审计 Suspicious：
   - 使用 `.agents/skills/clawhub-skill-optimizer`
   - 使用 `.agents/skills/clawhub-security-auditor`

## 6. 目前项目的阶段判断

这个项目现在不再是“纯研究阶段”，已经进入：

**迁移方法已建立 + 首批技能已产出 + 发布变体已开始成形**

更具体地说：

- 平台研究：已完成第一轮
- 模板设计：已完成
- 示例 skill 改造：已完成
- 第一批目标 skill 生成：已完成
- ClawHub 专用发布层：已开始，首批 4 个已生成
- 正式仓库同步：尚未在本仓库内执行
- 中文镜像 / EN-ZH 双版本发布：尚未系统化完成

## 7. 现在最重要的下一步

如果继续推进，这个项目最有价值的下一步是：

### 优先级 1

把 `targetSkills/` 中主推 skill 同步到正式仓库：

- `aisa-twitter-command-center`
- `aisa-twitter-post-engage`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`

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
