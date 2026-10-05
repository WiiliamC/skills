#!/usr/bin/env bash

# Shared review checkpoint / commit handoff content identity (includes HEAD).
readonly WORKTREE_FINGERPRINT_VERSION=v1

worktree_fingerprint() {
    "${JSON_PYTHON:-python3}" - "${1:-$project_root}" <<'PY'
import hashlib
import os
import stat
import subprocess
import sys

def git(root, *args, check=True):
    return subprocess.run(
        ["git", "-C", root, *args],
        check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

def add_field(h, label, value):
    h.update(label + b"\0" + len(value).to_bytes(8, "big") + value)

def repository_fingerprint(root, ancestors):
    canonical_root = os.path.realpath(root)
    if canonical_root in ancestors:
        raise RuntimeError(f"recursive submodule checkout detected at {root}")
    ancestors = ancestors | {canonical_root}
    root_bytes = os.fsencode(root)
    h = hashlib.sha256()

    head_result = git(root, "rev-parse", "--verify", "HEAD", check=False)
    if head_result.returncode == 0:
        head = head_result.stdout
    else:
        symbolic_head = git(root, "symbolic-ref", "-q", "HEAD", check=False)
        if symbolic_head.returncode != 0:
            raise subprocess.CalledProcessError(
                head_result.returncode, head_result.args,
                output=head_result.stdout, stderr=head_result.stderr
            )
        head = b"<unborn-head>\n"

    for label, value in (
        (b"head", head),
        (b"staged", git(root, "diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv").stdout),
        (b"unstaged", git(root, "diff", "--binary", "--no-ext-diff", "--no-textconv").stdout),
    ):
        add_field(h, label, value)

    paths = [
        path for path in
        git(root, "ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0")
        if path
    ]
    for path in sorted(paths):
        full = os.path.join(root_bytes, path)
        st = os.lstat(full)
        if stat.S_ISREG(st.st_mode):
            kind = b"file+x" if st.st_mode & 0o111 else b"file"
            with open(full, "rb") as stream:
                content = stream.read()
        elif stat.S_ISLNK(st.st_mode):
            kind = b"symlink"
            content = os.fsencode(os.readlink(full))
        elif stat.S_ISDIR(st.st_mode):
            kind, content = b"dir", b""
        else:
            kind, content = f"special:{stat.S_IFMT(st.st_mode):o}".encode(), b""
        h.update(b"untracked\0" + path + b"\0" + kind + b"\0")
        h.update(len(content).to_bytes(8, "big") + content)

    gitlinks = []
    for entry in git(root, "ls-files", "--stage", "-z").stdout.split(b"\0"):
        if not entry:
            continue
        metadata, separator, path = entry.partition(b"\t")
        fields = metadata.split()
        if separator and len(fields) == 3 and fields[0] == b"160000" and fields[2] == b"0":
            gitlinks.append((path, fields[1]))

    for path, object_id in sorted(gitlinks):
        submodule_root_bytes = os.path.join(root_bytes, path)
        submodule_root = os.fsdecode(submodule_root_bytes)
        top_level = git(submodule_root, "rev-parse", "--show-toplevel", check=False)
        if (
            top_level.returncode != 0 or
            os.path.realpath(os.fsdecode(top_level.stdout.rstrip(b"\n"))) !=
            os.path.realpath(submodule_root)
        ):
            state = b"uninitialized"
        else:
            nested = repository_fingerprint(submodule_root, ancestors)
            state = b"checked-out\0" + nested.encode("ascii")
        add_field(h, b"submodule", path + b"\0" + object_id + b"\0" + state)

    return h.hexdigest()

print(repository_fingerprint(sys.argv[1], set()))
PY
}
