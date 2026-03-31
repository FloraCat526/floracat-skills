# floracat-skills

FloraCat 的个人 skills 仓库，用于持续沉淀、整理和复用高价值的 Codex / Claude 类技能。

这个仓库优先服务于真实工作流中的长期积累：先把 skill 资产结构化沉淀下来，再逐步补充模板、脚本、参考资料和维护规范。

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

## 评测方式

仓库内已经补了一套可复用的 skill 评测脚手架：

- 每个 skill 在自己的 `evals/evals.json` 中维护评测 case
- 仓库统一用 `scripts/run_skill_eval.py` 执行 baseline / with-skill 对比
- 结果输出到 `workspaces/<skill-name>/iteration-N/`
- 评测页自动生成到 `review.html`
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
