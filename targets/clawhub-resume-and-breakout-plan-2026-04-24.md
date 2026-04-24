# ClawHub 续跑与爆款改造执行计划（2026-04-24）

## 1. 当前状态压缩结论

- 当前可以直接基于 `targets/clawhub-publish-state.json` 续跑 ClawHub，不必默认重做前面的 build / test / sync。
- 已新增 `scripts/clawhub_live_status.py`，可以独立回查已发布 artifact 的 `VirusTotal`、`OpenClaw verdict` 与 `Suspicious` 原因，并写回 publish state。
- `scripts/publish_clawhub_batch.py` 已支持可选 `--post-publish-scan`，可在发布或探测到远端已存在后立即做 live scan。
- 本地已有 20 个改动过的 skill 家族同步到了这些生成层：
  - `clawhub-release/`
  - `clawhub-plugin-release/`
  - `claude-release/`
  - `claude-marketplace/`
  - `agentskills-so-release/`
  - `agentskill-sh-release/`
- 但“已生成”不等于“已重新发布”。当前本地内容和历史 publish state 之间存在版本与发布时间漂移，不能直接把 state 当成最新版证明。
- `targets/clawhub-publish-state.json` 当前记录了 115 个 artifact，其中 109 个 `published`，6 个 `failed`。
- 2026-04-24 基于当前 state 执行 `python3 scripts/publish_clawhub_batch.py --targets both --accounts-file example/accounts --skip-build --dry-run --per-token-per-hour 4` 后，脚本只把 `7` 个 skill 判定为待续跑条目，当前没有额外 plugin pending。
- 已知失败项包括：
  - `plugin:aisa-perplexity-search-plugin`
    - 远端 probe / fetch 失败
  - `skill:aisa-perplexity-search`
    - slug 已被占用
  - `skill:perplexity-search`
    - slug 被锁到删除或封禁账号
  - `skill:search`
    - slug 已被占用
  - `skill:tavily-search`
    - slug 已被占用
  - `skill:twitter`
    - slug 已被占用

## 2. 当前真正的阻塞

### A. 版本语义还没收紧

- 例如 `clawhub-release/last30days/SKILL.md` 当前是 `version: 1.0.0`
- 但 `targets/clawhub-publish-state.json` 里 `skill:last30days` 最近一次已发布版本是 `1.0.3`
- `marketpulse`、`media-gen`、`openclaw-media-gen`、`prediction-market-arbitrage`、`prediction-market-data`、`twitter-autopilot` 也存在类似的“当前文件版本 <= 历史发布版本”现象
- 所以续跑前必须先做一次“内容变了但版本没有正确前进”的收口，不然会让真实线上状态和本地版本关系继续混乱

### B. 各平台外部发布仓并非都已对齐

- `../agent-skills`
  - 当前工作树是脏的，而且分支还是 `main`
  - 说明母 skill 的同步链路没有彻底收口
- `../Aisa-One-Skills-Claude` 与 `../Aisa-One-Plugins-Claude`
  - 对这次改动的 20 个 skill/plugin 来说：
  - `9` 个已经一致
  - `8` 个内容不同
  - `3` 个目标目录缺失：`crypto-market-data`、`multi-source-search`、`youtube-serp`
- `../Aisa-One-Skills-Hermes`
  - `last30days`、`last30days-zh` 两个改动 skill 与当前 `hermes-release/` 不一致
- `../agent-skills-own`
  - 与 `agentskills-so-release/`、`agentskill-sh-release/` 的差异仍然较大，不适合视为已完成发布

### C. `skillGet` 的爆款方法目前只算“部分接入”

- 已接入的部分：
  - 从 `../skillGet/public/downloads/*` 导入历史包
  - `targets/clawhub-plugin-structure-and-upload-plan-2026-04-20.md` 已引用 `skillGet` 的插件爆款判断
- 尚未系统接入的部分：
  - 母 skill 改名/改描述时的爆款文案规则
  - “旗舰包 / 变体包 / supporting variant”的矩阵决策
  - 从线上爆款 skill 反推 AIsa API 改造对象的固定流程

## 3. 执行顺序

### 第 1 阶段：先锁住发布基线

目标：

- 只审计当前已改内容，不重做 build / test / sync
- 明确哪些 skill/plugin 是“需要重新发布”的真实变更
- 修正版本回退或版本未前进的问题

动作：

- 只针对这次变更的 20 个 skill/plugin 做版本核对
- 把需要继续发到 ClawHub 的条目分成三类：
  - `state 里不存在`
  - `state 里失败`
  - `state 里已发布但本地内容已变`

### 第 2 阶段：按现有 state 续跑 ClawHub

目标：

- 不重做前面的 build / test / sync
- 优先把未发布、失败、缺失项续上

当前 `dry-run` 判定的待续跑 skill：

- `crypto-market-data`
- `multi-source-search`
- `perplexity-search`
- `search`
- `tavily-search`
- `twitter`
- `youtube-serp`

推荐命令：

```bash
python3 scripts/publish_clawhub_batch.py --targets both --skip-build --dry-run
python3 scripts/publish_clawhub_batch.py --targets skill --skip-build --per-token-per-hour 4
python3 scripts/publish_clawhub_batch.py --targets plugin --skip-build --per-token-per-hour 4
```

原则：

- 先 `dry-run`
- 先发 skill，再发 plugin
- 不对全部 artifact 做 `--force`
- 只在版本语义已经收紧后再做真实 publish

### 第 3 阶段：推进各平台发布仓收口

目标：

- 让生成层和外部目标仓一致
- 再决定 commit / push / 平台侧正式发布

推荐顺序：

```bash
bash scripts/publish-claude-release.sh --with-marketplace --skip-build
bash scripts/publish-hermes-release.sh --skip-build
bash scripts/publish-targetSkills-to-agent-skills.sh targetSkills ../agent-skills
```

补充说明：

- `../agent-skills` 的分支语义还需要单独钉死
- 在分支语义未确认前，先不要把它当成“已经可以直接推”的最终目标仓

### 第 4 阶段：把 `skillGet` 方法接进当前改造流

必须显式使用这些来源：

- `../skillGet/dist/reports/AISA_All_Skills_Breakout_Plan_ZH.md`
- `../skillGet/dist/reports/ClawHub_Viral_Boss_Report_ZH.md`
- `../skillGet/dist/reports/ClawHub_Plugin_Viral_Report_ZH.md`
- `../skillGet/dist/data/clawhub-top200-aisa-conversion-plan.json`
- `../skillGet/dist/data/aisa-api-analysis.json`

落地方式：

- 改 skill 文案前先看是否属于 `flagship`、`growth-variant`、`supporting-variant`
- 改 plugin 前先看当前 lane 更适合 `bundle-first` 还是以后再升到 `code plugin`
- 选新实验方向时先确认它是否真的映射到现有 AIsa API 能力

### 第 5 阶段：先做一个现有 AIsa skill 的爆款实验

首推实验对象：

- `aisa-twitter-api`

原因：

- `../skillGet/dist/reports/AISA_All_Skills_Breakout_Plan_ZH.md` 已把它列为 P0
- 它最接近当前本地 AIsa 技能矩阵里的旗舰包候选
- 适合把“研究 / 监控 / 发帖 / 互动”四层矩阵拆得更清楚

实验目标：

- 用更强的任务名和 `Use when:` 入口重写 skill surface
- 保持 runtime 不变，只改前台文案、示例请求、兄弟技能边界
- 同步更新对应 plugin surface
- 发布到 ClawHub 验证真实反馈

当前已落地：

- 母 skill 已收紧为 `Twitter/X command center` 旗舰位
- 发布层已同步强化 watchlist / competitor monitoring / publish-ready 的入口表述

### 第 6 阶段：再做一个“线上技能 -> AIsa API”实验

首推方向：

- 搜索赛道
- 以 `multi-search-engine` 这类线上高位技能为参考，强化 `aisa-multi-search-engine` / 搜索旗舰 lane

原因：

- `../skillGet/dist/data/clawhub-top200-aisa-conversion-plan.json` 里搜索赛道长期高频
- 当前 AIsa 能力与搜索类 API 的映射最直接
- 这条线更容易在不大改 runtime 的情况下先做出爆款标题、入口和 sibling ladder

备选方向：

- `skill-vetter`
  - 适合后续做安全审计 lane
  - 但更适合作为第二波，不建议抢在搜索 lane 前面

当前已落地：

- `search`
  - 调整为搜索旗舰位 `AIsa Search Command Center`
- `multi-source-search`
  - 调整为增长变体 `Multi-Source Search Verification Engine`
- `build_clawhub_release.py`
  - 已增加按 skill slug 区分的 publish profile，避免 ClawHub 发布层把搜索兄弟 skill 再次压成同一套泛化文案

## 4. 本轮建议先执行的最小闭环

1. 收紧这 20 个已改 skill/plugin 的版本语义
2. 用现有 `state` 做一次 `--skip-build --dry-run` 续跑确认
3. 优先续发真实未完成的 ClawHub skill/plugin
4. 开始做 `aisa-twitter-api` 的爆款实验改造

## 5. 本轮不建议做的事

- 不建议先全量重跑 build / test / sync
- 不建议先全量 `--force` 重发全部 ClawHub artifact
- 不建议在 `../agent-skills` 分支语义未钉死前，把它当成最终已发布基线
- 不建议同时开启多个新实验 skill，先把一个现有 AIsa flagship 实验跑通
