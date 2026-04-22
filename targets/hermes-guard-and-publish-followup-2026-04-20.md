# Hermes Guard And Publish Follow-up

## Summary

- `last30days`：Hermes 官方扫描结果 `SAFE`
- `last30days-zh`：Hermes 官方扫描结果 `SAFE`
- `example/accounts` 中的 `GITHUB_TOKEN` 已写入 `~/.hermes/.env`
- Hermes 内容侧阻塞已清空；当前剩余阻塞已从“缺少认证”变成“当前 PAT 无 PR 创建权限”
- `targets/hermes-fork-pr-batch-report-2026-04-20.json` 已记录 25 个缺口 skill 的最新批处理结果

## What Changed

- 把 `last30days` / `last30days-zh` 公开 skill 面收缩为无状态研究主链
- 删除 watchlist / briefing / store / setup_wizard / GitHub 第二凭证面
- 统一改为 repo-local 配置文件 `./.last30days-data/config.env` 或显式 `--api-key`
- 修复 `run-last30days.sh`，不再依赖已删除的 `dev-python.sh`
- 清掉两个 Hermes Guard 误命中：
  - `env.py` 中的 `env` 变量命名
  - `reddit.py` 中的敏感注释文本
- 新增 `scripts/batch_publish_hermes_prs.py`
  - 自动比对 `hermes-release/` 与已存在 PR
  - 自动把缺口 skill 推成 `add-skill-*` 远端分支
  - 自动尝试创建 PR，并把结果写入 JSON 报告

## Real Test Notes

- `targetSkills/last30days`：真实账号 + Python 3.12 运行成功，返回结构化 JSON
- `targetSkills/last30days-zh`：真实账号 + Python 3.12 运行成功，返回结构化 JSON
- 本轮上游真实数据结果出现 `grounding` 超时 / 空召回，但本地 skill 链路本身已跑通并正常返回 `warnings`

## External Publish State

- `Aisa-One-Skills-Claude` 已推到最新：`840d9ec`
- `Aisa-One-Plugins-Claude` 已推到最新：`6a2d8bf`
- `Aisa-One-Skills-Hermes` 已推到最新：`abb7c4e`

## Claude Plugin Verification

- `claude plugin install last30days@aisa-claude-marketplace`：成功
- `claude plugin install last30days-zh@aisa-claude-marketplace`：成功

## Hermes Batch Publish State

- 已读取并复用 `example/accounts` 里的 `GITHUB_TOKEN`
- 官方 `hermes skills publish ... --repo baofeng-tech/Aisa-One-Skills-Hermes` 现在能通过扫描，但在 fork 阶段仍会超时
- 改用仓库内批量脚本后，已确认 25 个原本还没有开放 PR 的 Hermes skill 都已推成远端分支
- 已用远端 `ls-remote` 复核这 25 个 `add-skill-*` 分支全部存在
- 当前批量创建 PR 的统一报错是：
  - `Resource not accessible by personal access token`
  - 这说明当前 PAT 只有读权限，不能创建 Pull Request

## Current Bottom Line

- Hermes 收录准备已经推进到：
  - 内容侧：通过 Guard / SAFE
  - 远端侧：缺口 skill 分支全部备好
  - 阻塞点：只剩“有写权限的 GitHub PR 创建”
- 后续若补一个具备 PR 写权限的 `GITHUB_TOKEN`，或提供已登录的 `gh auth login`，即可沿现有 `add-skill-*` 分支继续补开 PR，无需再重做技能内容整改
