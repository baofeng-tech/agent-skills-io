# Skills Platform 规范对照表

这份表把 `AgentSkills`、`OpenClaw / ClawHub`、`Hermes`、`Claude Code` 的 skill 结构和分发方式放在一起，方便做统一模板和多平台兼容设计。

## 总览

| 维度 | AgentSkills | OpenClaw / ClawHub | Hermes | Claude Code |
| --- | --- | --- | --- | --- |
| 定位 | 开放规范 | 运行时 + Registry | Agent runtime + Skills Hub | Agent runtime + Skills / Plugins |
| 最小入口 | `SKILL.md` | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| 是否兼容开放规范 | 是 | 基本兼容，但有私有扩展 | 是，且明确宣称兼容 | 基本兼容，但有大量私有扩展 |
| 最适合做母版 | 是 | 否 | 接近是 | 否 |

## 目录结构

| 平台 | 推荐结构 | 备注 |
| --- | --- | --- |
| AgentSkills | `skill-name/SKILL.md` + `scripts/` + `references/` + `assets/` | 最标准、最中立 |
| OpenClaw / ClawHub | `skill-name/SKILL.md` + 可选支持文件 | 能兼容标准结构，但文档更偏 OpenClaw 运行时 |
| Hermes | `category/skill-name/SKILL.md` + 支持文件 | 常带分类目录，如 `research/`、`productivity/` |
| Claude Code | standalone skill 或 plugin 内 `skills/<skill>/SKILL.md` | 团队分发通常配合 plugin |

## `SKILL.md` frontmatter

| 维度 | AgentSkills | OpenClaw / ClawHub | Hermes | Claude Code |
| --- | --- | --- | --- | --- |
| 核心字段 | `name` `description` | `name` `description` | `name` `description` | `description` 推荐，`name` 常用于 slash command |
| 可选标准字段 | `license` `compatibility` `metadata` `allowed-tools` | 部分兼容 | 可兼容使用 | 可兼容使用 |
| 私有扩展 | 通过 `metadata` 扩展 | `metadata.openclaw.*`、`user-invocable` 等 | `metadata.hermes.*`、平台/环境变量字段 | `when_to_use` `argument-hint` `context` `hooks` 等 |
| 命名风格 | 目录名与 `name` 一致，通常 kebab-case | 文档中存在不一致，既有开放规范兼容，也有 `snake_case` 示例 | 通常沿用开放规范风格 | 相对灵活，但建议目录与 skill 名一致 |

## 路径与脚本引用

| 平台 | 推荐路径写法 | 说明 |
| --- | --- | --- |
| AgentSkills | 相对路径，如 `scripts/client.py` | 最推荐的跨平台写法 |
| OpenClaw / ClawHub | 常见 `{baseDir}/scripts/...` | 这是 OpenClaw 运行时习惯，不建议写进跨平台母版 |
| Hermes | 相对路径 | 和开放规范最一致 |
| Claude Code | 相对路径或 `${CLAUDE_SKILL_DIR}` | 若追求跨平台，优先相对路径 |

## 环境变量与依赖声明

| 平台 | 推荐写法 | 说明 |
| --- | --- | --- |
| AgentSkills | `compatibility` + 正文 Setup | 中立且兼容性最好 |
| OpenClaw / ClawHub | `metadata.openclaw.requires.*` | 对 OpenClaw 友好，但偏私有 |
| Hermes | `required_environment_variables`、配置字段 | 明确支持 secret/config 提示 |
| Claude Code | 正文说明 + `allowed-tools` | 更多依赖提示写在说明里 |

## 安装位置

| 平台 | 常见本地位置 |
| --- | --- |
| AgentSkills | 由客户端决定，常见是 `.agents/skills/` |
| OpenClaw / ClawHub | `<workspace>/skills/`、`<workspace>/.agents/skills/`、`~/.agents/skills/`、`~/.openclaw/skills/` |
| Hermes | `~/.hermes/skills/<category>/<skill>/` |
| Claude Code | `~/.claude/skills/<skill>/`、`.claude/skills/<skill>/`、插件内 `skills/<skill>/` |

## 分发方式

| 平台 | 主要分发方式 | 说明 |
| --- | --- | --- |
| AgentSkills | GitHub、well-known、市场接入 | 适合作为统一源 |
| OpenClaw / ClawHub | ClawHub registry | 支持搜索、安装、更新、发布 |
| Hermes | official、GitHub、tap、well-known | 安装来源较多 |
| Claude Code | plugin marketplace | 共享和团队分发通常建议走 plugin |

## 适配建议

| 平台 | 建议策略 |
| --- | --- |
| AgentSkills | 作为母版规范 |
| OpenClaw / ClawHub | 仅补 `metadata.openclaw.*` 等薄适配 |
| Hermes | 几乎直接消费母版，只补 `metadata.hermes.*` |
| Claude Code | skill 可直接兼容；若要分发再包一层 plugin marketplace |

## 对 AIsa 的推荐落地方式

建议维护一套统一仓库：

```text
AIsaONE/agent-skills/
├── README.md
├── twitter-command-center/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── prediction-market/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── .claude-plugin/
    └── marketplace.json
```

实践建议：

1. `SKILL.md` 先按 AgentSkills 母版写。
2. OpenClaw 需要的能力只加到 `metadata.openclaw`。
3. Hermes 需要的标签和 related skills 加到 `metadata.hermes`。
4. Claude Code 分发时单独维护 `.claude-plugin/marketplace.json`。
5. 所有脚本引用优先使用相对路径，不把 `{baseDir}` 或 `${CLAUDE_SKILL_DIR}` 写死到母版里。

## 相关文档

- [platform-reference-links.md](/mnt/d/workplace/agent-skills-io/targets/platform-reference-links.md:1)
- [clawpub-to-agentskillsso-manual.md](/mnt/d/workplace/agent-skills-io/targets/clawpub-to-agentskillsso-manual.md:1)
