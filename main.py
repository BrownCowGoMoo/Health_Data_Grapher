from __future__ import annotations
import sys

from db import DBManager
from files import scan_files, get_files_to_include, extract_pdf_text
from parser import parse_reports
from plot import PlotItemsSelector, plot_graph

def main():
    # scan and extract
    files = scan_files()
    chosen = get_files_to_include(files)
    extract_pdf_text(chosen)

    # parse into simple dicts
    all_series = parse_reports(chosen)

    # store and query
    db = DBManager()
    db.create_tables()
    db.insert_info(all_series)
    shared = db.select_shared_names()
    if not shared:
        print("There are no shared results across all of your reports.")
        sys.exit()

    # select & plot
    item = PlotItemsSelector.get_item_to_plot(shared)
    values = db.select_values_for_name(item)
    plot_graph(values)

if __name__ == "__main__":
    main()