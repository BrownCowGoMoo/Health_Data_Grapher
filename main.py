from files import scan_files, Pdf
from typing import List

def main():
    files: List[Pdf] = scan_files()
    for file in files:
        print(file.name)

if __name__ == "__main__":
    main()