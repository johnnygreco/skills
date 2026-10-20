#!/usr/bin/env python3
"""Validate skills against the reference spec and shared invocation policy."""

from __future__ import annotations

import importlib.util
import os
import re
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


def run_with_dependencies() -> int:
    """Use installed Python packages, or let uvx supply an isolated environment."""
    uvx = shutil.which("uvx")
    if uvx and not os.environ.get("SKILLS_VALIDATOR_BOOTSTRAPPED"):
        return subprocess.run(
            [
                uvx, "--from", "skills-ref", "--with", "pyyaml",
                "python", str(Path(__file__).resolve()),
            ],
            env={**os.environ, "SKILLS_VALIDATOR_BOOTSTRAPPED": "1"},
            check=False,
        ).returncode

    print(
        "Install validation dependencies with `python -m pip install skills-ref pyyaml` "
        "or install uv.",
        file=sys.stderr,
    )
    return 127


def load_yaml(content: str):
    """Reject duplicate keys and use portable true/false boolean spellings."""
    import yaml

    class PolicyLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            mapping = super().construct_mapping(node, deep=deep)
            if len(mapping) != len(node.value):
                raise yaml.constructor.ConstructorError(
                    None, None, "duplicate mapping key", node.start_mark
                )
            return mapping

    boolean_tag = "tag:yaml.org,2002:bool"
    PolicyLoader.yaml_implicit_resolvers = {
        key: [(tag, pattern) for tag, pattern in resolvers if tag != boolean_tag]
        for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    PolicyLoader.add_implicit_resolver(
        boolean_tag, re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF")
    )
    return yaml.load(content, Loader=PolicyLoader)


def validate_skill(skill: Path) -> list[str]:
    import yaml
    from skills_ref.errors import ParseError
    from skills_ref.parser import parse_frontmatter
    from skills_ref.validator import validate_metadata

    try:
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content)
        # The reference parser treats scalars as strings. Parse their YAML types
        # separately so a quoted "true" cannot pass as a boolean policy value.
        typed = load_yaml(content.split("---", 2)[1])
    except (OSError, UnicodeError, ParseError, yaml.YAMLError) as error:
        return [str(error)]

    field = "disable-model-invocation"
    disabled = typed.get(field, False)
    errors = []
    if type(disabled) is not bool:
        errors.append(f"Field '{field}' must be a YAML boolean")
    # Only this documented Cursor/Claude Code extension is exempt from the
    # reference field allowlist; all other reference checks still apply.
    metadata.pop(field, None)
    errors.extend(validate_metadata(metadata, skill))

    config_path = skill / "agents" / "openai.yaml"
    implicit = True
    if config_path.exists():
        try:
            config = load_yaml(config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            return [*errors, f"agents/openai.yaml: {error}"]
        if not isinstance(config, dict):
            return [*errors, "agents/openai.yaml must be a YAML mapping"]
        policy = config.get("policy", {})
        if not isinstance(policy, dict):
            return [*errors, "agents/openai.yaml policy must be a YAML mapping"]
        implicit = policy.get("allow_implicit_invocation", True)
        if type(implicit) is not bool:
            errors.append(
                "agents/openai.yaml policy.allow_implicit_invocation must be a YAML boolean"
            )

    if type(disabled) is bool and type(implicit) is bool and disabled == implicit:
        errors.append(
            "Invocation policy differs across harnesses: SKILL.md "
            "disable-model-invocation must be the inverse of "
            "agents/openai.yaml policy.allow_implicit_invocation "
            "(defaults: false and true, respectively)"
        )
    return errors


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

    if any(importlib.util.find_spec(module) is None for module in ("skills_ref", "yaml")):
        return run_with_dependencies()

    failed = False
    for skill in skills:
        print(f"Validating {skill}")
        errors = validate_skill(skill)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        if not errors:
            print("  Skill is valid")
        failed = failed or bool(errors)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
