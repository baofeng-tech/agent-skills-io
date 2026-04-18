# targetSkills Test Matrix (2026-04-17)

本次测试优先覆盖 `targetSkills/` 中可独立执行的 skill，先跑无副作用或低副作用链路，再记录需要人工协助、实现整改、或上游恢复的部分。

## 测试环境

- Python: `3.12.9`
- Pytest: `9.0.3`
- AISA key: 来自 `example/accounts`
- 测试时间: `2026-04-17`

## 状态定义

- `PASS`: 已完成真实 smoke test，主链路可执行
- `PARTIAL`: 可运行，但结果质量、召回、或部分子能力存在问题
- `BLOCKED`: 受实现形态、人工交互、上游状态或外部条件限制

## 唯一实现级测试结果

| 组别 | 代表 skill / 实现 | 状态 | 说明 |
|---|---|---:|---|
| Twitter 只读搜索 | `aisa-twitter-command-center`, `aisa-twitter-api`, `openclaw-twitter`, `twitter-command-center-search-post` | PASS | `search`、`status`、`authorize` URL 生成通过 |
| Twitter 互动封装 | `aisa-twitter-post-engage`, `aisa-twitter-engagement-suite`, `twitter`, `twitter-autopilot`, `x-intelligence-automation` | PASS | OAuth 完成后已验证 `like` / `unlike` / `follow` / `unfollow` |
| YouTube 搜索 | `aisa-youtube-serp-scout`, `youtube`, `openclaw-youtube`, `aisa-youtube-search`, `youtube-search` | PASS | 真实 YouTube 搜索返回结果 |
| CN LLM / Router / Provider | `cn-llm`, `llm-router`, `aisa-provider` | PASS | 模型列表、provider probe 正常 |
| 搜索聚合 | `search`, `multi-search`, `openclaw-search`, `perplexity-search`, `perplexity-research`, `scholar-search`, `smart-search`, `tavily-search`, `tavily-extract`, `web-search`, `aisa-tavily`, `aisa-multi-search-engine` | PARTIAL | Web / Sonar / Verity / Tavily 可跑；`smart` 与部分 URI 仍有 `unsupported uri` |
| Market / Marketpulse | `market`, `marketpulse` | PARTIAL | 股票新闻、价格可跑；`crypto snapshot` 仍报 `unsupported uri` |
| Prediction Market | `prediction-market`, `prediction-market-data`, `prediction-market-data-zh`, `prediction-market-arbitrage`, `prediction-market-arbitrage-api`, `prediction-market-arbitrage-zh` | PASS | 市场列表、套利扫描命令可执行 |
| last30days | `last30days` | PASS | `test-aisa-provider.py`、`test-aisa-planner.py`、主流程均已跑通 |
| last30days-zh | `last30days-zh` | PASS | `test-aisa-provider.py`、`test-aisa-planner.py` 已跑通 |
| Stock analysis prompt wrappers | `stock-hot`, `stock-dividend`, `stock-analysis`, `stock-rumors` | PARTIAL | 已补 `--output json` 结构化提取；`stock-analysis`、`stock-rumors` 可稳定返回 JSON，`stock-hot`、`stock-dividend` 仍未稳定按约定输出 |
| Stock stateful utilities | `stock-portfolio`, `stock-watchlist` | PASS | `create/list/add/check` 已验证，状态文件会写入 `~/.clawdbot/skills/stock-analysis/` |
| us-stock-analyst | `us-stock-analyst` | PARTIAL | 已补标准 CLI 并验证 `--ticker AAPL --depth quick --json-only` 可执行；但上游接口仍有 `500/503` |
| Media generation | `media-gen`, `openclaw-media-gen` | BLOCKED | CLI 正常；真实图片生成时上游返回 `429` 负载饱和 |

## 关键发现

### 1. `last30days` 已从“环境阻塞”转为“可测试”

- `python3.12` 下可以完成 provider / planner probe。
- 主流程可执行，例如：
  - `targetSkills/last30days/scripts/last30days.py 'OpenAI coding agent updates' --search=grounding --quick --emit compact`
- 某些主题会出现“链路正常但召回为空”，应记为内容召回问题，而不是脚本故障。

### 2. `us-stock-analyst` 已补标准 CLI，但仍受上游稳定性影响

- 已为 `targetSkills/us-stock-analyst/scripts/stock_analyst.py` 增加标准参数入口。
- 已验证：
  - `--ticker AAPL`
  - `--depth quick`
  - `--json-only`
  - `--output /tmp/aisa-stock-analyst-aapl.json`
- 交互式 fallback 仍保留。
- 当前主要问题已从“入口不适合自动化”变为“上游接口仍出现 `500` / `503`”。

### 3. 股票类 skill 分成两类

- `stock-hot` / `stock-dividend` / `stock-analysis` / `stock-rumors`:
  - 更像 prompt wrapper，能调用但结果偏演示性质。
  - 本轮已为脚本补充 JSON block 提取，便于自动校验。
  - 复测结果进一步分化：
    - `stock-analysis AAPL --output json --fast`: 可稳定返回结构化 JSON
    - `stock-rumors --focus analyst --output json`: 可稳定返回结构化 JSON
    - `stock-hot --focus stocks --output json`: 返回“无实时金融工具访问”的兜底文案，未附 JSON
    - `stock-dividend JNJ --output json`: 只返回“正在抓取数据”的占位回复，未附 JSON
- `stock-portfolio` / `stock-watchlist`:
  - 更偏本地状态管理，行为可验证，测试信号更可靠。

### 4. Twitter 写操作仍需人工完成授权页面

- 授权 URL 可以正常生成。
- 当前终端无法直接确认浏览器中 OAuth 回调是否已完成。
- 在未明确授权完成前，不应直接测试公开发帖。

### 5. Twitter OAuth 写链路已完成真实验证

- 已生成授权 URL，并在用户确认完成授权后继续测试。
- 已成功发帖：
  - tweet id: `2044835614852628611`
  - text: `AISA relay OAuth write test 2026-04-17 01:50 CST`
- 已成功对用户自己的 tweet 执行：
  - `like-tweet`
  - `unlike-tweet`
- 已成功对 `@OpenAI` 执行：
  - `follow-user`
  - `unfollow-user`
- 对自己执行 `follow-user` 返回 `You cannot follow yourself.`，这是预期业务限制，不计为故障。

### 6. `unsupported uri` 已经通过直连接口复核

- 以下问题不只是脚本调用异常，而是直接请求 API 也返回同样结果：
  - `GET /financial/crypto/prices/snapshot`
  - `POST /scholar/search/smart`
  - `POST /search/smart`
  - `GET /financial/analyst/eps`
  - `GET /financial/insider/trades`
- 这更像上游节点退役、未开通或当前租户不可用。

### 7. `media-gen` 的阻塞属于上游容量

- 直接请求 `POST /v1/models/gemini-3-pro-image-preview:generateContent` 也返回 `429`
- 因此当前判定为上游负载饱和，而不是本地 `media_gen_client.py` 逻辑错误

## 建议执行顺序

1. 继续回归 `PASS` 组，作为基础健康检查
2. 针对 `PARTIAL` 组补“结果质量”测试，而不只看 CLI 成功
3. 优先排查 `us-stock-analyst` 依赖的上游 `500/503`
4. 等上游恢复后重试 `media-gen`
5. 人工完成 Twitter OAuth 后，再做 `post / like / follow` 写操作测试

## 建议后续整改

- 继续增强 `stock-hot` / `stock-dividend` 的结构化输出约束，避免只返回占位或兜底文案
- 排查 `market` 与 `smart-search` 的 `unsupported uri`
- 为 Twitter skill 增加更明确的“授权完成后验证”步骤
