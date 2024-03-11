"""
add third-party libraries to sys.path
"""

import sys
import os


def add_third_party_libraries_to_sys_path() -> None:
    root_dir = os.path.dirname(__file__)  # Use dirname instead of basename
    autogen_dir = os.path.abspath(os.path.join(root_dir, "..", "lib", "autogen"))

    try:
        # Find the index of autogen_dir in sys.path
        index = sys.path.index(autogen_dir)
        if index != 0:
            # Move autogen_dir to the beginning if it's not already there
            sys.path.insert(0, sys.path.pop(index))
    except ValueError:
        # Insert at the beginning if autogen_dir is not in sys.path
        sys.path.insert(0, autogen_dir)

    return None
