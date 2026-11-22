import csv
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python csv_cleaner_v2.py input.csv")

    source = Path(sys.argv[1])

    if not source.is_file():
        sys.exit("ERROR: Input file not found")

    clean_file = source.with_name(f"{source.stem}_clean.csv")
    duplicate_file = source.with_name(f"{source.stem}_duplicates.csv")
    review_file = source.with_name(f"{source.stem}_review.csv")

    outputs = [clean_file, duplicate_file, review_file]

    if source.resolve() in {p.resolve() for p in outputs}:
        sys.exit("ERROR: Output conflicts with input")

    seen = set()
    original = normalized = duplicates = review = clean = 0

    with source.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)

        if not reader.fieldnames:
            sys.exit("ERROR: Missing header")

        headers = [h.strip().lower() for h in reader.fieldnames]

        if len(set(headers)) != len(headers):
            sys.exit("ERROR: Duplicate column names")

        if "email" not in headers:
            sys.exit("ERROR: Missing email column")

        with (
            clean_file.open("w", encoding="utf-8", newline="") as cf,
            duplicate_file.open("w", encoding="utf-8", newline="") as df,
            review_file.open("w", encoding="utf-8", newline="") as rf
        ):
            writers = [
                csv.DictWriter(f, fieldnames=headers)
                for f in (cf, df, rf)
            ]

            for writer in writers:
                writer.writeheader()

            for raw in reader:
                original += 1

                if None in raw:
                    sys.exit("ERROR: Extra CSV fields")

                row = {}
                changed = False

                for old, value in raw.items():
                    key = old.strip().lower()
                    value = value or ""
                    cleaned = value.strip()

                    if key != old or cleaned != value:
                        changed = True

                    row[key] = cleaned

                email = row["email"].lower()

                if email != row["email"]:
                    changed = True

                row["email"] = email

                if changed:
                    normalized += 1

                if not email:
                    writers[2].writerow(row)
                    review += 1
                elif email in seen:
                    writers[1].writerow(row)
                    duplicates += 1
                else:
                    seen.add(email)
                    writers[0].writerow(row)
                    clean += 1

    assert original == clean + duplicates + review

    print("=" * 44)
    print("CSV CLEANER V2 REPORT")
    print("=" * 44)
    print(f"Original records : {original}")
    print(f"Normalized rows  : {normalized}")
    print(f"Clean records    : {clean}")
    print(f"Duplicates       : {duplicates}")
    print(f"Review records   : {review}")
    print(f"Reconciliation   : {clean + duplicates + review}")
    print("=" * 44)
    print("SUCCESS")

if __name__ == "__main__":
    main()
