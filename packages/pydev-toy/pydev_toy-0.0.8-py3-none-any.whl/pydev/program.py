"""pydev program"""

import re
import json
import click
import shutil
import logging

from urllib import request
from urllib.error import HTTPError

from . import utils
from . import messages

logger = logging.getLogger()


@click.group(chain=True)
def main():
    pass


@main.command
def info():
    """Project info including pypi versions"""
    name = utils.get_config("project.name")
    version = utils.get_config("project.version")
    project_root = utils.get_project_root()
    print("name", name)
    print("version", version)
    print("location", project_root)
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = list(data["releases"])
        print("pypi.releases", releases)
    except HTTPError:
        pass


@main.command
def clean():
    """Delete build and dist folders"""
    project_root = utils.get_project_root(strict=True)
    folders = "build", "dist"

    for folder in folders:
        path = project_root.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
@click.option("-y", "--yes", is_flag=True)
def prune(yes):
    """Delete all runtime folders"""
    project_root = utils.get_project_root(strict=True)
    folders = "build", "dist", ".venv", ".nox", ".tox"

    folders = [f for f in folders if project_root.joinpath(f).exists()]

    confirm = yes or utils.confirm_choice(
        f"Do you want to delete runtime folders {folders}"
    )
    if not confirm:
        exit(1)

    for folder in folders:
        path = project_root.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
def bump():
    """Bump static version in pyproject.toml"""
    project_root = utils.get_project_root()
    pyproject = project_root.joinpath("pyproject.toml").resolve(strict=True)
    buffer = pyproject.read_text()
    pattern = r"^version \s* = \s* \"(.+)\" \s*"
    match = re.search(pattern, buffer, flags=re.VERBOSE | re.MULTILINE)
    if not match:
        raise ValueError("Could not find version setting")
    version = tuple(int(i) for i in match.group(1).split("."))
    version = version[:-1] + (version[-1] + 1,)
    version = ".".join(str(v) for v in version)
    print(f"Updating version to {version} ...")
    output = re.sub(
        pattern, f'version = "{version}"\n', buffer, flags=re.VERBOSE | re.MULTILINE
    )
    pyproject.write_text(output)


@main.command
def build():
    """Build project wheel"""
    python = utils.get_python()
    project_root = utils.get_project_root()
    if project_root.joinpath("setup.py").exists():
        target = "sdist"
    else:
        target = "wheel"
    utils.run_command(f"{python} -m build --{target}")


@main.command
def dump():
    """Dump wheel and sdist contents"""
    project_root = utils.get_project_root()
    dist = project_root.joinpath("dist")

    for file in dist.glob("*.whl"):
        utils.run_command(f"unzip -l {file}")

    for file in dist.glob("*.tar.gz"):
        utils.run_command(f"tar -ztvf {file}")


@main.command
@click.option("-t", "--test-pypi", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def publish(test_pypi=False, verbose=False):
    """Publish project with twine"""

    if not utils.get_config("tool.pydev.allow-publish"):
        print(messages.ALLOW_PUBLISH)
        exit(1)

    python = utils.get_python()

    flags = ""
    if test_pypi:
        flags += " --repository testpypi"
    if verbose:
        flags += " --verbose"

    command = f"{python} -mtwine upload {flags} dist/*"

    utils.run_command(command)
