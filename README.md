# CSV Data Cleaning Tool

A lightweight Python CLI tool for cleaning and organizing customer CSV data.

## Features

- Normalize column names.
- Remove surrounding whitespace.
- Normalize email capitalization.
- Detect duplicate email addresses.
- Separate records with missing email addresses for review.
- Export clean, duplicate, and review CSV files.
- Report input and output record counts.

## Requirements

- Python 3.10+
- No external dependencies.

## Usage

    python csv_cleaner_v2.py demo/edge_cases.csv

## Output Files

- edge_cases_clean.csv
- edge_cases_duplicates.csv
- edge_cases_review.csv

## Run Tests

    python -m unittest discover -s tests -v

## Record Reconciliation

Original = Clean + Duplicates + Review

## Limitations

- Deduplication uses the email column.
- Email syntax is not validated.
- Records with missing email addresses are sent to review.
- Input files remain unchanged.
- The initial service scope is limited to CSV files.

## Project Structure

- csv_cleaner_v2.py — main application.
- tests/ — automated tests.
- demo/ — sample input data.
- SERVICE_OFFER.md — service description.
