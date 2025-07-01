from pathlib import Path
import sys
from dataclasses import dataclass, field
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

@dataclass
class Pdf:
    path: str
    name_w_ext: str
    name: str
    text: list[str] = field(default_factory=list)

def get_directory_path(default_directory="C:\Coding Projects\Python\health data") -> str:
    if not default_directory:
        while True:

            directory = input("Input the directory path to your files: ")
            directory = Path(directory).expanduser()

            if not directory.exists():
                print(f"{directory} Path does not exist.")

            elif not directory.is_dir():
                print(f"{directory} Is not a directory.")

            else:
                break
    else:
        directory = default_directory
        directory = Path(directory).expanduser()

    return directory

def scan_files() -> list[Pdf]:

    files = [Pdf(str(file), file.name, file.stem)
             for file in get_directory_path().iterdir()
             if file.is_file() and file.suffix.lower() == ".pdf"]
    
    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files

def get_files_to_include(files: list[Pdf]) -> list[Pdf]:
    chosen_files = []
    for file in files:
        while True:
            ans = input(f"Would you like to incude {file.name_w_ext}? (y/n): ")
            if ans.lower().strip() in ("yes", "y"):
                chosen_files.append(file)
                break
            elif ans.lower().strip() in ("no", "n"):
                break
            else:
                print("Invalid answer, please input 'y' or 'n'")
                
    return chosen_files

def extract_pdf_text(chosen_files: list[Pdf]) -> None:
    laparams = LAParams(line_overlap=0.5, char_margin=100.0, line_margin=0.5, word_margin=0.1)

    for file in chosen_files:
        lines = extract_text(file.path, laparams=laparams).split("\n")
        for line in lines:
            file.text.append(line)
    
if __name__ == "__main__":
    chosen_files = get_files_to_include(scan_files())
    extract_pdf_text(chosen_files)
    for file in chosen_files:
        print(f"{file.name}___ %%%%%%%%%%%%%___{file.text}")

