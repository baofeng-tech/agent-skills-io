# Claw平台排名  [https://clawcharts.com/](https://clawcharts.com/)

# 做三件事情：

# 1\. 在三个平台上上传（包括 OpenClaw 的 ClawHub.ai、Hermes 和 Claude）

# 2\. 上传两类技能：一个是 skills，另外一个是 plugin

# 3\. 我们不仅是要上传新的，还要把之前上传过的 skills 做一些修复和更新

#   平台一：Hermes Platform

Q： 研究这个项目 https://github.com/NousResearch/hermes-agent 和Openclaw对标，是否可以把之前面相Clawhub写的Skills, 给Openclaw写的PR改写提交到hermes上去？  https://github.com/AIsa-team/openclaw/pull/1

A: Let me research the Hermes Agent project first.这个 PR diff 太大了（320k 行删除），看起来是 OpenClaw 主仓的一个大型重构 PR。让我聚焦于关键对比分析：现在我有了完整的画面。让我给你分析：

---

Jordan，分析完了。以下是结论：

## **Hermes Agent vs OpenClaw 对标**

两者在 skill 系统上高度兼容——都使用 `SKILL.md` \+ YAML frontmatter \+ `scripts/` \+ `references/` 的结构，格式几乎一致。Hermes 明确声称兼容 [agentskills.io](https://agentskills.io/) 开放标准，和 OpenClaw/ClawHub 用的是同一套规范。

**关键差异：**

| 维度 | OpenClaw/ClawHub | Hermes Agent |
| ----- | ----- | ----- |
| 技术栈 | TypeScript/Node.js | Python |
| Skill 格式 | `SKILL.md` \+ `metadata.openclaw` | `SKILL.md` \+ `metadata.hermes` |
| 分发 | ClawHub registry / `clawhub publish` | Skills Hub / `hermes skills install` \+ GitHub |
| Provider 扩展 | `openclaw.plugin.json` \+ TypeScript plugin SDK | 直接改 Python 代码或用 skill 包装 |
| 已有 Polymarket | ❌ 无（你的 prediction-market skill 是新增） | ✅ 已有 `skills/research/polymarket/`（但只用公共 API，无 Kalshi，无 AIsa） |
| AIsa 集成 | PR \#1 是加 AIsa provider | ❌ 完全没有 |

## **能否改写提交？**

**可以，而且有明确价值。** 具体分三层：

### **1\. AIsa Prediction Market Skill → `optional-skills/research/aisa-prediction-markets/` ✅ 强推**

Hermes 现有的 `polymarket` skill 只支持 Polymarket 公共 API，**不支持 Kalshi，没有跨平台套利，没有 Python client 脚本**。你的 prediction-market skill 通过 AIsa 统一了 Polymarket \+ Kalshi \+ 跨平台体育市场，是明显的增量。放在 `optional-skills/` 最合适（因为需要 `AISA_API_KEY`，不是零依赖）。

改写工作量很小：把 `metadata.openclaw` 改成 `metadata.hermes`，调整 frontmatter 加上 `author`、`tags`，把路径引用从 `{baseDir}` 改成 Hermes 的路径约定。

### **2\. AIsa Provider（PR \#1 核心）→ 两种路径**

PR \#1 的核心是给 OpenClaw 加 AIsa 作为 native provider（TypeScript plugin）。Hermes 的 provider 系统不同——它用 OpenAI-compatible 端点，通过 `hermes model` 命令配置，不需要写 TypeScript plugin。

**路径 A：提交一个 AIsa skill（推荐）**  
 写一个 `optional-skills/` 下的 skill 教 Hermes 如何通过 AIsa 访问中国模型（Qwen、Kimi、DeepSeek 等），包含配置指南和模型列表。

**路径 B：提 PR 加 AIsa 为 built-in provider**  
 修改 `cli.py` / `run_agent.py` 加 AIsa 作为一个 provider option（类似现有的 OpenRouter、z.ai/GLM、Kimi/Moonshot 支持）。工作量更大但影响面大得多——Hermes 已经支持 Kimi/Moonshot 和 MiniMax 作为独立 provider，AIsa 作为统一入口正好解决了碎片化问题。

### **3\. Twitter Command Center → `optional-skills/communication/aisa-twitter/` ✅ 可行**

Hermes 没有 Twitter/X 数据访问 skill。可以直接改写放入。

## **不能直接搬的**

OpenClaw PR \#1 的 `openclaw.plugin.json` \+ TypeScript `definePluginEntry` 代码是 OpenClaw 特有的 plugin SDK，不能直接用于 Hermes。需要重写成纯 SKILL.md \+ Python scripts 的形式。

---

**建议优先级：**

1. **prediction-market** → Hermes `optional-skills/`（差异化最大，Hermes 现有 polymarket 不支持 Kalshi）  
2. **AIsa provider** → 作为 skill 或 built-in provider PR  
3. **Twitter** → `optional-skills/`

要我现在帮你改写 prediction-market skill 成 Hermes 格式并准备 PR？

Q：  AIsa有大量的Skills和Plugins, 不仅仅是Prediction Market Skill. Hermes有类似Clawhub这种skill marketplace吗？

A： 这下信息很充分了。Hermes 的 skill 生态比我之前分析的要丰富得多。

---

Jordan，关键发现来了——Hermes 的 skill marketplace 生态相当完整，而且**原生兼容 ClawHub**：

## **Hermes Skills Hub 全景**

Hermes 的 skill 安装系统支持 **6 个来源**，全部统一在 `hermes skills` CLI 下：

| 来源 | 命令 | 说明 |
| ----- | ----- | ----- |
| **Official optional** | `hermes skills install official/...` | repo 内 `optional-skills/`，builtin 信任 |
| **GitHub repos** | `hermes skills install github:org/repo/path` | 任意 GitHub repo |
| **skills.sh** | `hermes skills search --source skills-sh` | agentskills.io 官方 marketplace |
| **ClawHub** | `hermes skills install clawhub:<slug>` | ⚡ **直接兼容 ClawHub** |
| **Claude marketplace** | 兼容 Claude plugin manifest | 自动转换 |
| **LobeHub** | 自动从 LobeHub catalog 转换 | 社区源 |
| **Well-known URLs** | `/.well-known/skills/index.json` | 去中心化发现 |
| **Custom taps** | `hermes skills tap add org/repo` | 自建 registry |

**核心发现：Hermes 代码里有 `ClawHubSource` 适配器**（`tools/skills_hub.py` 第870行），直接对接 ClawHub registry API。也就是说——

## **AIsa 发在 ClawHub 上的所有 Skills，Hermes 用户已经能直接装了**

```shell
# Hermes 用户装你的 prediction-market skill
hermes skills install clawhub:aisa/prediction-market

# 装你的 twitter skill  
hermes skills install clawhub:aisa/twitter-command-center
```

你不需要"改写提交到 Hermes"——**你只需要把 skills 发到 ClawHub，Hermes 用户就自动能用。** 这就是 agentskills.io 开放标准的威力。

## **但还有增量机会**

虽然 ClawHub skills 可以直接被 Hermes 安装，但要在 Hermes 生态获得更大曝光，有几个额外动作值得做：

**1\. 发布到 agentskills.io / skills.sh** 这是 Hermes 的"官方推荐" marketplace。AIsa 可以直接把 skills 发到这里，获得跨平台可见性（Hermes、Claude Code、Cursor、Codex 都兼容）。

**2\. 提交到 HermesHub（hermeshub.xyz）** 社区驱动的 Hermes skill hub，带安全扫描（65+ threat rules）。目前才 22 个 verified skills，早期入驻有先发优势。

**3\. PR 到 `optional-skills/`** AIsa 作为一个统一中国模型 gateway 的 provider skill，放到 Hermes 官方 `optional-skills/` 里是合理的——Hermes 已经单独支持 Kimi/Moonshot 和 MiniMax，但没有统一入口。提一个 PR 把 AIsa provider skill 加到 `optional-skills/research/` 或 `optional-skills/productivity/`，被合并后就变成 "official" 来源，安装时不需要安全确认。

**4\. 支持 `/.well-known/skills/index.json`** 在 `aisa.one` 域名下发布 well-known endpoint，让 Hermes 用户可以：

```shell
hermes skills search https://aisa.one --source well-known
```

这是最去中心化的方式，不依赖任何第三方 registry。

**发布Skills到[Agentskills.so](http://Agentskills.so)  [baofeng@aisa.one](mailto:baofeng@aisa.one) [haonan liu](mailto:haonan@aisa.one)**

Jordan，skill 包已经打好了，完全符合 agentskills.io 规范。

用Claude打包的：  
[https://drive.google.com/drive/folders/18aHF\_TkTWarUgTHkp5p4YIWq4nliqwVz?usp=drive\_link](https://drive.google.com/drive/folders/18aHF_TkTWarUgTHkp5p4YIWq4nliqwVz?usp=drive_link)

总结一下关键参数和发布步骤：

**规范合规性：**

| 检查项 | 结果 |
| ----- | ----- |
| `name` 格式（小写+连字符，≤64字符，匹配目录名） | ✅ `aisa-twitter-command-center` (27字符) |
| `description` ≤1024字符，包含触发关键词 | ✅ 346字符 |
| `license` | ✅ Apache-2.0 |
| `compatibility` ≤500字符 | ✅ 59字符 |
| `metadata` (author, version, tags) | ✅ 5个键 |
| Body \< 500行 / \< 5000 tokens | ✅ 129行 / \~1065 tokens |
| Progressive disclosure（重型参考拆到 `references/`） | ✅ 完整API表在 `references/api-endpoints.md` |
| Scripts 语法合法 | ✅ 2个 Python 文件均通过 |

**发布步骤：**

**1\. 推到 GitHub**

```shell
# 在 AIsaONE/agent-skills 仓库下（建议新建这个 repo 作为统一 skill 仓库）
git clone https://github.com/AIsaONE/agent-skills.git
cp -r aisa-twitter-command-center/ agent-skills/
cd agent-skills && git add -A && git commit -m "add aisa-twitter-command-center skill" && git push
```

**2\. 提交到 agentskill.sh** 打开 `https://agentskill.sh/submit` → 粘贴 repo URL → Analyze & Import

**3\. 触发 skills.sh 注册**

```shell
npx skills add AIsaONE/agent-skills --yes
```

skills.sh 通过首次安装的 telemetry 自动注册 listing。

**4\. Hermes 用户安装**

```shell
hermes skills install github:AIsaONE/agent-skills/aisa-twitter-command-center
```

三个 marketplace（agentskill.sh、skills.sh、Hermes Hub）用的是同一份文件，一次发布全平台可用。

## **战略建议**

AIsa 的 skill 矩阵（LLM、Twitter、Search、Finance、Prediction Market、YouTube、Media Gen 等）不需要逐个改写适配 Hermes——**它们已经通过 ClawHub 桥自动可用**。你需要做的是：

1. **确保所有 skills 都发到 ClawHub**（你刚才打包的几个已经就绪）  
2. **在 aisa.one 发布 `/.well-known/skills/index.json`**，列出所有 AIsa skills 的索引  
3. **提一个 Hermes PR**：`optional-skills/productivity/aisa/SKILL.md`——不是单个 skill，而是一个 **meta-skill**，教 Hermes 用户如何通过一个 `AISA_API_KEY` 访问 AIsa 全部能力（类似 OpenRouter 在 Hermes 里的定位）  
4. **在 awesome-hermes-agent 提 PR**，把 AIsa skills 加到 "\[production\] skills" 列表里