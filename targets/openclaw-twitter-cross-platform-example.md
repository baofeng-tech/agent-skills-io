# `openclaw-twitter` 跨平台改造实战样例

这份文档选用本仓库现有样本 `sources/0xjordansg-yolo--openclaw-twitter.zip`，演示如何把一个典型 `clawpub/openclaw` skill 改造成：

1. 一份平台中立的母版
2. OpenClaw 适配建议
3. Hermes 适配建议
4. Claude Code 适配建议

目标不是重写脚本逻辑，而是**把 skill 描述层标准化**。

## 1. 原始 skill 特征

原始包结构：

```text
openclaw-twitter/
├── SKILL.md
├── scripts/
│   ├── twitter_client.py
│   └── twitter_oauth_client.py
└── references/
    └── post_twitter.md
```

原始 frontmatter 主要问题：

- `name` 带有 `openclaw-` 平台前缀，不利于跨平台品牌统一
- `homepage`、`author`、`requires` 直接放在顶层，偏 OpenClaw 风格
- `metadata.openclaw.files` 对开放规范意义不大
- 正文命令使用 `{baseDir}`，跨平台兼容性较差
- 标题和文案强绑定 OpenClaw，而不是 skill 本身的业务能力

## 2. 推荐的新目录名

建议把目录和 `name` 统一改成：

```text
aisa-twitter-command-center/
```

原因：

- 更贴近业务能力而不是平台
- 可直接作为跨平台母版名
- 方便后续在 GitHub、AgentSkills、Hermes、Claude 市场统一展示

## 3. 母版 `SKILL.md`

下面这份是推荐的跨平台母版版本。

```md
---
name: aisa-twitter-command-center
description: Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth. Use when the user asks for Twitter research, monitoring, or posting without sharing passwords.
license: Apache-2.0
compatibility: Requires python3, AISA_API_KEY, and internet access to api.aisa.one. Uses relative paths for scripts and references to maximize compatibility across AgentSkills-compatible clients.
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: twitter,x,social-media,research,posting
---

# AIsa Twitter Command Center

Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth.

## When to use

- The user wants Twitter/X research, monitoring, or content discovery.
- The user wants to inspect profiles, timelines, mentions, trends, replies, quotes, lists, or Spaces.
- The user wants to draft or publish posts after explicit OAuth approval without sharing passwords.

## When NOT to use

- The user needs password-based login, cookie extraction, or browser credential scraping.
- The workflow must avoid relay-based calls to `api.aisa.one`.
- The request is for unsupported engagement actions not covered by this package.

## Quick Reference

- Required environment variable: `AISA_API_KEY`
- Read client: `scripts/twitter_client.py`
- OAuth and posting client: `scripts/twitter_oauth_client.py`
- Posting guide: `references/post_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

All network calls go to `https://api.aisa.one/apis/v1/...`.

## Capabilities

- Read user data, timelines, mentions, followers, followings, and related profile information.
- Search tweets and users, inspect replies, quotes, retweeters, thread context, trends, lists, communities, and Spaces.
- Publish text, image, and video posts after explicit OAuth approval.
- Return an authorization link when posting access has not been approved yet.

## Common Commands

```bash
python3 scripts/twitter_client.py user-info --username elonmusk
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_client.py trends --woeid 1
python3 scripts/twitter_oauth_client.py status
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa"
```

## Posting Workflow

When the user asks to send, publish, reply, or quote on X/Twitter:

1. Check whether `AISA_API_KEY` is configured.
2. If the user intent is to publish, attempt the publish workflow.
3. If authorization has not been completed, return the OAuth authorization link first.
4. Use `--media-file` only for user-provided local workspace files.
5. Do not claim the post succeeded until the publish command actually succeeds.

## Guardrails

- Do not ask for Twitter passwords or browser cookies.
- Do not invent captions, tweet URLs, or attachment files.
- Do not default to browser opening unless the user explicitly wants local browser launch.
- Do not claim external posting succeeded until the API confirms success.

## Security Notes

- The workflow is relay-based and sends API requests, OAuth requests, and approved media uploads to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- This workflow does not require passwords, browser cookie extraction, or direct account credential sharing.

## References

- See `references/post_twitter.md` for detailed posting examples and OAuth guidance.
```

## 4. OpenClaw 适配建议

如果要发布到 OpenClaw / ClawHub，可以在母版上补下面这些字段：

```yaml
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: twitter,x,social-media,research,posting
  openclaw:
    emoji: "🐦"
    primaryEnv: AISA_API_KEY
    requires:
      bins:
        - python3
      env:
        - AISA_API_KEY
```

OpenClaw 特别建议：

- 如需更贴近 OpenClaw 习惯，可以在平台专用版本里把示例命令写成 `{baseDir}/scripts/...`
- 但不要把这个写法反向污染母版
- `metadata.openclaw.files` 可以省略
- `user-invocable` 只有在确实需要 OpenClaw 专有行为时再加

## 5. Hermes 适配建议

如果要让 Hermes 消费得更自然，可补：

```yaml
platforms:
  - linux
  - macos
  - windows
required_environment_variables:
  - AISA_API_KEY
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: twitter,x,social-media,research,posting
  hermes:
    tags:
      - twitter
      - research
      - posting
    related_skills:
      - aisa-youtube-research
```

Hermes 特别建议：

- 目录层可放到某个分类下，例如 `communication/aisa-twitter-command-center/`
- Hermes 基本可以直接消费母版正文和相对路径
- 不需要为了 Hermes 改成私有路径变量

## 6. Claude Code 适配建议

如果是作为 standalone skill，本质上可以直接使用母版。  
如果想增强 Claude Code 体验，可增加：

```yaml
allowed-tools: Read Grep Bash
```

可选增强：

- `when_to_use`
- `argument-hint`
- `disable-model-invocation`

但这些建议只用于 Claude 专用版本，不放回通用母版。

如果要通过 Claude Code 分发，建议额外封装成 plugin：

```text
aisa-social-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── aisa-twitter-command-center/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

最小 `plugin.json`：

```json
{
  "name": "aisa-social-plugin",
  "description": "AIsa social media skills for Claude Code",
  "version": "1.0.0"
}
```

## 7. 改造前后差异总结

### 保留的部分

- `scripts/twitter_client.py`
- `scripts/twitter_oauth_client.py`
- `references/post_twitter.md`
- 核心能力和业务流程

### 改掉的部分

- `name`: `openclaw-twitter` → `aisa-twitter-command-center`
- 平台绑定标题：`OpenClaw Twitter` → `AIsa Twitter Command Center`
- `requires` 顶层字段 → `compatibility`
- `author` / `homepage` → `metadata`
- `{baseDir}` 路径 → 相对路径

### 下沉为平台扩展的部分

- `metadata.openclaw.*`
- Hermes tags / related_skills
- Claude Code 的 `allowed-tools` 和 plugin 分发壳

## 8. 为什么这个样例适合作为母版

这个 skill 很适合拿来作为 AIsa 第一批跨平台模板，因为它具备：

- 标准的 `SKILL.md + scripts + references` 结构
- 明确的读写边界
- 清楚的环境变量依赖
- 容易说明的安全边界
- 真实的 API / OAuth / 媒体文件场景

也就是说，后续 prediction market、YouTube、search、finance 等 skill，都可以复用这套改法。

## 9. 推荐落地顺序

1. 先把这个 Twitter 样例真正展开成一个目录版 skill
2. 用这份母版做 AIsa 通用模板的首个实例
3. 再按同样模式批量改 prediction market、YouTube、search skills
4. 最后再补 Claude Code plugin marketplace 和 well-known 索引

## 10. 相关文件

- [aisa-universal-skill-template.md](/mnt/d/workplace/agent-skills-io/targets/aisa-universal-skill-template.md:1)
- [clawpub-to-agentskillsso-manual.md](/mnt/d/workplace/agent-skills-io/targets/clawpub-to-agentskillsso-manual.md:1)
- [platform-spec-compare.md](/mnt/d/workplace/agent-skills-io/targets/platform-spec-compare.md:1)
