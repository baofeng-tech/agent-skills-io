# AgentSkills.so 结构与发布方案

## 1. 结论先说

截至 2026-04-21，`agentskills.so` 仍然没有像 ClawHub 那样公开一套很细的“上传 CLI 规范”，但从公开页面、搜索结果和 sitemap 可以清楚看出几件事：

- 它展示完整 `SKILL.md`
- 它展示 GitHub 仓库作者与 star 信号
- 它提供 `Download Skill.zip`
- 它的公开 skill 卡片会显示 `Published` / `Crawled` 时间
- 它的 `sitemap.xml` 每天更新大量 skill detail URL
- 它的底层结构与 `agentskills.io` 开放规范一致

因此，最稳的发布方式不是做平台私有格式，而是：

1. 先把 skill 做成严格、干净的 Agent Skills 公开目录
2. 放到公开 GitHub 仓库
3. 用 GitHub 仓库作为主要收录源
4. 同时准备好 root-flat ZIP 以应对手工导入/上传场景

本轮已经按这个思路新增：

- `agentskills-so-release/`

## 2. 这个平台实际上在吃什么

### 可以确认的

从 2026-04-20 公开页面可直接观察到：

- skill 页面会渲染 `SKILL.md` 的 frontmatter 和正文
- 页面会显示 GitHub 仓库作者
- 页面会显示 GitHub star
- 页面会提供 zip 下载

这说明这个平台至少非常重视：

- 标准 `SKILL.md`
- GitHub 仓库身份与信任信号
- skill 目录结构可被打包/下载

### 需要明确标注为推断的

当前没有看到 `agentskills.so` 公布一份完整的“提交协议”文档，也没有找到公开 submit 页面，因此下面这些要明确标成基于公开行为的工程推断：

- GitHub 仓库很可能是主要收录源
- `SKILL.md` 规范兼容性会直接影响是否被正确解析
- README、license、仓库元数据会影响人工或半自动收录判断
- crawler 会周期性刷新站内 skill 页面与 sitemap，而不是只做一次性导入

所以这条线要按“GitHub-first marketplace ingestion”来设计，而不是按平台专有包格式去赌。

## 3. 官方开放规范仍然是核心基准

`agentskills.io` 当前公开规范仍然强调：

- 一个合法 skill 至少要有 `SKILL.md`
- 可选目录是 `scripts/`、`references/`、`assets/`
- frontmatter 核心字段是：
  - `name`
  - `description`
- 可选字段包括：
  - `license`
  - `compatibility`
  - `metadata`
  - `allowed-tools`

这意味着：

- 对 `agentskills.so` 最重要的不是平台私有字段
- 而是把 skill 做成标准、稳定、可 GitHub 展示、可 ZIP 分发的公开目录

## 4. 之前 agentskill.sh 用的是哪个文件夹

本仓库原先已经有一条明确面向 GitHub / skills.sh 生态的发布层：

- `claude-release/`

仓库里的现有文档和脚本都已经把它描述为：

- `Claude / skills.sh / GitHub` 分发层

而 `agentskill.sh` 当前公开教程显示，它本质上也是：

- GitHub 仓库提交
- 按标准 skill 目录收录

所以在这次工作之前，仓库里“最接近 agentskill.sh 发布层”的其实就是：

- `claude-release/`

也就是说：

- 不是完全没有
- 但它是 Claude-oriented 命名，不够标准生态中立

## 5. 为什么还要新增 `agentskills-so-release/`

虽然 `claude-release/` 可以继续服务 `agentskill.sh` / `skills.sh` / GitHub 分发，但它的问题也很明显：

- 命名上偏 Claude
- frontmatter 清洗目标偏 Claude 生态
- 文档语气偏 Claude 发布说明

如果目标是：

- 被 `agentskills.so` 收录
- 面向更中立的 Agent Skills 生态
- 给 GitHub 公开仓库一个更标准的门面

那就应该有一个独立的标准化发布层。

这就是本轮新增 `agentskills-so-release/` 的原因。

## 6. 新增目录的设计原则

`agentskills-so-release/` 采用的是：

- 标准 skill 目录放在仓库根层
- 每个 skill 仍然保留 `SKILL.md`
- frontmatter 尽量靠近开放规范
- `metadata` 改为更扁平的公开字段
- 每个 skill 额外生成 README
- 每个 skill 额外生成 root-flat zip

目标结构：

```text
agentskills-so-release/
├── skill-a/
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   └── references/
├── skill-b/
├── zips/
│   ├── skill-a.zip
│   └── skill-b.zip
├── README.md
├── PUBLISHING.md
├── AUDIT.md
└── index.json
```

## 7. 为什么这样更容易被收录

### 结构正确

- marketplace crawler 一眼就能找到 root-level skill directories
- ZIP 上传场景也有对应产物

### frontmatter 更稳

- `name`
- `description`
- `license`
- `compatibility`
- flat `metadata`

这比继续带大量平台私有嵌套字段更适合标准生态展示。

### GitHub 信任信号更强

公开平台会看：

- repo 是否整洁
- README 是否清楚
- skill 是否能独立阅读
- 依赖和副作用是否表达明确

`agentskills-so-release/` 就是为这件事准备的。

## 8. 发布时的具体注意事项

### 目录层

- skill 目录必须放在仓库根层
- `name` 必须与目录名一致
- 不要把 skill 再多包一层目录

### frontmatter 层

- `description` 既要写“做什么”，也要写“什么时候用”
- `compatibility` 要明确依赖与联网需求
- `metadata` 尽量保持扁平，不要过度平台私有化

### GitHub 层

- 仓库必须公开
- README 要解释这个仓库是公开 skill catalog
- skill 目录不要混入无关缓存、测试垃圾、临时构建物

### 安全层

- OAuth、发帖、上传、远程 API、持久化路径等副作用要明确写清
- 尽量用 repo-local state，避免 home-directory 默认写入
- 不要把内部测试脚本和高风险 helper 一起带进公开层

## 9. 本轮新增的实际产物

本轮已经新增：

- `agentskills-so-release/`
- `scripts/build_agentskills_so_release.py`
- `scripts/publish-agentskills-so-release.sh`

这个目录现在承担：

- `agentskills.so` 的标准生态发布层
- 一个比 `claude-release/` 更中立的 GitHub 公开分发层
- `agentskill.sh` 的备用或后续替代投递层

## 10. 推荐实际投递顺序

### 先做 GitHub 公开仓库

把 `agentskills-so-release/` 内容推到独立 public repo root。

### 再做两个目录提交 / 收录跟踪

1. 把 `agentskills-so-release/` 推到独立 public GitHub repo root
2. 确保 repo 首页、LICENSE、root catalog 文件都已就位
3. 观察 `agentskills.so` 是否在后续 crawler 周期中出现对应作者页 / skill detail 页
4. 如果仍未出现，再寻找站点 contact / issue / 社区入口做人工触达

这样两个平台吃的是同一份标准层。

## 11. 2026-04-21 新补到的人工入口

这轮重新核官网首页，已经拿到两个公开人工入口：

- 支持邮箱：`support@agentskills.so`
- Discord 邀请链接：`https://discord.gg/gwyWY8v9Ed`

官网首页 FAQ 当前明确写着：

- `Have another question about Agent Skills? Contact us on Discord or by email.`

这说明截至 2026-04-21：

- 仍然没有找到公开 `submit skill` 页面
- 但平台确实提供了公开人工触达通道

因此当前更稳的推进顺序是：

1. 保持 `baofeng-tech/agent-skills-so` 仓库结构完全符合 crawler 预期
2. 等待一个 crawler 周期观察是否自然收录
3. 若仍未出现，再带上 GitHub repo、代表 skill、目录结构说明，通过 `support@agentskills.so` 或 Discord 做人工收录请求

## 12. 最终建议

对外公开时，推荐这样用：

- `agentskill.sh`
  - 历史上可继续用 `claude-release/`
  - 但更推荐逐步切到 `agentskills-so-release/`
- `agentskills.so`
  - 直接用 `agentskills-so-release/`

这会让整个 Agent Skills 生态的发布口径更统一，也更适合后续被更多兼容平台复用。
