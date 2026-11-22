import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "csv_cleaner_v2.py"


class TestCSVCleaner(unittest.TestCase):

    def run_cleaner(self, directory, filename, content):
        source = Path(directory) / filename
        source.write_text(content, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(source)],
            capture_output=True,
            text=True
        )
        return source, result

    def read_csv(self, path):
        with path.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def test_normalization_and_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = self.run_cleaner(
                tmp,
                "customers.csv",
                " Name , EMAIL \n"
                "Ahmed,AHMED@example.com\n"
                "Ahmed,ahmed@example.com\n"
                " Sara , SARA@example.com \n"
                "Ali,\n"
                "Omar,omar@example.com\n"
            )

            self.assertEqual(result.returncode, 0)

            clean = self.read_csv(
                source.with_name("customers_clean.csv")
            )
            duplicates = self.read_csv(
                source.with_name("customers_duplicates.csv")
            )
            review = self.read_csv(
                source.with_name("customers_review.csv")
            )

            self.assertEqual(len(clean), 3)
            self.assertEqual(len(duplicates), 1)
            self.assertEqual(len(review), 1)

            self.assertEqual(
                clean[0]["email"], "ahmed@example.com"
            )
            self.assertEqual(
                clean[1]["email"], "sara@example.com"
            )

            self.assertEqual(
                len(clean) + len(duplicates) + len(review), 5
            )

    def test_missing_email_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, result = self.run_cleaner(
                tmp,
                "invalid.csv",
                "name,phone\nAhmed,123\n"
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing email column", result.stderr)

    def test_duplicate_headers_after_normalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, result = self.run_cleaner(
                tmp,
                "duplicate_headers.csv",
                "email, EMAIL\n"
                "a@example.com,b@example.com\n"
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Duplicate column names", result.stderr)

    def test_header_only_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = self.run_cleaner(
                tmp,
                "empty.csv",
                "name,email\n"
            )

            self.assertEqual(result.returncode, 0)

            for suffix in ("clean", "duplicates", "review"):
                output = source.with_name(
                    f"empty_{suffix}.csv"
                )
                self.assertTrue(output.is_file())
                self.assertEqual(self.read_csv(output), [])

    def test_case_and_whitespace_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = self.run_cleaner(
                tmp,
                "duplicates.csv",
                "name,email\n"
                "Omar,omar@example.com\n"
                " Omar , OMAR@EXAMPLE.COM \n"
            )

            self.assertEqual(result.returncode, 0)

            clean = self.read_csv(
                source.with_name("duplicates_clean.csv")
            )
            duplicates = self.read_csv(
                source.with_name("duplicates_duplicates.csv")
            )

            self.assertEqual(len(clean), 1)
            self.assertEqual(len(duplicates), 1)

    def test_all_records_are_reconciled(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = self.run_cleaner(
                tmp,
                "reconcile.csv",
                "name,email\n"
                "A,a@example.com\n"
                "B,b@example.com\n"
                "C,a@example.com\n"
                "D,\n"
                "E,c@example.com\n"
            )

            self.assertEqual(result.returncode, 0)

            counts = [
                len(self.read_csv(
                    source.with_name(f"reconcile_{suffix}.csv")
                ))
                for suffix in ("clean", "duplicates", "review")
            ]

            with source.open(encoding="utf-8", newline="") as f:
                original = sum(1 for _ in csv.DictReader(f))

            self.assertEqual(original, sum(counts))


if __name__ == "__main__":
    unittest.main(verbosity=2)
