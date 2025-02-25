import tempfile
from typing import Literal
import requests
import os
import sys
from pathlib import Path
import subprocess
import logging

from turboml_installer.colab import install_from_file_on_colab

logger = logging.getLogger("turboml_installer")

COLAB_INSTALLER_SCRIPT = "https://turbo-ml.com/turboml-0.1-Linux-x86_64.sh"

DEPS = [
    "python=3.11",
    "conda-forge::libstdcxx-ng",
    "conda-forge::protobuf",
    "conda-forge::libtorch",
    "conda-forge::pytorch",
    "conda-forge::torchvision",
    "conda-forge::torchaudio",
    "conda-forge::ncurses",
]


class InstallerError(Exception):
    pass


def install_on_colab(setup_env_only: bool = False):
    """
    Install TurboML along with all of its dependencies on Google Colab.

    Parameters
    ----------
    setup_env_only
        setup environment only and skip turboml-sdk installation
    """
    with tempfile.NamedTemporaryFile(
        prefix="turboml-installer", suffix=".sh", delete=True
    ) as tf:
        with requests.get(COLAB_INSTALLER_SCRIPT, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                tf.write(chunk)
        tf.flush()
        install_from_file_on_colab(Path(tf.name), setup_env_only)


def install(setup_only: bool = False):
    if not is_linux_x86_64():
        raise InstallerError("TurboML is only supported on Linux x86-64 at the moment.")

    if is_colab():
        logger.info("Running on Google Colab. Installing TurboML...")
        install_on_colab(setup_env_only=setup_only)
        return

    try:
        check_x_installed("pixi")
        logger.info("Pixi is installed. Using Pixi to install TurboML.")
        return install_with_pixi(setup_only=setup_only)
    except InstallerError:
        pass

    try:
        check_x_installed("conda")
        logger.info("Conda is installed. Using Conda to install TurboML.")
        return install_with_conda(setup_only=setup_only)
    except InstallerError:
        pass

    raise InstallerError(
        "No supported package manager found. Please install conda or pixi."
    )


def is_colab():
    try:
        import google.colab

        return True
    except ImportError:
        return False


def is_linux_x86_64():
    """
    Check if the system is running on Linux x86-64 architecture.
    Returns:
        bool: True if the system is Linux x86-64, False otherwise.
    """
    import platform

    system = platform.system()  # Get the OS name (e.g., 'Linux', 'Windows', 'Darwin')
    machine = (
        platform.machine()
    )  # Get the machine architecture (e.g., 'x86_64', 'arm64')

    return system == "Linux" and machine == "x86_64"


def install_with_conda(*, setup_only: bool = False):
    """
    Setup dependencies and optionally install turboml-sdk with conda
    """
    setup_with_x(x="conda", setup_only=setup_only)


def install_with_pixi(*, setup_only: bool = False):
    """
    Setup dependencies and optionally install turboml-sdk with Pixi + uv
    """
    setup_with_x(x="pixi", setup_only=setup_only)


def check_x_installed(x: Literal["conda", "pixi", "uv"]):
    """
    Check if x is installed and available in the system.
    Raises an exception if x is not found.
    """
    logger.debug(f"Checking if `{x}` is installed...")
    try:
        subprocess.run(
            [x, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise InstallerError(
            f"{x} is not installed or not found in your system. "
            f"Please install {x} and ensure it is in your PATH."
        )


def setup_with_x(*, x: Literal["conda", "pixi"], setup_only: bool = False):
    """
    Setup dependencies and optionally install turboml-sdk.

    Args:
        setup_only (bool): If True, only install the dependencies. If False, also install turboml-sdk.
    """
    if not os.environ.get("CONDA_PREFIX"):
        raise InstallerError(
            "TurboML Installer must be run in a conda/pixi environment."
        )

    conda_install = None
    match x:
        case "conda":
            conda_install = ["conda", "install", "-qq", "--no-pin", "-y"]
        case "pixi":
            conda_install = ["pixi", "add"]

    pip_install = None
    match x:
        case "conda":
            pip_install = ["pip", "install"]
        case "pixi":
            pip_install = ["uv", "pip", "install"]

    try:
        # Check if x is installed
        check_x_installed(x)

        # Install dependencies using x
        logger.info("Installing dependencies...")
        for dep in DEPS:
            logger.info(f"Installing {dep}...")
            subprocess.run(conda_install + [dep], check=True)

        if x == "pixi":
            try:
                check_x_installed("uv")
            except InstallerError:
                # Must install uv - pixi alone fails to resolve turboml-bindings for linux-64 for some reason
                logger.info("Missing uv. Installing uv...")
                subprocess.run(conda_install + ["uv"], check=True)

        # Optionally install turboml-sdk
        if not setup_only:
            logger.info("Installing turboml-sdk...")
            subprocess.run(pip_install + ["turboml-sdk"], check=True)

        logger.info("Setup completed successfully.")

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running a command: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
