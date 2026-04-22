# AgentSkills.so 收录触达模板

用于在 `agentskills.so` 尚未自然收录 `baofeng-tech/agent-skills-so` 时，通过官方公开入口做人工触达。

## 已确认的公开入口

- 邮箱：`support@agentskills.so`
- Discord：`https://discord.gg/gwyWY8v9Ed`

## 推荐触达信息

### 主题

```text
Request for AgentSkills.so ingestion: baofeng-tech/agent-skills-so
```

### 正文模板

```text
Hi AgentSkills team,

We prepared a public Agent Skills repository that follows the open SKILL.md structure and is intended for AgentSkills.so ingestion:

- Repo: https://github.com/baofeng-tech/agent-skills-so
- Author: baofeng-tech
- Structure: root-level skill directories + SKILL.md + README + LICENSE + zip artifacts

Representative skills:
- aisa-multi-search-engine
- aisa-twitter-command-center
- market
- last30days

We designed this repo as a clean, GitHub-first Agent Skills catalog for public indexing.

Could you please confirm:
1. whether this repo is eligible for ingestion,
2. whether there is a preferred submission path beyond crawler discovery,
3. and if any metadata or structure adjustments would help inclusion?

Thanks a lot.
```

## 建议附带的补充信息

- 当前仓库是公开仓库
- 所有 skill 目录位于 repo root
- `name` 与目录名一致
- skill 包含标准 `SKILL.md`
- 提供 root catalog 文件与 ZIP 产物
- 已经有 `agentskill.sh` 收录经验，可证明这批 skill 不是临时拼装目录

## 建议发送时机

1. 先等一个 crawler 周期
2. 若 `agentskills.so` 的 sitemap / 站内搜索仍未出现 `baofeng-tech`
3. 再发邮件或进 Discord 触达
