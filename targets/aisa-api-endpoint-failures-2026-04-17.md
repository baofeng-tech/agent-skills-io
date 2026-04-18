# AISA API Endpoint Failures (2026-04-17)

本清单只记录在本次 `targetSkills` 测试中已被脚本调用和直接 `curl` 双重复核的问题接口，方便后续对上游排查。

## 结论

以下异常已经确认不是本地 CLI 参数错误，也不是 Python 运行环境问题，而是接口层面返回异常：

- `unsupported uri`
- `429 upstream_error`
- `500 Internal Server Error`
- `503 Service Unavailable`

## 已复核失效接口

| Endpoint | Method | 关联 skill | 现象 | 结论 |
|---|---|---|---|---|
| `/financial/crypto/prices/snapshot` | GET | `market`, `marketpulse` | `{"error":"unsupported uri"}` | 上游节点当前不可用 |
| `/financial/crypto/prices` | GET | `market`, `marketpulse` | `{"error":"unsupported uri"}` | 上游节点当前不可用 |
| `/scholar/search/smart` | POST | `search`, `smart-search`, `multi-search`, `aisa-multi-search-engine` 等 | `{"error":"unsupported uri"}` | Smart 搜索节点当前不可用 |
| `/search/smart` | POST | 部分文档引用、历史兼容路径 | `{"error":"unsupported uri"}` | 历史路径已退役或不可用 |
| `/financial/analyst/eps` | GET | `market`, `marketpulse`, `us-stock-analyst` | `{"error":"unsupported uri"}` 或上游 500 | 当前不可稳定使用 |
| `/financial/insider/trades` | GET | `market`, `marketpulse`, `us-stock-analyst` | `{"error":"unsupported uri"}` 或上游 500 | 当前不可稳定使用 |

## endpoint 到仓库调用点映射

### `/financial/crypto/prices/snapshot`

- 直接脚本调用：
  - `targetSkills/market/scripts/market_client.py`
  - `targetSkills/marketpulse/scripts/market_client.py`
- SKILL / README 文档引用：
  - `targetSkills/market/SKILL.md`
  - `targetSkills/marketpulse/SKILL.md`

### `/financial/crypto/prices`

- 直接脚本调用：
  - `targetSkills/market/scripts/market_client.py`
  - `targetSkills/marketpulse/scripts/market_client.py`
- SKILL / README 文档引用：
  - `targetSkills/market/SKILL.md`
  - `targetSkills/marketpulse/SKILL.md`

### `/scholar/search/smart`

- 直接脚本调用：
  - `targetSkills/search/scripts/search_client.py`
  - `targetSkills/openclaw-search/scripts/search_client.py`
  - `targetSkills/smart-search/scripts/search_client.py`
  - `targetSkills/multi-search/scripts/search_client.py`
  - `targetSkills/web-search/scripts/search_client.py`
  - `targetSkills/scholar-search/scripts/search_client.py`
  - `targetSkills/tavily-search/scripts/search_client.py`
  - `targetSkills/tavily-extract/scripts/search_client.py`
  - `targetSkills/perplexity-research/scripts/search_client.py`
  - `targetSkills/aisa-multi-search-engine/scripts/search_client.py`
  - `targetSkills/aisa-multi-search-engine/index.ts`
- SKILL / README 文档引用：
  - `targetSkills/search/SKILL.md`
  - `targetSkills/openclaw-search/SKILL.md`
  - `targetSkills/aisa-multi-search-engine/SKILL.md`

### `/search/smart`

- 当前主要出现在文档与示例中：
  - `targetSkills/youtube-search/SKILL.md`
  - `targetSkills/openclaw-search/SKILL.md`
  - `targetSkills/search/SKILL.md`
  - `targetSkills/search/README.md`
- 结论：
  - 这是历史兼容路径或旧文档残留，不应再作为主调用路径依赖。

### `/financial/analyst/eps`

- 直接脚本调用：
  - `targetSkills/market/scripts/market_client.py`
  - `targetSkills/marketpulse/scripts/market_client.py`
  - `targetSkills/us-stock-analyst/scripts/stock_analyst.py`
- SKILL / README 文档引用：
  - `targetSkills/market/SKILL.md`
  - `targetSkills/marketpulse/SKILL.md`
  - `targetSkills/us-stock-analyst/SKILL.md`
  - `targetSkills/us-stock-analyst/README.md`

### `/financial/insider/trades`

- 直接脚本调用：
  - `targetSkills/market/scripts/market_client.py`
  - `targetSkills/marketpulse/scripts/market_client.py`
  - `targetSkills/us-stock-analyst/scripts/stock_analyst.py`
- SKILL / README 文档引用：
  - `targetSkills/market/SKILL.md`
  - `targetSkills/marketpulse/SKILL.md`
  - `targetSkills/us-stock-analyst/SKILL.md`
  - `targetSkills/us-stock-analyst/README.md`

## 已复核拥塞接口

| Endpoint | Method | 关联 skill | 现象 | 结论 |
|---|---|---|---|---|
| `/v1/models/gemini-3-pro-image-preview:generateContent` | POST | `media-gen`, `openclaw-media-gen` | `429 upstream_error` | 上游负载饱和，不是本地脚本故障 |

### `/v1/models/gemini-3-pro-image-preview:generateContent`

- 直接脚本调用：
  - `targetSkills/media-gen/scripts/media_gen_client.py`
  - `targetSkills/openclaw-media-gen/scripts/media_gen_client.py`
- SKILL / README 文档引用：
  - `targetSkills/media-gen/SKILL.md`
  - `targetSkills/media-gen/README.md`
  - `targetSkills/openclaw-media-gen/SKILL.md`

## 已观察到但未单独列为“unsupported uri”的上游不稳定接口

这些接口本次不是 `unsupported uri`，但真实分析时出现了 `500` 或 `503`，也值得一并反馈给上游：

| Endpoint | Method | 关联 skill | 现象 |
|---|---|---|---|
| `/scholar/search/web` | POST | `us-stock-analyst`，以及多组 search wrapper | 在 `us-stock-analyst` 实测中出现 `500 Internal Server Error` |
| `/v1/chat/completions` | POST | `us-stock-analyst`，以及大量 LLM 类 skill | 在 `us-stock-analyst` 实测中出现 `503 Service Unavailable`；但其它 skill 并非始终失败，说明更像上游波动而非永久下线 |

## 不属于接口失效、但已确认的本地调用层问题

这些问题在本次复测中更像 prompt / tool binding 不稳定，而不是某个固定 endpoint 已失效：

| Skill | 现象 | 结论 |
|---|---|---|
| `stock-hot` | `--output json` 时返回“当前没有实时金融工具访问”的兜底文案，未附 JSON | 更像模型未拿到工具或未遵循输出约束 |
| `stock-dividend` | `--output json` 时仅返回“正在抓取数据”的占位回复，未附 JSON | 更像 prompt wrapper 质量问题，不是明确的 API 路径失效 |

补充说明：

- `stock-analysis` 与 `stock-rumors` 在同轮复测中可以成功返回 JSON
- 因此这组问题暂不归入 `unsupported uri / 429 / 500 / 503` 清单，而应单独作为本地调用层整改项跟踪

## 已复核正常接口

这些接口本次可作为对照组，说明网络、认证和基础调用链路本身是通的：

| Endpoint | Method | 说明 |
|---|---|---|
| `/financial/news` | GET | 股票新闻正常返回 |
| `/financial/prices` | GET | 股票历史价格正常返回 |
| `/scholar/search/scholar` | POST | scholar 搜索正常返回 |
| `/twitter/auth_twitter` | POST | Twitter OAuth 授权 URL 正常返回 |
| `/twitter/post_twitter` | POST | Twitter 发帖正常 |

## 建议后续动作

1. 与 AISA 上游确认这些节点是否已退役、迁移或灰度关闭
2. 若有替代路径，统一更新 `targetSkills/` 中所有调用点与文档
3. 对 `unsupported uri` 节点增加更清晰的降级提示，避免用户误判为本地脚本故障
