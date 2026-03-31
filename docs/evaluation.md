# Skill Evaluation

`floracat-skills` 使用统一的仓库级评测脚本，配合每个 skill 自己的 `evals/evals.json`。
评测页生成器也已经内置在仓库内，默认不依赖桌面上的其他项目。

这样做的目的有两个：

- 后续新增 skill 时只补评测 case，不重写执行脚本
- 每次评测都产出统一目录结构，方便直接用 `skill-creator` 的 viewer 打开

## 目录约定

- 每个 skill 的评测配置：`skills/<skill-name>/evals/evals.json`
- 评测输出目录：`workspaces/<skill-name>/iteration-N/`
- 静态评测页：`workspaces/<skill-name>/iteration-N/review.html`
- 内置 viewer：`tools/skill-eval-viewer/`

## evals.json 最小结构

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "slug": "simple-case",
      "prompt": "用户任务",
      "expected_output": "理想结果说明",
      "files": [],
      "output_files": ["result.html"],
      "expectations": ["关键检查点"]
    }
  ]
}
```

字段说明：

- `skill_name`: 必须与 `SKILL.md` frontmatter 里的 `name` 一致
- `id`: 数字编号
- `slug`: 用于生成更可读的目录名
- `prompt`: 真实评测 prompt
- `expected_output`: 对理想结果的简述，会拼进执行 prompt
- `files`: 输入文件，相对 skill 根目录
- `output_files`: 期望生成的交付物文件名
- `expectations`: 先保留为定性检查点，后续可以继续扩展到 grading

## 一键运行

在仓库根目录执行：

```bash
python3 scripts/run_skill_eval.py floracat-architecture-diagram
```

常用参数：

```bash
python3 scripts/run_skill_eval.py floracat-architecture-diagram --cases 1
python3 scripts/run_skill_eval.py floracat-architecture-diagram --review-only
python3 scripts/run_skill_eval.py floracat-architecture-diagram --iteration 2 --review-only
```

## 脚本做了什么

脚本会自动：

- 在仓库 `.claude/skills/` 下挂载目标 skill
- 读取该 skill 的 `evals/evals.json`
- 为每个 case 跑两次：`with_skill` 和 `baseline`
- 把结果写到统一 workspace 目录
- 调用仓库内置 viewer 生成 `review.html`

## 当前边界

这套脚手架先解决“快速重复跑定性评测 + 直接看结果”。

暂时还没有自动补全：

- assertion programmatic grading
- benchmark 聚合
- 多轮平均值与方差分析

后续如果需要，再在这个框架上继续补。
