import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


class PublicationGuardTest(unittest.TestCase):
    def run_guard(self, target, env=None):
        root = pathlib.Path(__file__).resolve().parents[1]
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "publication_guard.py"), str(target)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=run_env,
        )

    def test_candidate_passes_without_external_denylist(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        result = self.run_guard(root)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_guard_rejects_generic_project_term(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            blocked = "ACME" + "_PRIVATE_" + "RESEARCH"
            (target / "note.md").write_text(blocked, encoding="utf-8")
            result = self.run_guard(target)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("generic_policy_match_detected", result.stdout)

    def test_guard_rejects_private_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            blocked = "C:" + "\\Users\\Example\\PrivateWorkspace"
            (target / "note.md").write_text(blocked, encoding="utf-8")
            result = self.run_guard(target)
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_guard_rejects_forbidden_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            (target / "artifact.ex5").write_text("placeholder", encoding="utf-8")
            result = self.run_guard(target)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("forbidden extension", result.stdout)

    def test_guard_rejects_simulated_credential(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            blocked = "token" + "=" + "example"
            (target / "note.md").write_text(blocked, encoding="utf-8")
            result = self.run_guard(target)
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_external_private_denylist_blocks_and_masks_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "target"
            target.mkdir()
            denylist = pathlib.Path(tmp) / "denylist.txt"
            term = "SENSITIVE_FIXTURE_VALUE"
            denylist.write_text(term, encoding="utf-8")
            (target / "note.md").write_text(term, encoding="utf-8")
            result = self.run_guard(target, {"PUBLICATION_PRIVATE_DENYLIST_FILE": str(denylist)})
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("private_denylist_match_detected", result.stdout)
        self.assertNotIn(term, result.stdout)

    def test_missing_external_private_denylist_does_not_break_ci(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            (target / "note.md").write_text("clean documentation", encoding="utf-8")
            missing = str(pathlib.Path(tmp) / "missing.txt")
            result = self.run_guard(target, {"PUBLICATION_PRIVATE_DENYLIST_FILE": missing})
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
