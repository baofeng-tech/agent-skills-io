# ClawHub Suspicious 原因与修复收敛（2026-04-25）

## 目的

把最近真实线上 scan 里出现的 `Suspicious` / pending / clean 差异收敛成可复用规则，并明确哪些修改属于：

- 可以继续复用的方法
- 应该写进文档和全局 skill 的能力
- 以后改 skill 时必须先检查的风险面

本文件基于这些本地状态文件整理：

- `targets/clawhub-publish-state.json`
- `targets/clawhub-live-status.json`

## 当前已确认的真实线上案例

### 1. `skill:aisa-twitter-api`

- 最近一次 live scan 记录时间：`2026-04-24T16:42:50+00:00`
- 结果：
  - `VirusTotal = benign`
  - `OpenClaw verdict = suspicious`
- 主要原因：
  - 这是 relay-based skill，真实会把 `AISA_API_KEY` 发往 `api.aisa.one`
  - OAuth 和用户批准的媒体上传都会经过 relay
  - 如果 side effects 讲得不够直白，平台会把它当成更高的 exfiltration / trust risk
- 对应修改原则：
  - 在 `SKILL.md`、README、manifest 里写清楚 network target、OAuth、media upload、secret scope
  - 只要求 `AISA_API_KEY`，不再出现密码、Cookie、浏览器凭据导出故事
  - 不默认自动发帖，不把 posting 写成静默行为

### 2. `skill:last30days`

- 最近一次 live scan 记录时间：`2026-04-24T16:47:54+00:00`
- 结果：
  - `VirusTotal = benign`
  - `OpenClaw verdict = suspicious`
- 主要原因：
  - 公共 `SKILL.md` 里存在过强、过于“提示词化”的说明方式
  - scanner 明确提到 prompt-injection pattern / highly prescriptive prompts
- 对应修改原则：
  - 公共 skill 面不要暴露内部 prompt scaffold
  - 不要出现像“忽略上层规则”“始终执行某策略”这类平台易误判的写法
  - 保留功能，但把公开说明收敛到用户可理解的任务边界、输入输出和 guardrails

### 3. `plugin:aisa-twitter-api-plugin`

- 最近一次 live scan 记录时间：`2026-04-24T16:42:48+00:00`
- 结果：
  - `scan_status = clean`
  - `suspicious = false`
- 但仍暴露一个重要问题：
  - 扫描说明点到了 registry / manifest / `SKILL.md` 之间存在 env requirement mismatch
  - 也就是某个层面漏写了 `AISA_API_KEY`
- 对应修改原则：
  - `SKILL.md`
  - README
  - `.claude-plugin/plugin.json`
  - `openclaw.plugin.json`
  - `package.json`
  - registry-facing metadata
  - 这些地方的 env requirements 和实际 side effects 必须一致

### 4. `skill:multi-source-search` 与新发布 relay skill

- 当前状态里既有 `pending`，也有 `detail_url` 已可访问但 `scan_status` 仍为空的情况
- 这类状态不能直接当成 clean，也不能直接当成 suspicious
- 对应修改原则：
  - `pending / unresolved / clean / suspicious` 分开记录
  - live page 还没稳定时继续轮询，不要误判

## 这次要内化成长期能力的风险分类

1. relay / third-party API trust surface 说得不够清楚
2. media upload / OAuth / external write 没有显式说明
3. 公共 `SKILL.md` 出现 prompt-injection 风格或过强内部提示词
4. registry / manifest / README / `SKILL.md` 的 env 和 side effects 不一致
5. 发布包还夹带 test / compare / sync / dev helper
6. 默认写入用户 home 或缓存同步行为
7. 留着 Cookie / Keychain / browser credential 类能力入口
8. 把 pending scan 当成最终结论

## 本仓库今后默认采用的修改动作

### 母版层

- 如果 skill 已存在于 `AIsa-team/agent-skills@agentskills`，先以该上游版本为基线
- 不在“优化文案”的名义下删功能或改功能
- 真正需要保守收窄时，优先放到发布层

### 发布层

- runtime-only 打包
- 去掉 compare / test / sync / migration / dev helper
- 统一 repo-local persistence
- 对 relay、OAuth、upload、posting 写清 side effects

### 审计层

- 把 `pending` 和 `suspicious` 区分开
- 对 EN / ZH 和 skill / plugin 变体做同样的 trim
- 对 live scan 返回的具体文案做“原因 -> 最小修复”映射，而不是泛泛地说安全

## 已同步进方法体系的对象

这份经验已经要求同步到：

- `targets/skill-modification-rules-2026-04-19.md`
- `targets/platform-skill-plugin-methodology.md`
- `clawhub-skill-optimizer-all`
- `clawhub-plugin-packager-all`
- `clawhub-security-auditor-all`

## 最小执行清单

以后每次改 skill / plugin，默认先做这 6 步：

1. 看它是否已存在于 `AIsa-team/agent-skills@agentskills`
2. 确认这次修改是不是只动 publish surface
3. 核对 env / manifest / README / `SKILL.md` 是否一致
4. 检查是否新增了 relay、upload、OAuth、home-dir persistence 等真实 side effects
5. 检查发布包里是否混入非运行时文件
6. live scan 时把 `pending`、`clean`、`suspicious` 分开记录

<!-- AUTO-DIAGNOSIS:BEGIN -->
## 最新自动诊断快照

- 诊断对象数：`10`
- `blocker`：`9`
- `warning`：`1`
- `pending`：`7`

### 当前高频规则

- `metadata_env_mismatch`: `9`
- `oauth_upload_side_effects`: `2`
- `pending_scan`: `9`
- `platform_trust_gap`: `9`
- `relay_trust_surface`: `8`

### 当前重点对象

- `plugin:aisa-multi-search-engine-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan`
  reason: Detected: suspicious.env_credential_access
- `plugin:aisa-twitter-api-command-center-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: The package is largely coherent with a Twitter/X relay client (it needs AISA_API_KEY and sends reads/posts to api.aisa.one), but there are metadata inconsistencies and privacy implications you should verify before installing.
- `plugin:aisa-twitter-post-engage-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: The package is largely coherent for a Twitter/X relay-based engagement and OAuth posting skill, but there are metadata inconsistencies (the registry metadata claims no required credentials while the shipped manifests and scripts require AISA_API_KEY) that should be clarified before installing.
- `skill:aisa-multi-search-engine`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This skill is internally consistent and appears to do what it claims: query AIsa endpoints and synthesize results. Before installing, confirm you trust the AIsa service (https://aisa.one) because any queries, provided URLs, and extracted page contents will be sent to that external API using your AISA_API_KEY. Do not submit private/internal URLs or sensitive documents unless your organizational policy allows sending them to an external service. If you want an extra check, inspect the bundled index.ts and scripts/search_client.py (already included) to verify there is no unexpected behavior, and consider using a scoped API key or monitoring usage/quotas on the AIsa account. If you need stricter guarantees about data handling, request the provider's privacy/data-retention policy before use. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 🔎 Clawdis Bins python3, node Env
- `skill:aisa-twitter-research-engage-relay`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This package appears internally consistent with its stated purpose. Before installing, consider: 1) You must provide an AISA_API_KEY — that key grants the skill the ability to act through the AIsa relay (likes, follows, posts, media uploads). Only supply the key if you trust the AIsa service/operator. 2) The scripts will upload any local workspace files you explicitly attach (images/videos) to api.aisa.one for posting—do not attach private files you don't want sent. 3) The package source and homepage are missing; if you need stronger assurance, review the included Python files yourself or validate the AIsa operator and API privacy/policies. 4) The skill can be invoked by the agent (normal default); if you want to restrict autonomous actions, avoid giving the agent broad autonomous permissions or invoke the skill only on demand. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 🐦 Clawdis Bins python3 Env
- `skill:market`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This package appears coherent: it needs one API key (AISA_API_KEY) and python3 and contains a simple client that calls https://api.aisa.one. Before installing, verify you trust the AIsa service and owner (the skill's source/homepage is unknown), avoid using high-privilege or long-lived production keys, and monitor the API key's usage. You can inspect scripts/market_client.py (bundled) to confirm no unexpected behavior. If you plan to use it in an automated agent, consider limiting capabilities and rotating the key regularly. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 📊 Clawdis Bins python3 Env
- `skill:marketpulse`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This skill appears coherent: it only needs python3 and an AISA_API_KEY to query AIsa's market API. Before installing, confirm you trust the AIsa service (aisa.one) and are comfortable providing its API key to the agent. Keep the API key secret, review provider terms/rate limits, and avoid installing this into highly privileged environments where network egress to third-party APIs is restricted. If you need higher assurance, verify the AIsa API key usage and inspect network logs when the skill runs. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 📊 Clawdis Bins python3 Env
- `skill:multi-source-search`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This skill legitimately needs and uses a single AISA_API_KEY to call api.aisa.one (which proxies web, scholar, Tavily, and Perplexity flows). Before installing: (1) Only provide an API key you trust the aisa.one service with — do not use highly privileged or long-lived keys if you can avoid it. (2) Avoid sending sensitive or private data to the skill because queries are sent to the external API. (3) Review the bundled scripts (scripts/search_client.py) if you want extra assurance — it only builds HTTP requests to aisa.one and reads AISA_API_KEY from the env. (4) Run the skill in a least-privileged environment or with a scoped key and monitor usage on your aisa.one account. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 🔎 Clawdis Bins python3 Env
- `skill:us-stock-analyst`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: This package appears internally consistent, but before installing consider: (1) Only provide an AISA_API_KEY you trust—this key grants the skill access to your AIsa account and usage/billing. Use a least-privilege or test key if possible. (2) The skill sends any analysis input (tickers, prompts, fetched content) to api.aisa.one including LLM prompts—do not send sensitive personal data. (3) Review the full scripts locally if you want assurance they won't call other endpoints or write sensitive local files; the code shown makes only HTTP calls to api.aisa.one and prints/saves reports. (4) Be aware of cost implications: SKILL.md mentions per-analysis costs. If you want extra assurance, run the included test_api_data.py in a sandbox environment with a test API key first. Like a lobster shell, security has layers — review code before you run it. Runtime requirements 📊 Clawdis Bins python3 Env
- `skill:prediction-market`
  severity: `warning` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: Participate in Base's GTM by betting if today's 18:00 UTC garden temperature will be higher or lower than yesterday's, sharing winnings from the pot.
<!-- AUTO-DIAGNOSIS:END -->
