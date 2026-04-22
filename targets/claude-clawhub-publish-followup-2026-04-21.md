# Claude / ClawHub 发布跟进（2026-04-21）

本文记录 2026-04-21 这轮对 Claude marketplace / standalone skills / ClawHub plugin 发布链路的真实执行结果，方便后续续跑。

## 0. 2026-04-22 复核更新

- `Aisa-One-Skills-Claude`、`Aisa-One-Plugins-Claude`、`Aisa-One-Skills-Hermes`、`agent-skills-own` 当前都已与 `origin/main` 对齐，旧文里的 “`0 1` 还差最后一次 push” 已不是当前阻塞
- 当前机器对 `git@github-work:baofeng-tech/Aisa-One-Plugins-Claude` 的直接 clone 已成功，旧文里“GitHub transport / clone 卡住”的判断应视为历史环境结论，不应继续作为当前事实引用
- 当前默认验证基线是本地目录源 `./claude-marketplace`，`claude plugin marketplace update aisa-claude-marketplace` 已成功，且本地安装检查仍为 51 / 51 成功
- 这里提到的 `crawler 周期` 指外部站点定时重新抓取 GitHub / marketplace 源的刷新周期，不代表仓库内还有安装失败或包内容残缺

## 0.1 2026-04-22 继续执行结果

- 使用新 probe 重试逻辑重新跑 `python3 scripts/publish_clawhub_batch.py --skip-build --targets both --dry-run` 后，`targets/clawhub-publish-state.json` 的 `failed` 从 4 降到 1
- 本轮重新识别为远端已存在的历史误报包括：
  - `smart-search`
  - `tavily-extract`
  - `prediction-market-arbitrage-zh` 以外的其余已探测条目
- 随后执行 `python3 scripts/publish_clawhub_batch.py --skip-build --targets skill --per-token-per-hour 4`，真实新增发布 8 个 skill：
  - `aisa-provider`
  - `aisa-tavily`
  - `aisa-twitter-command-center`
  - `aisa-twitter-engagement-suite`
  - `aisa-twitter-post-engage`
  - `aisa-youtube-serp-scout`
  - `cn-llm`
  - `last30days-zh`
- 该轮真发布结果：
  - `published: 8`
  - `failed: 0`
  - `pending: 14`
  - 两个 token 都按每小时 4 次的保守上限停下
- 当前 ClawHub 状态文件汇总为：
  - `45 published`
  - `56 planned`
  - `1 failed`
- 当前唯一仍显式挂着的 ClawHub 条目是：
  - `prediction-market-arbitrage-zh-plugin`
  - 对它做 `timeout 20 clawhub package inspect ...` 的短探测连续 3 次均返回 `rc=124`
  - 现阶段更像平台侧 `package inspect` 响应波动，不像命名或包结构错误
- 上一轮 `release-layer-test-report` 中残留的 4 个外部超时点，2026-04-22 定向复测已全部成功返回：
  - `claude-release/aisa-twitter-command-center`
  - `claude-release/search`
  - `hermes-release/research/aisa-youtube-serp-scout`
  - `clawhub-release/search`
  - 因此这些项当前应视为外部接口波动，而不是稳定构建缺陷

## 1. ClawHub：双 token 批量续传脚本已补齐

新增脚本：

- `scripts/publish_clawhub_batch.py`

能力：

- 同时处理 `clawhub-release/` skills 和 `clawhub-plugin-release/plugins/` code plugins
- 支持从 `example/accounts` 自动读取 `clawhub_ApI_token` / `clawhub_ApI_token2`
- 为两个 token 各自创建独立 `CLAWHUB_CONFIG_PATH`
- 用 `clawhub inspect` / `clawhub package inspect` 先探测远端是否已存在
- 用 `targets/clawhub-publish-state.json` 记录本地状态，便于续跑
- 支持保守的每 token 每小时上限
- 支持 `--dry-run`

本轮 dry-run 实测结果：

- 已能识别远端已存在的 plugin，例如：
  - `aisa-multi-search-engine-plugin`
  - `aisa-twitter-command-center-plugin`
  - `aisa-twitter-post-engage-plugin`
  - `aisa-youtube-search-plugin`
  - `aisa-youtube-serp-scout-plugin`
- 说明“未上传才继续发、已上传自动跳过”这条链路已经成立

推荐续跑命令：

```bash
python3 scripts/publish_clawhub_batch.py --skip-build --targets both --dry-run
python3 scripts/publish_clawhub_batch.py --skip-build --targets skill --per-token-per-hour 4
python3 scripts/publish_clawhub_batch.py --skip-build --targets plugin --per-token-per-hour 4
```

## 2. 构建脚本已补 runtime-only 过滤

本轮同时修正：

- `scripts/build_claude_marketplace.py`
- `scripts/build_clawhub_plugin_release.py`

新增忽略：

- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `.pytest_cache/`
- `node_modules/`
- `.DS_Store`

目的：

- 避免 `claude-marketplace/` 与 `clawhub-plugin-release/` 在源层被测试污染后继续把缓存目录打进发布包

## 3. Claude marketplace：内容层验证通过，GitHub clone 环境层有坑

### 3.1 GitHub marketplace 源实测

本机已有 marketplace：

- `aisa-claude-marketplace`
- Source：`GitHub (baofeng-tech/Aisa-One-Plugins-Claude)`

首次批量安装结果写入：

- `targets/claude-marketplace-install-check-2026-04-21.json`

结果：

- 总计 51 个 plugin
- 成功 43
- 失败 8

失败项：

- `market`
- `media-gen`
- `perplexity-search`
- `prediction-market`
- `prediction-market-arbitrage`
- `search`
- `twitter`
- `youtube`

失败报错统一为：

- `Plugin "<name>" not found in marketplace "aisa-claude-marketplace"`

### 3.2 根因

这些失败项并不是包内容损坏。

证据：

1. 它们都真实存在于仓库的 `.claude-plugin/marketplace.json`
2. `claude plugin marketplace update aisa-claude-marketplace` 在这台机器上失败
3. 失败日志显示 Claude CLI 在刷新 marketplace 时尝试 clone GitHub repo，但卡在 git clone 阶段
4. 当前环境里直接用 Claude CLI 走 GitHub marketplace add/update，会受本机 git transport / clone 环境影响

### 3.3 本地目录源复测

改用本地目录源：

```bash
claude plugin marketplace add ./claude-marketplace
```

全量 51 个 plugin 再次安装检查结果写入：

- `targets/claude-marketplace-local-install-check-2026-04-21.json`

结果：

- 51 / 51 全部安装成功

结论：

- `claude-marketplace/` 当前内容层是完整可安装的
- GitHub marketplace 的失败是当前机器上的 clone/update 环境问题，不是 plugin 包内容问题

## 4. Claude standalone skills：源仓库已同步到本地外部仓库，但 push 还差最后一步

外部 skill 仓库：

- `/mnt/d/workplace/Aisa-One-Skills-Claude`

本轮已执行：

- 使用 `bash scripts/publish-claude-release.sh --with-marketplace --skip-build` 完成同步
- 在外部 skill 仓库生成了新 commit：
  - `00de3bf chore: publish claude-release`

当前状态：

- `git status --short` 已 clean
- `git rev-list --left-right --count origin/main...HEAD` 返回：
  - `0 1`

含义：

- 本地 `HEAD` 比 GitHub `origin/main` 领先 1 个 commit
- 也就是内容已经准备好，但这台机器从当前 shell 做 GitHub push 会卡住，还没有把这 1 个 commit 推上去

## 5. claudemarketplaces.com：当前还没检索到 AIsa 页面

基于 2026-04-21 的公开检索：

- `baofeng-tech/Aisa-One-Plugins-Claude`
- `Aisa-One-Plugins-Claude`
- `aisa-claude-marketplace`
- `baofeng-tech/Aisa-One-Skills-Claude`

都暂未在公开搜索结果中搜到对应条目。

结合站点公开说明：

- marketplace 是从 GitHub 上含 `.claude-plugin/marketplace.json` 的仓库自动抓取
- standalone skills 是从 `skills.sh` 抓取，并带安装量过滤

因此当前判断是：

- Claude marketplace：需要等待 crawler 周期，或先确保 GitHub 仓库能被站点顺利抓取
- Claude standalone skills：除了 GitHub 仓库本身，还需要通过 `skills.sh` / 安装分发拿到收录信号

## 6. 后续直接继续做什么

优先顺序：

1. 在可正常连接 GitHub 的交互式环境里，把 `Aisa-One-Skills-Claude` 的领先 commit 推上去
2. 若需要继续验证 GitHub marketplace 源，优先排查为什么本机 `claude plugin marketplace add/update` 的 git clone 会卡住
3. 继续用 `scripts/publish_clawhub_batch.py` 按小时限额续传 ClawHub skills / plugins
4. 等 crawler 周期后，再复查 `claudemarketplaces.com` 是否已出现 AIsa marketplace 页面
