"""pydev utils"""

import os
import sys
import tomli
import subprocess

from pathlib import Path

from functools import lru_cache


def get_python():
    """
    Python executable path for sub commands

    Return:
        Python executable where the package is installed.
        This could be changed to use the python from
        the system path or a virtual env.
    """
    return sys.executable


@lru_cache
def get_project_root(strict=False):
    """Walk up to find pyproject.toml"""

    cwd = Path.cwd()

    for path in cwd, *cwd.parents:
        if path.joinpath("pyproject.toml").exists():
            return path

    if strict:
        raise FileNotFoundError("pyproject.toml")


def run_command(command, echo=True, strict=False, chgdir=True):
    """Run shell command"""

    if echo:
        print(command)

    cwd = None
    if chgdir:
        cwd = get_project_root()
        if cwd is None:
            print("pyproject.toml file not found!")
            exit(1)

    rc = subprocess.run(command, cwd=cwd, shell=True)

    if strict and rc != 0:
        raise RuntimeError("Command failed!")


@lru_cache
def load_config():
    """Load pyproject.toml file"""

    pyproject = Path("pyproject.toml").resolve(strict=True)

    with pyproject.open("rb") as f:
        return tomli.load(f)


def get_config(item: str, default=None):
    """Query pyproject.toml file"""

    data = load_config()

    for i in item.split("."):
        data = data.get(i, None)
        if data is None:
            return default

    return data


def search_path(pattern: str, path=None):
    """Search items in path"""

    if path is None:
        path = os.getenv("PATH")
    if isinstance(path, str):
        path = path.split(os.pathsep)
    if isinstance(path, os.PathLike):
        path = [path]

    for p in path:
        p = Path(p)
        yield from p.glob(pattern)


def system_python(version=None):
    """Python in the system path"""
    if not version:
        version = "3"

    path = os.getenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin")
    path = path.split(os.pathsep)

    pattern = "python" + version
    items = [i for p in path for i in Path(p).glob(pattern)]

    return next(items, None)


def pyenv_versions():
    """pyenv versions"""

    pyenv_root = os.getenv("PYENV_ROOT", "~/.pyenv")
    pyenv_root = Path(pyenv_root).expanduser()

    return pyenv_root.glob("versions/*")


def pyenv_python(version: str = None) -> Path:
    """pyenv binary for version prefix"""

    if not version:
        version = "3.*"
    elif version.count(".") < 2:
        version += ".*"

    pyenv_root = os.getenv("PYENV_ROOT", "~/.pyenv")
    pyenv_root = Path(pyenv_root).expanduser()

    if not pyenv_root.exists():
        return None

    pattern = f"versions/{version}/bin/python"

    return next(pyenv_root.glob(pattern), None)


def conda_envs():
    """conda environments"""

    conda_root = os.getenv("CONDA_PREFIX", "~/miniconda3")
    conda_root = Path(conda_root).expanduser()

    return [p for p in conda_root.glob("envs/*") if p.joinpath("bin/python").exists()]


def conda_python(name: str = None) -> Path:
    """conda binary for named env"""

    conda_root = os.getenv("CONDA_PREFIX", "~/miniconda3")
    conda_root = Path(conda_root).expanduser()

    if name:
        conda_env = conda_root.joinpath(f"envs/{name}")
    else:
        conda_env = conda_root

    if conda_env.exists():
        return conda_env.joinpath("bin/python")


def which_python(version=None, target=None):
    """Locate python matching version/target"""
    if target == "pyenv":
        return pyenv_python(version)

    if target == "conda":
        return conda_python(version)

    if target in ("system", None):
        return system_python(version)


def confirm_choice(message, default: bool = None):
    prompt = f"{message} (yes/no):"

    while True:
        user_input = input(prompt)
        if user_input.lower() in ("y", "yes"):
            return True
        if user_input.lower() in ("n", "no"):
            return False
        if user_input == "" and default is not None:
            return default
