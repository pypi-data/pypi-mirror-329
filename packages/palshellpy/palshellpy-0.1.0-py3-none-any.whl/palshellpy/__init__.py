__version__ = "0.1.0"

import os
import pathlib
import subprocess
import tarfile
import hashlib
import uuid
from os import PathLike
from typing import Union


def get_user_home_dir():
    return subprocess.getoutput('echo $HOME').strip()


def get_tmp_dir() -> pathlib.Path:
    if os.name == 'posix':
        return pathlib.Path('/tmp/')
    else:
        raise NotImplemented


def get_random_str_v1():
    return uuid.uuid4().hex

def sha256sum_file(file_path: Union[str | PathLike]) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def sha256sum_data(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def make_tar(relative_to: Union[str|PathLike], files: list, tar_file_path: Union[str | PathLike]) -> pathlib.Path:
    with tarfile.open(tar_file_path, "w") as tar:
        for f in files:
            if pathlib.Path(relative_to).joinpath(f).exists():
                tar.add(pathlib.Path(relative_to).joinpath(f), arcname=f)
    return pathlib.Path(tar_file_path)


def extract_tar(tar_file: Union[str|PathLike], to_dir: Union[str|PathLike]) -> pathlib.Path:
    with tarfile.open(tar_file) as tar:
        tar.extractall(to_dir)
    return pathlib.Path(to_dir)


def confirm_file_parent_dir_exists(file_path: Union[str|PathLike]):
    file_path = pathlib.Path(file_path)
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def confirm_dir_exists(dir_path: Union[str|PathLike]):
    dir_path = pathlib.Path(dir_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


