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
  - `ClawScan / OpenClaw verdict = suspicious`
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
  - `ClawScan / OpenClaw verdict = suspicious`
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
9. 忽略 `Static analysis` 第三维扫描结论

## 本仓库今后默认采用的修改动作

### 母版层

- 如果 skill 已存在于 `AIsa-team/agent-skills@main`，先以该上游版本为基线
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

1. 看它是否已存在于 `AIsa-team/agent-skills@main`
2. 确认这次修改是不是只动 publish surface
3. 核对 env / manifest / README / `SKILL.md` 是否一致
4. 检查是否新增了 relay、upload、OAuth、home-dir persistence 等真实 side effects
5. 检查发布包里是否混入非运行时文件
6. live scan 时把 `pending`、`clean`、`suspicious` 分开记录

<!-- AUTO-DIAGNOSIS:BEGIN -->
## 最新自动诊断快照

- 诊断对象数：`15`
- `blocker`：`14`
- `warning`：`1`
- `pending`：`3`

### 当前高频规则

- `metadata_env_mismatch`: `1`
- `oauth_upload_side_effects`: `3`
- `pending_scan`: `3`
- `platform_trust_gap`: `8`
- `relay_trust_surface`: `3`
- `static_analysis_patterns`: `1`

### 当前重点对象

- `plugin:aisa-perplexity-search-sonar-plugin`
  severity: `blocker` | status: `pending`
  rules: `pending_scan, relay_trust_surface`
  reason: The search client mostly matches its purpose, but the published requirement metadata conflicts with the bundled manifests and code about needing Python and an AISA_API_KEY.
- `plugin:aisa-tavily-search-plugin`
  severity: `blocker` | status: `suspicious`
  rules: `static_analysis_patterns`
  reason: Detected: suspicious.env_credential_access
- `plugin:last30days-plugin`
  severity: `blocker` | status: `pending`
  rules: `pending_scan`
  reason: This looks mostly like a legitimate recent-research skill, but its published metadata understates the credentials, binaries, and network behavior that the bundled skill actually uses.
- `skill:openclaw-twitter`
  severity: `blocker` | status: `suspicious`
  rules: `oauth_upload_side_effects`
  reason: The skill can perform public Twitter/X posting and is instructed to try publishing directly when posting intent is detected.
- `skill:prediction-market`
  severity: `blocker` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: The skill provides raw on-chain betting transactions and weak project provenance for a real-money market.
- `skill:prediction-market-arbitrage`
  severity: `blocker` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: The skill uses unpinned dependency installs and a broad `update --all`, plus a disclosed recurring monitoring loop.
- `skill:smart-search`
  severity: `blocker` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: The skill uses purpose-aligned shell and Docker tooling, but unsafe .env sourcing and the broad persistent SearX deployment need review.
- `skill:stock-analysis`
  severity: `blocker` | status: `suspicious`
  rules: `relay_trust_surface`
  reason: Optional third-party CLI installation and user-configured cron automation are disclosed and purpose-aligned, but users should review them before enabling.
- `skill:tavily-extract`
  severity: `blocker` | status: `suspicious`
  rules: `oauth_upload_side_effects`
  reason: The main concern is automatic execution of an unpinned npm OAuth helper during first-run authentication.
- `skill:twitter-autopilot`
  severity: `blocker` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: Direct public Twitter/X mutation commands and optional autonomous cron operation create material public-action risk, though the behavior is disclosed and purpose-aligned.
- `skill:web-search`
  severity: `blocker` | status: `suspicious`
  rules: `platform_trust_gap`
  reason: This skill should be used when users need to search the web for information, find current content, look up news articles, search for images, or find videos. It uses DuckDuckGo's search API to return results in clean, formatted output (text, markdown, or JSON). Use for research, fact-checking, finding recent information, or gathering web resources.
- `skill:x-intelligence-automation`
  severity: `blocker` | status: `suspicious`
  rules: `metadata_env_mismatch, oauth_upload_side_effects, platform_trust_gap, relay_trust_surface`
  reason: The skill is broadly coherent with a Twitter/X automation client using the AIsa relay, but there are a few mismatches you should be aware of before installing (undeclared env overrides and uploading local files to an external relay).
<!-- AUTO-DIAGNOSIS:END -->
