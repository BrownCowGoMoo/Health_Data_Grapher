from __future__ import annotations
from typing import TYPE_CHECKING
from db import DBManager
from files import scan_files,get_files_to_include, extract_pdf_text
from parser import parse_reports

if TYPE_CHECKING:
    from models import Pdf, ResultInfoSeries


def main():
    files: list[Pdf] = scan_files()
    chosen_files: list[Pdf] = get_files_to_include(files)
    extract_pdf_text(chosen_files)
    all_records: list[ResultInfoSeries] = parse_reports(chosen_files)
    db = DBManager()
    db.create_tables()
    db.insert_info(all_records)
    db.select_shared_names()


if __name__ == "__main__":
    main()