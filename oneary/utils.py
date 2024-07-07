from argparse import Namespace
from pathlib import Path
from pkg_resources import get_distribution
from os import environ
from shutil import which, rmtree
from subprocess import getoutput, getstatusoutput
from typing import Union
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT

from . import logger


def get_data_dir() -> Path:
    """Get path to data directory

    Returns:
        Path: Path to data directory
    """

    home_env = environ.get("Oneary_HOME")
    if home_env:
        return Path(home_env)

    xdg_config = environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config) / "oneary"

    return Path.home() / ".config/oneary"


def get_version() -> str:
    """Get current version of Oneary

    Returns:
        str: Oneary version
    """

    if Path(".git").exists():
        return f'{get_distribution(__package__).version}-{getoutput("git rev-parse --abbrev-ref HEAD")}-{getoutput("git rev-parse --short HEAD")}'
    else:
        return get_distribution(__package__).version


def run(command: str, args: Namespace) -> None:
    """Run a command

    Args:
        command (str): Command to run
        args (Namespace): Args namespace
    """

    if "|" in command:
        name = command.split("|")[-1].replace(" ", "")
    else:
        name = command.split()[0]

    if "/" in name:
        name = name.split("/")[-1]

    print(f"Running {name}")
    logger.debug(f"Running command: {command}", args.debug)
    status, output = getstatusoutput(command)
    if status != 0:
        logger.error(f"An error occurred when running {name}: {output}")
        exit(1)


def erase_dir(path: Path) -> None:
    """Delete a directory then mkdir it

    Args:
        path (Path): Directory path
    """

    rmtree(path, ignore_errors=True)
    path.mkdir()
