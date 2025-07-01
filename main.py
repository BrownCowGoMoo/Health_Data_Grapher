from files import scan_files,get_files_to_include, extract_pdf_text, Pdf
from parser import parse_results
from typing import List

def main():
    files: List[Pdf] = scan_files()
    chosen_files: list[Pdf] = get_files_to_include(files)
    extract_pdf_text(chosen_files)
    parse_results(chosen_files)


if __name__ == "__main__":
    main()