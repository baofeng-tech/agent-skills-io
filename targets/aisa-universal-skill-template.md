# AIsa 通用 Skill 模板

这是一份面向 `AgentSkills`、`OpenClaw / ClawHub`、`Hermes`、`Claude Code` 四个平台兼容的通用 `SKILL.md` 骨架。

设计原则：

- 先以 `AgentSkills` 开放规范为母版
- 只使用跨平台最稳定的字段
- 私有平台增强统一收口到扩展段说明
- 路径统一使用相对路径

## 最新硬规则

这套模板现在额外约束下面几条，默认对所有新 skill 和大改动都生效：

- Python 运行时默认只允许标准库，不引入 `requests`、`httpx`、`pytest` 之类第三方依赖。
- 母版 `SKILL.md` 统一使用 `metadata.aisa`，不要再把 `metadata.openclaw` 当成母版主结构。
- 母版正文命令统一写成 `scripts/...` 相对路径，不使用 `${SKILL_ROOT}`、`${CLAUDE_SKILL_DIR}`、`${LAST30DAYS_PYTHON}` 这类运行时专有变量。
- 发布到公共仓库的 skill 目录只保留运行时需要的文件；测试、评估、同步、开发脚本和 `pyproject.toml` 之类不随 skill 一起发布。
- 如果某个数据源需要第二套凭证或本地持久化能力，必须在正文里明确标成“可选扩展”，不能混进默认主路径。

## 推荐目录结构

```text
my-skill/
├── SKILL.md
├── README.md
├── scripts/
│   └── client.py
├── references/
│   └── usage.md
└── assets/
    └── optional-files
```

## 通用母版 `SKILL.md`

```md
---
name: my-skill
description: Explain clearly what this skill does and when it should be used. Include the main user intents and trigger keywords so compatible clients can load it automatically.
license: Apache-2.0
metadata:
  aisa:
    emoji: "🛠"
    requires:
      bins:
        - python3
      env:
        - MY_API_KEY
    primaryEnv: MY_API_KEY
    compatibility:
      - openclaw
      - claude-code
      - hermes
---

# My Skill

One-paragraph summary of the skill's purpose, user value, and high-level workflow.

## When to use

- The user asks for ...
- The task needs ...
- The workflow benefits from ...

## When NOT to use

- The user needs ...
- The workflow must avoid ...
- The task requires capabilities outside this package ...

## Quick Reference

- Required environment variables: `MY_API_KEY`
- Main script: `scripts/client.py`
- Detailed guide: `references/usage.md`

## Setup

```bash
export MY_API_KEY="your-key"
```

Add any other setup instructions here, such as required binaries, auth steps, or API host configuration. Keep the default path stdlib-only and runtime-only.

## Capabilities

- Capability 1
- Capability 2
- Capability 3

## Common Commands

```bash
python3 scripts/client.py status
python3 scripts/client.py search --query "example"
python3 scripts/client.py run --input "example"
```

## Workflow

When the user asks for this workflow:

1. Check the required environment variables.
2. Determine whether the user wants read-only or write actions.
3. Run the matching command from `scripts/`.
4. If an approval or authorization step is required, return that step clearly before claiming success.
5. Only report success after the command actually succeeds.

## Guardrails

- Do not request passwords if the workflow is designed for API-key or OAuth use.
- Do not fabricate files, URLs, or IDs that were not provided by the user or command output.
- Do not claim external side effects succeeded until the API or script confirms success.
- If the action is sensitive, ask for explicit confirmation before write operations.

## References

- See `references/usage.md` for extended examples, API notes, and troubleshooting.

## Security Notes

- Explain what secrets are required.
- Explain where requests are sent.
- Explain what sensitive data is not collected.
- Explain any authorization or approval requirements.
```

## OpenClaw 适配建议

如果要兼容 OpenClaw / ClawHub，可以在母版基础上额外生成发布层，而不是把母版改成 `metadata.openclaw`：

```yaml
metadata:
  openclaw:
    emoji: "🛠"
    primaryEnv: MY_API_KEY
    requires:
      bins:
        - python3
      env:
        - MY_API_KEY
```

建议：

- 保持正文命令仍然使用 `scripts/client.py` 相对路径
- 不要把 `{baseDir}` 写死进母版
- 不要把 OpenClaw 私有配置提升为母版核心字段

## Hermes 适配建议

如果要兼容 Hermes，可在母版基础上增补：

```yaml
metadata:
  author: AIsa
  version: "1.0.0"
  homepage: https://aisa.one
  tags: category,keyword,workflow
  hermes:
    tags:
      - category
      - workflow
    related_skills:
      - another-skill
platforms:
  - linux
  - macos
  - windows
required_environment_variables:
  - MY_API_KEY
```

建议：

- Hermes 基本可以直接消费母版
- 只补平台标签、相关 skill、环境变量提示
- Hermes 如果要公开发布，优先生成一个 runtime-only 的发布层，把参考文档和高风险示例从发布包里拿掉

## Claude Code 适配建议

Claude Code 可以直接使用母版 skill，但如果要增强体验，可额外加入：

```yaml
allowed-tools: Read Grep Bash
```

如果是 Claude 专用增强版，还可以考虑：

- `when_to_use`
- `argument-hint`
- `disable-model-invocation`

但这些不建议放进跨平台母版。

如果要通过 Claude Code 分发，建议再额外包装一个 plugin：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

## 推荐命名规则

- skill 目录名：`kebab-case`
- `name` 与目录名保持一致
- AIsa 系列建议统一前缀，例如：
  - `aisa-twitter-command-center`
  - `aisa-prediction-market`
  - `aisa-youtube-research`

## 推荐写法清单

建议：

- 用相对路径引用脚本和参考文档
- 把运行依赖写到 `metadata.aisa.requires`
- 把平台私有内容限制在扩展字段或单独发布层
- 把复杂文档拆到 `references/`
- 把可选的第二凭证路径单独标成扩展能力
- 只发布运行时真正需要的文件

避免：

- 把 `{baseDir}`、`${CLAUDE_SKILL_DIR}` 写进通用母版
- 把平台私有 frontmatter 当成跨平台必需字段
- 在母版或发布层里引入 `requests` / `httpx` / `pyproject.toml`
- 把测试、评估、同步脚本一起塞进最终 skill 包
- 在正文塞过长的 API 表格
- 在未验证成功前声称写操作完成
