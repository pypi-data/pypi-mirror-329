# config.py
import logging
import shutil
import subprocess
import sys
from importlib import resources
from importlib.metadata import version as poetry_version
from pathlib import Path

import requests
import typer
from packaging import version

from stratio.config import Config


# Set up a logger for the CLI.
def get_logger() -> logging.Logger:
    """Set up a module–level logger."""
    logger = logging.getLogger("StratioCLI")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARN)
        # Set boto3 and botocore loggers to WARNING level
        logging.getLogger("boto3").setLevel(logging.WARNING)
        logging.getLogger("botocore").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
    return logger


logger = get_logger()
_config = None


def load_config(config_path: str) -> Config:
    """
    Load the configuration from the specified YAML file.
    """
    try:
        config = Config.load_from_file(config_path)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise typer.Exit(1) from e


# ─── VERSIONING AND UPDATE ────────────────────────────────────────────────────────────

__version__ = poetry_version("aws-marketplace-toolkit")


def check_for_updates():
    pypi_url = "https://pypi.org/pypi/aws-marketplace-toolkit/json"
    response = requests.get(pypi_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    latest_version = data["info"]["version"]
    if version.parse(latest_version) > version.parse(__version__):
        print(f"\nA new version ({latest_version}) is available (you have {__version__}).")
        answer = input("Would you like to update now? [Y/n] ").strip().lower()
        if answer in ("", "y", "yes"):
            print("Updating aws-marketplace-toolkit (pip install --upgrade aws-marketplace-toolkit)...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "aws-marketplace-toolkit"])
            print("\nUpdate installed successfully. Please restart the CLI to use the updated version.")
            sys.exit(0)


def copy_default_config_if_missing():
    """
    Check if the default configuration file exists in ~/.marketplace.
    If not, copy the bundled config_default.yaml from the package resources.
    """
    dest_dir = Path.home() / ".marketplace"
    config_dest = dest_dir / "config_default.yaml"
    if not config_dest.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        try:
            # Access the config_default.yaml file within the stratio.cli package.
            # Ensure that your package’s structure includes the config_default.yaml file in the correct location.
            with resources.open_binary("stratio.cli", "config_default.yaml") as src_file, open(
                config_dest, "wb"
            ) as dst_file:
                shutil.copyfileobj(src_file, dst_file)
            print(f"Default configuration copied to {config_dest}")
        except Exception as e:
            raise RuntimeError(f"Could not copy default configuration: {e}") from e


def get_current_version():
    return __version__
