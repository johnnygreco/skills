#!/usr/bin/env python3
"""Append one decision row to a single-writer TSV audit log."""

from __future__ import annotations

import argparse
import csv
import io
import os
from datetime import datetime, timezone
from pathlib import Path


HEADER = b"ts\tphase\tdecision\twhy\tevidence\tresult\n"
FIELDS = ("phase", "decision", "why", "evidence", "result")


def clean_cell(value: str) -> str:
    """Keep a cell on one line and inert when opened in a spreadsheet."""
    value = value.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    if not value.strip():
        raise ValueError("cells must not be empty; use an explicit unknown state")
    if value.lstrip().startswith(("=", "+", "-", "@")):
        value = "'" + value
    return value


def append_row(path: Path, cells: list[str]) -> None:
    cleaned = [clean_cell(cell) for cell in cells]
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    timestamp = timestamp.replace("+00:00", "Z")
    buffer = io.StringIO(newline="")
    csv.writer(buffer, delimiter="\t", lineterminator="\n").writerow(
        [timestamp, *cleaned]
    )
    row = buffer.getvalue().encode("utf-8")

    path.parent.mkdir(parents=True, exist_ok=True)
    # Append mode prevents truncation. The caller must serialize writers.
    with path.open("a+b") as log:
        log.seek(0, os.SEEK_END)
        size = log.tell()
        if size:
            log.seek(0)
            if log.readline().rstrip(b"\r\n") != HEADER.rstrip(b"\n"):
                raise ValueError("existing log has an incompatible header")
            log.seek(-1, os.SEEK_END)
            if log.read(1) != b"\n":
                raise ValueError("existing log has no final newline; preserve it and recover explicitly")

        log.write((HEADER if not size else b"") + row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logfile", type=Path)
    for field in FIELDS:
        parser.add_argument(field)
    args = parser.parse_args()
    try:
        append_row(args.logfile, [getattr(args, field) for field in FIELDS])
    except (OSError, ValueError) as error:
        parser.exit(1, f"log.py: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
