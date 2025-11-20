import os

def read_files_in_folder(folder_path, allowed_extensions={'.txt', '.md'}):
    """
    Reads all text or markdown files in the given folder and returns a
    dictionary mapping filenames to their contents.

    :param folder_path: Path to the folder to read files from.
    :param allowed_extensions: Set of file extensions to include.
    :return: Dict of {filename: file_contents}
    """
    files_data = {}
    for filename in os.listdir(folder_path):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in allowed_extensions:
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_data[filename] = f.read()
            except Exception as e:
                # Could add logging here instead of print in real code
                print(f"Could not read {file_path}: {e}")
    return files_data
