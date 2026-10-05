# Codex Skills

## 提交技能

- `quick-commit`：直接提交当前仓库全部 tracked 改动和未被忽略的新文件，不另行审查或运行测试。
- `review-and-commit`：审查并修复问题，通过后调用 `quick-commit` 的共用提交脚本，并校验审查快照。

两个 skill 必须安装在同一父目录下。提交实现和共用工作区指纹函数位于 `quick-commit/scripts/`；提交消息默认使用 `gpt-6-luna`，Git hooks 和签名正常执行。

## 本机配置：执行提交脚本时免重复询问

Codex 的命令允许规则可以让指定脚本在沙箱外运行而不重复弹出权限询问。脚本的 `-y` 仅跳过脚本自身的提交确认，不能代替 Codex 权限配置。

在 `~/.codex/rules/commit-skills.rules` 中添加以下规则。将示例中的 `/path/to/skills` 替换为本机技能安装目录的实际绝对路径：

```python
prefix_rule(
    pattern = ["bash", "/path/to/skills/quick-commit/scripts/commit_by_codex.sh"],
    decision = "allow",
)

prefix_rule(
    pattern = ["bash", "/path/to/skills/review-and-commit/scripts/review_and_commit.sh"],
    decision = "allow",
)
```

这些前缀允许后续附加任意脚本参数，包括目标仓库 `--repo`。第一条授权提交脚本；第二条授权完整的审查、修复和提交流程。规则按脚本路径匹配，修改该路径下的脚本后仍然适用。

调用时保持 `bash` 加绝对脚本路径的形式，例如：

```bash
bash /path/to/skills/quick-commit/scripts/commit_by_codex.sh --repo /path/to/repository -y
bash /path/to/skills/review-and-commit/scripts/review_and_commit.sh --review-scope branch --repo /path/to/repository
```

可使用以下命令检查规则是否匹配；检查不会实际执行提交：

```bash
codex execpolicy check --pretty --rules ~/.codex/rules/commit-skills.rules -- bash /path/to/skills/quick-commit/scripts/commit_by_codex.sh --repo /path/to/repository -y
codex execpolicy check --pretty --rules ~/.codex/rules/commit-skills.rules -- bash /path/to/skills/review-and-commit/scripts/review_and_commit.sh --review-scope branch --repo /path/to/repository
```

预期结果为 `decision: allow`。保存后重启 Codex，以加载新规则。其他匹配规则或管理员策略如果要求询问或禁止执行，仍以更严格的决定为准。这两条规则不授权单独执行 `git push`。

也可以在权限弹窗支持的情况下保存对应命令前缀。不要将允许范围扩大为所有 `bash` 命令。

参考：[OpenAI 官方 Rules 文档](https://learn.chatgpt.com/docs/agent-configuration/rules)。
