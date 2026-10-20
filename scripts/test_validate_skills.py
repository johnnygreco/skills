"""Run with: uvx --from skills-ref --with pyyaml python -m unittest discover -s scripts."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "validate_skills", Path(__file__).with_name("validate-skills.py")
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "example"
        self.skill.mkdir()

    def write_skill(self, extra="", config=None, name="example", description="Example skill"):
        (self.skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n{extra}---\nInstructions.\n"
        )
        config_path = self.skill / "agents" / "openai.yaml"
        if config is not None:
            config_path.parent.mkdir(exist_ok=True)
            config_path.write_text(config)
        else:
            config_path.unlink(missing_ok=True)

    def test_default_and_manual_invocation_agree(self):
        for extra, config in (
            ("", None),
            ("disable-model-invocation: false\n", None),
            ("", "policy:\n  allow_implicit_invocation: true\n"),
            ("disable-model-invocation: true\n", "policy:\n  allow_implicit_invocation: false\n"),
        ):
            with self.subTest(extra=extra, config=config):
                self.write_skill(extra, config)
                self.assertEqual(validator.validate_skill(self.skill), [])

    def test_rejects_divergent_invocation_policy(self):
        for extra, config in (
            ("disable-model-invocation: true\n", None),
            ("disable-model-invocation: true\n", "policy:\n  allow_implicit_invocation: true\n"),
            ("", "policy:\n  allow_implicit_invocation: false\n"),
        ):
            with self.subTest(extra=extra, config=config):
                self.write_skill(extra, config)
                self.assertIn("differs across harnesses", " ".join(validator.validate_skill(self.skill)))

    def test_rejects_nonboolean_policy_values(self):
        for value in ('"true"', '"false"', 'null', '1', 'sometimes', 'yes', 'no', 'on', 'off'):
            for location in ("frontmatter", "codex"):
                with self.subTest(value=value, location=location):
                    if location == "frontmatter":
                        self.write_skill(f"disable-model-invocation: {value}\n")
                    else:
                        self.write_skill(config=f"policy:\n  allow_implicit_invocation: {value}\n")
                    self.assertIn("YAML boolean", " ".join(validator.validate_skill(self.skill)))

    def test_reference_errors_survive_extension_handling(self):
        for extra, name, description in (
            ("unexpected: value\n", "example", "Example skill"),
            ("", "wrong-directory", "Example skill"),
            ("", "example", '""'),
            ("", "example", "x" * 1025),
        ):
            with self.subTest(extra=extra, name=name, description=description):
                self.write_skill(
                    "disable-model-invocation: true\n" + extra,
                    "policy:\n  allow_implicit_invocation: false\n",
                    name,
                    description,
                )
                self.assertTrue(validator.validate_skill(self.skill))

    def test_rejects_malformed_or_duplicate_frontmatter(self):
        for content in (
            "No frontmatter",
            "---\nname: example\n",
            "---\nname: example\nname: other\ndescription: Example\n---\n",
        ):
            with self.subTest(content=content):
                (self.skill / "SKILL.md").write_text(content)
                self.assertTrue(validator.validate_skill(self.skill))

    def test_rejects_malformed_codex_configuration(self):
        for config in ("- value\n", "policy: false\n", "policy: [\n"):
            with self.subTest(config=config):
                self.write_skill(config=config)
                self.assertTrue(validator.validate_skill(self.skill))

    def test_rejects_duplicate_codex_policy_keys(self):
        for config in (
            "policy:\n  allow_implicit_invocation: true\n  allow_implicit_invocation: false\n",
            "policy:\n  allow_implicit_invocation: true\npolicy:\n  allow_implicit_invocation: false\n",
        ):
            with self.subTest(config=config):
                self.write_skill("disable-model-invocation: true\n", config)
                self.assertIn("duplicate mapping key", " ".join(validator.validate_skill(self.skill)))

    def test_incomplete_directories_are_detected(self):
        self.write_skill()
        incomplete = self.root / "incomplete"
        incomplete.mkdir()
        (self.root / ".hidden").mkdir()
        with patch.object(validator, "SKILLS_ROOT", self.root):
            self.assertEqual(validator.find_skills(), [self.skill])
            self.assertEqual(validator.find_incomplete_skill_dirs(), [incomplete])


if __name__ == "__main__":
    unittest.main()
