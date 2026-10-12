# PDF tables to SQLite - demo con datos ficticios

DEMO con datos ficticios. No es un trabajo de cliente. Todos los datos de ejemplo son inventados.

Extracts tables from a text-based PDF and loads them into a SQLite database.

## Usage

    pip install pdfplumber
    python pdf_to_sqlite.py invoices.pdf out.db

Each table found is stored as `table_<page>_<n>`. The first row is used as the header.
