from pathlib import Path
import subprocess
import argparse
from create_random_file import create_random_file


def create_folder_structure(num_folders: int, random_file_size_mb: int) -> None:
    for i in range(1, num_folders + 1):
        package_name = f"pkg_{i}"
        path = Path(package_name)
        src_path = path / package_name
        random_file_name = f"random_file_{i}.bin"

        # create pgk_{i}/pkg_{i}
        src_path.mkdir(exist_ok=True, parents=True)

        # create pgk_{i}/pkg_{i}/__init__.py
        (src_path / "__init__.py").touch()

        # Create hello.py
        (src_path / "hello.py").write_text(
            f"""import numpy as np
def say_hello():
    print('Hello from pkg_{i}')
    np.random.rand()
"""
        )

        # Create pyproject.toml
        (path / "pyproject.toml").write_text(
            f"""[tool.poetry]
name = "{package_name}"
version = "0.1.0"
description = ""
authors = ["Jonathan Rayner <jonathan.j.rayner@gmail.com>"]
packages = [{{ include = "{package_name}"}}]
include = [{{ path = "{random_file_name}"}}]
            
[tool.poetry.dependencies]
python = "^3.10 <3.13"
numpy = "^1.21.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
        )

        # Create random file
        create_random_file(path=path / random_file_name, size_mb=random_file_size_mb)


def run_poetry_lock(num_folders: int) -> None:
    for i in range(1, num_folders + 1):
        folder_name = f"pkg_{i}"
        src_path = Path(folder_name)
        print(f"Running 'poetry lock' for {folder_name}")
        try:
            subprocess.run(["poetry", "lock"], cwd=src_path, check=True)
            print(f"Successfully ran 'poetry lock' for {folder_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error running 'poetry lock' for {folder_name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Create folder structure and run poetry lock"
    )
    parser.add_argument(
        "-n", "--num_folders", type=int, help="Number of folders to create"
    )
    parser.add_argument(
        "-s", "--size", default=50, type=int, help="Size of the file in MB"
    )
    args = parser.parse_args()

    create_folder_structure(
        num_folders=args.num_folders,
        random_file_size_mb=args.size,
    )
    print(f"Folder structure created successfully for {args.num_folders} folders.")
    run_poetry_lock(args.num_folders)
    print("Finished running 'poetry lock' for all packages.")


if __name__ == "__main__":
    main()
