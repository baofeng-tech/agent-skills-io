# GitHub Actions Review 2026-05-04

## Remote Run Status

- `Unified Skill Pipeline #49` is still `Queued`, not actively running. The hosted `sync-build-test` job completed in about 4 minutes, but the workflow stayed queued behind self-hosted lanes.
- `#48`, `#47`, `#46`, `#44`, `#43`, and `#42` were canceled by queue/concurrency pressure, not by a fresh build/test failure.
- `#45` reached `self-hosted-publish` for about 11 hours before manual cancellation.
- `#41` failed after waiting 24 hours for a self-hosted runner.
- `#40` failed on a self-hosted artifact upload `ECONNRESET`, while `#39` failed in `sync-build-test` before later workflow hardening.

Relevant public run pages:

- https://github.com/baofeng-tech/agent-skills-io/actions/runs/25260600938
- https://github.com/baofeng-tech/agent-skills-io/actions/runs/25201997115
- https://github.com/baofeng-tech/agent-skills-io/actions/runs/25201900930

## Findings

### Blocker

- Self-hosted jobs could be queued even when no runner was online. This caused the observed all-day wait and the 24-hour runner timeout.
- Scheduled automation could request long self-hosted publish/remediation lanes repeatedly, so older runs were canceled or left waiting behind newer runs.

### Warning

- Only the workflow-level concurrency was defined. Manual reruns could still overlap within the same self-hosted lane and race downstream publish repos.
- The breakout artifact upload still used `actions/upload-artifact@v4`, which kept the Node 20 deprecation warning alive after other actions had already moved forward.
- Self-hosted lanes had no explicit bounded runtime, so a stuck publish command could consume a runner for too long.

### Note

- The current suspicious diagnosis snapshot still contains 33 ClawHub artifacts, with 32 blockers and 17 pending scan states. Most remaining reasons are live publish-state or registry-metadata drift, not local package omissions.
- The breakout lane currently has 2 declared variants: `aisa-twitter-api-command-center` and `aisa-twitter-research-engage-relay`.

## Fixes Applied

- Added `self-hosted-preflight`, a hosted runner API check that gates publish, suspicious repair, and breakout rollout before they can queue on self-hosted.
- Added manual `force_self_hosted_queue` and scheduled `AUTO_FORCE_SELF_HOSTED_QUEUE` escape hatches for intentional waiting.
- Added lane-level concurrency and `timeout-minutes` to the three self-hosted lanes.
- Updated the remaining breakout artifact upload step to `actions/upload-artifact@v6`.
- Documented the new runner-gated switches in the unified pipeline runbook and project overview.

## Verdict

The old `#49` queued run itself still needs cancellation or a runner coming online because it was created from the old workflow definition. Future runs from the updated workflow should skip unavailable self-hosted lanes quickly instead of waiting all day.
