from files import get_files_from_dir

def main():
    file_name_wEXT, file_name = zip(*get_files_from_dir())
    print(file_name_wEXT)
    print(file_name)


if __name__ == "__main__":
    main()