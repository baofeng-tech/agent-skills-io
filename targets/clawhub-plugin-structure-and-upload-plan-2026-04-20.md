# ClawHub Plugin 结构与发布方案

## 1. 结论先说

截至 2026-04-21，OpenClaw / ClawHub 文档已经明确把插件分成两条路：

1. `Code Plugin`
2. `Bundle Plugin`

而且当前文档还明确说明：

- native plugin 必须有 `openclaw.plugin.json`
- 兼容 bundle 可以用 `.claude-plugin/plugin.json`
- 如果两种标记同时存在，OpenClaw 会优先按 native plugin 处理

因此本仓库当前这批 AIsa 资产，最佳路径不再是“只有 Claude bundle 外壳”，而是：

- 用 `openclaw.plugin.json` + `package.json` + `index.ts` + `skills/<skill>/` 生成 native-first code plugin
- 同时保留 `.claude-plugin/plugin.json`，让包继续兼容 Claude marketplace 生态
- 用 native-first dual-format 先占住 ClawHub plugin 分发位，再根据爆款信号决定是否继续做更重的 runtime 能力扩展

这条路径更稳，也更符合你当前“先爆款、后纵深”的策略。

## 2. 为什么现在优先做 Bundle Plugin

### 不是所有 skill 都该硬变成重型 runtime Code Plugin

当前 AIsa 这批资产的本质仍然是：

- skill-first
- 以 `SKILL.md` + `scripts/` 为主
- 更像“可安装工作流能力包”

如果直接改成带复杂 runtime 能力的 native OpenClaw code plugin，需要额外承担：

- `openclaw.plugin.json`
- `openclaw.extensions`
- native runtime entrypoint
- config schema
- 更多安装/运行时责任

这会把当前发布工作从“分发包装”变成“产品重构”。

### Native-first 包壳更适合现在的发布目标

OpenClaw 当前文档已经说明：

- `openclaw.plugin.json` 是 native plugin 的正式清单
- 插件可以通过 manifest 声明 `skills` 目录，把 skill payload 跟 plugin 一起发
- Claude bundle 只是兼容 bundle 形态，不是 ClawHub code plugin 的正式替代
- `clawhub package publish` 用于 plugin 包发布

所以当前阶段更合理的做法是：

- 保持 skill 语义不变
- 增加 native plugin 外壳
- 保留 Claude bundle fallback
- 让它进入 plugin catalog

## 3. ClawHub 当前发布规则

### 发布命令

plugin 不是走 `clawhub skill publish`，而是：

```bash
clawhub package publish <source>
```

`<source>` 可以是：

- 本地目录
- `owner/repo`
- `owner/repo@ref`
- GitHub URL

### native code plugin 的关键结构

当前最重要的结构不是只放 `.claude-plugin/plugin.json`，而是至少具备：

- `openclaw.plugin.json`
- `package.json`
- `openclaw.extensions`
- native entrypoint（比如 `index.ts`）
- 如果要让 plugin 自动带出 skill，再在 `openclaw.plugin.json` 中声明 `skills`

本仓库当前先用最轻量的 native wrapper：

- `index.ts` 只提供最小 `register()` 壳
- 真正的能力仍来自打包进去的 `skills/<skill>/`
- 配置校验通过 `openclaw.plugin.json` 里的 `configSchema` 暴露

### dual-format 的现实策略

OpenClaw 当前也明确支持 bundle 检测：

- `.claude-plugin/plugin.json`
- 默认 Claude bundle layout
- 以及其他兼容 bundle marker

因此本仓库新增的 `clawhub-plugin-release/` 采用：

```text
plugin-name/
├── openclaw.plugin.json
├── index.ts
├── .claude-plugin/
│   └── plugin.json
├── package.json
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       └── ...
└── README.md
```

这不是“Claude plugin 冒充 ClawHub plugin”，而是：

- 以 OpenClaw native 结构为主
- 用 `.claude-plugin/plugin.json` 作为兼容补充
- 让同一个包在 ClawHub / OpenClaw / Claude marketplace 路径上都更顺滑

## 4. 结合 skillGet 的爆款判断

`D:\workplace\skillGet` 这边在 2026-04-20 的插件分析里已经有几个很清楚的结论：

- 真正排前面的多数是 `Code Plugin`
- 名称越直接指向系统/任务，越容易赢
- `source-linked + clean/benign` 是强信任资产
- 插件不是越大越好，而是越“副作用边界清楚”越好

这对当前 AIsa 的启发是：

### 第一阶段

先用 bundle plugin 把现有高价值 AIsa skill 体系全部占住。

重点是：

- 结构正确
- 来源清楚
- 副作用清楚
- 运行边界清楚

### 第二阶段

再从真实表现里挑几条最值得 code 化的主线：

- Governance / Security
- Growth / Business Ops
- Commerce / Storage / Chain
- 外部 SaaS Connector

也就是说：

- 现在新增 `clawhub-plugin-release/`
- 不等于现在就把 51 个 skill 全改造成 native code plugin

## 5. 仓库里新增的实际产物

本轮已经新增并修正：

- `clawhub-plugin-release/`
  - `plugins/<skill>-plugin/`
  - `zips/<skill>-plugin.zip`
- `scripts/build_clawhub_plugin_release.py`
- `scripts/publish-clawhub-plugin-release.sh`

每个 plugin 包：

- 内嵌 1 个已清洗过的 `clawhub-release` skill
- 带 `openclaw.plugin.json`
- 带 `index.ts`
- 带 `.claude-plugin/plugin.json`
- 带 `package.json` 的 `openclaw` 块
- 带 root-flat zip

## 6. 推荐发布顺序

不建议 51 个一起首发。

建议先发：

1. `aisa-twitter-command-center-plugin`
2. `aisa-twitter-post-engage-plugin`
3. `aisa-youtube-search-plugin`
4. `aisa-youtube-serp-scout-plugin`
5. `last30days-plugin`
6. `market-plugin`

理由：

- 主题清晰
- 能直接体现 AIsa 的远程能力
- 更容易让 ClawHub 用户理解“安装后能做什么”

## 7. 发布时要注意什么

### 结构层

- zip 根目录不能多一层包壳
- 必须让 `openclaw.plugin.json`、`index.ts`、`package.json`、`.claude-plugin/`、`skills/` 直接出现在 archive root

### 信任层

- README 必须清楚写：
  - 这是 native-first plugin，不是只有 Claude bundle 的兼容包
  - 内嵌 skill 在 `skills/<skill>/`
  - 需要哪些环境变量
  - 数据会发往哪里

### 选品层

- plugin 名要直说系统或任务
- 描述要强调“安装后获得什么能力”
- 不要把 bundle plugin 页面写成 skill 页面复读

## 8. 2026-04-21 真实发布验证

本轮已经把 `clawhub-plugin-release/` 接到了真实可用的 ClawHub 发布环境。

### 本机环境现状

- 已安装 `clawhub` CLI：`v0.9.0`
- 已安装 `openclaw` CLI：`2026.3.28`
- 已成功使用本地 ClawHub 账号 `@bibaofeng` 登录

### 官方文档与本机 CLI 的一个差异

官方文档当前写了：

```bash
clawhub package publish your-org/your-plugin --dry-run
```

但本机可安装到的 `clawhub v0.9.0` 实测 **不支持** `--dry-run`。

也就是说：

- 文档描述的是较新的命令面
- 当前可用 CLI 只能直接走真实 publish
- 发布前要先靠本地结构校验脚本把风险收敛好

### 本轮已真实发布成功的首批 plugin

1. `aisa-multi-search-engine-plugin`
2. `aisa-twitter-command-center-plugin`
3. `market-plugin`
4. `last30days-plugin`
5. `aisa-twitter-post-engage-plugin`
6. `aisa-youtube-search-plugin`
7. `aisa-youtube-serp-scout-plugin`

发布后通过 `clawhub package inspect <name>` 可以直接查到：

- Family: `Code Plugin`
- Channel: `community`
- Source Repo: `baofeng-tech/agent-skills-io`
- Source Commit: `048abaf`
- Verification: `source-linked / artifact-only`

当前首批 7 个包的扫描状态都还是：

- `Scan: pending`

所以这一步现在的真实状态是：

- 已发布
- 已被 registry 识别
- 等待站内扫描与后续公开展示面刷新

## 9. 后续升级路线

等第一批 native-first plugin 有真实反馈后，再判断哪些值得继续升成更重的 runtime code plugin：

- 如果需要真正的 OpenClaw runtime hooks
- 如果需要 config schema
- 如果需要 provider/channel/guard 类 runtime entry
- 如果需要强平台集成

才进入 code plugin 路线。

当前这轮新增的目标，是：

- 先完成发布层闭环
- 先进入 plugin catalog
- 先开始拿真实市场信号
