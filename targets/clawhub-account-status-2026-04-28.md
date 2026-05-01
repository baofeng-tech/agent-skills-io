# ClawHub 三账号状态审计（2026-04-28）

## 复核方式

本轮在当前会话里重新执行了：

```bash
python3 scripts/clawhub_live_status.py --targets both --include-status published --render-mode off --request-timeout 20
python3 scripts/clawhub_suspicious_diagnosis.py --doc-mode skip
```

当前重新验证后的 live summary：

- live artifacts: `120`
- `suspicious`: `35`
- `pending`: `2`
- diagnosis artifacts: `37`
  - 说明：diagnosis 会把 `35 suspicious + 2 pending` 一并纳入规则分析

## 账号映射说明

ClawHub WSL CLI 的 `whoami` 在本机没有稳定返回，因此下面的 token -> 账号句柄映射是基于“本地发布产物 + live page publisher_handle”做的**工作推断**，不是 CLI 官方返回值。

当前自动化采用的工作映射是：

- `token-1`
  - 主要发布账号：`baofeng-tech`
- `token-2`
  - 主要发布账号：`bibaofeng`
- `token-3`
  - 主要发布账号：`aisadocs`

这个推断对当前文档归档足够用，但如果后续要做账号迁移或清库，仍建议在 Windows / self-hosted 环境再跑一次稳定的 `clawhub whoami` 复核。

## 2026-05-01 补充：slot 策略已经正式成为运行时规则

在旧 slug owner token 暂时拿不到的情况下，当前自动化不再把 owner/slug 冲突当成“必须人工停下”的异常，而是采用下面的工作规则：

1. skill 若发生 owner/slug 冲突，默认退回 `-slot1` / `-slot2` / `-slot3` fallback slug。
2. plugin 若同名 skill 已经存在 fallback slug，plugin fallback slug 必须跟随 skill，例如：
   - `aisa-provider` -> `aisa-provider-slot3`
   - `aisa-provider-plugin` -> `aisa-provider-slot3-plugin`
3. publish state 与 live status 必须把“原始 artifact key”和“当前 live fallback slug”同时保留，避免新发 slot 包继续被旧 key 的页面视图覆盖。

## 每个 token 的当前状态

### `token-1`（主要为 `baofeng-tech`）

- 已记录已发布 artifact：`56`
- `ok`: `36`
- `suspicious`: `19`
- `pending`: `1`

代表性问题对象：

- `plugin:aisa-tavily-plugin`
- `plugin:market-plugin`
- `plugin:stock-analysis-plugin`
- `plugin:youtube-plugin`
- `skill:aisa-provider`
- `skill:stock-analysis`
- `skill:stock-dividend`
- `skill:stock-rumors`
- `skill:web-search`

主要原因归类：

- registry / metadata / env mismatch
- relay / upload / API key 信任面表达不足
- 部分历史 skill 属于旧 owner，不是本轮新发布 clean 物料

### `token-2`（主要为 `bibaofeng`）

- 已记录已发布 artifact：`44`
- `ok`: `32`
- `suspicious`: `12`
- `pending`: `0`

代表性问题对象：

- `plugin:aisa-provider-plugin`
- `plugin:last30days-plugin`
- `plugin:smart-search-plugin`
- `plugin:twitter-command-center-search-post-plugin`
- `plugin:x-intelligence-automation-plugin`
- `skill:prediction-market`
- `skill:twitter-autopilot`

主要原因归类：

- metadata / registry mismatch
- relay / OAuth / media upload side effects 说明不够直白
- 个别 skill/plugin 的 live owner 不是当前主账号，属于历史 slug 继承

### `token-3`（主要为 `aisadocs`）

- 已记录已发布 artifact：`20`
- `ok`: `15`
- `suspicious`: `4`
- `pending`: `1`

代表性问题对象：

- `plugin:aisa-twitter-engagement-suite-plugin`
- `plugin:prediction-market-arbitrage-api-plugin`
- `plugin:stock-rumors-plugin`
- `plugin:youtube-search-plugin`
- `plugin:aisa-multi-search-engine-plugin` (`pending`)

主要原因归类：

- metadata / env mismatch
- relay trust 和 upload side effects 没有在 registry-facing surface 上完全说透
- `pending` 与 `suspicious` 同时存在，不能混为一个状态

## 当前最高频原因

本轮 diagnosis 高频规则：

- `metadata_env_mismatch`: `30`
- `pending_scan`: `20`
- `relay_trust_surface`: `20`
- `platform_trust_gap`: `20`
- `oauth_upload_side_effects`: `9`
- `prompt_scaffold_copy`: `1`

一句话总结：

- 最大头不是代码执行本身
- 最大头是“公开页看到的 metadata / env / trust 文案”和“真正 shipped runtime”不一致

## 已确认的“新 clean 物料”

本轮最重要的正向信号是，新的 breakout 物料已经有 clean 样本：

- `skill:aisa-twitter-api-command-center`
- `plugin:aisa-twitter-api-command-center-plugin`
- `skill:aisa-twitter-research-engage-relay`
- `plugin:aisa-twitter-research-engage-relay-plugin`

这说明：

- breakout 方向本身不是问题
- 主要问题是旧 slug、旧 live 版本、旧 registry metadata 仍在线上并存

## 本地版本与线上版本漂移

当前已发现多条“本地已改，但线上还没换新版本”的案例：

- `plugin:aisa-twitter-engagement-suite-plugin`
  - live: `1.0.2`
  - local: `1.0.3`
- `plugin:aisa-twitter-post-engage-plugin`
  - live: `1.0.2`
  - local: `1.0.3`
- `skill:aisa-twitter-api`
  - live: `1.0.4`
  - local: `1.0.5`
- `plugin:market-plugin`
  - live: `1.0.0`
  - local: `1.0.1`
- `plugin:aisa-multi-search-engine-plugin`
  - live: `1.0.0`
  - local: `1.0.2`

这意味着当前要区分三件事：

1. 本地代码是否已经修
2. 外部 GitHub 发布仓库是否已经同步
3. ClawHub live artifact 是否已经重新发布并完成新一轮扫描

## 建议的下一步

1. 优先处理仍是旧 live 版本、但本地版本已经前进的 suspicious artifact。
2. 新旧 slug 并存时，优先把 clean breakout 物料作为增长位保留。
3. 对旧 slug 的 suspicious 历史包，不要只看本地代码，要看 live page 版本和 owner。
