# CSV Data Cleaning Service

Python CLI tool for cleaning CSV records.

## Features
- Normalize column names.
- Remove surrounding whitespace.
- Normalize email addresses.
- Detect duplicate emails.
- Separate missing emails for review.
- Export three independent CSV files.
- Verify record reconciliation.

## Requirements
Python 3.10+
No external dependencies.

## Usage
python csv_cleaner_v2.py demo/edge_cases.csv

## Outputs
- edge_cases_clean.csv
- edge_cases_duplicates.csv
- edge_cases_review.csv

## Reconciliation
Original = Clean + Duplicates + Review

## Limitations
- Deduplication uses email.
- Email syntax is not validated.
- Missing emails are sent to review.
- Input files remain unchanged.
