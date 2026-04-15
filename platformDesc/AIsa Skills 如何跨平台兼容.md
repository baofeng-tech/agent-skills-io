如何跨平台兼容： OpenClaw· Claude Code· Codex· Cursor等 

这个问题的答案其实你已经在用了——**agentskills.io 规范本身就是跨平台兼容层**。但具体到"一份代码怎么让所有平台都能装"，有几个实操细节需要注意。

## **核心原理：一个 SKILL.md，N 个平台**

所有这些平台都实现了同一个加载逻辑：

1. 扫描 `skills/` 目录找到 `SKILL.md`  
2. 读 YAML frontmatter 里的 `name` \+ `description`（决定什么时候激活）  
3. 激活时加载 body（instructions）  
4. 按需加载 `scripts/`、`references/`

这意味着只要你的 skill 目录结构符合 agentskills.io 规范，所有平台**原生兼容**，不需要写适配代码。

## **但平台间有差异**

差异不在 skill 格式上，而在三个地方：**安装方式**、**脚本路径引用**、**metadata 扩展字段**。

**安装方式各不相同，但指向同一个 GitHub repo：**

```shell
# OpenClaw
openclaw skills install github:AIsa-team/agent-skills/twitter-autopilot
# 或通过 ClawHub
clawhub install aisa/twitter-autopilot

# Claude Code (Plugin 模式)
/plugin install twitter-autopilot@aisa-marketplace
# 或手动复制
cp -r twitter-autopilot ~/.claude/skills/

# Codex / Cursor / Copilot / Windsurf / Zed
# 复制到 .agents/skills/ (agentskills.io 默认路径)
cp -r twitter-autopilot .agents/skills/

# Hermes Agent
hermes skills install github:AIsa-team/agent-skills/twitter-autopilot

# skills.sh / agentskill.sh (通用)
npx skills add AIsa-team/agent-skills
/learn @AIsa-team/twitter-autopilot
```

你只需要维护**一个 GitHub repo**，所有渠道从同一个源安装。

**脚本路径是最容易踩的坑：**

| 平台 | 脚本路径变量 | 示例 |
| ----- | ----- | ----- |
| Claude Code Plugin | `${CLAUDE_PLUGIN_ROOT}` | `${CLAUDE_PLUGIN_ROOT}/scripts/client.py` |
| OpenClaw | `{baseDir}` | `{baseDir}/scripts/client.py` |
| Hermes Agent | 无变量，相对路径 | `scripts/client.py` |
| agentskills.io 规范 | 相对路径 | `scripts/client.py` |
| Codex / Cursor | 相对路径 | `scripts/client.py` |

**兼容方案：统一用相对路径。** agentskills.io 规范就是这么写的——`scripts/client.py` 而不是带变量的绝对路径。OpenClaw 的 `{baseDir}` 和 Claude Code 的 `${CLAUDE_PLUGIN_ROOT}` 是各自的扩展，不是规范要求。Agent 足够聪明，看到 `scripts/client.py` 会自己解析到正确的绝对路径。

你现有 skills 里的 `{baseDir}/scripts/` 引用就是兼容性问题的来源——之前帮你改成 `scripts/` 相对路径就是为了这个。

**metadata 扩展字段各平台不同但互不冲突：**

```
metadata:
  # agentskills.io 标准字段（所有平台通用）
  author: aisa
  version: "1.0.0"

  # OpenClaw 扩展（OpenClaw 读，其他平台忽略）
  openclaw:
    emoji: "🐦"
    requires:
      bins: [curl, python3]
      env: [AISA_API_KEY]
    primaryEnv: AISA_API_KEY

  # Hermes 扩展（Hermes 读，其他平台忽略）
  hermes:
    tags: [twitter, social-media]
    related_skills: [youtube-serp]
```

各平台只读自己认识的 key，其余忽略。所以你可以在同一个 `metadata` 里放多个平台的扩展字段，不会冲突。

## **AIsa 的最佳实践：三层结构**

```
AIsa-team/agent-skills/          ← GitHub repo（单一真实来源）
├── README.md                     ← 人类文档 + 安装命令汇总
├── twitter-autopilot/
│   ├── SKILL.md                  ← agentskills.io 合规 frontmatter
│   ├── scripts/
│   │   ├── twitter_client.py     ← 纯 stdlib，无外部依赖
│   │   └── twitter_oauth_client.py
│   └── references/
│       ├── api-endpoints.md
│       └── post_twitter.md
├── prediction-market-data/
│   ├── SKILL.md
│   └── scripts/
│       └── prediction_market_client.py
├── marketpulse/
│   └── ...
└── .claude-plugin/               ← Claude Code Plugin marketplace 索引（可选）
    └── marketplace.json
```

**第一层：skill 本身**——每个子目录是一个独立 skill，严格遵循 agentskills.io 规范。这确保 Codex、Cursor、Copilot、Windsurf、Hermes 等所有遵循规范的平台都能直接用。

**第二层：metadata 多平台扩展**——在 SKILL.md 的 `metadata` 里同时放 `openclaw` 和 `hermes` 的扩展字段。各平台只取自己的，互不影响。

**第三层：平台特定索引文件**（可选）——比如 `.claude-plugin/marketplace.json` 让 Claude Code 用户通过 `/plugin marketplace add` 发现你的 skills。这些文件不影响其他平台。

## **脚本兼容性的关键约束**

AIsa 的 Python scripts 已经做对了最重要的一点：**只用标准库**（`urllib`、`argparse`、`json`、`os`）。这意味着任何有 `python3` 的环境都能跑，不需要 `pip install`。如果 skill 依赖第三方包，跨平台兼容性会大幅下降——不同平台的沙箱环境差异很大。

## **一句话总结**

**写一份 agentskills.io 合规的 SKILL.md \+ 纯 stdlib scripts，放到一个 GitHub repo，然后向每个渠道提交一次。** 格式层面不需要任何适配——规范本身就是兼容层。平台特定的 metadata 扩展可以共存在同一个文件里。安装方式不同但源是同一个 repo。

