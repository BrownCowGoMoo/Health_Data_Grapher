
import sys
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Pdf:
    path: str
    name_w_ext: str
    name: str

def get_directory_path() -> str:
    while True:

        directory = input("Input the directory path to your files: ")
        directory = Path(directory).expanduser()

        if not directory.exists():
            print(f"{directory} Path does not exist.")

        elif not directory.is_dir():
            print(f"{directory} Is not a directory.")

        else:
            break

    return directory

def scan_files() -> list[Pdf]:

    files = [Pdf(str(file), file.name, file.stem)
             for file in get_directory_path().iterdir()
             if file.is_file() and file.suffix.lower() == ".pdf"]
    
    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files

def get_files_to_include(files: list[Pdf]) -> list[str]:
    chosen_files = []
    for file in files:
        while True:
            ans = input(f"Would you like to incude {file.name_w_ext}? (y/n): ")
            


    

if __name__ == "__main__":
    print(scan_files())
