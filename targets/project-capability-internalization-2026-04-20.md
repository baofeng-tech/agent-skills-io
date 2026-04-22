# 本项目已内化的能力说明

这份文档把最近几轮对话里形成的方法、脚本、环境和经验，沉淀为本项目的可复用能力。

## 1. 技能迁移能力

项目已经能稳定完成：

- 从历史技能包中抽取 `SKILL.md`、脚本与参考材料
- 重组为跨平台母版技能
- 统一采用 `targetSkills/` 作为长期源层
- 将平台私有字段从母版中剥离，改由发布层处理

## 2. 多发布层生成能力

项目已经具备三类下游发布层的自动生成能力：

- Claude 独立 skill 发布层：`claude-release/`
- Claude Marketplace plugin 发布层：`claude-marketplace/`
- Hermes skill 发布层：`hermes-release/`

默认入口脚本为：

- `scripts/build_claude_release.py`
- `scripts/build_claude_marketplace.py`
- `scripts/build_hermes_release.py`

## 3. 技能安全收敛能力

项目已经沉淀出适用于大多数 AISA skill 的统一整改方法：

- 母版层统一使用 `metadata.aisa`
- 发布层只保留运行时文件
- 默认避免 home 目录持久化
- 默认避免自动打开浏览器
- 尽量改成显式参数传递，不在公开发布层直接依赖环境变量
- 对复合型大 skill，公开面只保留主执行 / 主研究链路

这些规则已经固化到：

- `targets/skill-modification-rules-2026-04-19.md`
- `targets/aisa-universal-skill-template.md`

## 4. 真实数据测试能力

项目现在不只是“生成目录”，还具备真实数据验证能力：

- 统一从 `example/accounts` 读取账号与环境信息
- 可在 Python 3.12 环境下对 skill 做真实运行验证
- 可对生成后的 Claude/Hermes 发布层做结构与 smoke test
- 能区分“本地 skill 链路正常”与“上游 API 空召回 / 超时”

## 5. Claude 侧发布能力

项目已经验证过：

- `claude-release/` 能同步到独立 GitHub 仓库
- `claude-marketplace/` 能同步到独立 GitHub 仓库
- Claude Marketplace 能真实安装 plugin
- `last30days` 与 `last30days-zh` 的 Claude plugin 安装链路已跑通

## 6. Hermes 侧收录准备能力

项目已经形成一整套 Hermes 适配能力：

- 生成符合 Hermes 目录结构的 `hermes-release/`
- 对技能内容做 Guard 风险收敛
- 使用官方 `hermes skills publish` 验证扫描结果
- 对 CLI 的 fork 不稳定问题，提供仓库内替代批量脚本：
  - `scripts/batch_publish_hermes_prs.py`

该脚本现在可以：

- 自动识别哪些 skill 已经有开放 PR
- 自动把缺口 skill 推成远端 `add-skill-*` 分支
- 自动尝试创建 PR
- 把结果写成可追踪 JSON 报告

## 7. 环境自举能力

项目已验证并沉淀的本地环境能力包括：

- WSL 中可用 `python3.12`
- WSL 中可用 `node/npm/npx`
- WSL 中可用 `hermes` CLI
- WSL 中可用 `claude` CLI
- 支持 `github-work` / `github-personal` SSH 配置

## 8. 当前能力边界

当前项目能力已经足以完成：

- 技能整改
- 发布层生成
- 真实测试
- 外部仓库同步
- Hermes 分支级批量收录准备

当前仍依赖外部授权的一步是：

- GitHub PR 创建权限

也就是说，项目能力本身已覆盖“内容、结构、测试、分支推送”，剩余瓶颈是账号权限，而不是仓库方法不完整。

## 9. 推荐复用方式

以后继续做新 skill 或批量收录时，建议默认按下面顺序走：

1. 先改 `targetSkills/` 母版
2. 用生成脚本重建三个发布层
3. 做结构校验和真实数据验证
4. 同步到外部发布仓库
5. Hermes 侧先过 Guard，再批量推 `add-skill-*` 分支
6. 最后用具备写权限的 GitHub 凭据补开 PR
