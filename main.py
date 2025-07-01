from files import get_files_from_dir, Pdf
from typing import List

def main():
    files: List[Pdf] = get_files_from_dir()
    for file in files:
        print(file.name)

if __name__ == "__main__":
    main()