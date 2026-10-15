#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
commit_script="$script_dir/../../quick-commit/scripts/commit_by_codex.sh"

usage() {
    cat <<'HELP'
Usage: review_and_commit.sh [OPTIONS]

Run review/fix cycles, then automatically commit only if review succeeds.

  --review-scope S  auto (default), changes, or branch (local main/master baseline).
                    Auto reviews uncommitted changes when present, otherwise branch.
  --repo PATH       Repository to review and commit. Default: current directory.
  --max-loops N     Maximum review/fix loops. Default: 12.
  --log-dir PATH    Review log directory outside the target repository.
  --fast            Use the Fast service tier for review/fix steps.
  --resume [LOG]    Resume LOG, or the newest incomplete run for the repository.
  --allow-worktree-changes
                    Allow expected worktree changes when resuming.
  --model MODEL     Override the shared commit tool's model (default: gpt-6-luna).
  -h, --help        Show this help message.

The commit step always uses -y to skip confirmation. Git hooks and signing
retain their normal behavior. Except for --review-scope, --model and help, all options are
forwarded to the selected review script. Branch scope uses
review_pr_untill_satisfied.sh; changes scope uses
review_changes_untill_satisfied.sh. Its resume rules apply, including
--resume=LOG. The commit always targets the repository selected by review.
Auto scope with an explicit resume log uses its saved review mode. Without a
log, auto selects by repository status; specify a scope to resume that mode.
HELP
}

fail() { printf 'Error: %s\n' "$*" >&2; exit 2; }
review_scope=auto
repo_target="$PWD"
resume_log=""
review_args=()
commit_args=()
while (($#)); do
    case "$1" in
        --review-scope)
            (($# >= 2)) && [[ "$2" == auto || "$2" == changes || "$2" == branch ]] || fail "$1 requires auto, changes or branch"
            review_scope="$2"
            shift 2 ;;
        --repo|--max-loops|--log-dir)
            (($# >= 2)) && [[ -n "$2" && "$2" != -* ]] || fail "$1 requires a value"
            if [[ "$1" == --repo ]]; then repo_target="$2"; fi
            review_args+=("$1" "$2")
            shift 2 ;;
        --resume)
            resume_log=""
            review_args+=("$1")
            if (($# >= 2)) && [[ "$2" != -* ]]; then
                resume_log="$2"
                review_args+=("$2")
                shift 2
            else
                shift
            fi ;;
        --resume=*)
            resume_log="${1#--resume=}"
            [[ -n "$resume_log" ]] || fail '--resume requires a value'
            review_args+=("$1")
            shift ;;
        --model)
            (($# >= 2)) && [[ -n "$2" && "$2" != -* ]] || fail "$1 requires a value"
            commit_args+=("$1" "$2")
            shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) review_args+=("$1"); shift ;;
    esac
done

[[ -f "$commit_script" ]] || fail 'Missing dependency: quick-commit/scripts/commit_by_codex.sh. Install quick-commit alongside review-and-commit.'

if [[ "$review_scope" == auto ]]; then
    if [[ -n "$resume_log" ]]; then
        json_python="${REVIEW_UNTIL_PYTHON:-}"
        if [[ -z "$json_python" ]]; then
            json_python=$(command -v python3 || command -v python) || fail 'Python is required to read resume state.'
        fi
        review_scope=$("$json_python" - "${resume_log}.state.json" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as stream:
        mode = json.load(stream).get("review_mode", "changes")
    if mode not in ("pr", "changes"):
        raise ValueError("unsupported review_mode")
except (OSError, ValueError, AttributeError) as exc:
    print(f"Error: could not determine saved review scope: {exc}", file=sys.stderr)
    sys.exit(2)
print("branch" if mode == "pr" else "changes")
PY
        ) || fail 'Cannot select review scope from resume state.'
    else
        repo_root=$(git -C "$repo_target" rev-parse --show-toplevel) || fail 'Not a working-tree Git repository.'
        worktree_status=$(git -C "$repo_root" status --porcelain --untracked-files=all) || fail 'Cannot inspect repository status.'
        if [[ -n "$worktree_status" ]]; then
            review_scope=changes
        else
            review_scope=branch
        fi
    fi
fi
printf 'Review scope: %s\n' "$review_scope"

review_script="$script_dir/review_changes_untill_satisfied.sh"
if [[ "$review_scope" == branch ]]; then
    review_script="$script_dir/review_pr_untill_satisfied.sh"
fi

# Review owns repository selection, including selection from a resume log.
result_dir=$(mktemp -d)
trap 'rm -rf -- "$result_dir"' EXIT
review_pid=""
interrupt_review() {
    trap '' INT TERM
    if [[ -n "$review_pid" ]]; then
        # Background shells can inherit ignored SIGINT; TERM reliably invokes
        # the review script's cleanup while we retain the caller's exit status.
        kill -TERM "$review_pid" 2>/dev/null || true
        wait "$review_pid" 2>/dev/null || true
    fi
    exit "$1"
}
trap 'interrupt_review 130' INT
trap 'interrupt_review 143' TERM
result_file="$result_dir/review-result"
REVIEW_UNTIL_RESULT_FILE="$result_file" bash "$review_script" "${review_args[@]}" <&0 &
review_pid=$!
wait "$review_pid"
review_pid=""
[[ -f "$result_file" ]] || fail 'Review did not report its repository and snapshot.'
{
    IFS= read -r -d '' repo || fail 'Invalid review repository result.'
    IFS= read -r -d '' reviewed_snapshot || fail 'Missing reviewed snapshot.'
    if IFS= read -r -d '' extra || [[ -n "$extra" ]]; then
        fail 'Invalid review repository result.'
    fi
} < "$result_file"
[[ "$repo" == /* ]] || fail 'Review repository must be an absolute path.'
resolved_repo=$(git -C "$repo" rev-parse --show-toplevel) || fail 'Review repository is not a working-tree Git repository.'
[[ "$resolved_repo" == "$repo" ]] || fail 'Review repository must be the repository root.'
rm -rf -- "$result_dir"
trap - EXIT INT TERM
exec bash "$commit_script" --repo "$repo" --reviewed-snapshot "$reviewed_snapshot" "${commit_args[@]}" -y
