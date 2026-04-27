# AISA API 爆款改造分层与执行计划（2026-04-28）

## 1. 当前状态

- 仓库里已经具备 AISA API skill 的批量精修链路：
  - `scripts/llm_refine_aisa_skills.py`
  - `.github/workflows/unified-skill-pipeline.yml`
- 但当前真正落地产物只有 `targets/llm-skill-refinement/aisa-twitter-api.json` 这一份。
- `skillGet` 证据层已经明确：
  - `aisa-twitter-api` 是当前最适合先打爆的 P0 旗舰位
  - 后续应扩 Twitter 家族、Search 家族、YouTube 家族，再推进更高收入的 GitHub / Workspace / Finance 方向
- 当前最大的结构性问题不是“有没有 skill 可改”，而是“兄弟 skill 是否在抢同一搜索面”。
- 当前自动诊断仍有一个 blocker：
  - `plugin:aisa-twitter-engagement-suite-plugin`
  - 核心问题是 relay trust、OAuth/upload side effects、metadata/env 对齐仍不够干净

## 2. 结论

### 2.1 爆款 skill 现在怎么样了

- 已经从“想法阶段”进入“可批量复制的方法阶段”
- 但还没有进入“全家族稳定放量阶段”
- 当前真正跑通的只有：
  - `aisa-twitter-api` 作为旗舰实验样本
- 当前还没跑通的关键环节：
  - Twitter 家族兄弟位还没完全拉开
  - Search / YouTube / Market 家族还没按 `flagship / growth / supporting` 系统排位
  - suspicious 修复闭环还只覆盖到少量重点 artifact

### 2.2 所有 AISA API skill 能不能都按爆款思路修改

可以，但不能一刀切。

应该做的是：

- 全量纳入爆款改造范围
- 分家族分角色推进
- 一个家族只保留一个真正的旗舰搜索面
- 其它兄弟 skill 只抢高意图长尾词，不抢旗舰词

不应该做的是：

- 所有 skill 都改成“command center”
- 所有 skill 都写成同一套“one API key + everything”
- 同时把多个兄弟 skill 都推成旗舰

## 3. 家族矩阵

| 家族 | 旗舰位 | 增长变体 | 支撑变体 | 暂缓/说明 |
| --- | --- | --- | --- | --- |
| Twitter / X | `aisa-twitter-api` | `aisa-twitter-engagement-suite` | `aisa-twitter-command-center`, `aisa-twitter-post-engage` | `x-intelligence-automation` 先保留为实验名，不抢旗舰词 |
| Search / Research | `search` | `aisa-multi-search-engine`, `multi-source-search` | `web-search`, `scholar-search`, `smart-search`, `tavily-search`, `tavily-extract`, `perplexity-search`, `perplexity-research` | `openclaw-search` 主要作为兼容层 |
| YouTube | `aisa-youtube-serp-scout` | `youtube-serp` | `aisa-youtube-search`, `youtube-search`, `youtube` | `openclaw-aisa-youtube-aisa`, `openclaw-youtube` 为兼容层 |
| Market / Finance | `market` | `marketpulse`, `prediction-market` | `crypto-market-data`, `prediction-market-data`, `prediction-market-arbitrage`, `stock-*`, `us-stock-analyst` | 先分“宽盘数据”和“细分策略” |
| LLM / Provider | `llm-router` | `cn-llm` | `aisa-provider` | 先不与其它家族抢资源 |
| Media | `media-gen` | `openclaw-media-gen` | - | 结构简单，可后置推进 |
| 综合研究 | `last30days` | `last30days-zh` | - | 这条线先以 suspicious 风险控制为优先，不先做爆款化扩写 |

## 4. 执行顺序

### 第 1 波：先收 Twitter 家族

目标：

- 明确 `aisa-twitter-api` 是唯一旗舰位
- 让 `aisa-twitter-engagement-suite` 抢“engagement / reply / follow / like”高意图词
- 让 `aisa-twitter-command-center` 改成监控 / watchlist / trend desk
- 让 `aisa-twitter-post-engage` 收到“发布后跟进”场景

原因：

- 当前证据最强
- 当前线上 suspicious 问题也集中在这一家
- 改完后最容易形成“旗舰 + 兄弟位 + plugin 修复”的完整闭环

### 第 2 波：推进 Search / YouTube

目标：

- `search` 稳住统一旗舰
- `multi-source-search` 抢 verification / confidence / compare
- `aisa-multi-search-engine` 抢 multi-engine / one-key / one-surface
- `aisa-youtube-serp-scout` 抢 content research / competitor tracking / trend discovery

### 第 3 波：推进 Market / Finance

目标：

- `market` 做宽盘旗舰
- `marketpulse` 抢 equities + filings + analyst estimates
- 预测市场与 stock 子工具全部降到细分高意图词，不再和宽盘旗舰正面冲突

### 第 4 波：推进 LLM / Media / 长尾实验

- `llm-router`
- `cn-llm`
- `media-gen`
- `x-intelligence-automation`
- 其余长尾 skill

## 5. 这一轮建议你接下来做什么

优先级从高到低：

1. 先把 Twitter 家族发布层重建并重新看 suspicious 结果
2. 再跑 Search / YouTube 的第一轮爆款改造
3. 最后再扩 Market / Finance

推荐命令：

```bash
python3 scripts/build_clawhub_release.py
python3 scripts/build_clawhub_plugin_release.py
python3 scripts/build_claude_release.py
python3 scripts/build_claude_marketplace.py
python3 scripts/build_hermes_release.py
python3 scripts/test_release_layers.py
```

如果要只看 AISA API 改造目标，可先用：

```bash
python3 scripts/llm_refine_aisa_skills.py --plan
```

## 6. 本轮已执行动作

- 修复了 unified pipeline 调度频率的文档漂移：
  - 现在统一为每 4 小时一次（`21 */4 * * *`）
- 新增本分层执行计划文档
- 下一步直接按本计划先执行 Twitter 家族的第一批母 skill 收口
