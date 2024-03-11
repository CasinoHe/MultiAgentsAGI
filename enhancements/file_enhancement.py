"""
Enhancements for AIGC agents
Agents can use these tools to read and write files and directories.
"""
import os
from typing import Annotated
from autogen import ConversableAgent  # type: ignore


def read_file(file_path: Annotated[str,
                                   "The absolute or relative path to the file."
                                   ]
              ):
    """
    Reads a file and returns the contents.
    """
    resolved_path = os.path.abspath(os.path.normpath(file_path))
    with open(resolved_path, "r") as f:
        return f.read()


def read_directory_contents(directory_path: Annotated[str,
                                                      "The absolute or relative path to the directory. NOTE: By default the current working directory for this function is {WORK_DIR}."
                                                      ],
                            ):
    """
    Reads the contents of a directory and returns the contents (i.e. the file names).
    """
    resolved_path = os.path.abspath(os.path.normpath(directory_path))
    return os.listdir(resolved_path)


def read_multiple_files(file_paths: Annotated[str,
                                              "A list of absolute or relative paths to the files. "]
                        ):
    """
    Reads multiple files and returns the contents.
    """
    resolved_paths = [os.path.abspath(os.path.normpath(file_path)) for file_path in file_paths]
    file_contents = []
    for resolved_path in resolved_paths:
        with open(resolved_path, "r") as f:
            file_contents.append(f.read())
    return file_contents


def save_file(file_path: Annotated[str,
                                   "The absolute or relative path to the file."],
              file_contents: Annotated[str,
                                       "The contents of the file to be saved."]
              ):
    """
    Saves a file to disk.
    """
    resolved_path = os.path.abspath(os.path.normpath(file_path))
    # Throw error if file already exists
    if os.path.exists(resolved_path):
        raise Exception(f"File already exists at {resolved_path}.")

    # Create directory if it doesn't exist
    directory = os.path.dirname(resolved_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(resolved_path, "w") as f:
        f.write(file_contents)

    return f"File saved to {resolved_path}."


def save_multiple_files(file_paths: Annotated[str,
                                              "A list of absolute or relative paths to the files."],
                        file_contents: Annotated[str,
                                                 "A list of the contents of the files to be saved."]
                        ):
    """
    Saves multiple files to disk.
    """
    resolved_paths = [os.path.abspath(os.path.normpath(file_path)) for file_path in file_paths]
    # Throw error if file already exists
    for resolved_path in resolved_paths:
        if os.path.exists(resolved_path):
            raise Exception(f"File already exists at {resolved_path}.")

    for i, resolved_path in enumerate(resolved_paths):
        # Create directory if it doesn't exist
        directory = os.path.dirname(resolved_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(resolved_path, "w") as f:
            f.write(file_contents[i])

    return f"Files saved to {resolved_paths}."


def ehance_agent_with_file_tools(caller: ConversableAgent, executor: ConversableAgent = None):
    """
    Enhances an agent with file tools.
    """

    if caller is None:
        return False

    # file read enhancement
    f = caller.register_for_llm(description=read_file.__doc__)(read_file)
    if executor:
        executor.register_for_execution()(f)

    # directory read enhancement
    f = caller.register_for_llm(description=read_directory_contents.__doc__)(read_directory_contents)
    if executor:
        executor.register_for_execution()(f)

    # multiple file read enhancement
    f = caller.register_for_llm(description=read_multiple_files.__doc__)(read_multiple_files)
    if executor:
        executor.register_for_execution()(f)

    # file write enhancement
    f = caller.register_for_llm(description=save_file.__doc__)(save_file)
    if executor:
        executor.register_for_execution()(f)

    # multiple file write enhancement
    f = caller.register_for_llm(description=save_multiple_files.__doc__)(save_multiple_files)
    if executor:
        executor.register_for_execution()(f)

    return True
