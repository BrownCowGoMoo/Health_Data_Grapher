
import sys
from pathlib import Path

def get_files_from_dir() -> list[tuple[str, str]]:
    """
    Gets all pdf files from the given directory and returning the name with and without the extension.

    Returns:
        files: A list of tuples where each tuple contains the name with and without the extension.
            tuple[0] = name with extension
            tuple[1] = name without extension
    """

    while True:

        directory = input("Input the directory path to your files: ")
        directory = Path(directory).expanduser()

        if not directory.exists():
            print(f"{directory} Path does not exist.")

        elif not directory.is_dir():
            print(f"{directory} Is not a directory.")

        else:
            break

    files = [(file.name, file.stem)
             for file in directory.iterdir()
             if file.is_file() and file.suffix.lower() == ".pdf"]
    
    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files
    