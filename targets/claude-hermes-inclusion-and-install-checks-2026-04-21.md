# Claude / Hermes 收录与可安装检查手册

本文档用于回答两个实际问题：

1. 某个 Claude skill / Claude plugin / Hermes skill 现在是否已经“被收录”
2. 某个发布层是否已经达到了“用户可以真实安装”的状态

目标是让后续聊天无需翻历史，也能快速判断当前项目的发布状态与验证方法。

## 1. 先区分“收录”是什么意思

不同平台里，“收录”不是同一件事。

### Claude standalone skill

这里通常不是一个统一的“官方仓库已收录”概念，而是：

- `claude-release/` 已生成
- 已同步到公开 GitHub skill 仓库
- 目录结构与 `SKILL.md` 符合 Claude 可消费的 skill 形态

因此，Claude standalone skill 更适合用“已生成并已同步到公开仓库”来判断，而不是用“Hub 已收录”来判断。

### Claude plugin marketplace

这里的“收录”更接近：

- marketplace GitHub 仓库已经存在并可访问
- Claude Code 已成功 `marketplace add`
- 具体 plugin 可以 `plugin install`

### Hermes skill

这里至少有三层状态：

1. 已进入我们自己的 Hermes GitHub / tap 仓库
2. 已经能被 Hermes `inspect` / `search` / `install`
3. 已走官方 `skills publish -> fork -> PR` 流程，等待或完成上游合并

因此 Hermes 要分开记录，不要把“tap 可安装”和“官方 Hub 已合并”混为一谈。

## 2. 当前项目的默认发布目标

本仓库当前对应的外部发布仓库是：

- Claude standalone skills:
  - `D:\workplace\Aisa-One-Skills-Claude`
  - GitHub 仓库用于承接 `claude-release/`
- Claude marketplace:
  - `D:\workplace\Aisa-One-Plugins-Claude`
  - GitHub 仓库：`baofeng-tech/Aisa-One-Plugins-Claude`
- Hermes skills:
  - `D:\workplace\Aisa-One-Skills-Hermes`
  - GitHub 仓库：`baofeng-tech/Aisa-One-Skills-Hermes`

## 3. Claude 如何检查

### 3.1 Claude standalone skill 是否已发布

当前环境下，没有一个等价于 “`claude skills search owner/repo/...`” 的稳定一手 CLI 命令。  
因此本项目采用下面这套判断标准。

#### 判断标准

满足以下三项，就视为 Claude standalone skill 已进入可分发状态：

1. `claude-release/` 已由脚本重建
2. `scripts/test_release_layers.py` 通过 Claude 层结构校验
3. 对应 GitHub 仓库已同步到最新

#### 推荐检查命令

在本仓库根目录执行：

```bash
python3 scripts/build_claude_release.py
PYTHON_EXE=$HOME/.local/bin/python3.12 python3 scripts/test_release_layers.py
```

再到外部发布仓库确认同步状态：

```bash
cd /mnt/d/workplace/Aisa-One-Skills-Claude
git status --short
git log -1 --oneline
```

如果：

- `claude-release/` 重建成功
- 测试脚本没有 Claude 结构错误
- 外部 Git 仓库已经推到最新

则可认为该 skill 已经处于 Claude standalone 可分发状态。

### 3.2 Claude plugin marketplace 是否已被 Claude 识别

这一条是 Claude 侧最可靠的真实验证方式。

#### 查看当前已配置 marketplace

```bash
claude plugin marketplace list
```

2026-04-21 本机实测结果：

- 已配置 marketplace：`aisa-claude-marketplace`
- 来源：`GitHub (baofeng-tech/Aisa-One-Plugins-Claude)`

#### 添加 marketplace

```bash
claude plugin marketplace add baofeng-tech/Aisa-One-Plugins-Claude
```

也可以使用本地路径或 URL，CLI 帮助中明确支持：

- URL
- path
- GitHub repo

#### 安装单个 plugin

```bash
claude plugin install last30days@aisa-claude-marketplace
```

或：

```bash
claude plugin install aisa-twitter-command-center@aisa-claude-marketplace
```

CLI 帮助中还支持安装范围：

```bash
claude plugin install --scope user plugin-name@marketplace-name
```

#### 发布前本地校验

在 marketplace 根目录：

```bash
claude plugin validate .
```

#### Claude plugin 的“已收录”判断标准

推荐按下面顺序判断：

1. `claude-marketplace/` 已生成
2. GitHub marketplace 仓库已同步
3. `claude plugin marketplace list` 能看到 marketplace
4. `claude plugin install plugin@marketplace` 成功

前 1-2 步表示“已发布到来源仓库”；  
前 3-4 步表示“已被 Claude 客户端识别并且真实可安装”。

## 4. Hermes 如何检查

### 4.1 先看 tap 是否已配置

```bash
hermes skills tap list
```

2026-04-21 本机实测结果：

- 已配置 tap：`baofeng-tech/Aisa-One-Skills-Hermes`
- Path：`skills/`

### 4.2 Hermes 里的 tap 是什么

`tap` 只是把某个 GitHub 仓库登记为 skill 来源。  
它不等于“已经安装 skill”，也不等于“官方 Hermes Hub 已合并收录”。

可以把它理解为：

- 已告诉 Hermes 去哪个 GitHub 仓库找技能
- 之后 Hermes 可以从这个来源执行 `inspect` / `install`

### 4.3 添加 tap

```bash
hermes skills tap add baofeng-tech/Aisa-One-Skills-Hermes
```

CLI 帮助确认 `tap add` 的参数就是 GitHub `owner/repo`。

### 4.4 检查单个 skill 是否已能被 Hermes 发现

最直接的检查命令是：

```bash
hermes skills inspect baofeng-tech/Aisa-One-Skills-Hermes/research/search
```

2026-04-21 本机实测：

- 上述命令可以返回完整 skill 预览
- 返回的 Identifier 为：
  - `skills-sh/baofeng-tech/Aisa-One-Skills-Hermes/research/search`

这说明至少 `search` 这个 skill 已经能被 Hermes 解析与展示。

#### 通用检查模板

```bash
hermes skills inspect owner/repo/category/skill-name
```

如果能看到：

- skill 名称
- 描述
- 来源
- repo 链接
- `SKILL.md Preview`

就说明这个 skill 已经到达“可发现 / 可预览”的状态。

### 4.5 搜索某类 skill

```bash
hermes skills search aisa --limit 20
```

也可以限制来源：

```bash
hermes skills search aisa --source github --limit 20
hermes skills search aisa --source skills-sh --limit 20
```

注意：

- 当前环境下 `search` 对 GitHub 来源有时较慢
- `inspect owner/repo/category/skill` 往往比全局 `search` 更适合做单 skill 验证

### 4.6 安装单个 Hermes skill

```bash
hermes skills install owner/repo/category/skill-name --yes
```

例如：

```bash
hermes skills install baofeng-tech/Aisa-One-Skills-Hermes/research/search --yes
```

CLI 帮助还支持：

- `--category`
- `--force`
- `--yes`

其中 `--force` 只应用于你明确知道扫描风险的情况。

### 4.7 查看当前本机已安装的 Hermes hub skills

```bash
hermes skills list --source hub
```

2026-04-21 本机实测结果：

- 当前本机 `hub-installed = 0`

这表示：

- tap 已配置
- 但当前机器还没有保留一个已安装的 hub skill 本地实例

### 4.8 Hermes 官方收录与我们自有 tap 分发的区别

本项目里需要区分两件事：

#### A. 自有 Hermes 仓库可安装

判断标准：

1. `hermes-release/` 已生成并同步到 `baofeng-tech/Aisa-One-Skills-Hermes`
2. `hermes skills tap list` 能看到仓库
3. `hermes skills inspect owner/repo/category/skill` 成功
4. `hermes skills install owner/repo/category/skill --yes` 成功

这说明它已经是“自有来源可安装”。

#### B. 官方 Hermes publish 收录

判断标准：

1. `hermes skills publish path/to/skill --to github --repo owner/repo` 成功发起
2. 对应 fork / PR 已创建
3. 后续 PR 被上游接受

命令形式：

```bash
hermes skills publish hermes-release/research/search --to github --repo baofeng-tech/Aisa-One-Skills-Hermes
```

注意：

- 这一步更像“把 skill 送入官方流程”
- 它与“我们的 tap 仓库已经可安装”不是同一个状态

## 5. 本项目建议的验证顺序

以后每次要确认发布结果，优先按这个顺序：

1. 重建发布层

```bash
python3 scripts/build_claude_release.py
python3 scripts/build_claude_marketplace.py
python3 scripts/build_hermes_release.py
```

2. 跑结构与 smoke test

```bash
PYTHON_EXE=$HOME/.local/bin/python3.12 python3 scripts/test_release_layers.py
```

3. 核对外部仓库是否同步

- `D:\workplace\Aisa-One-Skills-Claude`
- `D:\workplace\Aisa-One-Plugins-Claude`
- `D:\workplace\Aisa-One-Skills-Hermes`

4. Claude 验证 marketplace

```bash
claude plugin marketplace list
claude plugin install plugin-name@aisa-claude-marketplace
```

5. Hermes 验证 tap / inspect / install

```bash
hermes skills tap list
hermes skills inspect owner/repo/category/skill-name
hermes skills install owner/repo/category/skill-name --yes
```

6. 如果目标是“官方 Hermes 收录”，再额外执行：

```bash
hermes skills publish hermes-release/<category>/<skill> --to github --repo baofeng-tech/Aisa-One-Skills-Hermes
```

## 6. 当前可直接引用的结论

截至 2026-04-21，本机已经确认：

- Claude marketplace 已配置：
  - `aisa-claude-marketplace`
- Claude marketplace 来源：
  - `baofeng-tech/Aisa-One-Plugins-Claude`
- Hermes tap 已配置：
  - `baofeng-tech/Aisa-One-Skills-Hermes`
- Hermes 可成功预览示例 skill：
  - `baofeng-tech/Aisa-One-Skills-Hermes/research/search`
- 当前本机仍未保留任何 hub-installed Hermes skill：
  - `hermes skills list --source hub` 返回 `0`

## 7. 以后聊天如何使用这份文档

后续若有人问：

- Claude skill 现在到底算不算发布成功
- Claude plugin 是否真的能安装
- Hermes skill 是否已经被收录
- Hermes 现在是 tap 可安装还是官方 PR 已完成

优先读取本文档，再结合：

- [targets/current-context-compression-2026-04-20.md](/mnt/d/workplace/agent-skills-io/targets/current-context-compression-2026-04-20.md:1)
- [targets/hermes-guard-and-publish-followup-2026-04-20.md](/mnt/d/workplace/agent-skills-io/targets/hermes-guard-and-publish-followup-2026-04-20.md:1)
- [targets/claude-and-hermes-upload-guide-2026-04-17.md](/mnt/d/workplace/agent-skills-io/targets/claude-and-hermes-upload-guide-2026-04-17.md:1)

如果状态发生变化，应优先更新本文档中的：

- 当前状态快照
- 验证命令
- 已确认可安装的 marketplace / tap / skill 示例
