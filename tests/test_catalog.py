import tempfile
import unittest
from pathlib import Path

from scripts.install_skills import build_install_plan, install_plan
from scripts.validate_catalog import validate_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_is_consistent(self):
        self.assertEqual(validate_catalog(), [])

    def test_install_plan_contains_twelve_distinct_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            plan = build_install_plan(Path(directory))
        names = [name for name, _, _ in plan]
        self.assertEqual(len(names), 12)
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("project-compass", names)
        self.assertIn("repo-steward", names)
        self.assertIn("project-challenge-lab", names)
        self.assertIn("gate", names)
        self.assertIn("hackathon-practice", names)
        self.assertIn("recall-loop", names)
        for _, source, _ in plan:
            self.assertTrue((source / "SKILL.md").is_file())

    def test_installer_copies_twelve_discoverable_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            plan = build_install_plan(target)
            install_plan(plan)
            installed = sorted(path.parent.name for path in target.glob("*/SKILL.md"))

        self.assertEqual(
            installed,
            sorted(
                [
                    "project-compass",
                    "sop-creator",
                    "actor-reader",
                    "socratic-discuss",
                    "skill-review",
                    "postmortem-note",
                    "repo-steward",
                    "human-elite-english",
                    "project-challenge-lab",
                    "gate",
                    "hackathon-practice",
                    "recall-loop",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
