# GitHub Actions And ClawHub Review 2026-05-11

## Scope

本轮按“先计划后执行”的方式处理四件事：

- 解释为什么会出现“没有可用 self-hosted runner”
- 以资深测试工程师视角 review GitHub Actions / CI 脚本
- 以 AI 工程视角修复测试发现的问题
- 继续刷新 ClawHub suspicious 状态和 breakout skill/plugin 推进状态

## Self-Hosted Runner 结论

当前仓库 runner 库存：

- GitHub API: `repos/baofeng-tech/agent-skills-io/actions/runners`
- Result: `total_count=0`

这表示 GitHub 仓库层面没有注册任何 repository self-hosted runner。

什么情况下“有 runner”：

1. 在 GitHub 仓库、组织或 enterprise runner 页面注册过 runner。
2. runner 服务正在运行并显示 `online`。
3. workflow 的 `runs-on` label 全部能匹配该 runner。
4. runner group 允许这个 repository 使用。
5. preflight 使用的 token 有权限读取 runner inventory。

什么情况下“没有可用 runner”：

1. `total_count=0`，仓库没有注册 repository runner。
2. 注册过 runner 但机器关机、服务停止、离线或被删除。
3. `SELF_HOSTED_RUNNER_RUNS_ON_JSON` 指定的 label 不匹配任何 online runner。
4. runner 在 organization 层，但仓库 owner 是个人账号或 runner group 未授权本 repo。
5. `SELF_HOSTED_RUNNER_API_TOKEN` 看不到 runner inventory，导致 preflight 无法确认 runner。

关键点：`SELF_HOSTED_RUNNER_RUNS_ON_JSON` 只选择 label，不会创建、注册或启动 runner。

## Latest Remote Run Review

拉取后当前 HEAD：

- `e56a822375fb53eb9f9d56fb892d99745a97a1a0`

最新远端 run：

- Run: `25638481528`
- Created: `2026-05-10T20:05:23Z`
- Head SHA: `e56a822375fb53eb9f9d56fb892d99745a97a1a0`
- Conclusion: `failure`
- Failing job: `sync-build-test`
- Failing step: `Run AISA API skill regression`

这次失败不是 self-hosted runner 直接导致的。`sync-build-test` 在 GitHub-hosted runner 上先失败，后面的 `self-hosted-preflight`、publish、suspicious repair、breakout rollout 都因为前置 job 失败而 skipped。

## Test Engineer Findings

### 1. Current-HEAD Actions 失败点是 prediction-market 客户端 bug

Severity: blocker

`prediction-market-data` 和 `prediction-market-arbitrage` 的 `scripts/prediction_market_client.py polymarket markets --limit 1` 收到合法 JSON list 后会打印结果，但随后执行：

```python
result.get("success", True)
```

list 没有 `.get()`，因此成功响应被客户端自己变成 `AttributeError`，CI 报 hard failure。

### 2. 上游 all-sync 会重新带回同类 bug

Severity: blocker

这两个 runtime 文件来自 `AIsa-team/agent-skills` 上游同步。只手改 `targetSkills/` 会在下一次 `selection=all` 时被覆盖，所以需要在 pipeline 同步后自动硬化。

### 3. self-hosted runner 状态和本次失败容易混淆

Severity: warning

仓库 runner inventory 仍然是 `total_count=0`，但最新 run 失败位置在 hosted AISA regression，尚未走到 runner preflight。结论应分开表达：

- 当前 run 的直接失败原因是 AISA regression 客户端 bug。
- 仓库确实没有注册 self-hosted runner。
- 修复 regression 后，continuation lane 会由 preflight 决定使用真实 self-hosted runner、hosted fallback，或 fail-fast。

### 4. ClawHub diagnosis 旧快照偏重

Severity: warning

拉取后的旧 diagnosis 显示 `11` 个 suspicious blocker。重新 live refresh 后，当前剩余 suspicious 降到 `8` 个 blocker，且都不是已知自有账号 `baofeng-tech`、`bibaofeng`、`aisadocs`。

## Engineering Fixes

### Prediction-market runtime hardening

修复位置：

- `targetSkills/prediction-market-data/scripts/prediction_market_client.py`
- `targetSkills/prediction-market-arbitrage/scripts/prediction_market_client.py`
- 由构建脚本同步到所有 release layers

修复内容：

- 增加 `api_result_ok()`，允许成功的非 dict JSON payload 正常退出。
- 增加 `decode_json_body()`，把 JSON list 包装成 `{"success": true, "data": ...}`。
- 将非 JSON upstream 响应转成 `UPSTREAM_NON_JSON` 结构化错误。
- 将 `TimeoutError` / `OSError` 归为 `NETWORK_ERROR`。

### Pipeline recurrence guard

修复位置：

- `scripts/unified_skill_pipeline.py`
- `scripts/test_github_actions_workflow.py`

修复内容：

- 新增 `harden_prediction_market_client()`。
- `sync_skill()` 在每次 upstream copy 后调用 `harden_synced_skill_runtime()`。
- workflow guard 新增临时 fixture，验证 hardening 会添加 JSON decoder、list-safe exit、timeout/network error handling，并保持幂等。

## ClawHub Status After Refresh

Live status refresh:

- Total artifacts: `120`
- Suspicious: `8`
- Pending: `1`

Owned suspicious remediation plan:

- `--owned-only --severity blocker --status suspicious`: `0` artifacts
- `--owned-only --severity all --status pending`: `0` artifacts

Remaining suspicious blockers are external publisher artifacts:

- `skill:prediction-market`
- `skill:smart-search`
- `skill:stock-analysis`
- `skill:tavily-extract`
- `skill:twitter-autopilot`
- `skill:web-search`
- `skill:youtube`
- `skill:youtube-search`

The remaining pending warning is:

- `plugin:aisa-twitter-research-engage-plugin`
- Publisher: `Convex`

Because these are not owned by the configured publishing handles, this pass did not publish fallback slugs or claim them as repaired.

## Breakout Rollout Status

Declared breakout variants remain:

- `aisa-twitter-api -> aisa-twitter-api-command-center @ 1.0.3`
- `aisa-twitter-engagement-suite -> aisa-twitter-research-engage-relay @ 1.0.6`
- `aisa-twitter-engagement-suite -> twitter-post-aisa @ 1.0.3`
- `aisa-tavily -> aisa-tavily-search @ 1.0.3`

Current live artifact status:

- `skill:aisa-twitter-api-command-center`: clean
- `plugin:aisa-twitter-api-command-center-plugin`: clean
- `skill:aisa-twitter-research-engage-relay`: clean
- `plugin:aisa-twitter-research-engage-relay-plugin`: clean
- `skill:twitter-post-aisa`: clean
- `plugin:twitter-post-aisa-plugin`: clean
- `skill:aisa-tavily-search`: clean
- `plugin:aisa-tavily-search-plugin`: clean

No breakout live drift was found in this pass.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_github_actions_workflow.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_batch_publish_exit.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_plugin_auth_metadata.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_twitter_oauth_client_safety.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_aisa_api_skills.py --skills prediction-market-data,prediction-market-arbitrage --timeout 45 --retries 0 --delay 0.25 --report /tmp/aisa-api-regression-prediction-market-fix.json`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_release_layers.py`: passed
