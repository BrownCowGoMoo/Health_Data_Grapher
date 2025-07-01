from pathlib import Path
import sys
from dataclasses import dataclass, field
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

@dataclass
class Pdf:
    """
    Dataclass to hold pdf file information.

    Attributes:
        path: str = path to the file
        name_w_ext: str = file name with extension
        name: str = file name without extension
        text: list[str] = A list containg each line of text in the file
    """
    path: str 
    name_w_ext: str
    name: str
    text: list[str] = field(default_factory=list)

def get_directory_path(default_directory="C:\Coding Projects\Python\health data") -> str:
    """
    Gets the path to the directory containing the pdf files from user if there is not default path.

    Args:
        default_direcrtory: str = A default path to a directory.

    Returns:
        directory: [str] = String representing a directory path containing the pdf files.
    """
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
    """
    Creates a list of Pdf objects for each pdf file in the directory.
    Exits if there are no pdf files in the directory.

    Returns:
        files: list[Pdf] = A list of pdf objects representing the pdf files in the directory.
    """

    files = [Pdf(str(file), file.name, file.stem)
             for file in get_directory_path().iterdir()
             if file.is_file() and file.suffix.lower() == ".pdf"]
    
    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files

def get_files_to_include(files: list[Pdf]) -> list[Pdf]:
    """
    Prompts the user to as which files they want included.

    Args:
        files: list[Pdf] = List of Pdf objects

    Retuns:
        chosen_files: list[Pdf] = List of chosen Pdf files
    """
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
    """
    Extracts text from the pdf and adds each line as an item to the text list of its object.

    Args:
        chosen_files: list[Pdf] = List of pdf objects
    """
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

