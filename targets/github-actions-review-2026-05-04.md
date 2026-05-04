# GitHub Actions Review 2026-05-04

## Scope

本轮按测试工程师和 GitHub/AI 发布工程视角复核：

- `.github/workflows/unified-skill-pipeline.yml`
- `scripts/unified_skill_pipeline.py`
- `scripts/publish_clawhub_batch.py`
- ClawHub suspicious remediation / breakout rollout 的 workflow 参数链

## Findings

### Blocker

- Self-hosted 预检直接用 `GITHUB_TOKEN` 调 GitHub runners API。该接口需要仓库 Administration read 级别权限，普通 workflow `GITHUB_TOKEN` 很容易返回 `403`，导致 runner 在线时也被误判为不可排队。
- `scripts/unified_skill_pipeline.py` 在没有上游 skill 变化时直接返回。这样手动打开 self-hosted publish、ClawHub 续发、下游 repo 同步时，当前发布层不会被发布，suspicious 修复和爆款推进会停在入口前。
- ClawHub dry-run 发布路径会触发 `publish_clawhub_batch.py` 重建，并把 `targets/clawhub-publish-state.json` 里的 artifact `path` 写成本机绝对路径，造成无意义状态 churn 和跨机器漂移。

### Warning

- `diagnosis-pr` job 在 hosted lane 已经直接 commit 输出之后重新 checkout 触发 SHA，不会拿到前一 job 的工作区变更，基本是空转 PR lane。
- Downstream publish repo 的准备阶段始终使用公开 HTTPS clone URL，私有 repo 或需要 token 的 runner 会在 clone/fetch 时失败。
- Downstream repo push 没有 fetch/rebase/retry，多个 lane 或人工改动同时推进时容易 non-fast-forward。
- 正常 self-hosted publish lane 只调用 `publish_clawhub_batch.py`，没有显式传 `--post-publish-scan`，导致真实续发后还要等后续 live-status job 才能回写 scan 状态。
- 预检支持 `SELF_HOSTED_RUNNER_LABELS`，但 self-hosted jobs 固定 `runs-on: self-hosted`，当 runner 需要额外 label 时会出现“预检命中一个 runner，实际 job 却可能排到另一个 runner”的错位。
- schedule 侧的 self-hosted publish / suspicious repair / breakout rollout 开关仍默认关闭；如果仓库变量没配，手动 dispatch 是打开的，定时任务却不会继续真实发布链。
- preflight 只查 repository-level runners；本地复测发现 `/repos/baofeng-tech/agent-skills-io/actions/runners` 返回 `200` 但 runners 数为 `0`，如果实际 runner 是 organization-level，会被误判为没有在线 runner。

### Note

- 当前 action tag 可从 GitHub 远端解析到，不是缺失 tag 问题。
- 本轮 suspicious plan 仍有 `21` 个自有 blocker suspicious artifact，对应 `14` 个 source skill。当前生成包已能看到 `AISA_API_KEY` 与 `api.aisa.one` metadata，大量剩余项更像 live registry / 已发布旧包 drift，需要重新发布与复扫。
- Breakout rollout 当前仍是 2 个变体：`aisa-twitter-api-command-center` 与 `aisa-twitter-research-engage-relay`。

## Fixes Applied

- workflow_dispatch 默认打开 publish、AISA API regression、suspicious repair、breakout rollout、ClawHub CLI install。
- self-hosted 预检新增 `SELF_HOSTED_RUNNER_API_TOKEN` / `DOWNSTREAM_REPO_TOKEN` token fallback；如果 runner API 仍不可访问，则明确跳过，只有 `force_self_hosted_queue` / `AUTO_FORCE_SELF_HOSTED_QUEUE` 才会刻意排队等待。
- `unified_skill_pipeline.py` 在无上游变化但 publish/sync 被请求时，会从当前 `targetSkills/` 继续 rebuild、sync、publish 和 diagnosis。
- ClawHub batch publish 现在把 artifact path 写成 repo-relative 路径，避免把本机绝对路径写入 state。
- ClawHub publish 调度总是向 batch publisher 传 `--skip-build`；发布层构建由 unified pipeline 统一负责。
- 移除空转的 `diagnosis-pr` job 和多余 `pull-requests: write` 权限。
- Downstream repo clone/fetch 支持 `DOWNSTREAM_REPO_TOKEN`，push 增加 fetch/rebase/retry。
- normal self-hosted publish lane 新增 `clawhub_post_publish_scan` / `AUTO_CLAWHUB_POST_PUBLISH_SCAN`，并传递到 `scripts/unified_skill_pipeline.py --clawhub-post-publish-scan`，让真实 publish 或 remote-existing skip 后立即复扫。
- schedule 默认请求 publish、suspicious repair、breakout rollout、AISA API regression、ClawHub CLI install 与 post-publish scan；仍由 preflight 决定是否真的排队。
- self-hosted jobs 改为使用 `SELF_HOSTED_RUNNER_RUNS_ON_JSON` 控制 `runs-on`，preflight 同时能解析该 JSON label 列表，避免 label 检查和实际调度目标分叉。
- runner preflight 在 `403` 等失败时会把 GitHub 返回的 message、`x-accepted-github-permissions` 和 `x-github-sso` hint 写入 summary，方便判断是 repo access、org approval/SSO 还是 token 权限问题。
- preflight 在 repo-level runners 未命中时会继续查 organization-level runners，并在 summary 中明确提示 org-level runner 需要 `Self-hosted runners: read` organization permission。

## Verdict

workflow 现在更适合“开关默认打开、但 self-hosted 排队仍受预检约束”的运行方式。下一步真正消除 live `Suspicious` 需要在有 runner、ClawHub CLI 和 token 的环境里跑 self-hosted suspicious repair / breakout rollout，并完成 post-publish scan。
