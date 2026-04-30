# ClawPub Skill 迁移到 AgentSkills.so 手册

## 1. 结论先说

`agentskills.so` 展示和分发的底层标准不是 ClawPub/OpenClaw 私有格式，而是 `agentskills.io` 的 Agent Skills 开放规范。  
这意味着：**大多数 ClawPub skill 不需要重写业务逻辑，只需要把包结构和 `SKILL.md` frontmatter 调整到标准格式，就可以迁移到 AgentSkills.so。**

从本仓库现有 OpenClaw 发布包来看，典型结构已经很接近标准格式：

```text
skill-name/
├── SKILL.md
├── scripts/
└── references/
```

比如 `sources/0xjordansg-yolo--openclaw-twitter.zip` 和 `sources/aisadocs--openclaw-twitter-post-engage.zip` 都是这类结构，说明你们原始资产本身已经具备较高迁移兼容性。

## 2. AgentSkills.so / Agent Skills 的官方规范要点

根据 `agentskills.io/specification`，一个合法 skill 至少需要一个目录和一个 `SKILL.md`：

```text
skill-name/
├── SKILL.md          # 必需
├── scripts/          # 可选
├── references/       # 可选
├── assets/           # 可选
└── ...
```

`SKILL.md` 必须由两部分组成：

1. YAML frontmatter
2. Markdown 正文

### 2.1 必填字段

- `name`
  - 必填
  - 1 到 64 个字符
  - 只能用小写字母、数字、连字符
  - 不能以 `-` 开头或结尾
  - 不能有连续 `--`
  - 必须与父目录名完全一致
- `description`
  - 必填
  - 1 到 1024 个字符
  - 需要同时说明“做什么”和“什么时候用”
  - 应包含可触发 skill 的关键词

### 2.2 可选字段

- `license`
- `compatibility`
  - 最多 500 字
  - 用于说明环境依赖、网络需求、目标平台
- `metadata`
  - 任意键值对
  - 适合放作者、版本、标签、平台扩展字段
- `allowed-tools`
  - 实验性字段
  - 用空格分隔列出预批准工具

### 2.3 结构建议

- `SKILL.md` 建议控制在 500 行以内
- 主体建议低于 5000 tokens
- 重内容放到 `references/`
- 脚本放到 `scripts/`
- 模板、图片、静态资源放到 `assets/`

这套设计的核心是 **progressive disclosure**：

1. 启动时只加载 `name + description`
2. 命中后再读取完整 `SKILL.md`
3. 有需要时再读取 `scripts/`、`references/`、`assets/`

## 3. ClawPub / OpenClaw Skill 与 Agent Skills 的关系

从你仓库里的现有包看，ClawPub/OpenClaw skill 实际上已经是“Agent Skills 兼容格式 + 平台扩展字段”的模式。

例如本地样本 `openclaw-twitter` 的 frontmatter：

```yaml
---
name: openclaw-twitter
description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords. Supports read APIs, authorization links, and media-aware posting.
homepage: https://openclaw.ai
author: 0xjordansg-yolo
user-invocable: true
requires:
  bins:
    - python3
  env:
    - AISA_API_KEY
metadata:
  openclaw:
    emoji: "🐦"
    requires:
      bins:
        - python3
      env:
        - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    files:
      - "scripts/*"
      - "references/*"
---
```

这里可以分成两类：

- **标准层**
  - `name`
  - `description`
  - `scripts/`
  - `references/`
- **平台私有扩展层**
  - `homepage`
  - `author`
  - `user-invocable`
  - `requires`
  - `metadata.openclaw.*`

迁移时的关键原则是：

**保留标准层，收敛私有层，把 OpenClaw 专属字段迁到 `metadata` 或正文说明里。**

## 4. 字段映射表

下面这张表是从 ClawPub/OpenClaw skill 迁移到 AgentSkills.so 时最实用的映射规则。

| ClawPub / OpenClaw 字段 | AgentSkills.so 处理建议 | 说明 |
| --- | --- | --- |
| `name` | 保留 | 必须合法且目录同名 |
| `description` | 保留并优化 | 建议补充触发关键词 |
| `homepage` | 建议移入 `metadata.homepage` 或正文 | 非核心标准字段 |
| `author` | 建议移入 `metadata.author` | 更稳妥 |
| `user-invocable` | 删除或放入 `metadata` | 非标准字段，平台支持不稳定 |
| `requires.bins` | 写入 `compatibility`，必要时在正文 Setup 补充 | 标准字段没有 `requires` |
| `requires.env` | 写入 `compatibility`，并在 Setup 明确列出 | 比 YAML 私有字段更通用 |
| `metadata.openclaw.*` | 可保留在 `metadata`，但不要依赖它触发核心能力 | 作为兼容扩展信息 |
| `metadata.openclaw.requires` | 合并进 `compatibility` | 更符合开放规范 |
| `metadata.openclaw.files` | 删除 | Agent Skills 默认就是技能目录内文件 |
| `scripts/` | 保留 | 这是标准目录 |
| `references/` | 保留 | 这是标准目录 |
| `assets/` | 如有静态模板可新增 | 标准支持 |

## 5. 推荐迁移后的 frontmatter 模板

推荐把 OpenClaw 的私有元数据收敛成下面这种格式：

```yaml
---
name: aisa-twitter-command-center
description: Search X/Twitter profiles, tweets, trends, and posting workflows through the AISA relay. Use when the user asks for Twitter research, monitoring, content drafting, or approved posting without sharing passwords.
license: Apache-2.0
compatibility: Requires python3, AISA_API_KEY, and internet access to api.aisa.one. Designed for Agent Skills compatible clients such as AgentSkills.so, Claude-compatible skill runners, and similar tools.
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: twitter,x,social-media,automation
  openclaw:
    primaryEnv: AISA_API_KEY
    emoji: "🐦"
---
```

这个写法有几个好处：

- 核心依赖都进入标准字段，兼容性更强
- OpenClaw 扩展信息仍然保留在 `metadata.openclaw`
- AgentSkills.so 抓取时更容易识别
- 后续分发到 Hermes、Claude 生态时也更稳

## 6. 正文如何改

`SKILL.md` 正文本身没有强制模板，但推荐保持下面的结构：

```md
# Skill Title

## When to use
- ...

## When NOT to use
- ...

## Setup
~~~bash
export AISA_API_KEY="your-key"
~~~

## Quick Reference
- ...

## Common Commands
~~~bash
python3 scripts/twitter_client.py search --query "AI agents"
~~~

## Workflow
- ...

## References
- See `references/post_twitter.md`
```

迁移时建议注意 4 点：

1. 把 `{baseDir}` 改成相对路径写法  
   例如：
   - 原来：`python3 {baseDir}/scripts/twitter_client.py ...`
   - 推荐：`python3 scripts/twitter_client.py ...`

2. 不要让正文过长  
   复杂 API 参数、错误码、长表格移到 `references/`

3. 把平台审核说明放到单独小节  
   比如 relay、OAuth、数据流向、不会读取密码等

4. 不要在正文里依赖 OpenClaw 专有运行时概念  
   如 OpenClaw session cache、OpenClaw 专属 CLI 包装器、私有安装流程

## 7. 目录改造规则

如果你的 ClawPub skill 目前是“运行时发布包”，推荐整理成下面这种标准仓库结构：

```text
aisa-twitter-command-center/
├── SKILL.md
├── README.md
├── scripts/
│   ├── twitter_client.py
│   ├── twitter_oauth_client.py
│   └── twitter_engagement_client.py
├── references/
│   ├── post_twitter.md
│   └── engage_twitter.md
└── assets/
    └── optional-files
```

说明：

- `README.md` 不是规范强制，但**强烈建议保留**
- 对外市场展示时，`SKILL.md` 是机器入口，`README.md` 是人类入口
- 如果 zip 里没有 `README.md`，不会阻止 skill 被识别，但不利于 GitHub 展示和团队维护

## 8. 从你当前包出发的具体改造步骤

下面这套流程适合你们现在的 AIsa / OpenClaw skill 包。

### 第一步：解包并重命名目录

目标：

- 目录名与 `name` 完全一致
- 用业务名，不要继续用 `openclaw-` 当前缀，除非这是品牌策略的一部分

例子：

- `openclaw-twitter` → `aisa-twitter-command-center`
- `openclaw-twitter-post-engage` → `aisa-twitter-post-engage`

### 第二步：清洗 frontmatter

保留：

- `name`
- `description`
- `license`
- `compatibility`
- `metadata`

迁移：

- `author` → `metadata.author`
- `homepage` → `metadata.homepage`
- `requires.*` → `compatibility + Setup`

降级为兼容扩展：

- `metadata.openclaw.*`

删除：

- 强绑定 OpenClaw 运行时的字段
- 对公开市场没有意义的内部发布字段

### 第三步：改正文中的路径和平台措辞

重点修改：

- `OpenClaw Twitter` 这类标题，改成产品中立标题
- `optimized for publication metadata and upload safety` 这类平台发布文案，改成用户价值导向文案
- `{baseDir}` 改相对路径
- “OpenClaw preferred path” 改成 “compatible clients recommended path”

### 第四步：拆长文档

符合 Agent Skills 的最佳实践：

- 核心 instructions 留在 `SKILL.md`
- API 列表、错误处理、审核说明、OAuth 流程放进 `references/`

### 第五步：补 README

建议最少包含：

- skill 简介
- 目录结构
- 环境变量
- 本地运行方式
- 支持的平台
- 数据安全说明

### 第六步：本地校验

如果能使用官方参考库，运行：

```bash
skills-ref validate ./aisa-twitter-command-center
```

至少做人工检查：

- `name` 是否合法
- 目录名是否一致
- `description` 是否在 1024 字以内
- `compatibility` 是否在 500 字以内
- `SKILL.md` 是否可读
- `scripts/` 是否能独立运行
- `references/` 链接是否有效

## 9. 一个最小迁移示例

### 迁移前

```yaml
---
name: openclaw-twitter
description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords.
homepage: https://openclaw.ai
author: 0xjordansg-yolo
user-invocable: true
requires:
  bins:
    - python3
  env:
    - AISA_API_KEY
metadata:
  openclaw:
    emoji: "🐦"
    primaryEnv: AISA_API_KEY
---
```

### 迁移后

```yaml
---
name: aisa-twitter-command-center
description: Search X/Twitter profiles, tweets, trends, communities, and posting workflows through the AISA relay. Use when the user asks for Twitter research, monitoring, content drafting, or approved posting without sharing passwords.
license: Apache-2.0
compatibility: Requires python3, AISA_API_KEY, and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: twitter,x,automation,content
  openclaw:
    emoji: "🐦"
    primaryEnv: AISA_API_KEY
---
```

正文命令同时改成：

```bash
python3 scripts/twitter_client.py user-info --username elonmusk
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
```

## 10. 发布到 AgentSkills.so 的建议流程

`agentskills.so` 页面展示的信息通常来自 skill 本身和其源码仓库。实践上建议采用下面流程：

1. 为 skill 建立公开 GitHub 仓库，或统一放进 `AIsaONE/agent-skills`
2. 每个 skill 一个独立目录
3. 保证目录下有标准 `SKILL.md`
4. 尽量补充 `README.md`
5. 确保 license、作者、版本、主页等信息齐全
6. 如果平台支持导入 GitHub repo，就优先导入 GitHub 源
7. 如果平台要求 zip 包，再按技能目录根打包，不要多一层嵌套目录

打包前检查：

- zip 根目录下应直接出现 `SKILL.md`
- 或者 zip 根目录是合法 skill 目录，且内部有 `SKILL.md`
- 不要把 `.git`、测试缓存、私有文档、内部脚本打进去

## 11. 审核和安全风险建议

你们这类 AIsa skill 很容易在市场审核里被重点关注，尤其是涉及：

- OAuth
- 社交媒体发帖
- 代理转发 API
- 文件上传
- 外部网络访问

建议在 `SKILL.md` 或 `README.md` 明确写清：

- 需要什么环境变量
- 数据会发往哪里
- 是否通过 relay
- 是否需要用户显式授权
- 不会采集哪些敏感信息
- 不支持哪些高风险动作

比如下面这些表述会显著降低审核阻力：

- Does not require passwords or browser cookie extraction
- Requires explicit OAuth approval before write actions
- Media uploads only use user-provided local files
- All API requests are sent to `api.aisa.one`

## 12. 四个平台逐一分析

这一节基于各平台当前公开文档，对 `ClawHub/OpenClaw`、`AgentSkills`、`Hermes`、`Claude Code` 分别做结构和规范分析。

### 12.1 AgentSkills

这是最标准、最中立的一层。

官方规范明确要求：

- skill 是一个目录
- 至少包含一个 `SKILL.md`
- 可选目录包括 `scripts/`、`references/`、`assets/`
- `name` 和 `description` 是核心 frontmatter
- `license`、`compatibility`、`metadata`、`allowed-tools` 是可选字段

推荐目录：

```text
my-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

推荐写法：

- 文件引用使用相对路径
- 依赖写到 `compatibility`
- 平台扩展写到 `metadata`
- 不依赖任何私有运行时变量

这是你们跨平台 skill 的“母版格式”。

### 12.2 ClawHub / OpenClaw

OpenClaw 官方文档明确说明它使用 **AgentSkills-compatible** skill folder，但在此之上增加了一层 OpenClaw 私有能力。

OpenClaw 加载顺序：

1. `skills.load.extraDirs`
2. bundled skills
3. `~/.openclaw/skills`
4. `~/.agents/skills`
5. `<workspace>/.agents/skills`
6. `<workspace>/skills`

高优先级覆盖低优先级。

ClawHub 是 OpenClaw 的公开 registry，支持：

- 搜索
- 安装
- 更新
- 发布
- 版本化
- zip 下载

常用命令：

```bash
openclaw skills install <skill-slug>
clawhub skill publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
```

OpenClaw 的关键私有扩展：

- `metadata.openclaw.requires.*`
- `metadata.openclaw.primaryEnv`
- `metadata.openclaw.install`
- `user-invocable`
- `disable-model-invocation`
- `command-dispatch`
- `command-tool`

还有一个很重要的 OpenClaw 约定：

- 文档建议在正文里用 `{baseDir}` 引用 skill 根目录

例如：

```bash
python3 {baseDir}/scripts/twitter_client.py search --query "AI agents"
```

### 12.2.1 OpenClaw 文档中的不一致点

这里需要特别注意，因为它直接影响你们如何写“跨平台版本”。

OpenClaw 文档内部存在几处不一致：

1. `name` 命名规则不完全一致  
   一个页面写 `snake_case`，另一个页面和 AgentSkills 兼容页又明显靠近 kebab-case/开放规范。

2. frontmatter 解析能力与开放规范不完全一致  
   OpenClaw 文档提到：
   - parser 支持单行 frontmatter key
   - `metadata` 建议写成单行 JSON 对象

3. 路径写法偏向 `{baseDir}`  
   这和 AgentSkills / Hermes / Claude Code 推荐的相对路径不是一回事。

因此结论是：

**如果目标是纯 OpenClaw 运行时优化，可以保留 OpenClaw 私有写法；如果目标是一份 skill 同时兼容多个平台，必须以 AgentSkills 写法为主，只把 OpenClaw 私有能力留在 `metadata.openclaw`。**

### 12.3 Hermes

Hermes 官方文档明确说它 **compatible with the agentskills.io open standard**，而且 skill 是首选扩展方式。

Hermes 的目录组织更强分类：

```text
skills/
├── research/
│   └── arxiv/
│       ├── SKILL.md
│       └── scripts/
└── productivity/
    └── some-skill/
```

本地安装目录：

```text
~/.hermes/skills/<category>/<skill-name>/
```

Hermes 的常见 frontmatter 扩展：

- `version`
- `author`
- `license`
- `platforms`
- `required_environment_variables`
- `metadata.hermes.tags`
- `metadata.hermes.related_skills`

Hermes 比较有特色的能力：

- `platforms: [macos, linux, windows]`
- `required_environment_variables` 可以安全提示用户配置 secret
- `skills.config.*` 支持非密钥配置注入
- 内置 bundled skills 和 optional skills

Hermes 官方发布/安装方式包括：

- `hermes skills install official/<category>/<skill>`
- `hermes skills install github:<owner>/<repo>/<path>`
- `hermes skills tap add <owner>/<repo>`
- 支持 well-known endpoint `/.well-known/skills/index.json`

从官方文档看，Hermes 对开放规范的兼容是比较“正统”的。  
所以对 Hermes 来说，**AgentSkills 风格目录 + 相对路径 + 标准 frontmatter** 是最稳的。

### 12.4 Claude Code

Claude Code 同时支持两种形态：

1. standalone skills
2. plugin 内嵌 skills

#### standalone skill

位置可以在：

- `~/.claude/skills/<skill-name>/SKILL.md`
- `.claude/skills/<skill-name>/SKILL.md`
- 插件内 `<plugin>/skills/<skill-name>/SKILL.md`

Claude Code 的 skill 支持非常强的私有扩展字段：

- `when_to_use`
- `argument-hint`
- `disable-model-invocation`
- `user-invocable`
- `allowed-tools`
- `model`
- `effort`
- `context: fork`
- `agent`
- `hooks`
- `paths`
- `shell`

另外它还支持变量替换：

- `$ARGUMENTS`
- `$0`, `$1`
- `${CLAUDE_SESSION_ID}`
- `${CLAUDE_SKILL_DIR}`

其中 `${CLAUDE_SKILL_DIR}` 是 Claude Code 特别实用、但不具备跨平台通用性的路径变量。

#### plugin skill

Claude Code 要共享和分发 skills，官方推荐通过 plugin：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── hello/
        └── SKILL.md
```

最小 manifest：

```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0"
}
```

安装和分发通常通过 plugin marketplace：

```bash
claude plugin marketplace add owner/repo
/plugin install my-plugin@marketplace-name
```

### 12.4.1 Claude Code 和开放规范的关系

Claude Code 支持标准 Agent Skill 结构，但它在 `SKILL.md` frontmatter 层做了很多增强。  
所以：

- 想做最大兼容：只用 `name + description + allowed-tools + 常规 markdown`
- 想做 Claude 原生体验：再加 `when_to_use`、`argument-hint`、`context: fork`、`${CLAUDE_SKILL_DIR}` 等增强

## 13. 四个平台差异总表

| 维度 | AgentSkills | ClawHub / OpenClaw | Hermes | Claude Code |
| --- | --- | --- | --- | --- |
| 核心格式 | 开放标准 | 兼容开放标准 + 私有扩展 | 兼容开放标准 + Hermes 扩展 | 兼容开放标准 + Claude 扩展 |
| 最小入口 | `SKILL.md` | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| 推荐目录 | `scripts/` `references/` `assets/` | 同左，但常见 OpenClaw 特殊字段 | 同左，常带 category 目录 | standalone 或 plugin `skills/` |
| 路径写法 | 相对路径 | 常见 `{baseDir}` | 相对路径 | 相对路径或 `${CLAUDE_SKILL_DIR}` |
| 环境依赖声明 | `compatibility` | `metadata.openclaw.requires.*` | `required_environment_variables` / config | `allowed-tools` 与正文说明 |
| 平台扩展字段 | `metadata` | `metadata.openclaw.*` | `metadata.hermes.*` | 多个顶层 frontmatter 私有键 |
| 本地位置 | 未强制 | `<workspace>/skills`、`~/.agents/skills` 等 | `~/.hermes/skills/<category>/<name>` | `~/.claude/skills/<name>` 或 `.claude/skills/<name>` |
| 发布方式 | GitHub / well-known / 市场接入 | ClawHub | official / GitHub / tap / well-known | plugin marketplace |
| 最适合做母版吗 | 是 | 否 | 接近是 | 否 |

## 14. 给 AIsa / ClawPub 的兼容策略

针对你们这批 skill，我建议不要维护 4 份独立格式，而是做 **1 个母版 + 3 个平台薄适配层**。

### 14.1 母版

母版直接采用 AgentSkills 规范：

- 目录名使用 kebab-case
- `SKILL.md` 使用标准 frontmatter
- 命令和引用全部用相对路径
- 依赖写入 `compatibility`
- 作者、版本、标签写入 `metadata`

### 14.2 OpenClaw 适配层

只加这些：

- `metadata.openclaw.requires`
- `metadata.openclaw.primaryEnv`
- `metadata.openclaw.install`
- 必要时保留 `user-invocable`

避免：

- 把 `{baseDir}` 写死在母版里
- 把 OpenClaw 专属解析假设写死在正文里

### 14.3 Hermes 适配层

只加这些：

- `metadata.hermes.tags`
- `metadata.hermes.related_skills`
- `platforms`
- `required_environment_variables`

Hermes 适合做“几乎直接吃母版”的平台。

### 14.4 Claude Code 适配层

区分两种分发：

- 如果只是本地/项目内使用：直接作为 standalone skill
- 如果要团队分发：包装成 plugin marketplace

只在 Claude 专用版本里加：

- `when_to_use`
- `argument-hint`
- `context: fork`
- `${CLAUDE_SKILL_DIR}`

不要把这些写进通用母版。

## 15. 推荐的迁移策略

如果你们要批量把 ClawPub skill 迁到 AgentSkills.so，我建议按这个优先级执行：

1. 先统一 skill 命名规则  
   全部改为稳定的 kebab-case 品牌名

2. 再统一 frontmatter 模板  
   把 `author/homepage/requires` 全部规范收敛

3. 再统一正文结构  
   `When to use / Setup / Commands / Workflow / References`

4. 最后处理平台差异字段  
   OpenClaw 私有字段全部收口到 `metadata.openclaw`

这样做的好处是：

- 一套内容可以同时给 AgentSkills.so、Hermes、Claude 兼容客户端使用
- 降低对单一平台私有字段的依赖
- 后续维护成本明显更低

## 16. 最终建议

对你们当前这批 skill，不建议“重写一套 AgentSkills 版”。  
更好的方式是：

- 保留现有 `scripts/` 和 `references/`
- 重构 `SKILL.md` frontmatter
- 去除 OpenClaw 强耦合表述
- 补 `README.md`
- 按标准目录重新打包发布

本质上这不是“从零迁移”，而是一次 **标准化清洗 + 市场化包装**。

如果后面要真的做发布，我建议按这个顺序落地：

1. 先把 skill 母版全部统一成 AgentSkills 风格
2. 先发到 GitHub 统一仓库
3. 再做 AgentSkills / Hermes / ClawHub 分发
4. Claude Code 单独补 plugin marketplace 封装
5. 最后补 `/.well-known/skills/index.json`

---

## 参考来源

- Agent Skills 官方规范：<https://agentskills.io/specification>
- Agent Skills 客户端接入：<https://agentskills.io/client-implementation/adding-skills-support>
- Agent Skills 介绍页：<https://agentskills.io/what-are-skills>
- 技能描述优化指南：<https://agentskills.io/skill-creation/optimizing-descriptions>
- AgentSkills.so 示例页面：<https://agentskills.so/skills/bntvllnt-agent-skills-skill-builder>
- OpenClaw Skills：<https://docs.openclaw.ai/tools/skills>
- OpenClaw Creating Skills：<https://docs.openclaw.ai/tools/creating-skills>
- OpenClaw ClawHub：<https://docs.openclaw.ai/tools/clawhub>
- Hermes Creating Skills：<https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills/>
- Hermes Working with Skills：<https://hermes-agent.nousresearch.com/docs/guides/work-with-skills/>
- Claude Code Skills：<https://code.claude.com/docs/en/skills>
- Claude Code Plugins：<https://code.claude.com/docs/en/plugins>
- Claude Code Plugin Marketplaces：<https://code.claude.com/docs/en/plugin-marketplaces>
- 本地样本包：
  - `sources/0xjordansg-yolo--openclaw-twitter.zip`
  - `sources/aisadocs--openclaw-twitter-post-engage.zip`
