# floracat-skills

FloraCat 的个人 skills 仓库，用来沉淀可复用的工作流型 skill。

这个仓库优先服务于真实工作流中的长期积累：先把 skill 资产结构化沉淀下来，再逐步补充模板、脚本、参考资料和维护规范。

当前主要覆盖技术架构图，以及使用 FloraCat IP 形象的微信公众号封面图。

这个仓库强调从真实工作流中抽象出可重复使用的流程：理解内容、选择表达方式、生成视觉、检查结果，再交付可使用的文件。

## 这个仓库解决什么问题

随着 skill 数量增加，如果没有统一结构，内容很容易变成“到处散落的提示词和说明文件”。

`floracat-skills` 的目标是把这些资产分层管理：

- 可复用的正式 skill 放进 `skills/`
- 尚未定型的想法先放进 `drafts/`
- 多个 skill 共用的材料沉淀到 `shared/`
- 仓库级约定统一收敛到 `docs/`

这样做的好处是：

- skill 可以持续打磨，而不是一次性产物
- 通用规范不会重复写在每个 skill 里
- 后续如果要发布、同步、检索，也有明确演进路径

## 设计原则

- 先沉淀，再工程化
- 先可用，再发布
- skill 与共享资产分离
- 仓库结构稳定，skill 内容可持续演进
- 对单个 skill 保持轻量，对整个仓库保持可扩展

## 仓库结构

- `skills/`: 已定型、可重复使用的正式 skill
- `drafts/`: 仍在整理中的 skill 草稿
- `shared/references/`: 跨多个 skill 共用的参考资料
- `shared/templates/`: 跨多个 skill 共用的模板
- `shared/assets/`: 跨多个 skill 共用的素材
- `shared/prompts/`: 可复用 prompt 片段
- `docs/`: 仓库规范、命名规则、生命周期说明
- `scripts/`: 仓库级辅助脚本，包括通用 skill 评测入口
- `archive/`: 已废弃或历史版本

## 当前 skills

当前 skill 清单见：[skills-index.md](./skills-index.md)

### 1. floracat-architecture-diagram

用途：生成和修改适合演示、公众号、技术分享场景的 HTML/SVG 架构图、流程图、时序图。

特点：

- 输出为 standalone HTML + inline SVG
- 风格偏 PPT 化、人工编辑感强
- 强调箭头精准、排版清晰、中文可读性
- 适合对既有 SVG 图进行持续微调

位置：`skills/floracat-architecture-diagram`

对外发布包：`docs/floracat-architecture-diagram-release-pack.md`

### 2. floracat-wechat-cover

用途：根据文章、标题或架构图，生成使用 FloraCat IP 形象的微信公众号封面，并交付左侧大封面、右侧方形缩略封面的合成图。

支持三种表达方式：

- **场景化封面**：提炼文章的主题和使用场景，让 IP 人物在办公室、咖啡馆等环境中展示核心内容。
- **标题化封面**：以清晰的大标题为主，配合 IP 人物和少量主题元素。
- **架构图式封面**：保留原架构的关键节点、箭头方向和关系，配合标题与 IP 人物。

两种配色都可用于三种模式：**蓝紫色**（云雾、浅蓝与淡紫、深蓝标题）和 **浅黄色**（奶油白或浅黄底、深蓝文字、橙色强调）。IP 身份参考、配色与构图参考随 skill 打包，可从安装目录直接读取。

默认交付布局为左侧 **2.13:1** 大封面 + 右侧 **1:1** 缩略封面，两张图等高、无间距拼接。默认大图为 `2130×1000`，缩略图为 `1000×1000`，合成图为 `3130×1000`。缩略图单独构图，突出人物与短标题。

图片由宿主提供的图片生成或编辑工具生成，调用时传入对应参考图片文件。skill 内的 `scripts/compose_covers.py` 负责等比规范尺寸、拼接与校验，默认完整保留内容；裁切仅在明确选择 `--fit cover` 时使用。输出两张独立 PNG、一张合成 PNG，以及记录尺寸和拼接区域的 `layout.json`。

位置：[skills/floracat-wechat-cover](./skills/floracat-wechat-cover)

使用示例：

```text
$floracat-wechat-cover 根据这篇文章生成场景化公众号封面，蓝紫色风格，使用自带的 FloraCat IP，交付左大右小合成图。
```

```text
$floracat-wechat-cover 标题为“Jev：当 AI 的判断成为工程标准件”，生成浅黄色标题化封面。
```

```text
$floracat-wechat-cover 根据附件架构图生成浅黄色架构图式封面，保留原有节点和连接关系。
```

## 安装与使用

将需要的整个 skill 目录复制到宿主的 skills 目录，保留其中的 `references/`、`assets/`、`scripts/` 和 `evals/`：

- Codex：`~/.codex/skills/<skill-name>/`
- Claude Code：`~/.claude/skills/<skill-name>/`

封面生成需要宿主具有图片生成或编辑能力，并支持读取本地参考图片。拼接脚本需要 Python 3 和 Pillow；它只处理已有图片。具体流程、脚本参数和验收要求见该 skill 的 `SKILL.md`。

## 评测方式

仓库内提供基于 Claude Code CLI 的 skill 评测脚手架：

- 每个 skill 在自己的 `evals/evals.json` 中维护评测 case
- 使用 `scripts/run_skill_eval.py` 执行 baseline / with-skill 对比
- 结果输出到 `workspaces/<skill-name>/iteration-N/`
- 评测页自动生成到 `review.html`
- 评测 viewer 已内置到仓库

`evals.json` 中的案例是待运行的验证场景，不能单凭这些配置认定生成结果已经通过验收。封面图片还需检查文字、IP 一致性、架构关系和缩略图可读性；本地拼接检查不能代替实际出图验收。

示例命令：

```bash
python3 scripts/run_skill_eval.py floracat-architecture-diagram
```

更完整说明见：[docs/evaluation.md](./docs/evaluation.md)。

## 后续演进方向

后续可以逐步增加：

- skill 总索引自动生成
- skill 元数据规范
- 统一校验脚本
- 发布到公开仓或 marketplace 的流程
- 截图、示例、样板输出

在那之前，这个仓库首先是一套服务于日常工作的个人 skill 资产库。
