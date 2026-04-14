# Skills Index

用于登记 `floracat-skills` 中已经定型的正式 skill。

## Status 说明

- `active`: 正在使用、可继续复用
- `draft`: 仍在打磨，尚未正式纳入 `skills/`
- `archived`: 历史版本或暂停维护

## 正式 skills

| Name | Status | Purpose | Path |
|------|--------|---------|------|
| `floracat-architecture-diagram` | `active` | 生成和修改适合演示、公众号、技术分享场景的 HTML/SVG 架构图、流程图、时序图 | `skills/floracat-architecture-diagram` |
| `floracat-rednote` | `active` | 把原始内容转成适合小红书发布的多图图片流程，完成分析、策略确认、prompt 组装和逐张 PNG 输出 | `skills/floracat-rednote` |
| `floracat-image-gen` | `active` | 根据 prompt 或 prompt 文件直接输出 PNG，支持 provider、模型、参考图、尺寸比例和批量任务 | `skills/floracat-image-gen` |

## 登记规则

新增正式 skill 时，至少补充以下信息：

- `Name`: 与 `SKILL.md` frontmatter 中的 `name` 一致
- `Status`: `active` / `draft` / `archived`
- `Purpose`: 用一句话说明主要用途
- `Path`: skill 目录相对路径

## 推荐维护方式

- 草稿阶段先放到 `drafts/`
- 当 skill 结构稳定、可重复使用后，再迁入 `skills/`
- 迁入 `skills/` 后，同步在本文件登记
- 如 skill 废弃或被新版本替代，移入 `archive/` 并更新状态
