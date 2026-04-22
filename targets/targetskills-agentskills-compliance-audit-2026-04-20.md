# targetSkills Agent Skills 合规审查

## 结论

截至 2026-04-20，这个仓库里的 `targetSkills/` 已完成一轮面向 `agentskills.io` 开放规范的母版审查与修复。

当前结论：

- 51 / 51 个 skill 都保留标准目录结构：`SKILL.md` + 可选 `scripts/` / `references/` / `assets/`
- 51 / 51 个 skill 的 frontmatter `name` 已与目录名完全一致
- 51 / 51 个 skill 已具备 `description`
- 51 / 51 个 skill 已补齐 top-level `compatibility`
- 51 / 51 个 skill 已保留仓库约定的 `metadata.aisa`
- 51 / 51 个 skill 已清除 `${SKILL_ROOT}`、`${LAST30DAYS_PYTHON}`、`{baseDir}` 等旧路径占位符
- 0 个 skill 超过 500 行

这意味着：

- `targetSkills/` 现在可以继续作为跨平台母版层
- 对外公开到 Agent Skills 生态时，不应再直接拿早期未清洗版本
- 更适合外部 GitHub / marketplace 的标准化公开层，应该优先使用 `agentskills-so-release/`

## 本轮修复了什么

### 1. frontmatter 名称硬伤

修复前存在 8 个母 skill 的 frontmatter `name` 与目录名不一致，这不符合 `agentskills.io` 对 `name` 和父目录名一致的要求。

已修复目录对应关系，包括：

- `market`
- `media-gen`
- `perplexity-search`
- `prediction-market`
- `prediction-market-arbitrage`
- `search`
- `twitter`
- `youtube`

### 2. 依赖声明缺口

修复前 `aisa-provider`、`youtube-search` 等 skill 的 `metadata.aisa.requires.bins` 不完整。

本轮已改为：

- 优先从已存在元数据继承
- 再从文件后缀推断
- 再从 `SKILL.md` 中的命令样例推断（如 `curl`、`python3`、`openclaw`）

### 3. 错域触发语句

修复前 `youtube-search` 的描述尾部仍残留 Twitter 触发语句。

本轮已补上规则：

- 以 skill 名称所属领域为准
- 自动重建 `Use when:` 触发语句
- 避免“主体内容正确，但触发条件串台”的情况

### 4. 旧路径占位符

修复前仍有 23 个 skill 保留 OpenClaw 风格的 `{baseDir}` 路径占位符。

本轮已统一改为真正的相对路径：

- `python3 {baseDir}/scripts/foo.py` → `python3 scripts/foo.py`
- `{baseDir}` 单独出现时改为 `.` 或直接去掉前缀

## 当前仍需注意但不算阻塞

### README 覆盖率

当前 `targetSkills/` 中：

- 有 `README.md` 的 skill：27
- 缺少 `README.md` 的 skill：24

这不是 `agentskills.io` 规范阻塞项，因为开放规范的必需入口是 `SKILL.md`。

但它仍然影响：

- GitHub 展示质量
- 团队维护体验
- 第三方市场对仓库可信度的人工判断

所以建议：

- 母版层允许 README 不齐
- 对外公开层优先使用自动生成的发布目录，而不是直接把 `targetSkills/` 原样推上去

## 推荐使用方式

### 继续作为母版层

`targetSkills/` 继续承担：

- 跨平台 skill 的真实 source of truth
- 后续所有发布层的生成输入
- 迁移、改造、保留完整语义的工作区

### 对外公开时不要直接拿母版

对外建议：

- `clawhub-release/`：ClawHub skill 发布层
- `clawhub-plugin-release/`：ClawHub plugin 发布层
- `claude-release/`：Claude / skills.sh / GitHub 分发层
- `hermes-release/`：Hermes 分发层
- `agentskills-so-release/`：Agent Skills 标准生态分发层

## 这轮审查的判断标准

本轮主要依据：

- `agentskills.io/specification`
- 本仓库已有的 `AGENTS.md`
- `PROJECT_OVERVIEW.md`
- 本仓库的母版规范脚本与发布层脚本

其中要点包括：

- `name` 必须与目录名一致
- `description` 需要描述“做什么 + 何时使用”
- 推荐相对路径
- 推荐 progressive disclosure
- 支持 `compatibility`
- 允许 `metadata`

## 最终建议

`targetSkills/` 现在已经足够作为“规范化母版层”继续往下游生成。

下一阶段重点不再是“修正基础格式”，而是：

1. 继续用脚本生成各平台发布层
2. 把外部市场投递尽量统一到标准化发布目录
3. 逐步补齐缺少 README 的母版 skill，但不要为此阻塞发布链路
