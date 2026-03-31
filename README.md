# floracat-skills

用于持续沉淀、整理和复用的个人技能库。

这个仓库优先服务于日常工作中的长期积累，而不是一开始就做成重型发布仓库。
它参考了 `baoyu-skills` 的优点，但刻意保持更轻、更适合个人演进。

## 设计原则

- `skills/` 只放已经可复用的正式 skill
- `drafts/` 放还在整理中的 skill 草稿
- `shared/` 放跨多个 skill 复用的通用资料
- `docs/` 放仓库规范、命名规则、编写与维护说明
- `scripts/` 放后续可能补充的校验、同步、索引脚本
- 先沉淀，再工程化；先可用，再发布

## 目录结构

- `skills/`: 正式 skill
- `drafts/`: 草稿 skill
- `shared/references/`: 跨 skill 共用参考资料
- `shared/templates/`: 跨 skill 共用模板
- `shared/assets/`: 跨 skill 共用素材
- `shared/prompts/`: 可复用 prompt 片段
- `docs/`: 仓库说明与约定
- `scripts/`: 仓库辅助脚本
- `archive/`: 已废弃或历史版本

## 当前 skills

### floracat-architecture-diagram

用途：生成和修改适合演示、公众号、技术分享场景的 HTML/SVG 架构图、流程图、时序图。

特点：
- 输出为 standalone HTML + inline SVG
- 风格偏 PPT 化、人工编辑感强
- 强调箭头精准、排版清晰、中文可读性
- 适合对既有 SVG 图进行持续微调

位置：`skills/floracat-architecture-diagram`

## 为什么不直接照搬 baoyu-skills

`baoyu-skills` 很适合作为公开发布和市场化分发的技能仓库，但对个人私有积累来说有几点偏重：

- 发布相关目录和脚本较多，维护成本高
- screenshots 与 package 体系适合产品化，不适合早期沉淀
- 仓库一开始就过重，不利于快速新增 skill

所以 `floracat-skills` 采用“轻仓 + 可扩展”的方式：
先把 skill 资产结构化沉淀好，等以后确实需要对外发布，再补 marketplace、release、screenshots、packages 这类能力。
