# 爆款 Skill / Plugin 名称与账号记录（2026-04-28）

## 目的

把当前 ClawHub breakout 变体、对应 plugin、以及观察到的发布账号句柄单独记录，避免后续混淆“母版名”“原版 slug”“breakout slug”“plugin slug”。

## 当前 breakout 变体来源

当前唯一来源文件：

- `targets/clawhub-breakout-variants.json`

当前声明的 breakout 变体有 4 个，覆盖 3 个母版来源。

## 额外说明：fallback slug 也要单独跟踪

breakout slug 和 owner-conflict fallback slug 不是一回事：

- breakout slug
  - 是 `targets/clawhub-breakout-variants.json` 里主动声明的增长位兄弟包
- fallback slug
  - 是因为 ClawHub owner/slug 冲突，发布器按 `suffix-by-aisa` 策略临时或长期接受的替代 live slug
  - 2026-05-07 起，新 fallback 优先使用 `-aisa` / `-aisa-api` / `-aisa-one`，历史 `-slotN` 只作为旧状态兼容

当前已经确认需要长期跟踪的历史 slot fallback 例子：

- source key: `skill:aisa-provider`
  - live slug: `aisa-provider-slot3`
  - live owner: `aisadocs`
- source key: `plugin:aisa-provider-plugin`
  - live slug: `aisa-provider-slot3-plugin`
  - live owner: `aisadocs`
  - 规则：plugin fallback slug 跟随同名 skill 的 fallback slug，而不是各自独立乱跳

2026-05-08 breakout 续推后新增确认的 AIsa 后缀 fallback：

- source key: `plugin:aisa-twitter-api-command-center-plugin`
  - live slug: `aisa-twitter-api-command-center-aisa-api-plugin`
  - live publisher: `bibaofeng`
- source key: `skill:aisa-twitter-research-engage-relay`
  - live slug: `aisa-twitter-research-engage-relay-aisa-api`
  - live owner: `bibaofeng`
- source key: `plugin:aisa-twitter-research-engage-relay-plugin`
  - live slug: `aisa-twitter-research-engage-relay-aisa-api-plugin`
  - live publisher: `bibaofeng`
- source key: `skill:twitter-post-aisa`
  - live slug: `twitter-post-aisa-aisa-one`
  - live owner: `aisadocs`

当前工作结论：

1. 如果拿不到旧 slug 的原 owner token，就正式接受 fallback slug 作为当前 live 事实，但新命名优先使用 AIsa 后缀。
2. `targets/clawhub-publish-state.json` 必须同时保留：
   - 原始 artifact key
   - `published_name`
   - live `detail_url`
   - live `publisher_handle`
3. `targets/clawhub-live-status.json` 的扫描结果也必须围绕 fallback live slug 回写，而不是再把结果错误归到旧 canonical slug 视角。

## 1. `aisa-twitter-api` 家族

### 母版 skill

- source skill: `aisa-twitter-api`
- 母版目录：`targetSkills/aisa-twitter-api`

### ClawHub breakout skill

- breakout slug: `aisa-twitter-api-command-center`
- 发布层目录：`clawhub-release/aisa-twitter-api-command-center`
- 当前 live 状态：`clean`
- 当前 live skill slug：`aisa-twitter-api-command-center`
- 当前 live skill owner：`aisadocs`

### ClawHub breakout plugin

- plugin slug: `aisa-twitter-api-command-center-plugin`
- 发布层目录：`clawhub-plugin-release/plugins/aisa-twitter-api-command-center-plugin`
- 当前 live 状态：`clean`
- 当前 live plugin slug：`aisa-twitter-api-command-center-aisa-api-plugin`
- 当前 live plugin publisher：`bibaofeng`

### 对照的旧原版

- skill slug: `aisa-twitter-api`
- plugin slug: `aisa-twitter-api-plugin`

## 2. `aisa-twitter-engagement-suite` 家族

### 母版 skill

- source skill: `aisa-twitter-engagement-suite`
- 母版目录：`targetSkills/aisa-twitter-engagement-suite`

### ClawHub breakout skill

- breakout slug: `aisa-twitter-research-engage-relay`
- 发布层目录：`clawhub-release/aisa-twitter-research-engage-relay`
- 当前 live 状态：`clean`
- 当前 live skill slug：`aisa-twitter-research-engage-relay-aisa-api`
- 当前 live skill owner：`bibaofeng`

### ClawHub breakout plugin

- plugin slug: `aisa-twitter-research-engage-relay-plugin`
- 发布层目录：`clawhub-plugin-release/plugins/aisa-twitter-research-engage-relay-plugin`
- 当前 live 状态：`clean`
- 当前 live plugin slug：`aisa-twitter-research-engage-relay-aisa-api-plugin`
- 当前 live plugin publisher：`bibaofeng`

### 对照的旧原版

- skill slug: `aisa-twitter-engagement-suite`
- plugin slug: `aisa-twitter-engagement-suite-plugin`

### 额外 ClawHub 修复 / 增长 slug

- breakout slug: `twitter-post-aisa`
- 发布层目录：`clawhub-release/twitter-post-aisa`
- plugin slug: `twitter-post-aisa-plugin`
- 发布层目录：`clawhub-plugin-release/plugins/twitter-post-aisa-plugin`
- 当前 live skill 状态：`clean`
- 当前 live skill slug：`twitter-post-aisa-aisa-one`
- 当前 live skill owner：`aisadocs`
- 当前 live plugin 状态：`clean`
- 当前 live plugin slug：`twitter-post-aisa-plugin`
- 当前 live plugin publisher：`bibaofeng`
- 当前用途：保留原 URL/原 slug 的发帖后跟进增长位，不替代 `aisa-twitter-engagement-suite` 母版

## 3. `aisa-tavily` 家族

### 母版 skill

- source skill: `aisa-tavily`
- 母版目录：`targetSkills/aisa-tavily`

### ClawHub breakout skill

- breakout slug: `aisa-tavily-search`
- 发布层目录：`clawhub-release/aisa-tavily-search`
- 当前 live 状态：`clean`
- 当前 live skill owner：`bibaofeng`

### ClawHub breakout plugin

- plugin slug: `aisa-tavily-search-plugin`
- 发布层目录：`clawhub-plugin-release/plugins/aisa-tavily-search-plugin`
- 当前 live 状态：`clean`
- 当前 live plugin publisher：`bibaofeng`

## 当前判断

### 不会直接冲突的点

- 原版 slug 和 breakout slug 目前都不同
- skill 与 plugin 也都各自使用独立 slug

### 仍然容易混淆的点

- `clawhub-release/` 当前是平铺目录
- `clawhub-plugin-release/plugins/` 也是平铺目录
- 人在看目录时，很容易把：
  - 原版
  - breakout 版
  - plugin 版
  混成一层

## 当前建议

1. 继续保留 breakout slug 清单文件作为唯一声明入口。
2. 继续把母版 skill、原版 ClawHub skill、breakout ClawHub skill、plugin slug 分开记录。
3. 目录暂不物理拆层，原因是当前 publish / test / live-status 脚本都依赖 flat-root 发现方式。
4. 如果 breakout 继续扩到 5 组以上，再统一做一轮物理目录重构。
