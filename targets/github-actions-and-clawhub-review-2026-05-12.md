# GitHub Actions And ClawHub Review 2026-05-12

## Scope

本轮按单 agent 串行执行：

- 先 `git pull --ff-only`
- 复核 `SELF_HOSTED_RUNNER_RUNS_ON_JSON` 的正确配置方式
- 以测试工程师视角 review GitHub Actions / CI 脚本
- 以 AI 工程师视角修复可操作问题
- 刷新 ClawHub suspicious 与 breakout 状态
- 清理工作区并推送必要修改

## Self-Hosted Runner 配置结论

当前 GitHub runner inventory：

- API: `repos/baofeng-tech/agent-skills-io/actions/runners`
- Result: `total_count=0`

当前仓库没有注册 repository self-hosted runner。`SELF_HOSTED_RUNNER_RUNS_ON_JSON=["self-hosted"]` 只是在 workflow 里选择 label，不会创建、注册、启动或保持任何 runner 在线。

本轮处理：

- 已删除 repo variable `SELF_HOSTED_RUNNER_RUNS_ON_JSON`
- workflow 内部仍默认使用 `["self-hosted"]` 作为 preflight label selector
- `AUTO_ALLOW_HOSTED_CONTINUATION=true` 继续控制无 self-hosted runner 时是否走 `ubuntu-latest` hosted fallback

推荐规则：

- 没有 self-hosted runner：删除或不要配置 `SELF_HOSTED_RUNNER_RUNS_ON_JSON`
- 有默认 label runner：也可以不配置，workflow 默认就是 `["self-hosted"]`
- 有专用 runner label：配置为真实 label 数组，例如 `["self-hosted","linux","clawhub"]`
- 不要把它配置成 `["ubuntu-latest"]`；hosted fallback 不是通过这个变量控制

## Latest Remote Run Review

拉取后当前 HEAD：

- `7e892ed5`

最新远端 run：

- Run: `25673284894`
- Created: `2026-05-11T13:30:40Z`
- Head SHA: `5dd1f008a8869841c67f2a403e441a1324a52a10`
- Conclusion: `success`

结论：最新成功 run 不是当前 HEAD。因为拉取后的 `7e892ed5` 是 Actions 成功后自动提交的 state refresh，所以本地和远端代码逻辑变化仍需在本轮 push 后触发一次 current-HEAD validation。

## Test Engineer Findings

### 1. `SELF_HOSTED_RUNNER_RUNS_ON_JSON` 容易被误读为 runner 开关

Severity: warning

当前 repo 没有 runner，仓库变量却配置为 `["self-hosted"]`。这不会导致 runner 存在，只会让 preflight 查找这个 label。保留这个变量会让排障时误以为“已经配置了 self-hosted runner”。

### 2. 最新成功 Actions run 不是当前 HEAD

Severity: warning

最新成功 run 的 `headSha` 是 `5dd1f008`，当前 HEAD 是 `7e892ed5`。根据本 repo 工作规则，不能把旧 head 的成功 run 当成当前 HEAD 已验证。

### 3. Preflight summary 的 “Runner labels” wording 不够精确

Severity: minor

当 hosted fallback 生效时，真正运行目标是 `["ubuntu-latest"]`，原 summary 里的 `Runner labels` 仍显示 `["self-hosted"]`，容易让人把 label selector 和实际 `runs-on` 混在一起。

### 4. ClawHub suspicious 当前没有自有 blocker 可修

Severity: info

刷新后 live summary：

- Total artifacts: `120`
- Suspicious: `8`
- Pending: `1`

`--owned-only --severity blocker --status suspicious` 选择结果为 `0`。剩余 suspicious blocker 都是外部 publisher artifact，不能用 fallback slug 当作原 URL 修复。

### 5. Breakout rollout 当前无 drift

Severity: info

当前声明的 4 个 breakout 变体仍是：

- `aisa-twitter-api -> aisa-twitter-api-command-center @ 1.0.3`
- `aisa-twitter-engagement-suite -> aisa-twitter-research-engage-relay @ 1.0.6`
- `aisa-twitter-engagement-suite -> twitter-post-aisa @ 1.0.3`
- `aisa-tavily -> aisa-tavily-search @ 1.0.3`

Continuation planner 返回 `breakout_requested=false`，说明当前没有 changed breakout source 或 live breakout scan issue。

## Engineering Fixes

本轮修复：

- 删除远端 repo variable `SELF_HOSTED_RUNNER_RUNS_ON_JSON`
- 在 `.github/workflows/unified-skill-pipeline.yml` 中补充注释，说明该变量只是 label selector
- 将 preflight summary 从 `Runner labels` 改为 `Self-hosted label selector`
- 在 `scripts/test_github_actions_workflow.py` 中锁定新的 summary wording 和 optional-variable 注释
- 更新 `README.md`、`targets/task-execution-index.md`、`targets/unified-pipeline-and-github-actions.md`
- 刷新 `targets/clawhub-live-status.json` 与 `targets/clawhub-publish-state.json`

## ClawHub Status After Refresh

Remaining suspicious blockers:

- `skill:prediction-market`
- `skill:smart-search`
- `skill:stock-analysis`
- `skill:tavily-extract`
- `skill:twitter-autopilot`
- `skill:web-search`
- `skill:youtube`
- `skill:youtube-search`

Remaining pending warning:

- `plugin:aisa-twitter-research-engage-plugin`

These are not selected for owned remediation in this pass.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_github_actions_workflow.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_batch_publish_exit.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_plugin_auth_metadata.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_twitter_oauth_client_safety.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_release_layers.py`: passed
- `python3 -m compileall -q scripts`: passed
- `git diff --check`: passed

Remote current-HEAD validation should be triggered after this local fix is pushed.
