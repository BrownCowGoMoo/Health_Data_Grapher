from __future__ import annotations
from typing import TYPE_CHECKING
import sys
from db import DBManager
from files import scan_files,get_files_to_include, extract_pdf_text
from parser import parse_reports
from plot import PlotItemsSelector, plot_graph

if TYPE_CHECKING:
    from models import Pdf, ResultInfoSeries


def main():
    # Gets the list of Pdf objects
    files: list[Pdf] = scan_files()
    
    chosen_files: list[Pdf] = get_files_to_include(files)
    extract_pdf_text(chosen_files)
    all_chosen_records: list[ResultInfoSeries] = parse_reports(chosen_files)

    db = DBManager()
    db.create_tables()
    db.insert_info(all_chosen_records)
    shared_names = db.select_shared_names()
    if not shared_names:
        print("There are no shared results across all of your reports.")
        sys.exit()

    item_to_plot = PlotItemsSelector.get_item_to_plot(shared_names)

    plot_values = db.select_values_for_name(item_to_plot)
    plot_graph(plot_values)

if __name__ == "__main__":
    main()