# 平台分层与规则拆分审计（2026-04-28）

## 结论

当前仓库已经有“母版 -> 多平台发布层”的基本分层，但还没有完全把“母版中性规则”“ClawHub breakout 规则”“ClawHub suspicious 修复规则”在默认调用入口上拆开。

这次复核后的结论是：

1. `targetSkills/` 没有被 breakout slug 直接污染。
2. `targetSkills/` 仍保持 `metadata.aisa` 为主，没有混入 `metadata.openclaw` / `metadata.hermes`。
3. Claude / AgentSkills.so / agentskill.sh 的正文仍大量继承母版，平台特性主要体现在 frontmatter、README、目录结构，不是完全重写。
4. Hermes 的平台化最明显，已经有分类目录、`metadata.hermes.tags`、`required_environment_variables` 和更短的发布版正文。
5. `.agents/skills` 之前默认只提供全局 `*-all` publish skill，上下文能跑，但默认精修会把 source / ClawHub / breakout 规则混在一起。
6. 本轮已把 repo-local LLM 精修入口拆成三个 profile：
   - `source`
   - `clawhub_breakout`
   - `clawhub_suspicious`

## 1. 母版是否被 breakout 污染

### 已确认未污染的点

- `targets/clawhub-breakout-variants.json` 当前只声明两个 breakout slug：
  - `aisa-twitter-api-command-center`
  - `aisa-twitter-research-engage-relay`
- 这两个 slug 的目录只出现在：
  - `clawhub-release/`
  - `clawhub-plugin-release/`
- 它们没有扩散到：
  - `targetSkills/`
  - `claude-release/`
  - `hermes-release/`
  - `agentskills-so-release/`
  - `agentskill-sh-release/`

### 仍需注意的点

- `targetSkills/` 的部分母版文案已经带有明显家族排位语气，例如：
  - `command center`
  - `flagship`
  - `engagement suite`
- 这不等于 ClawHub 污染，但说明“母版中性层”和“增长位文案层”此前没有被默认调用入口严格隔离。

## 2. 各平台结构是否真的不同

### `targetSkills/`

- 平台定位：中性母版
- 结构特征：
  - root-level skill 目录
  - canonical `metadata.aisa`
  - 跨平台兼容说明和较完整正文

### `clawhub-release/`

- 平台定位：ClawHub skill 上传层
- 结构特征：
  - root-level skill 目录
  - 增加 upload-friendly frontmatter
  - 使用 `metadata.openclaw`
  - breakout slug 与原版 slug 并排存在

### `clawhub-plugin-release/`

- 平台定位：ClawHub / OpenClaw native-first plugin 层
- 结构特征：
  - `plugins/<slug>-plugin/`
  - `openclaw.plugin.json`
  - `.claude-plugin/plugin.json`
  - `package.json`
  - `skills/<skill>/`

### `claude-release/`

- 平台定位：Claude standalone / skills.sh 发布层
- 结构特征：
  - root-level skill 目录
  - frontmatter 收敛到 `name/description/allowed-tools/when_to_use`
  - release-specific README
- 当前差距：
  - 正文多数仍直接继承母版，不是完整的 Claude 专用正文

### `claude-marketplace/`

- 平台定位：Claude Git-based marketplace wrapper
- 结构特征：
  - `.claude-plugin/marketplace.json`
  - `plugins/<plugin>/`
  - 每个 plugin 内嵌 `skills/<skill>/`

### `hermes-release/`

- 平台定位：Hermes skills / tap 发布层
- 结构特征：
  - 按 category 分目录，例如 `communication/`, `research/`, `finance/`
  - `metadata.hermes.tags`
  - `required_environment_variables`
  - 更短、更 Hermes 化的正文

### `agentskills-so-release/` 与 `agentskill-sh-release/`

- 平台定位：GitHub-backed 公共 skill 目录层
- 结构特征：
  - root-level skill 目录
  - 扁平化 metadata
  - index / zip / crawler-friendly 文件
- 当前差距：
  - 正文多数仍继承母版，只在 metadata 和 README 上做平台化

## 3. `.agents/skills` 是否混在一起

### 复核前

repo-local `.agents/skills` 只有这些全局 publish helper：

- `clawhub-skill-optimizer-all`
- `clawhub-plugin-packager-all`
- `clawhub-security-auditor-all`

`scripts/llm_refine_aisa_skills.py` 默认直接把其中的 optimizer + auditor 整包喂给模型。

这意味着：

- 可以运行
- 但默认上下文会同时带入：
  - 全平台发布规则
  - ClawHub suspicious 规则
  - breakout positioning 规则

### 本轮修改后

新增 repo-local skill profile：

- `.agents/skills/aisa-source-skill-editor/SKILL.md`
- `.agents/skills/aisa-clawhub-breakout-editor/SKILL.md`

并把精修入口改成：

- `python3 scripts/llm_refine_aisa_skills.py --profile source`
  - 默认给 `targetSkills/` 母版用
- `python3 scripts/llm_refine_aisa_skills.py --profile clawhub_breakout`
  - 只给 ClawHub breakout 用
- `python3 scripts/llm_refine_aisa_skills.py --profile clawhub_suspicious`
  - 只给 diagnosis-driven suspicious remediation 用

同时：

- `scripts/unified_skill_pipeline.py`
  - hosted / normal LLM 精修默认走 `source`
- `scripts/clawhub_suspicious_remediation.py`
  - ClawHub 修复链路改走 `clawhub_suspicious`

## 4. `clawhub-release/` 原版 slug 与 breakout slug 是否冲突

### 当前结论

- 线上不会因为 slug 重名而冲突
- 当前的风险主要是“人看目录时容易混淆”，不是 registry slug collision

### 为什么现在没有直接做物理拆目录

当前这些脚本都默认 `clawhub-release/*/SKILL.md` 是平铺结构：

- `scripts/publish_clawhub_batch.py`
- `scripts/test_release_layers.py`
- `scripts/clawhub_live_status.py`

如果直接把 breakout 技能移到二级目录，需要同步改：

- 本地发现逻辑
- publish 逻辑
- test 逻辑
- live-status 回查映射

### 本轮处理原则

- 先保留平铺目录，避免打断现有发布脚本
- 用独立 breakout 清单和文档把“逻辑分层”讲清楚
- 等 breakout 数量继续增长时，再做物理目录重构

## 5. 当前建议

1. 母版继续保持中性，不把 ClawHub-only slug 或 plugin wrapper 写回 `targetSkills/`。
2. breakout 文案只在 ClawHub 专用 profile 和 ClawHub 生成层里强化。
3. Claude / AgentSkills.so 后续如要进一步平台化，优先补正文结构差异，而不是再改母版。
4. `clawhub-release/` 在下一轮可考虑增加逻辑索引分组，但不建议在当前 flat-root 发布链路上直接搬目录。
