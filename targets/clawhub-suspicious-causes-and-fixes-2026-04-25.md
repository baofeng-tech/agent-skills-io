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

- 诊断对象数：`61`
- `blocker`：`20`
- `warning`：`41`
- `pending`：`36`

### 当前高频规则

- `metadata_env_mismatch`: `18`
- `oauth_upload_side_effects`: `7`
- `pending_scan`: `44`
- `platform_trust_gap`: `13`
- `prompt_scaffold_copy`: `1`
- `relay_trust_surface`: `12`

### 当前重点对象

- `plugin:last30days-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan`
  reason: The package appears to implement a legitimate AIsa-backed research tool, but the manifest and bundled runtime disagree with the registry metadata about required secrets and there are a few runtime behaviors (local HTTP probes, bundled executable scripts) that warrant caution before installing.
- `plugin:market-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap`
  reason: The package is plausibly what it claims (a market data client) and only needs a single API key, but there are internal inconsistencies in the manifest/registry metadata (missing required env/binary declarations) that should be resolved before trusting it.
- `plugin:openclaw-twitter-post-engage-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: The package's code and SKILL.md are coherent with a Twitter/X engagement/posting skill (using an AIsa relay) but the registry metadata and top-level claims contradict the actual requirements and there is reliance on a third-party relay (AISA_API_KEY) that the user must trust.
- `plugin:smart-search-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, relay_trust_surface`
  reason: The package is plausibly a search client that contacts aisa.one and requires an AISA_API_KEY and python3, but the registry metadata omits those requirements and there are manifest mismatches you should confirm before installing.
- `plugin:stock-analysis-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, relay_trust_surface`
  reason: The package mostly matches a stock-analysis skill, but the published registry metadata (saying no env vars/credentials required) contradicts the embedded plugin and SKILL.md which require an AISA_API_KEY and contact an external AIsa API — this mismatch should be clarified before installing.
- `plugin:twitter-command-center-search-post-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: The package is functionally aligned with its Twitter/X posting/search purpose, but it relies on an external relay (api.aisa.one) that will receive your AISA_API_KEY and any uploaded media, and the runtime reads a few environment variables that the manifest/SKILL.md don't fully declare — you should review/trust the relay before installing.
- `plugin:youtube-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, pending_scan, platform_trust_gap, relay_trust_surface`
  reason: The package mostly does what it says (YouTube research via AIsa) but the manifest/registry metadata and the bundled skill disagree about required environment variables and runtime, and the skill will send your AISA_API_KEY to api.aisa.one — confirm you trust that upstream and the pkg metadata before installing.
- `plugin:youtube-search-plugin`
  severity: `blocker` | status: `pending`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, pending_scan, relay_trust_surface`
  reason: The package is internally inconsistent: it is named 'Youtube Search' but the bundled skill and manifests describe Twitter/X search/posting and require an AISA_API_KEY; functionality and naming don't line up even though the runtime footprint itself is small.
- `skill:aisa-provider`
  severity: `blocker` | status: `suspicious`
  rules: `relay_trust_surface`
  reason: The skill's declared requirements (only AISA_API_KEY) match its stated purpose, but the runtime instructions reference shipped scripts and flows that are not present and make strong external-claims (partnerships, ZDR) that should be verified before use.
- `skill:aisa-twitter`
  severity: `blocker` | status: `suspicious`
  rules: `metadata_env_mismatch, platform_trust_gap, relay_trust_surface`
  reason: The package is a coherent Twitter/X relay client that contacts api.aisa.one and requires an AISA_API_KEY, but the registry metadata and package frontmatter disagree about required env and versioning—confirm the missing environment declaration and trust in the relay before installing.
- `skill:aisa-twitter-api`
  severity: `blocker` | status: `suspicious`
  rules: `oauth_upload_side_effects, relay_trust_surface`
  reason: The skill does what its name/description claim (search/post to X) but routes all traffic, OAuth, and uploaded media through a third-party relay (aisa.one) and has a few minor mismatches that increase privacy/exfiltration risk.
- `skill:openclaw-aisa-youtube-aisa`
  severity: `blocker` | status: `suspicious`
  rules: `metadata_env_mismatch, platform_trust_gap`
  reason: The skill's code and SKILL.md match the described YouTube search purpose and only require an AISA API key, but the registry metadata incorrectly omits that required credential and overall provenance (homepage/owner) is thin — this mismatch warrants caution before installing.
<!-- AUTO-DIAGNOSIS:END -->
