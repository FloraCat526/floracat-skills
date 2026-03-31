# floracat-skills 仓库结构

## 推荐路径

- 正式 skill: `skills/<skill-name>/`
- 草稿 skill: `drafts/<skill-name>/`
- 共用参考资料: `shared/references/`
- 共用模板: `shared/templates/`
- 共用素材: `shared/assets/`
- 共用 prompt 片段: `shared/prompts/`

## skill 目录最低要求

每个正式 skill 至少包含：

- `SKILL.md`

按需增加：

- `references/`
- `scripts/`
- `assets/`
- `prompts/`
- `evals/`
- `agents/openai.yaml`

## 评测相关路径

- skill 级 case 配置：`skills/<skill-name>/evals/evals.json`
- 仓库级执行脚本：`scripts/run_skill_eval.py`
- 运行结果输出：`workspaces/<skill-name>/iteration-N/`

## 命名建议

- skill 名称使用小写英文和中划线
- 目录名与 skill frontmatter `name` 保持一致
- 优先使用动作 + 对象的命名方式，例如：
  - `floracat-architecture-diagram`
  - `wechat-article-polish`
  - `podcast-transcript-cleanup`
