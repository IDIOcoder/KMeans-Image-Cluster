#!/usr/bin/env python3

from utils import core
import os
import subprocess
import sys
from utils import core


def setup_virtual_environment():
    """Automatically set up a virtual environment and install requirements."""
    venv_dir = ".venv"
    requirements_file = "requirements.txt"

    # Step 1: Check if virtual environment exists, if not, create it
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

    # Step 2: Install requirements if they are not installed
    pip_executable = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts",
                                                                                               "pip")
    print(f"Using pip: {pip_executable}")

    # Upgrade pip and install dependencies
    subprocess.check_call([pip_executable, "install", "--upgrade", "pip"])
    if os.path.exists(requirements_file):
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call([pip_executable, "install", "-r", requirements_file])
    else:
        print("requirements.txt not found, skipping dependencies installation.")


if __name__ == '__main__':
    core.run()
