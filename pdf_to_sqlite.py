"""Demo: extract tables from a PDF into SQLite. Sample data is fictitious."""
import re
import sqlite3
import sys

import pdfplumber


def clean(name, i):
    name = re.sub(r"\W+", "_", (name or "").strip().lower()).strip("_")
    return name or f"col{i}"


def main(pdf_path, db_path):
    con = sqlite3.connect(db_path)
    with pdfplumber.open(pdf_path) as pdf:
        for p, page in enumerate(pdf.pages, 1):
            for n, table in enumerate(page.extract_tables(), 1):
                if len(table) < 2:
                    continue
                cols = [clean(c, i) for i, c in enumerate(table[0])]
                name = f"table_{p}_{n}"
                con.execute(f'DROP TABLE IF EXISTS "{name}"')
                con.execute(f'CREATE TABLE "{name}" ({", ".join(chr(34)+c+chr(34) for c in cols)})')
                marks = ",".join("?" * len(cols))
                con.executemany(f'INSERT INTO "{name}" VALUES ({marks})', table[1:])
                print(f"{name}: {len(table) - 1} rows")
    con.commit()
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python pdf_to_sqlite.py input.pdf output.db")
    main(sys.argv[1], sys.argv[2])
