#!/usr/bin/env python3
"""Run reusable skill evaluations and build a static review page.

This runner follows the local workspace shape and uses the vendored review
viewer bundled in this repository by default.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKSPACES_ROOT = REPO_ROOT / "workspaces"
DEFAULT_VIEWER_PATH = REPO_ROOT / "tools" / "skill-eval-viewer"
AUTH_ERROR_HINTS = (
    "does not have access to Claude",
    "Please login again",
    "Invalid API key",
    "authentication",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a reusable with-skill vs baseline evaluation for a skill.",
    )
    parser.add_argument("skill_name", help="Skill name, for example floracat-architecture-diagram")
    parser.add_argument(
        "--workspaces-root",
        type=Path,
        default=DEFAULT_WORKSPACES_ROOT,
        help="Workspace root for generated eval results.",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        help="Claude model name passed to the CLI.",
    )
    parser.add_argument(
        "--claude-bin",
        default=shutil.which("claude") or "claude",
        help="Claude CLI binary path.",
    )
    parser.add_argument(
        "--cases",
        default="",
        help="Comma-separated eval ids to run. Default runs every eval in evals/evals.json.",
    )
    parser.add_argument(
        "--review-only",
        action="store_true",
        help="Skip execution and only rebuild review.html from an existing iteration.",
    )
    parser.add_argument(
        "--iteration",
        default="latest",
        help="Iteration number or path. Used by --review-only. Default: latest.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_skill_dir(skill_name: str) -> Path:
    skill_dir = REPO_ROOT / "skills" / skill_name
    if not skill_dir.is_dir():
        raise SystemExit("Skill not found: %s" % skill_dir)
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit("SKILL.md not found in %s" % skill_dir)
    return skill_dir


def parse_skill_frontmatter(skill_dir: Path) -> Dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise SystemExit("SKILL.md frontmatter is missing in %s" % skill_dir)
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_eval_config(skill_dir: Path) -> Dict[str, Any]:
    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.is_file():
        raise SystemExit("Eval config not found: %s" % evals_path)
    config = load_json(evals_path)
    if "evals" not in config or not isinstance(config["evals"], list):
        raise SystemExit("Invalid eval config: %s" % evals_path)
    return config


def parse_case_filter(raw: str) -> Optional[List[int]]:
    if not raw.strip():
        return None
    result = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        result.append(int(item))
    return result


def select_evals(config: Dict[str, Any], case_filter: Optional[List[int]]) -> List[Dict[str, Any]]:
    evals = config["evals"]
    if case_filter is None:
        return evals
    selected = [item for item in evals if int(item["id"]) in case_filter]
    if len(selected) != len(case_filter):
        found = {int(item["id"]) for item in selected}
        missing = [str(item) for item in case_filter if item not in found]
        raise SystemExit("Unknown eval ids: %s" % ", ".join(missing))
    return selected


def ensure_skill_link(skill_name: str, skill_dir: Path) -> Path:
    skills_dir = REPO_ROOT / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    link_path = skills_dir / skill_name
    target = skill_dir.resolve()
    if link_path.exists() or link_path.is_symlink():
        if link_path.is_symlink() and link_path.resolve() == target:
            return link_path
        raise SystemExit("Skill link already exists and does not match: %s" % link_path)
    link_path.symlink_to(target)
    return link_path


def next_iteration_dir(workspaces_root: Path, skill_name: str) -> Path:
    skill_root = workspaces_root / skill_name
    skill_root.mkdir(parents=True, exist_ok=True)
    highest = 0
    for child in skill_root.iterdir():
        match = re.match(r"iteration-(\d+)$", child.name)
        if child.is_dir() and match:
            highest = max(highest, int(match.group(1)))
    return skill_root / ("iteration-%d" % (highest + 1))


def resolve_iteration_dir(workspaces_root: Path, skill_name: str, raw_iteration: str) -> Path:
    candidate = Path(raw_iteration).expanduser()
    if candidate.exists():
        return candidate.resolve()
    skill_root = workspaces_root / skill_name
    if raw_iteration == "latest":
        choices = []
        if skill_root.is_dir():
            for child in skill_root.iterdir():
                match = re.match(r"iteration-(\d+)$", child.name)
                if child.is_dir() and match:
                    choices.append((int(match.group(1)), child))
        if not choices:
            raise SystemExit("No iterations found under %s" % skill_root)
        return sorted(choices)[-1][1]
    if raw_iteration.isdigit():
        candidate = skill_root / ("iteration-%s" % raw_iteration)
        if candidate.is_dir():
            return candidate
    raise SystemExit("Iteration not found: %s" % raw_iteration)


def write_eval_metadata(eval_dir: Path, eval_case: Dict[str, Any]) -> None:
    payload = {
        "eval_id": eval_case["id"],
        "eval_name": eval_case.get("slug", "eval-%s" % eval_case["id"]),
        "prompt": eval_case["prompt"],
        "expected_output": eval_case.get("expected_output", ""),
        "assertions": eval_case.get("expectations", []),
    }
    (eval_dir / "eval_metadata.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def copy_inputs(skill_dir: Path, eval_case: Dict[str, Any], run_dir: Path) -> List[str]:
    copied = []
    for relative_path in eval_case.get("files", []):
        src = skill_dir / relative_path
        if not src.is_file():
            raise SystemExit("Eval input file not found: %s" % src)
        dst = run_dir / "inputs" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append("inputs/%s" % src.name)
    return copied


def build_prompt(skill_name: str, eval_case: Dict[str, Any], use_skill: bool, copied_inputs: List[str]) -> str:
    output_files = eval_case.get("output_files", [])
    lines = []
    if use_skill:
        lines.append("Use the $%s skill." % skill_name)
        lines.append("")
    lines.append(eval_case["prompt"].strip())
    lines.append("")
    lines.append("Execution rules:")
    lines.append("- Work only inside the current directory.")
    lines.append("- Put every generated deliverable inside outputs/.")
    lines.append("- Keep file names exact.")
    if copied_inputs:
        lines.append("- Read input files only from %s." % ", ".join(copied_inputs))
    if output_files:
        lines.append(
            "- You must create these files: %s." % ", ".join("outputs/%s" % name for name in output_files)
        )
    lines.append("- Keep the final chat response brief.")
    if eval_case.get("expected_output"):
        lines.append("")
        lines.append("Expected result:")
        lines.append(eval_case["expected_output"].strip())
    return "\n".join(lines).strip() + "\n"


def find_viewer_python() -> Optional[str]:
    candidates = [
        os.environ.get("FLORACAT_VIEWER_PYTHON", ""),
        shutil.which("python3.14") or "",
        shutil.which("python3.13") or "",
        shutil.which("python3.12") or "",
        shutil.which("python3.11") or "",
        shutil.which("python3.10") or "",
        shutil.which("python3") or "",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            result = subprocess.run(
                [candidate, "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        text = (result.stdout or result.stderr).strip()
        match = re.search(r"Python\s+(\d+)\.(\d+)", text)
        if not match:
            continue
        major = int(match.group(1))
        minor = int(match.group(2))
        if major > 3 or (major == 3 and minor >= 10):
            return candidate
    return None


def save_run_logs(run_dir: Path, prompt: str, result: subprocess.CompletedProcess, started_at: float) -> None:
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    (run_dir / "stdout.txt").write_text(result.stdout or "", encoding="utf-8")
    (run_dir / "stderr.txt").write_text(result.stderr or "", encoding="utf-8")
    timing = {
        "executor_start_epoch": started_at,
        "executor_end_epoch": time.time(),
        "executor_duration_seconds": round(time.time() - started_at, 2),
    }
    (run_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n", encoding="utf-8")
    run_info = {
        "returncode": result.returncode,
        "command": result.args,
    }
    (run_dir / "run.json").write_text(json.dumps(run_info, indent=2) + "\n", encoding="utf-8")
    assistant_output = (result.stdout or "").strip()
    if assistant_output:
        (run_dir / "outputs" / "assistant-response.md").write_text(assistant_output + "\n", encoding="utf-8")


def run_claude(
    claude_bin: str,
    model: str,
    run_dir: Path,
    prompt: str,
) -> None:
    cmd = [
        claude_bin,
        "-p",
        prompt,
        "--permission-mode",
        "bypassPermissions",
        "--add-dir",
        str(run_dir),
        "--model",
        model,
    ]
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    started_at = time.time()
    result = subprocess.run(
        cmd,
        cwd=str(run_dir),
        capture_output=True,
        text=True,
        env=env,
    )
    save_run_logs(run_dir, prompt, result, started_at)
    combined = "%s\n%s" % (result.stdout or "", result.stderr or "")
    if result.returncode != 0:
        for hint in AUTH_ERROR_HINTS:
            if hint.lower() in combined.lower():
                raise SystemExit(
                    "Claude CLI authentication failed. Please login again, then rerun this command."
                )
        raise SystemExit("Claude run failed in %s. See stderr.txt for details." % run_dir)


def generate_review(skill_name: str, iteration_dir: Path, viewer_path: Path) -> Optional[Path]:
    viewer_script = viewer_path / "generate_review.py"
    if not viewer_script.is_file():
        print("Skip review generation: viewer not found at %s" % viewer_script, file=sys.stderr)
        return None
    viewer_python = find_viewer_python()
    if not viewer_python:
        print("Skip review generation: Python 3.10+ not found for viewer.", file=sys.stderr)
        return None
    review_path = iteration_dir / "review.html"
    subprocess.run(
        [
            viewer_python,
            str(viewer_script),
            str(iteration_dir),
            "--skill-name",
            skill_name,
            "--static",
            str(review_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return review_path


def execute_eval_case(
    skill_name: str,
    skill_dir: Path,
    eval_case: Dict[str, Any],
    iteration_dir: Path,
    claude_bin: str,
    model: str,
) -> None:
    slug = eval_case.get("slug", "eval-%s" % eval_case["id"])
    eval_dir = iteration_dir / ("eval-%s-%s" % (eval_case["id"], slug))
    eval_dir.mkdir(parents=True, exist_ok=True)
    write_eval_metadata(eval_dir, eval_case)

    for run_name, use_skill in (("with_skill", True), ("baseline", False)):
        run_dir = eval_dir / run_name
        (run_dir / "inputs").mkdir(parents=True, exist_ok=True)
        (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
        copied_inputs = copy_inputs(skill_dir, eval_case, run_dir)
        prompt = build_prompt(skill_name, eval_case, use_skill, copied_inputs)
        run_claude(claude_bin=claude_bin, model=model, run_dir=run_dir, prompt=prompt)


def main() -> None:
    args = parse_args()
    viewer_path = DEFAULT_VIEWER_PATH
    skill_dir = find_skill_dir(args.skill_name)
    frontmatter = parse_skill_frontmatter(skill_dir)
    config = load_eval_config(skill_dir)
    if config.get("skill_name") != frontmatter.get("name"):
        raise SystemExit("skill_name in evals.json does not match SKILL.md frontmatter.")

    if args.review_only:
        iteration_dir = resolve_iteration_dir(args.workspaces_root, args.skill_name, args.iteration)
        review_path = generate_review(args.skill_name, iteration_dir, viewer_path)
        if review_path:
            print("Review written to %s" % review_path)
        return

    ensure_skill_link(args.skill_name, skill_dir)

    selected_evals = select_evals(config, parse_case_filter(args.cases))
    iteration_dir = next_iteration_dir(args.workspaces_root, args.skill_name)
    iteration_dir.mkdir(parents=True, exist_ok=True)

    for eval_case in selected_evals:
        execute_eval_case(
            skill_name=args.skill_name,
            skill_dir=skill_dir,
            eval_case=eval_case,
            iteration_dir=iteration_dir,
            claude_bin=args.claude_bin,
            model=args.model,
        )

    review_path = generate_review(args.skill_name, iteration_dir, viewer_path)

    print("Skill eval finished.")
    print("Iteration: %s" % iteration_dir)
    if review_path:
        print("Review: %s" % review_path)


if __name__ == "__main__":
    main()
