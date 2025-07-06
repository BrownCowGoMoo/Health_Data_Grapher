from pathlib import Path
import sys

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def get_directory_path(default_directory=".") -> str:
    """
    Gets the path to the directory containing the pdf files from user if there is not default path.

    Args:
        default_direcrtory: A default path to a directory.

    Returns:
        directory: String representing a directory path containing the pdf files.
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
        directory = Path(default_directory).expanduser()

    return directory

def scan_files() -> list[dict]:
    """
    Creates a list of dicts for each pdf file in the directory.
    Exits if there are no pdf files in the directory.

    Returns:
        files: A list of dicts representing the pdf files.
            Each dict has keys: path, name_w_ext, name, text.
    """
    directory = get_directory_path()
    files = []
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() == ".pdf":
            files.append({
                "path": str(file),
                "name_w_ext": file.name,
                "name": file.stem,
                "text": []
            })

    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files

def get_files_to_include(files: list[dict]) -> list[dict]:
    """
    Prompts the user to ask which files they want included.

    Args:
        files: List of file-dicts

    Returns:
        chosen_files: list of file-dicts representing chosen files
    """
    chosen_files = []
    for f in files:
        while True:
            ans = input(f"Would you like to include {f['name_w_ext']}? (y/n): ")
            if ans.lower().strip() in ("yes", "y"):
                chosen_files.append(f)
                break
            elif ans.lower().strip() in ("no", "n"):
                break
            else:
                print("Invalid answer, please input 'y' or 'n'")

    return chosen_files

def extract_pdf_text(chosen_files: list[dict]) -> None:
    """
    Extracts text from the pdf and appends each line to the file dict's text list.

    Args:
        chosen_files: List of file-dicts
    """
    laparams = LAParams(line_overlap=0.5,
                        char_margin=100.0,
                        line_margin=0.5,
                        word_margin=0.1)

    for f in chosen_files:
        raw = extract_text(f["path"], laparams=laparams)
        f["text"] = raw.splitlines()


