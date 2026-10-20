"""Regression checks for the skill's append-only TSV logger CLI."""

import csv
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


LOGGER = Path(__file__).resolve().parents[1] / "skills/show-me-your-work/scripts/log.py"
CELLS = ["verify", "Keep the change", "Regression passed", "evidence.txt", "passed"]


class LoggerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.log = Path(temporary.name) / "nested" / "decisions.tsv"

    def append(self, cells):
        return subprocess.run(
            [sys.executable, str(LOGGER), "--", str(self.log), *cells],
            capture_output=True,
            text=True,
            check=False,
        )

    def rows(self):
        return list(csv.reader(io.StringIO(self.log.read_text()), delimiter="\t", strict=True))

    def test_quotes_round_trip_without_consuming_later_rows(self):
        decisions = ['"Defer release', 'Keep "quoted" text', '"', 'Keep café 東京']
        prefix = b""
        expected = []
        for decision in decisions:
            cells = [*CELLS]
            cells[1] = decision
            result = self.append(cells)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(self.log.read_bytes().startswith(prefix))
            prefix = self.log.read_bytes()
            expected.append(cells)
        rows = self.rows()
        self.assertEqual(rows[0], ["ts", "phase", "decision", "why", "evidence", "result"])
        self.assertEqual([row[1:] for row in rows[1:]], expected)

    def test_empty_cells_are_rejected_without_changing_history(self):
        for existing in (False, True):
            if existing:
                self.assertEqual(self.append(CELLS).returncode, 0)
            before = self.log.read_bytes() if existing else None
            for index in range(len(CELLS)):
                with self.subTest(existing=existing, index=index):
                    cells = [*CELLS]
                    cells[index] = " \t\r\n "
                    self.assertNotEqual(self.append(cells).returncode, 0)
                    after = self.log.read_bytes() if self.log.exists() else None
                    self.assertEqual(after, before)

    def test_incompatible_or_truncated_history_is_preserved(self):
        for original in (
            b"wrong\theader\n",
            b"ts\tphase\tdecision\twhy\tevidence\tresult\npartial",
        ):
            with self.subTest(original=original):
                self.log.parent.mkdir(parents=True, exist_ok=True)
                self.log.write_bytes(original)
                self.assertNotEqual(self.append(CELLS).returncode, 0)
                self.assertEqual(self.log.read_bytes(), original)

    def test_control_characters_and_formula_prefixes(self):
        cells = ["verify\tphase", '=HYPERLINK("x")', "+why\nnow", "-evidence\r\npath", " @result"]
        result = self.append(cells)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][1:], [
            "verify phase", "'=HYPERLINK(\"x\")", "'+why now", "'-evidence  path", "' @result"
        ])


if __name__ == "__main__":
    unittest.main()
