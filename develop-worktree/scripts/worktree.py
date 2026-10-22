"""Default Git worktree helpers. No project configuration or third-party modules."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


class CheckError(RuntimeError):
    pass


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False
    )
    if result.returncode:
        raise CheckError(
            os.fsdecode(result.stderr).strip() or "Git check failed: " + " ".join(args)
        )
    return result.stdout


def entries(root):
    result, entry = [], {}
    # Probe support instead of relying on version strings or translated errors.
    help_result = subprocess.run(
        ["git", "-C", str(root), "worktree", "list", "-h"],
        capture_output=True, check=False, env=dict(os.environ, LC_ALL="C"),
    )
    supports_null = b"-z" in help_result.stdout + help_result.stderr
    if supports_null:
        fields = git(root, "worktree", "list", "--porcelain", "-z").split(b"\0")
    else:
        # Old Git emits literal paths, including embedded newlines. Reject
        # ambiguous records rather than risk selecting the wrong worktree.
        fields = git(root, "worktree", "list", "--porcelain").split(b"\n")
    for field in fields:
        if not field:
            if entry:
                result.append(entry)
                entry = {}
        else:
            key, _, value = os.fsdecode(field).partition(" ")
            if not supports_null and (
                key not in {"worktree", "HEAD", "branch", "detached", "bare", "locked", "prunable"}
                or key in entry
                or (not entry and key != "worktree")
            ):
                raise CheckError("Ambiguous legacy worktree listing; use Git with list -z support")
            entry[key] = value
    if entry:
        result.append(entry)
    return result


def local_commit(root, branch):
    return git(
        root, "rev-parse", "--verify", "refs/heads/" + branch + "^{commit}"
    ).strip()


def validate(args):
    root = args.project_root.resolve(strict=True)
    if (
        Path(
            os.fsdecode(git(root, "rev-parse", "--show-toplevel")).rstrip("\n")
        ).resolve()
        != root
    ):
        raise CheckError("--project-root must be a worktree root")
    git(root, "check-ref-format", "refs/heads/" + args.branch)
    if args.branch == args.base_branch:
        raise CheckError("Task branch must differ from base")
    git(root, "check-ref-format", "refs/heads/" + args.base_branch)
    local_commit(root, args.base_branch)
    return root


def canonical_new_path(path):
    path = Path(os.path.abspath(path))
    if path.resolve() != path:
        raise CheckError("Refusing symlink-redirected worktree path: " + str(path))
    return path


def create(args, root):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_]*", args.branch):
        raise CheckError(
            "Default creation uses lowercase letters, digits and underscores"
        )
    path = canonical_new_path(
        args.worktree_path or root.parent / (root.name + ".worktrees") / args.branch
    )
    if path == root or root in path.parents:
        raise CheckError("Default helper requires a worktree outside the source tree")
    refs = git(
        root, "for-each-ref", "--format=%(refname)", "refs/heads/" + args.branch
    ).splitlines()
    if ("refs/heads/" + args.branch).encode() in refs or os.path.lexists(path):
        raise CheckError("Branch or worktree path already exists")
    if any(Path(e["worktree"]) == path for e in entries(root)):
        raise CheckError("Path already registered; inspect existing worktrees")
    git(
        root,
        "worktree",
        "add",
        "-b",
        args.branch,
        str(path),
        "refs/heads/" + args.base_branch,
    )
    print("Created worktree: " + str(path))


def target(root, args):
    matches = [
        e for e in entries(root) if e.get("branch") == "refs/heads/" + args.branch
    ]
    if len(matches) != 1:
        raise CheckError("Expected exactly one registered task worktree")
    entry = matches[0]
    task = Path(entry["worktree"])
    if (
        "locked" in entry
        or "prunable" in entry
        or not task.is_dir()
        or task.resolve() != task
    ):
        raise CheckError("Task worktree is locked, missing or redirected")
    # A main checkout must never be removed, even if currently on a task branch.
    git_dir = Path(
        os.fsdecode(git(task, "rev-parse", "--absolute-git-dir")).rstrip("\n")
    ).resolve()
    common_dir = Path(
        os.fsdecode(git(task, "rev-parse", "--git-common-dir")).rstrip("\n")
    )
    if not common_dir.is_absolute():
        common_dir = task / common_dir
    common_dir = common_dir.resolve()
    if task == root or task in root.parents or git_dir == common_dir:
        raise CheckError("Refusing to remove source or primary worktree")
    if (
        git(task, "symbolic-ref", "--quiet", "HEAD").strip()
        != ("refs/heads/" + args.branch).encode()
    ):
        raise CheckError("Task branch and registration disagree")
    tip = local_commit(root, args.branch)
    base = local_commit(root, args.base_branch)
    git(root, "merge-base", "--is-ancestor", tip.decode(), base.decode())
    return task, tip, base


def clean(task):
    # A force removal must never erase unreviewed ignored files inside a submodule.
    for record in git(task, "ls-files", "--stage", "-z").split(b"\0"):
        if record.startswith(b"160000 "):
            relative = os.fsdecode(record.split(b"\t", 1)[1])
            if os.path.lexists(task / relative / ".git"):
                raise CheckError(
                    "Initialized submodules require project-specific cleanup: "
                    + relative
                )
    # Real filters intentionally used: filter failures must not bypass checks.
    changes = git(
        task,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignore-submodules=none",
    )
    if changes:
        raise CheckError(
            "Uncommitted or untracked changes: " + repr(os.fsdecode(changes))
        )
    # Refuse active operations even if their working tree happens to be clean.
    for marker in (
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "rebase-merge",
        "rebase-apply",
        "sequencer",
    ):
        path = Path(
            os.fsdecode(git(task, "rev-parse", "--git-path", marker)).rstrip("\n")
        )
        if not path.is_absolute():
            path = task / path
        if path.exists():
            raise CheckError("Task has an in-progress Git operation: " + marker)


def ignored(task):
    return set(
        filter(
            None,
            git(
                task, "ls-files", "--others", "--ignored", "--exclude-standard", "-z"
            ).split(b"\0"),
        )
    )


def within(value, task):
    if value.endswith(" (deleted)"):
        value = value[:-10]
    path = Path(value)
    return path.is_absolute() and (path == task or task in path.parents)


def check_processes(task):
    if sys.platform != "linux" or not Path("/proc/self/cmdline").is_file():
        raise CheckError("Automatic cleanup requires Linux host /proc")
    if os.environ.get("WORKTREE_HOST_PROCESS_CHECK") != "1":
        raise CheckError(
            "Run on the host and set WORKTREE_HOST_PROCESS_CHECK=1 after confirming host visibility"
        )
    pattern = re.compile(re.escape(str(task)) + r"(?=$|[/\s\"\x27])")
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit() or int(proc.name) == os.getpid():
            continue
        try:
            if proc.stat().st_uid != os.getuid():
                continue
            args = [
                os.fsdecode(x)
                for x in (proc / "cmdline").read_bytes().split(b"\0")
                if x
            ]
            # Same-user kernel threads/zombies have no userspace cwd or open files.
            if not args:
                continue
            cwd = os.readlink(proc / "cwd")
            used = within(cwd, task) or any(pattern.search(a) for a in args)
            for arg in args:
                value = arg.split("=", 1)[-1]
                if value:
                    used |= within(os.path.abspath(os.path.join(cwd, value)), task)
            for fd in (proc / "fd").iterdir():
                try:
                    used |= within(os.readlink(fd), task)
                except FileNotFoundError:
                    continue
            for line in (proc / "maps").read_text().splitlines():
                fields = line.split(None, 5)
                if len(fields) == 6:
                    used |= within(fields[5], task)
            if used:
                raise CheckError("Process still using task worktree: PID " + proc.name)
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError as exc:
            raise CheckError(
                "Cannot fully inspect same-user PID " + proc.name + "; cleanup stopped"
            ) from exc


def inspect(root, args):
    state = target(root, args)
    task = state[0]
    clean(task)
    artifacts = ignored(task)
    if artifacts:
        print("Ignored files (archive or explicitly approve discarding):", flush=True)
        for path in sorted(artifacts):
            print("  " + repr(os.fsdecode(path)), flush=True)
        if not args.artifacts_reviewed:
            raise CheckError("Review ignored files before --artifacts-reviewed")
    check_processes(task)
    return state, artifacts


def remove(args, root):
    state, artifacts = inspect(root, args)
    if args.check:
        print("Checks passed; nothing removed.")
        return
    # Caller must stop concurrent editing; these rechecks narrow, not eliminate, races.
    latest, latest_artifacts = inspect(root, args)
    if latest != state or latest_artifacts != artifacts:
        raise CheckError("Worktree changed during checks; inspect again")
    task, tip, _ = state
    command = ["worktree", "remove"]
    if artifacts:
        command.append("--force")
    git(root, *command, str(task))
    # CAS protects a task ref that moved after the ancestor check.
    git(root, "update-ref", "-d", "refs/heads/" + args.branch, tip.decode())
    if os.path.lexists(task) or any(
        e.get("worktree") == str(task) for e in entries(root)
    ):
        raise CheckError("Worktree cleanup incomplete; inspect remaining state")
    if (
        git(root, "for-each-ref", "--format=%(refname)", "refs/heads/" + args.branch)
        .splitlines()
        .count(("refs/heads/" + args.branch).encode())
    ):
        raise CheckError("Task branch remains; inspect concurrent changes")
    print("Removed worktree and branch: " + args.branch)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("add", "remove"))
    parser.add_argument("branch")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--base-branch", required=True)
    parser.add_argument("--worktree-path", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--artifacts-reviewed", action="store_true")
    args = parser.parse_args()
    if args.operation == "add" and (args.check or args.artifacts_reviewed):
        parser.error("Removal flags are not supported for add")
    if args.operation == "remove" and args.worktree_path:
        parser.error("Removal resolves its path from Git registration")
    try:
        root = validate(args)
        (create if args.operation == "add" else remove)(args, root)
        return 0
    except (CheckError, OSError) as exc:
        print("Error: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
