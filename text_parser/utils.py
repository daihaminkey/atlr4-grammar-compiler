import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def clear_dir(path: Path, ignore_absence: bool = True) -> None:
    if path.exists():
        print(f'Очистка директории {path}...')
        for file in path.glob('*'):
            if file.is_dir():
                shutil.rmtree(file)
            else:
                file.unlink()
    elif not ignore_absence:
        raise FileNotFoundError


def delete_files_by_patterns(dir_path: Path, *patterns: str) -> None:
    for pattern in patterns:
        for file in dir_path.glob(pattern):
            os.remove(str(file))


def run(command: str, stdin=None, timeout: Optional[int] = 5) -> None:
    subprocess.check_call(command, shell=True, timeout=timeout, stdin=stdin)


def calculate_hash(path: Path) -> str:
    file_hash = hashlib.md5()
    with path.open() as file_to_hash:
        file_hash.update(file_to_hash.read().encode('utf-8'))
    return file_hash.hexdigest()
