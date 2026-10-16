# Codex Skills

## 文档改进

- [`improve-docs`](improve-docs/SKILL.md)：仅显式调用，通常用于开发收尾。根据当前对话和实际改动检查项目文档、各级 `AGENTS.md`、相关 skill，以及需要落盘的新契约或约定；先展示具体建议，用户批准后再更新或新增文档，无必要更新时直接说明。调用示例：`使用 $improve-docs 检查本次开发需要更新或补充的文档和约定。`

## 提交技能

- `quick-commit`：默认提交本次任务的改动，按用户提示和对话确定文件及代码块范围；当前 agent 阅读完整候选 diff、复用提交消息提示词并直接执行 Git 提交，不另行审查或运行测试。
- `review-and-commit`：主 agent 编排独立 review / fix 子代理，复核缺陷和保持功能的简化建议，循环收敛后调用 quick-commit skill。默认有未提交改动时审查 changes，否则审查 branch；可用自然语言明确指定仓库、范围和基线。

quick-commit 优先提交本次任务的改动，保留可识别的任务外改动，包括已暂存内容；无法确认本次任务范围时，无需再次确认，提交目标仓库全部 tracked 改动及非忽略新文件。也支持明确指定文件、功能、仅已暂存内容或全部改动；明确范围优先，不受兜底规则影响。review-and-commit 按其已确定并审查通过的提交范围调用 quick-commit。遵守目标仓库规范，正常执行 Git hooks 和签名，不自动 amend 或 push。提交失败时核对实际 Git 状态，不盲目重试。

## 实现与权限

review-and-commit 需要可用的独立子代理，以及可读取的 review-changes、simplify-changes 和 quick-commit。审查标准复用已有参考资料，主 agent 复核建议后才交给修复代理。quick-commit 由当前 agent 完成，不依赖提交消息模型或额外 Codex CLI 会话。

旧的审查循环、提交脚本、自定义工作区指纹、CLI 参数和日志恢复入口已删除。无需为这些脚本新增免审批规则；已有按旧脚本路径匹配的规则不再用于新流程，可由使用者自行清理。不将旧脚本权限扩大为所有 Bash 或 Git 命令，实际 Git 写入按当前环境权限机制执行。

审查与提交之间检查实际内容变化；会修改文件的 hook 应在进入审查前完成，后续内容变化需重新核实相关审查结论。相同的 git status 不代表内容未变。
