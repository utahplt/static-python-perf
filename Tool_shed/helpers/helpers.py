import os


def get_files(filepath) -> list[str]:
    dir_files = []
    exclude = [".git", ".venv"]
    for root, dirs, files in os.walk(filepath, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            dir_files.append(os.path.join(root, file))

    return dir_files

