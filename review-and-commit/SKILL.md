---
name: review-and-commit
description: 审查改动、自动修复缺陷及保持功能的简化建议，反复复核，通过后直接提交。用于“review and commit”“审查修复并提交”“review 到满意后提交”及恢复此流程；默认覆盖当前分支相对本地 main/master 的全部改动，也支持仅未提交改动。不用于只读 review 或跳过审查的快速提交。
---

# 审查、修复并提交

使用随 skill 安装的脚本完成 review/fix 循环，通过后调用 [quick-commit 的提交脚本](../quick-commit/scripts/commit_by_codex.sh)。当前 agent 负责选择范围、执行工具、跟进进度与呈现结果；审查脚本中的独立 Codex 会话负责审查和修复，共用提交脚本中的只读 Codex 会话负责生成提交消息。不要在当前 agent 重复整套审查，也不要把循环改成递归调用本 skill。

调用本 skill 表示授权修复审查发现的问题，并在通过后暂存、提交目标仓库全部 tracked 改动及非忽略的新文件，包括已有工作区改动；无需再问是否提交。遵守用户指定的范围及仓库指令。若用户只允许提交特定文件，现有工具不支持文件白名单，应先对齐处理方式，不能扩大提交范围。不自动 amend 或 push，不绕过 hooks 或签名。

## 选择范围与参数

- 默认使用 `--review-scope branch`：只查本地 main，缺失时查本地 master；固定 merge-base，审查分支提交及 staged、unstaged、相关 untracked 文件。需要新启动的 Codex 能使用 review-changes、其 simplify-changes 依赖及独立子代理。缺少基线、共同祖先、skill、依赖或委派能力时停止，不降级或提交。
- 用户明确说“只审查未提交改动”时用 `--review-scope changes`：保留内嵌的本地改动审查流程。
- 仓库从用户指定路径或当前工作目录确定，传递绝对 `--repo`。显式恢复日志能自行确定仓库，不要用当前目录覆盖日志中的目标。
- 默认最多 12 轮、默认 service tier。用户要求时传 `--max-loops N` 或 `--fast`。`--model MODEL` 只改变提交消息模型，默认使用共用提交工具的 `gpt-6-luna`。
- 分支模式中的 P0–P3 缺陷及可操作、保持功能的简化建议均阻止通过；改变功能或范围的建议只报告，不自动执行。

## 执行工具

将下面示例中的 `/path/to/review-and-commit` 替换为当前 SKILL.md 所在目录。使用 skill 内的脚本，不依赖 ez_tools checkout。依赖 Bash、Git、Python 3、Codex CLI、flock、setsid，以及目标仓库既有的 hooks/签名环境。

`quick-commit` 必须与本 skill 安装在同一父目录下。本 skill 保有审查入口和循环；`quick-commit/scripts/` 保有提交实现及审查/提交共用的工作区指纹函数。缺少该依赖时停止，不回退到另一套提交实现。

默认分支流程：

```bash
bash /path/to/review-and-commit/scripts/review_and_commit.sh --review-scope branch --repo /path/to/repository
```

仅未提交改动：

```bash
bash /path/to/review-and-commit/scripts/review_and_commit.sh --review-scope changes --repo /path/to/repository --max-loops 5
```

让工具持续运行，使用执行会话跟进并转述有意义的进展。耗时或工具暂时 yield 不表示失败，不要重启相同运行。沙箱限制仍需通过正常授权机制处理，不使用 sudo、Docker 或自动放宽权限作为替代。

工具只有在完整审查通过后才调用 `commit_by_codex.sh -y`。提交工具根据完整候选快照生成消息，检查仓库提交/隐私规则并验证内容一致性；消息生成被阻止、hooks、签名或一致性检查失败时报告失败，不绕过检查。没有待提交改动时报告“无改动可提交”。

## 停止与恢复

- 审查不通过达到轮数上限返回 1；审查未完成、输出无效、基线/恢复检查失败返回 2；Codex 超时返回 124。其他子步骤失败码原样返回。均不把失败当作通过，不自动提高轮数或反复重试。
- 日志在仓库外，分支与本地改动分别使用 `review_pr_untill_satisfied`、`review_changes_untill_satisfied` 状态目录。日志和 sidecars 是私有运行数据，不加入 Git，也不在答复中粘贴原始事件。
- 用户请求恢复时，按状态 sidecar 的 `review_mode` 选择 branch（pr）或 changes；旧版缺少模式的状态只支持 changes。可读取必要状态字段，避免加载整份日志。
- `--resume LOG` 追加原日志；不带 LOG 时在对应范围、仓库的日志目录查找最新未完成运行。恢复沿用已保存 service tier，不能同时传 `--fast`。
- 不自动添加 `--allow-worktree-changes`；只有用户明确允许预期漂移时才使用。已固定基线变化后必须启动新运行。
- 已通过的 review 日志不能恢复，因而提交阶段失败不能靠 `--resume` 重试提交。修复提交环境后重新执行本流程，以重新审查当前内容。

分支运行的恢复示例：

```bash
bash /path/to/review-and-commit/scripts/review_and_commit.sh --review-scope branch --resume /path/to/original-run.log
```

结束时报告审查范围、是否通过、主要修复与验证结果，以及是否创建提交；新提交给出短 hash 和 subject。失败时给出失败步骤、退出码及日志位置，不泄露原始日志中的私密内容。
