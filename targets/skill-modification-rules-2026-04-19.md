# Skill Modification Rules

这份规则用于约束以后对 `targetSkills/` 及其发布层的修改方式，重点吸收了 `last30days` 评审里暴露出来的共性问题。

## 母版层规则

- 如果 skill 已存在于 `https://github.com/AIsa-team/agent-skills`，默认先以该仓库的 `agentskills` 分支为运行时基线。
- 修改现有 skill 前，先对照上游版本确认：
  - 当前 repo 改的是文案 / frontmatter / 发布层包装，还是确实需要改运行时能力
  - 任何优化都不能静默删掉上游已有主功能
- 除非任务明确要求变更能力，否则母版层和发布层都应保持“功能完整、行为不变”，优先只调整：
  - 命名
  - 描述
  - `metadata.aisa`
  - 发布层保守文案
  - runtime-only 打包范围
- 如果公开发布需要更保守的表述或更窄的 shipped surface，应在生成发布层时做，而不是直接把母版 skill 的核心运行时剪坏。
- 母版默认是跨平台版本，正文命令统一使用 `scripts/...` 相对路径。
- 母版 `SKILL.md` 统一采用 `metadata.aisa`：
  - `emoji`
  - `requires`
  - `primaryEnv`
  - `compatibility`
- 不再把 `metadata.openclaw`、`allowed-tools`、`argument-hint`、`user-invocable` 这类平台私有字段当成母版必填项。
- Python skill 默认走标准库实现，不引入 `requests`、`httpx`、`pyproject.toml` 或测试框架依赖。
- 默认主路径只保留一套凭证故事；第二套凭证、官方直连 API、或额外持久化能力必须明确标为“可选扩展”。
- 对体量明显超出普通 skill 的复合型项目，公开 skill 面默认只保留主研究 / 主执行 CLI；`watchlist`、`briefing`、`store`、第二凭证 GitHub 面等应拆出或降为非公开扩展。

## 目录内容规则

- skill 目录默认只保留运行时文件：
  - `SKILL.md`
  - `README.md`
  - `scripts/`
  - `references/`
  - `assets/`（仅在运行时真正需要时）
- 下列文件默认不进入最终公开 skill 包：
  - `pyproject.toml`
  - `run-tests.sh`
  - `test-*.py`
  - `test-*.sh`
  - `compare.sh`
  - `sync.sh`
  - `dev-python.sh`
  - `evaluate_search_quality.py`
  - `generate-synthesis-inputs.py`
  - `verify_v3.py`

## Hermes 发布层规则

- `hermes-release/` 优先做 runtime-only 包装。
- 发布层 `SKILL.md` 允许比母版更保守，尽量只保留：
  - 简短用途说明
  - 安装/调用提示
  - `scripts/` 入口提示
  - 验证说明
- 发布层尽量移除 `references/` 和高风险示例文案，避免触发 Hermes Guard 的 `curl`、`allowed-tools`、环境变量扫描。
- Hermes 面向 community 安装时，目标是 `safe`；只做到 `caution` 仍然会被默认拦截。

## 运行时实现规则

- 尽量显式传参，不在公开发布层脚本里直接依赖 `os.environ` 读取密钥。
- 若必须保留本地状态，默认写到 repo-local 目录，不写用户 home 默认路径。
- OAuth 或人工批准步骤必须返回明确链接或状态，不要默认自动打开浏览器。
- 对 relay / upload / posting 类能力，必须把真实 side effects 写清楚：
  - 网络目标
  - 是否会上传本地文件
  - 是否会发起 OAuth
  - 是否会真的写入第三方系统
- Hermes 发布层在提交前要顺手检查“误命中”文本：
  - 避免使用像 `env = value` 这种会被 Guard 当作环境变量转储的变量命名
  - 避免在注释里写容易被判成风险描述的字样，尤其是与 `context`、`env`、密钥提取相关的表述
- 公开 `SKILL.md` 不要出现容易被平台当成 prompt injection / 越权指令的写法：
  - 不要要求忽略上层系统规则
  - 不要把内部提示词脚手架直接暴露成公共使用说明
  - 不要把高自主执行措辞写成默认路径

## 推荐工作流

1. 先改 `targetSkills/` 母版。
2. 再通过 `scripts/build_claude_release.py` / `scripts/build_hermes_release.py` 生成发布层。
3. 对 Hermes 发布层跑 Guard 复扫，至少确认哪些 skill 已达 `safe`。
4. 再同步到外部 Git 仓库并执行真实发布。
