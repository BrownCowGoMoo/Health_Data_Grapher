import os
import sys

def get_files_from_dir() -> list[tuple[str]]:

    while True:

        directory = input("Input the directory path to your files")

        if not os.path.exists(directory):
            print(f"{directory} Path does not exist.")

        elif not os.path.isdir(directory):
            print(f"{directory} Is not a directory.")

        else:
            break

    files = [(file, os.path.splitext(file)[0])
             for file in os.listdir(directory)
             if os.path.isfile(file) and os.path.splitext(file)[1] == ".pdf"]
    
    if not files:
        sys.exit("There are no .pdf files within the directory.")

    return files
    