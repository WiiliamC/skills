# Worktree 脚本选择与默认接口

## 项目实现优先

创建和删除独立选择：先读取项目指令指定入口，其次检查项目 `scripts/add_worktree.sh`、`scripts/remove_worktree.sh`，仅对应操作缺失时使用本 skill 的默认脚本。不能执行名称相近但未经检查的文件；项目脚本接口不必与默认接口一致，先读帮助或代码，确认基线、目标路径、环境初始化和检查能力。脚本若调用 sudo 或 Docker，遵循环境规则交由用户执行。

显式传递项目要求的根目录变量；不要继承未知 `PROJECT_ROOT`。项目实现报错、缺依赖或检查拒绝都不属于“缺失”。删除入口不匹配创建路径时先协调实际参数或说明阻塞，不能猜路径或强制删除。默认删除通过 Git 注册定位，因此可删除项目脚本创建的已注册 worktree，但仍遵循全部检查。

## 默认接口

依赖 Bash、Git、Python 3（标准库，Python 3.8+）。脚本不加载项目 `env.sh`。自动检测 `git worktree list -z` 支持；旧版 Git 使用等价的 `git worktree list --porcelain`，保留注册、锁定及清理检查。旧版输出遇到换行路径等无法可靠解析的记录时停止并提示升级 Git，不猜测路径。可设置 `WORKTREE_PYTHON` 选择 Python 可执行文件，否则使用 `python3`。

从 skill 所在目录解析下面的脚本绝对路径；示例中的 `/path/to/skill` 和仓库路径需替换为实际路径。

```bash
bash /path/to/skill/scripts/add_worktree.sh feat_search --project-root /path/to/repo --base-branch main
bash /path/to/skill/scripts/add_worktree.sh feat_search --project-root /path/to/repo --base-branch main --worktree-path /path/to/task
```

根目录必须是 Git worktree 根目录，基线必须为现有本地分支，默认创建的任务分支仅允许小写字母、数字和下划线；删除接受项目脚本创建的合法 Git 分支名（包括 `/`），均不能等于基线。默认目标为仓库旁 `<仓库名>.worktrees/<branch>`。拒绝已有分支、已有目录、链接重定向路径和注册冲突；不覆盖，不自动回滚失败后的现场。

删除只支持 Linux。必须先确认命令运行在宿主环境，再显式设置 `WORKTREE_HOST_PROCESS_CHECK=1`；该变量是调用者的环境确认，不是脚本自行验证已逃离容器或沙箱。沙箱内不得设置它作为绕过检查的手段。

```bash
env WORKTREE_HOST_PROCESS_CHECK=1 bash /path/to/skill/scripts/remove_worktree.sh feat_search --project-root /path/to/repo --base-branch main --check
env WORKTREE_HOST_PROCESS_CHECK=1 bash /path/to/skill/scripts/remove_worktree.sh feat_search --project-root /path/to/repo --base-branch main --artifacts-reviewed
```

`--check` 不删除内容；有未处理 ignored 文件时列出文件并非零退出。`--artifacts-reviewed` 表示调用者已保存或批准丢弃当前列出的 ignored 文件，不批准未提交代码或其他检查失败。默认脚本不省略缓存，也不特判模型资源。

含已初始化子模块的任务 worktree 拒绝默认自动清理，需使用能检查子模块产物的项目流程；不以 `--artifacts-reviewed` 绕过。检查使用真实 Git filters，LFS 错误时修复权限或环境，不禁用过滤器来证明可删除。任何不可靠的同用户进程信息都阻止删除；不自动终止进程。检查当前工作目录、命令行路径及打开的文件/映射，不能代替主代理停止并发工作。删除前复查目标和分支 commit；遇到新的 ignored 文件要求重新检查。只在检查通过且 ignored 内容已审阅时使用 Git 的 force 移除文件树；任务分支以预期 commit 为条件删除，不能删除并发更新后的分支。

## 验证默认实现

运行 `python3 /path/to/skill/tests/test_worktree.py`。测试在临时 Git 仓库验证生命周期、拒绝路径、子模块保护和并发引用保护；进程检查使用受控 `/proc` 样本，生命周期测试替换宿主扫描。因此测试通过不代表当前宿主具备读取全部同用户进程的权限；真实清理仍须通过宿主检查。
