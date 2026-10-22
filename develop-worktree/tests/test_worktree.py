import argparse
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/worktree.py"
spec = importlib.util.spec_from_file_location("worktree", SCRIPT)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="worktree-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces"
        self.root.mkdir()
        self.git("init", "-b", "develop")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        (self.root / ".gitignore").write_text("output/\n")
        (self.root / "file").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-m", "initial")
        self.args = argparse.Namespace(
            branch="feat_test",
            project_root=self.root,
            base_branch="develop",
            worktree_path=None,
            check=False,
            artifacts_reviewed=False,
        )
        self.task = self.root.parent / (self.root.name + ".worktrees") / "feat_test"
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def git(self, *args):
        return w.git(self.root, *args)

    def create(self):
        w.create(self.args, w.validate(self.args))

    def remove(self):
        with patch.object(w, "check_processes"):
            w.remove(self.args, w.validate(self.args))

    def assert_present(self):
        self.assertTrue(self.task.is_dir())
        self.assertEqual(
            len(
                [
                    e
                    for e in w.entries(self.root)
                    if e.get("branch") == "refs/heads/feat_test"
                ]
            ),
            1,
        )

    def test_non_main_full_lifecycle(self):
        self.create()
        self.assertEqual(
            w.local_commit(self.root, "develop"), w.local_commit(self.root, "feat_test")
        )
        self.args.check = True
        self.remove()
        self.assert_present()
        self.args.check = False
        self.remove()
        self.assertFalse(self.task.exists())
        self.assertNotIn(
            b"refs/heads/feat_test", self.git("for-each-ref", "--format=%(refname)")
        )

    def test_explicit_base_not_current_head(self):
        self.git("checkout", "-b", "other")
        (self.root / "file").write_text("different")
        self.git("commit", "-am", "other")
        self.create()
        self.assertEqual((self.task / "file").read_text(), "base\n")

    def test_unmerged_refusal_preserves_files(self):
        self.create()
        (self.task / "file").write_text("new")
        w.git(self.task, "commit", "-am", "new")
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assertEqual((self.task / "file").read_text(), "new")
        self.git("merge", "--no-ff", "feat_test", "-m", "merge")
        self.remove()

    def test_dirty_and_untracked_refusal(self):
        self.create()
        (self.task / "file").write_text("dirty")
        self.args.artifacts_reviewed = True
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assertEqual((self.task / "file").read_text(), "dirty")
        w.git(self.task, "checkout", "--", "file")
        (self.task / "new").write_text("keep")
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assertEqual((self.task / "new").read_text(), "keep")

    def test_ignored_requires_review(self):
        self.create()
        (self.task / "output").mkdir()
        (self.task / "output/data").write_text("result")
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assertEqual((self.task / "output/data").read_text(), "result")
        self.args.artifacts_reviewed = True
        self.remove()
        self.assertFalse(self.task.exists())

    def test_lock_refusal(self):
        self.create()
        self.git("worktree", "lock", str(self.task))
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assert_present()

    def test_duplicate_branch_and_path_refusal(self):
        self.create()
        with self.assertRaises(w.CheckError):
            self.create()
        self.args.branch = "feat_other"
        self.args.worktree_path = self.task
        with self.assertRaises(w.CheckError):
            self.create()
        self.assert_present()

    def test_existing_and_symlink_path_refusal(self):
        self.args.worktree_path = self.root.parent / "existing"
        self.args.worktree_path.mkdir()
        (self.args.worktree_path / "keep").write_text("keep")
        with self.assertRaises(w.CheckError):
            self.create()
        link = self.root.parent / "redirect"
        link.symlink_to(self.args.worktree_path, target_is_directory=True)
        self.args.worktree_path = link / "task"
        with self.assertRaises(w.CheckError):
            self.create()
        self.assertFalse((link / "task").exists())

    def test_invalid_branch_and_root(self):
        self.args.branch = "../escape"
        with self.assertRaises(w.CheckError):
            w.validate(self.args)
        self.args.branch = "develop"
        with self.assertRaises(w.CheckError):
            w.validate(self.args)
        self.args.branch = "feat_test"
        self.args.project_root = self.root / "nested"
        self.args.project_root.mkdir()
        with self.assertRaises(w.CheckError):
            w.validate(self.args)

    def test_missing_base(self):
        self.args.base_branch = "missing"
        with self.assertRaises(w.CheckError):
            self.create()
        self.assertFalse(self.task.exists())

    def test_source_worktree_refusal(self):
        self.create()
        self.args.project_root = self.task
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assert_present()

    def test_primary_worktree_refusal(self):
        self.git("checkout", "-b", "feat_test")
        with self.assertRaises(w.CheckError):
            w.target(self.root, self.args)
        self.assertTrue((self.root / "file").exists())

    def test_changed_state_between_checks(self):
        self.create()
        real_inspect = w.inspect
        count = 0

        def mutate(root, args):
            nonlocal count
            count += 1
            if count == 2:
                (self.task / "output").mkdir()
                (self.task / "output/new").write_text("new artifact")
            return real_inspect(root, args)

        self.args.artifacts_reviewed = True
        with patch.object(w, "inspect", side_effect=mutate), self.assertRaises(
            w.CheckError
        ):
            self.remove()
        self.assert_present()

    def test_registration_resolves_custom_path(self):
        self.args.worktree_path = self.root.parent / "custom worktree"
        self.create()
        self.task = self.args.worktree_path
        self.args.worktree_path = None
        self.remove()
        self.assertFalse(self.task.exists())

    def test_wrapper(self):
        result = subprocess.run(
            [
                "bash",
                str(SCRIPT.parent / "add_worktree.sh"),
                "feat_test",
                "--project-root",
                str(self.root),
                "--base-branch",
                "develop",
            ],
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_present()

    def test_no_host_attestation_refusal(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(w.CheckError):
            w.check_processes(self.task)

    def test_non_linux_refusal(self):
        with patch.object(w.sys, "platform", "darwin"), self.assertRaises(w.CheckError):
            w.check_processes(self.task)

    def test_in_progress_operation(self):
        self.create()
        marker = Path(
            os.fsdecode(
                w.git(self.task, "rev-parse", "--git-path", "MERGE_HEAD")
            ).strip()
        )
        marker.write_bytes(w.local_commit(self.root, "develop") + b"\n")
        with self.assertRaises(w.CheckError):
            self.remove()
        self.assert_present()

    def test_process_blocks_removal_even_reviewed(self):
        self.create()
        self.args.artifacts_reviewed = True
        with patch.object(
            w, "check_processes", side_effect=w.CheckError("busy")
        ), self.assertRaises(w.CheckError):
            w.remove(self.args, self.root)
        self.assert_present()

    def test_project_created_slash_branch(self):
        self.args.branch = "feature/search"
        self.git("worktree", "add", "-b", self.args.branch, str(self.task), "develop")
        self.remove()
        self.assertFalse(self.task.exists())

    def test_initialized_submodule_refusal(self):
        sub = self.root.parent / "sub"
        sub.mkdir()
        w.git(sub, "init")
        w.git(sub, "config", "user.name", "Test")
        w.git(sub, "config", "user.email", "test@example.invalid")
        (sub / ".gitignore").write_text("results/\n")
        w.git(sub, "add", ".")
        w.git(sub, "-c", "commit.gpgsign=false", "commit", "-m", "initial")
        self.git(
            "-c", "protocol.file.allow=always", "submodule", "add", str(sub), "module"
        )
        self.git("commit", "-am", "add submodule")
        self.create()
        w.git(
            self.task,
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "update",
            "--init",
        )
        w.git(self.task, "config", "submodule.module.ignore", "all")
        (self.task / "module/results").mkdir()
        (self.task / "module/results/valuable").write_text("preserve")
        (self.task / "output").mkdir()
        (self.task / "output/log").write_text("reviewed")
        self.args.artifacts_reviewed = True
        with self.assertRaisesRegex(w.CheckError, "Initialized submodules"):
            self.remove()
        self.assertEqual(
            (self.task / "module/results/valuable").read_text(), "preserve"
        )

    def fake_proc(self):
        proc = self.root.parent / "proc"
        (proc / "self").mkdir(parents=True)
        (proc / "self/cmdline").write_bytes(b"test")
        process = proc / "987654321"
        process.mkdir()
        (process / "cmdline").write_bytes(b"worker\0")
        (process / "cwd").symlink_to(self.root, target_is_directory=True)
        (process / "fd").mkdir()
        (process / "maps").write_text("")
        real_path = Path

        def mapped(value):
            if str(value) == "/proc":
                return proc
            if str(value) == "/proc/self/cmdline":
                return proc / "self/cmdline"
            return real_path(value)

        return process, patch.object(w, "Path", side_effect=mapped)

    def test_process_cwd_and_open_file(self):
        self.create()
        process, mapping = self.fake_proc()
        with mapping, patch.dict(os.environ, {"WORKTREE_HOST_PROCESS_CHECK": "1"}):
            w.check_processes(self.task)
            (process / "fd/3").symlink_to(self.task / "file")
            with self.assertRaisesRegex(w.CheckError, "Process still using"):
                w.check_processes(self.task)
            (process / "fd/3").unlink()
            (process / "cwd").unlink()
            (process / "cwd").symlink_to(self.task)
            with self.assertRaisesRegex(w.CheckError, "Process still using"):
                w.check_processes(self.task)

    def test_process_command_and_mapping(self):
        self.create()
        process, mapping = self.fake_proc()
        with mapping, patch.dict(os.environ, {"WORKTREE_HOST_PROCESS_CHECK": "1"}):
            (process / "cmdline").write_bytes(
                b"worker\0--input=" + os.fsencode(self.task / "file") + b"\0"
            )
            with self.assertRaises(w.CheckError):
                w.check_processes(self.task)
            (process / "cmdline").write_bytes(b"worker\0")
            (process / "maps").write_text(
                "0000-1000 r--p 0 00:00 1 " + str(self.task / "file") + "\n"
            )
            with self.assertRaises(w.CheckError):
                w.check_processes(self.task)

    def test_process_permission_failure(self):
        self.create()
        _, mapping = self.fake_proc()
        with mapping, patch.dict(
            os.environ, {"WORKTREE_HOST_PROCESS_CHECK": "1"}
        ), patch.object(
            w.os, "readlink", side_effect=PermissionError()
        ), self.assertRaisesRegex(
            w.CheckError, "Cannot fully inspect"
        ):
            w.check_processes(self.task)

    def test_reference_cas_preserves_concurrent_update(self):
        self.create()
        original = w.git

        def move_ref(root, *args):
            if args[:2] == ("update-ref", "-d"):
                new = (
                    original(
                        self.root,
                        "-c",
                        "user.name=Test",
                        "-c",
                        "user.email=test@example.invalid",
                        "commit-tree",
                        "develop^{tree}",
                        "-p",
                        "develop",
                        "-m",
                        "concurrent",
                    )
                    .strip()
                    .decode()
                )
                original(self.root, "update-ref", "refs/heads/feat_test", new)
            return original(root, *args)

        with patch.object(w, "git", side_effect=move_ref), self.assertRaises(
            w.CheckError
        ):
            self.remove()
        self.assertNotEqual(
            w.local_commit(self.root, "feat_test"), w.local_commit(self.root, "develop")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
