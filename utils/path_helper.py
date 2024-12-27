"""
Ensure third-party libraries are installed and added to sys.path
"""

import os
import sys
import subprocess


def ensure_core() -> None:
    """
    Check if the core module (autogen-core) is installed. If not, install it.
    """
    core_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "lib", "autogen", "python", "packages", "autogen-core")
    )
    try:
        __import__("autogen_core")
    except ImportError:
        print("Installing autogen-core...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", core_path])


def ensure_agentchat() -> None:
    """
    Check if the agentchat module (autogen-agentchat) is installed. If not, install it.
    """
    agentchat_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "lib", "autogen", "python", "packages", "autogen-agentchat")
    )
    try:
        __import__("autogen_agentchat")
    except ImportError:
        print("Installing autogen-agentchat...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", agentchat_path])


def ensure_ext(submodules=None) -> None:
    """
    Check if the ext module (autogen-ext) is installed. If not, install it along with optional submodules.

    :param submodules: List of optional submodules to install (e.g., ["openai", "langchain"]).
    """
    ext_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "lib", "autogen", "python", "packages", "autogen-ext")
    )
    try:
        __import__("autogen_ext")
    except ImportError:
        print("Installing autogen-ext...")
        if submodules:
            extras = ",".join(submodules)
            install_command = f"pip install -e '{ext_path}[{extras}]'"
        else:
            install_command = f"pip install -e '{ext_path}'"
        subprocess.check_call([sys.executable, "-m"] + install_command.split())


def ensure_all(submodules=None) -> None:
    """
    Ensure all the modules are installed, including optional submodules for autogen-ext.

    :param submodules: List of optional submodules to install for autogen-ext.
    """
    ensure_core()
    ensure_agentchat()
    ensure_ext(submodules=submodules)
