from __future__ import annotations
from typing import TYPE_CHECKING
from files import scan_files,get_files_to_include, extract_pdf_text
from parser import parse_results

if TYPE_CHECKING:
    from models import Pdf


def main():
    files: list[Pdf] = scan_files()
    chosen_files: list[Pdf] = get_files_to_include(files)
    extract_pdf_text(chosen_files)
    print(parse_results(chosen_files))


if __name__ == "__main__":
    main()