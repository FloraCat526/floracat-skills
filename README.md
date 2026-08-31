

# floracat-skills

FloraCat 的个人 skills 仓库，用来沉淀可复用的工作流型 skill。

这个仓库优先服务于真实工作流中的长期积累：先把 skill 资产结构化沉淀下来，再逐步补充模板、脚本、参考资料和维护规范。

当前主要覆盖小红书图文生成、底层 PNG 图片生成，以及适合技术表达场景的图表与可视化能力。

这个仓库强调从真实工作流中抽象出可重复使用的流程，而不是只保存零散提示词。当前已经支持从内容分析、策略确认、prompt 组装到最终 PNG 输出的一整套小红书图片流程。

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

### 2. floracat-rednote

用途：把原始内容转成适合小红书发布的多图图片流程，覆盖分析、策略确认、prompt 组装和最终 PNG 输出。

特点：
- 先做内容分析，再推荐策略、风格、布局和图片张数
- 支持 quick confirm、自定义调整、详细模式三段确认流程
- 输出 `analysis.md`、`outline.md`、`prompts/` 和最终 PNG 图片
- 系列图默认按首图参考链保持视觉一致性

位置：`skills/floracat-rednote`

### 3. floracat-image-gen

用途：根据 prompt 或 prompt 文件直接输出最终 PNG，作为小红书图文、封面图、插图等工作流的底层出图能力。

特点：
- 支持 OpenAI、Azure、Google、OpenRouter、DashScope、MiniMax、Jimeng、Seedream、Replicate
- 支持 `--ref` 参考图、长宽比、尺寸、质量和批量生成
- 通过 `scripts/main.ts` 直接执行，适合被其他 skill 调用
- 使用 `.floracat-skills/` 下的偏好配置和 `.env`

位置：`skills/floracat-image-gen`

## 评测方式

仓库内已经补了一套可复用的 skill 评测脚手架：

- 每个 skill 在自己的 `evals/evals.json` 中维护评测 case
- 仓库统一用 `scripts/run_skill_eval.py` 执行 baseline / with-skill 对比
- 结果输出到 `workspaces/<skill-name>/iteration-N/`
- 评测页自动生成到 `workspaces/<skill-name>/iteration-N/review.html`
- 评测 viewer 已内置到仓库，不依赖桌面其他目录

示例命令：

```bash
python3 scripts/run_skill_eval.py floracat-architecture-diagram
```

更完整说明见：`docs/evaluation.md`

## 后续演进方向

后续可以逐步增加：
- skill 总索引自动生成
- skill 元数据规范
- 统一校验脚本
- 发布到公开仓或 marketplace 的流程
- 截图、示例、样板输出

在那之前，这个仓库首先是一套服务于日常工作的个人 skill 资产库。
