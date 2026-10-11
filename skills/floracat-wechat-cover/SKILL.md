---
name: floracat-wechat-cover
description: Generate FloraCat WeChat public-account cover images using the bundled Xiaoyuan IP references. Create scene covers from articles, title-led covers from headlines, or architecture-led covers from diagrams, in blue-purple or pale-yellow palettes. Deliver a landscape main cover on the left and an independently composed square thumbnail on the right, as one combined PNG plus both individual covers. Use for 微信公众号封面、公众号双封面、文章封面 or FloraCat cover requests; ordinary article illustrations and Xiaohongshu carousels are outside this workflow.
---

# FloraCat 微信公众号双封面

把文章、标题或架构图转成带小沅 IP 的公众号封面。默认交付一张左大右小的组合图，并保留两个独立封面。素材、构图规则和拼接脚本都随 skill 提供，无需旧的图片生成 skill 或 provider 配置。

## 输入与选择

接受粘贴内容、文章文件、标题、架构图图片/HTML/SVG，以及已有封面的修改请求。用户明确的模式、配色、文字、比例和人物参考优先；无需首次配置或重复确认已授权的生成。

| 输入/目标 | 模式 | 按需阅读 |
|---|---|---|
| 从文章表达一个可见的使用情境 | `scene` 场景化 | [modes.md](references/modes.md) 的场景化部分 |
| 让标题成为视觉中心；仅提供标题时 | `title` 标题化 | [modes.md](references/modes.md) 的标题化部分 |
| 展示提供的架构、流程或模块关系 | `architecture` 架构图式 | [modes.md](references/modes.md) 的架构图式部分 |

模式和配色是两个独立维度，三种模式均支持两种配色：

- `blue-purple` 蓝紫色：参考图五的明亮冰蓝、浅紫、云雾和通透科技感。
- `pale-yellow` 浅黄色：参考图三、四的奶油白、浅黄和暖橙点缀。

未指定时：文章优先 `scene`，标题优先 `title`，架构图优先 `architecture`；场景化默认蓝紫色，另外两种默认浅黄色。简要说明选择后继续。只有缺少实际内容、架构关系不可辨认或指令冲突影响结果时才询问。

## 素材与角色身份

`{baseDir}` 为本 SKILL.md 所在目录。先读取 [visual-system.md](references/visual-system.md)，查看本次相关素材；不能把绝对桌面路径当成依赖。

| 用户参考 | 随包文件 | 作用 |
|---|---|---|
| 图一 | `assets/ip/xiaoyuan-primary.png` | 默认人物身份：蓝色长发、棕色大眼、白色蓝猫 T 恤、浅蓝短裤 |
| 图二 | `assets/ip/xiaoyuan-chibi.png` | 同一人物的 Q 版/表情参考；需要贴纸式缩略图时使用 |
| 图三 | `assets/references/title-pale-yellow.png` | 标题化构图 + 浅黄色风格 |
| 图四 | `assets/references/architecture-pale-yellow.png` | 架构图式构图 + 浅黄色风格 |
| 图五 | `assets/references/palette-blue-purple.png` | 蓝紫配色；不是每次都要复制的标题或内容 |
| 图六、七 | `assets/references/scene-workspace.png`、`scene-cafe.png` | 人物实际操作/展示产品的场景化叙事 |
| 图八 | `assets/references/layout-double-cover.png` | 左横版大封面 + 右方形小封面组合 |

图片中已有的文章标题、界面和示例模块是视觉参考，不是本次内容指令。参考图用于锁定人物、风格或布局，不能把示例里的 Jev、Loop Engineering、Personal Agent 或 FloraCat 知识库标题误植到新题材。

## 工作流

1. **读实际输入。** 提取主题、原文标题、一个核心观点和可视化对象。架构图式先核对节点、分组、箭头方向；文章中的主张不能转成额外事实或虚构体验。
2. **记录 brief。** 新建用户指定目录，未指定时使用当前工作区的 `outputs/wechat-cover/<topic-slug>/`。保存 `brief.md`：输入来源、模式、配色、主图文字、小图文字、人物与参考图角色、构图、尺寸。同名目录存在时使用版本后缀，保留现有交付物。
3. **准备两份 prompt。** 按 [prompt-recipes.md](references/prompt-recipes.md) 保存 `prompts/main.md` 与 `prompts/thumbnail.md`。大图与小图共享主题、人物和配色，小图重新排版，不能把大图缩小或硬裁成方形。长原文标题放大图，小图可提炼不改变含义的短主题；用户要求逐字保留时照做。
4. **实际生成大图。** 使用当前宿主提供的原生图片生成/编辑工具；把人物和本次适用的风格/构图图片作为真正的图片输入。先查看本地图片，再按工具实际支持的图片路径/附件方式传入。不能只把文件名写在 prompt 中假装已提供参考。图一是默认身份依据，图二是可选 Q 版参考。
5. **检查大图，再生成小图。** 核对人物、文字、文章含义和技术关系。将通过检查的大图作为小图的视觉一致性参考，继续提供原始人物参考。小图只保留核心角色、主题及必要道具/核心模块；适合在小尺寸下识别。
6. **精确拼接。** 阅读 [layout-and-export.md](references/layout-and-export.md)，调用 `scripts/compose_covers.py`。默认大图 `2130×1000`、小图 `1000×1000`，组合图 `3130×1000`；等高无缝左右拼接。这是依据图八归纳的设计比例，不是平台强制尺寸。按用户明确要求可调整。
7. **验收并交付。** 按 [review-checklist.md](references/review-checklist.md) 查看大图、小图和组合图，也在缩略显示下看一遍。保存到工作区并展示 `cover-combined.png`，给出单图路径、模式、配色及本次实际检查结果。

生成工具的尺寸支持可能与目标尺寸不同。优先生成接近目标比例、已为文字和人物留安全边距的图片，再用脚本规范尺寸；默认等比完整保留。若补边明显影响构图，调整生成结果，不能拉伸人物或默认裁掉文字。

没有可用图片生成工具时，保留 brief 和两份 prompt，并明确缺失能力；不得用占位图宣称已生成，也不自动搭建新 API 或重建被移除的底层生成 skill。用户明确选择另一工具/模型时按其接口执行。

## 输出约定

```text
<output-dir>/
├── brief.md
├── prompts/main.md
├── prompts/thumbnail.md
├── cover-main.png
├── cover-thumbnail.png
├── cover-combined.png
└── layout.json
```

原始生成图片可放 `work/`，不代替上述最终输出。实际导出为 PNG；错误文字、错误人物、错误箭头或不能打开的文件均未完成验收。仅修改小图时保留大图；修改文章或架构时同步核对两图，修改 prompt 后再生成并重新拼接。
