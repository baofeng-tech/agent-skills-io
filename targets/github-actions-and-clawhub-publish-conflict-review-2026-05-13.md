# GitHub Actions And ClawHub Publish Conflict Review 2026-05-13

## Scope

本轮按单 agent 串行执行：

- `git pull --ff-only`
- review GitHub Actions 与 ClawHub 批发布脚本
- 解释 2026-05-12 远端变量“安全档”
- 修复 slug / version 归属冲突导致全量发布失败的问题
- 刷新 suspicious / breakout 推进状态

## Safety Variables Meaning

2026-05-12 的“安全档”是临时止血配置，不是长期发布策略：

- `AUTO_PIPELINE_SELECTION=changed`
- `AUTO_RUN_LLM_STEP=false`
- `AUTO_LLM_APPLY=false`
- `AUTO_RUN_AISA_API_REGRESSION=false`
- `AUTO_FULL_PLATFORM_PUBLISH=false`
- `AUTO_CLAWHUB_PUBLISH=none`

含义：

- 前四项降低定时任务的 AISA 付费流量，保留是合理的。
- `AUTO_FULL_PLATFORM_PUBLISH=false` 会禁止发布续跑 lane，即使有变更也不进入 downstream / ClawHub 发布。
- `AUTO_CLAWHUB_PUBLISH=none` 会让发布 lane 即使运行也不发 ClawHub skill/plugin。

结论：不能靠这两个发布开关长期规避冲突。发布应恢复为自动续跑，但发布器必须把冲突分类处理，不能直接让整条 workflow failed。

## Test Engineer Findings

### 1. Full publish was disabled instead of made resilient

Severity: blocker

远端变量把 `AUTO_FULL_PLATFORM_PUBLISH=false` 和 `AUTO_CLAWHUB_PUBLISH=none` 同时打开后，定时任务不会继续 ClawHub 全量发布。这避免了失败，但也停止了正常发布推进。

### 2. Slug conflict fallback only tried one suffix

Severity: high

`publish_clawhub_batch.py` 原来每个 token 只尝试当前 slot 对应的 fallback slug。遇到 `-aisa` / `-aisa-api` / `-aisa-one` 其中一个也冲突时，脚本会把 artifact 标成 failed，并使批量任务失败。

### 3. Three-token ownership conflicts were not routed clearly

Severity: high

错误文本中已经包含 `Existing skill: /baofeng-tech/...`、`/bibaofeng/...` 等 owner 线索，但脚本没有先判断是否属于配置内三个 ClawHub token。结果可能用错误 token 反复发布同一个 owned slug。

### 4. Version conflict had no bump path

Severity: high

`Version already exists` 只会进入 already-exists / failed 分支。对于配置内 token 可控的 slug，合理策略应该是先确认远端版本，再尝试简单 patch version bump。

### 5. External-owner conflicts were fatal and repeatedly retried

Severity: medium

如果 slug 明确属于非三 token owner，或 locked / reserved，脚本应记录为以后同版本跳过，而不是让全量发布失败并在后续定时任务里重复失败。

## Engineering Fixes

本轮修复：

- `publish_clawhub_batch.py`
  - 解析 ClawHub 错误里的 existing owner
  - 将 `baofeng-tech` / `bibaofeng` / `aisadocs` 映射到 `token-1..3`
  - 对三 token 内但当前 token 不匹配的冲突，标记为 `deferred_owner_token`
  - 对外部 owner、locked slug、fallback 全部不可用的冲突，标记为非致命 blocker
  - fallback slug 改为尝试完整产品后缀序列：`-aisa`、`-aisa-api`、`-aisa-one`
  - 新增 `--version-conflict-strategy bump-patch`
  - 对简单数字版本的 version conflict 尝试 patch bump
  - 自动 bump 时同步临时 skill/plugin manifest version，避免发布包元数据漂移
  - blocked 冲突不再让 batch exit code 失败；同版本以后跳过，新版本重新评估
- workflow / helper scripts
  - self-hosted publish、suspicious repair、breakout rollout 都传入 version-conflict strategy
  - suspicious repair 仍保持 slug conflict 默认 `fail`，避免 fallback slug 冒充原可疑 URL 修复
- tests
  - 扩展 ClawHub batch publish exit / conflict state 测试
  - 扩展 GitHub Actions workflow guard 测试

## Remote Variable Recommendation

建议恢复发布开关，但保留省钱项：

```text
AUTO_PIPELINE_SELECTION=changed
AUTO_RUN_LLM_STEP=false
AUTO_LLM_APPLY=false
AUTO_RUN_AISA_API_REGRESSION=false
AUTO_FULL_PLATFORM_PUBLISH=auto
AUTO_CLAWHUB_PUBLISH=both
AUTO_CLAWHUB_VERSION_CONFLICT_STRATEGY=bump-patch
```

这样定时任务仍只同步 changed upstream，仍不跑付费 LLM refine / AISA API regression，但 release / ClawHub 发布不会被禁止。

## Suspicious And Breakout Status

本轮刷新后的 live / diagnosis 快照：

- total artifacts: 120
- suspicious blockers: 8
- pending warnings: 22
- owned suspicious blockers under `baofeng-tech,bibaofeng,aisadocs`: 0

所以本轮没有直接可修的 owned suspicious blocker。外部 publisher 的 suspicious URL 不能用 fallback slug 当作修复。

当前 breakout 声明仍是 4 个：

- `aisa-twitter-api -> aisa-twitter-api-command-center @ 1.0.3`
- `aisa-twitter-engagement-suite -> aisa-twitter-research-engage-relay @ 1.0.6`
- `aisa-twitter-engagement-suite -> twitter-post-aisa @ 1.0.3`
- `aisa-tavily -> aisa-tavily-search @ 1.0.3`

刷新 live status 后，这 4 个 breakout skill 的 skill 页仍有 pending 扫描状态，因此 continuation planner 会请求 breakout rollout。下一步应在当前代码推送后，用 current HEAD 触发 breakout lane，让新发布器处理版本/slug 冲突。

## Validation

Initial validation after code changes:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_batch_publish_exit.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_github_actions_workflow.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_live_status_review.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_clawhub_plugin_auth_metadata.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_twitter_oauth_client_safety.py`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_release_layers.py`: passed
- `python3 -m compileall -q scripts`: passed
- `git diff --check`: passed
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/clawhub_suspicious_remediation.py --plan --owned-only --severity blocker --status suspicious`: 0 owned artifacts
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/clawhub_breakout_rollout.py --plan`: 4 declared variants
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/clawhub_live_status.py --targets both --include-status published --render-mode auto`: 120 total, 8 suspicious, 22 pending
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/clawhub_suspicious_diagnosis.py --doc-mode update`: 30 artifacts, 8 blockers, 22 warnings
