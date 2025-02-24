import argparse
import pathlib
import shutil


def clean(folder: pathlib.Path):
    full_path = "runs" / folder
    shutil.rmtree(full_path)
    print(f"{full_path} removed.")


def UseCLI():
    """clean cli"""

    def main():
        parser = argparse.ArgumentParser("Cleaner for pointcnn")
        parser.add_argument("folder", type=pathlib.Path)
        args = parser.parse_args()
        clean(args.folder)

    return main
