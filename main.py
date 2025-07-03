from __future__ import annotations
from typing import TYPE_CHECKING
from db import DBManager
from files import scan_files,get_files_to_include, extract_pdf_text
from parser import parse_reports
from plot import get_items_to_prompt, sort_data_by_date

if TYPE_CHECKING:
    from models import Pdf, ResultInfoSeries


def main():
    files: list[Pdf] = scan_files()
    chosen_files: list[Pdf] = get_files_to_include(files)
    extract_pdf_text(chosen_files)
    all_chosen_records: list[ResultInfoSeries] = parse_reports(chosen_files)
    db = DBManager()
    db.create_tables()
    db.insert_info(all_chosen_records)
    shared_names = db.select_shared_names()
    get_items_to_prompt(shared_names)
    sort_data_by_date(all_chosen_records)


if __name__ == "__main__":
    main()