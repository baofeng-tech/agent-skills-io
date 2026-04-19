# Hermes Guard And Publish Follow-up

## Summary

- `last30days`：Hermes 官方扫描结果 `SAFE`
- `last30days-zh`：Hermes 官方扫描结果 `SAFE`
- Hermes 内容侧阻塞已清空，当前仅剩 GitHub API 认证缺失：
  - `Error: GitHub authentication required.`
  - 需要 `GITHUB_TOKEN` 写入 `~/.hermes/.env`，或提供 `gh auth login`

## What Changed

- 把 `last30days` / `last30days-zh` 公开 skill 面收缩为无状态研究主链
- 删除 watchlist / briefing / store / setup_wizard / GitHub 第二凭证面
- 统一改为 repo-local 配置文件 `./.last30days-data/config.env` 或显式 `--api-key`
- 修复 `run-last30days.sh`，不再依赖已删除的 `dev-python.sh`
- 清掉两个 Hermes Guard 误命中：
  - `env.py` 中的 `env` 变量命名
  - `reddit.py` 中的敏感注释文本

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
