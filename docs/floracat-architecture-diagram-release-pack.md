# floracat-architecture-diagram Release Pack

这份发布包只服务于 `floracat-architecture-diagram` 这个 skill，用于对外发布时直接复用。

适用场景：

- GitHub 仓库首页简介
- Skills 平台上架文案
- 公众号 / 知乎 / 小红书 / Product Hunt 简介
- 朋友推荐、群内转发、社区自荐

## 1. Skill 定位

一句话定位：

`floracat-architecture-diagram` 用来把 Mermaid、草图式流程图或模糊需求，整理成适合公众号和演示场景的 standalone HTML + SVG 架构图。

核心价值：

- 不只是“能画图”，而是能画出人类愿意看的图
- 输出不是 Mermaid，而是可直接交付的 HTML + inline SVG
- 强调中文可读性、节点分层、箭头准确性和排版稳定性
- 特别适合架构图、流程图、时序图、Agent 架构图这类需要持续微调的图

适合的人群：

- 写技术公众号的人
- 做产品架构说明的人
- 需要给老板、客户、团队展示系统结构的人
- 想把 AI 输出的“草图感”图表变成“可发布成品”的人

## 2. GitHub 用文案

### Repo Description

用于 GitHub 仓库描述，建议直接放在仓库简介栏：

`A skill for creating PPT-like architecture, flow, sequence, and agent diagrams in standalone HTML/SVG with precise arrows and publication-ready readability.`

### Repo Subtitle 中文版

`一个把架构图、流程图、时序图和 Agent 图做成“可发布成品”的 HTML/SVG skill。`

### README 开头短介绍

```md
`floracat-architecture-diagram` 是一个专门用于生成和修改技术图的 skill。

它的目标不是产出“能运行的图代码”，而是产出“人类能直接拿去展示的图”。

适合的图类型包括：

- 总体架构图
- 核心运行链路图
- 时序图
- Agent 设计模式图
- 多 Agent 协作图

默认输出为 standalone HTML + inline SVG，强调中文可读、箭头精准、布局稳定、整体风格接近 PPT 成品。
```

### GitHub Topics

建议 topics：

- `ai-skill`
- `claude-skill`
- `codex-skill`
- `architecture-diagram`
- `svg-diagram`
- `html-svg`
- `sequence-diagram`
- `flow-diagram`
- `agent-design`
- `multi-agent`
- `prompt-engineering`
- `technical-writing`

## 3. Skills 平台上架文案

### Title

`floracat-architecture-diagram`

### Short Description

`Create PPT-like architecture and agent diagrams in standalone HTML/SVG with clear Chinese labels and precise arrows.`

### Long Description

`floracat-architecture-diagram is a diagram-focused skill for turning rough technical ideas into publication-ready HTML/SVG visuals. It is designed for architecture diagrams, runtime flows, sequence diagrams, and modern agent-system diagrams. The skill prioritizes readable Chinese labels, precise arrow routing, balanced spacing, and a polished PPT-like visual style instead of raw Mermaid output. It is especially useful when a diagram needs multiple rounds of refinement and must look understandable to real people, not just engineers reading source code.`

### When To Use

`Use this skill when you need a human-readable architecture, flow, sequence, or agent diagram in standalone HTML/SVG, especially for blogs, presentations, team docs, or public-facing technical content.`

### Key Differentiators

- `HTML + inline SVG output, not just Mermaid`
- `Better for Chinese technical publishing`
- `Arrow precision and overlap handling are first-class concerns`
- `Designed for iterative refinement, not one-shot rough diagrams`
- `Strong fit for Agent architecture visuals`

## 4. 社区发布短文案

### 中文短版

`我做了一个 diagram skill：floracat-architecture-diagram。它专门把架构图、流程图、时序图、Agent 图做成 standalone HTML + SVG，不是 Mermaid 草图风，而是更接近公众号 / PPT 的成品风格。重点优化中文可读性、箭头准确性和版式稳定性。`

### 中文稍长版

`最近把自己一直在反复打磨的画图流程整理成了一个 skill：floracat-architecture-diagram。它适合生成和修改架构图、流程图、时序图，以及这两年很常见的 Agent / Multi-Agent 架构图。输出是 standalone HTML + inline SVG，重点不是“代码最短”，而是“人能一眼看懂，拿去就能展示”。如果你也经常需要把技术结构讲给非研发同学、客户或公众号读者看，这个 skill 会比较顺手。`

### 英文短版

`I packaged my diagram workflow into a reusable skill: floracat-architecture-diagram. It generates publication-ready architecture, flow, sequence, and agent diagrams in standalone HTML/SVG, with a stronger focus on readability, layout control, and precise arrows than typical Mermaid-based outputs.`

## 5. 公众号 / 知乎标题建议

可选标题：

- `我把“技术架构图美化”做成了一个可复用 skill`
- `一个专门画架构图和 Agent 图的 HTML/SVG skill`
- `让 AI 画出来的技术图，从草图感变成成品感`
- `如何把 Mermaid 风格的图，改成适合公众号发布的图`
- `我做了一个专门生成 Agent 架构图的 skill`

## 6. 发布检查表

正式对外发布前，建议确认：

- 仓库 README 首页能在 10 秒内说明这个 skill 是干什么的
- 至少有 2 到 4 张代表性图例
- 有一个最短使用示例
- 有明确的安装方式或复制方式
- 有一页评测结果对比
- 平台简介和 GitHub 简介口径一致
- skill 名称、`SKILL.md` frontmatter、平台标题保持一致

## 7. 最推荐的发布组合

如果只发一轮，推荐：

1. GitHub 仓库作为主发布页
2. 公众号或知乎发一篇图例展示文章
3. Skills 平台发一份简版 listing，把流量导回 GitHub

这套顺序最稳，因为：

- GitHub 负责承载完整信息
- 中文内容平台负责解释使用场景
- Skills 平台负责被搜索和被发现

## 8. 对外表达的重点

发布时最该强调的不是“我也能画图”，而是这三点：

- `它输出的是可交付的 HTML/SVG 成品，不是草图`
- `它特别适合中文技术内容发布`
- `它对 Agent 架构图这类复杂关系图尤其有价值`
