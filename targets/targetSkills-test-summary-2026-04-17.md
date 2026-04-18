# targetSkills 测试简报（2026-04-17）

## 结论

这轮 `targetSkills/` 全量回归的主结论是：

- 大多数核心 skill 已经可以完成真实 smoke test
- `last30days` / `last30days-zh` 已从“环境阻塞”变成“可稳定测试”
- Twitter OAuth 写链路已真实打通
- 剩余问题主要集中在：
  - 上游接口返回 `unsupported uri`
  - 上游容量或稳定性问题（`429` / `500` / `503`）
  - 个别 skill 的入口形态不适合自动化

## 已通过的重点能力

- Twitter 只读搜索：通过
- Twitter 写操作：通过
  - 已验证 `post`
  - 已验证 `like / unlike`
  - 已验证 `follow / unfollow`
- YouTube 搜索：通过
- Provider / Router / CN LLM：通过
- Prediction Market：通过
- `last30days` / `last30days-zh`：通过
- `stock-portfolio` / `stock-watchlist`：通过
- `stock-analysis` / `stock-rumors`：现已可输出结构化 JSON，适合自动校验

## 关键真实结果

### Twitter OAuth 写链路

- 成功发帖，tweet id: `2044835614852628611`
- 成功对自己的 tweet 执行 `like` 与 `unlike`
- 成功对 `@OpenAI` 执行 `follow` 与 `unfollow`

### last30days

- `test-aisa-provider.py`：通过
- `test-aisa-planner.py`：通过
- 主流程：可跑通

## 当前主要阻塞

### 1. `unsupported uri`

以下问题已经用脚本和直接 `curl` 双重确认，不是本地 CLI 参数错误：

- `market` / `marketpulse`
  - `GET /financial/crypto/prices/snapshot`
- 搜索聚合中的 smart 相关路径
  - `POST /scholar/search/smart`
  - `POST /search/smart`
- `us-stock-analyst` 依赖的部分金融节点
  - `GET /financial/analyst/eps`
  - `GET /financial/insider/trades`

这更像上游节点已下线、未开通，或当前租户不可用。

### 2. `media-gen`

- 图片生成请求可到达上游
- 但两次复测都返回上游 `429`
- 目前应判定为“上游容量阻塞”，不是本地脚本故障

### 3. `us-stock-analyst`

- 现在已经支持标准 CLI 参数入口
- 已实测 `--ticker AAPL --depth quick --json-only`
- 当前剩余问题主要是部分上游金融/LLM 接口的 `500/503`

### 4. 股票 prompt wrapper 的现状已经进一步收敛

- 已为 `stock-hot` / `stock-dividend` / `stock-analysis` / `stock-rumors` 补 JSON block 提取
- 其中：
  - `stock-analysis AAPL --output json --fast`：通过
  - `stock-rumors --focus analyst --output json`：通过
  - `stock-hot --focus stocks --output json`：仍返回无工具兜底文案
  - `stock-dividend JNJ --output json`：仍停在抓取数据占位回复
- 结论：
  - 这组 skill 仍应整体记为 `PARTIAL`
  - 但 `stock-analysis`、`stock-rumors` 已明显更适合作为自动化回归样本

## 建议优先级

1. 保持当前 `PASS` 组作为日常回归基线
2. 优先排查上游 `unsupported uri`
3. 等上游恢复后重试 `media-gen`
4. 优先把 `stock-hot` / `stock-dividend` 的 prompt 或工具约束补强
5. 后续继续排查 `us-stock-analyst` 的上游 `500/503`

## 对外汇报一句话版本

`targetSkills` 的主链路已经大面积跑通，尤其是 `last30days` 和 Twitter OAuth 写操作；当前剩余风险主要来自上游接口可用性，而不是本地脚本无法执行。
