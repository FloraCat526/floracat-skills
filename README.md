# FloraCat Skills

用于技术内容创作的 skills，支持架构图和微信公众号封面生成。

## Skills

| Skill | 用途 |
|---|---|
| [floracat-architecture-diagram](skills/floracat-architecture-diagram/SKILL.md) | 生成或修改中文架构图、流程图和时序图，输出可直接打开的 HTML/SVG。 |
| [floracat-wechat-cover](skills/floracat-wechat-cover/SKILL.md) | 使用小沅 IP，根据文章、标题或架构图生成公众号双封面。 |

## 公众号封面

| 模式 | 输入 | 表达方式 |
|---|---|---|
| 场景化 | 文章 | 让小沅在具体场景中操作、展示或讲解文章主题。 |
| 标题化 | 标题 | 大标题搭配小沅和少量主题元素。 |
| 架构图式 | 架构图 | 核心节点与连接关系搭配小沅讲解。 |

三种模式均支持 **蓝紫色** 和 **浅黄色**，内置小沅 IP 与风格参考素材。

默认交付 **左侧横版大封面 + 右侧方形缩略图** 的组合 PNG，同时保留两张独立封面。缩略图单独排版。

**布局参考：**

![左侧横版大封面与右侧方形缩略图的布局参考](skills/floracat-wechat-cover/assets/references/layout-double-cover.png)

## 使用

将所需的整个 skill 文件夹复制到对应目录，保留随包素材：

- Codex：`~/.codex/skills/`
- Claude Code：`~/.claude/skills/`

Codex 调用示例：

```text
$floracat-wechat-cover 根据这篇文章生成蓝紫色场景化公众号封面。
$floracat-architecture-diagram 把这套系统画成中文架构图。
```

公众号封面需要支持参考图的图片生成或编辑能力；图片拼接需要 Python 3 和 Pillow。完整流程见各 skill 的 `SKILL.md`。
