#!/usr/bin/env python3
"""Validate every skill in this repository."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


SKILLS_ROOT = Path("skills")


def find_skills() -> list[Path]:
    if not SKILLS_ROOT.exists():
        return []

    return [
        path
        for path in sorted(SKILLS_ROOT.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    ]


def find_incomplete_skill_dirs() -> list[Path]:
    if not SKILLS_ROOT.exists():
        return []

    return [
        path
        for path in sorted(SKILLS_ROOT.iterdir())
        if path.is_dir()
        and not path.name.startswith(".")
        and not (path / "SKILL.md").is_file()
    ]


def validator_prefix() -> list[str] | None:
    agentskills = shutil.which("agentskills")
    if agentskills:
        return [agentskills, "validate"]

    uvx = shutil.which("uvx")
    if uvx:
        return [uvx, "--from", "skills-ref", "agentskills", "validate"]

    return None


def main() -> int:
    incomplete_dirs = find_incomplete_skill_dirs()
    if incomplete_dirs:
        print(
            "Found directories under skills/ without SKILL.md:",
            file=sys.stderr,
        )
        for path in incomplete_dirs:
            print(f"  - {path}", file=sys.stderr)
        print(
            "Every visible direct child directory of skills/ must be a skill folder.",
            file=sys.stderr,
        )
        return 1

    skills = find_skills()
    if not skills:
        print(f"No skills found under {SKILLS_ROOT}; nothing to validate.")
        return 0

    prefix = validator_prefix()
    if prefix is None:
        print(
            "Could not find agentskills or uvx. Install with "
            "`python -m pip install skills-ref` or install uv.",
            file=sys.stderr,
        )
        return 127

    failed = False
    for skill in skills:
        print(f"Validating {skill}")
        result = subprocess.run([*prefix, str(skill)], check=False)
        failed = failed or result.returncode != 0

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
