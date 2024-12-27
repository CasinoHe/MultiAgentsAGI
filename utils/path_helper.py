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


def ensure_ext() -> None:
    """
    Check if the ext module (autogen-ext) is installed. If not, install it.
    """
    ext_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "lib", "autogen", "python", "packages", "autogen-ext")
    )
    try:
        __import__("autogen_ext")
    except ImportError:
        print("Installing autogen-ext...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", ext_path])


def ensure_all() -> None:
    """
    Ensure all the modules are installed
    """
    ensure_core()
    ensure_agentchat()
    ensure_ext()
