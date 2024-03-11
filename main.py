import argparse
import os
import importlib


COMMAND_DESCRIPTION = """Run Multi-Agents AGI

    example:
        python main.py --run_type test --filename test_two_agents  # run the test_two_agents.py under the test folder
"""


def init_autogen_environment():
    from utils import path_helper
    path_helper.add_third_party_libraries_to_sys_path()


def test(**kwargs):
    """
    Starting test under the test directory simply by running the script directly
    """
    # parse the arguments, and give the example of how to use the script
    parser = argparse.ArgumentParser(description=COMMAND_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--filename", type=str, default="", help="The filename of the test script under the test folder, for example: test_two_agents")

    args_list = sum([[f"--{k}", v] for k, v in kwargs.items()], [])
    # parse the arguments from kwargs
    args, unknown = parser.parse_known_args(args_list)

    filename = args.filename
    # print help msg
    if not filename:
        parser.print_help()
        return 0

    # strip the ".py" extension and space
    filename = filename.strip().replace(".py", "")
    # check the existence of the file
    if not os.path.exists(f"test/{filename}.py"):
        raise FileNotFoundError(f"File not found: test/{filename}.py")

    # load module from test folder, and run the module
    importlib.import_module(f".{filename}", package="test")
    return 0


def dry_run(**kwargs):
    """
    Placeholder, not implemented yet
    """
    print("Dry run is not implemented yet")


VALIDATE_MODULE = {
    "test": test,
    "dry_run": dry_run,
}


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)

    # Add the first argument for run type
    parser.add_argument("-t", "--run_type", choices=["test", "dry_run"], help="Type of run (test or dry_run)")

    # Parse the arguments
    args, unknown = parser.parse_known_args()

    # The run type is stored in args.run_type
    run_type = args.run_type

    # Validate the run type
    if run_type not in VALIDATE_MODULE:
        raise ValueError(f"Invalid run type: {run_type}")

    # Convert unknown arguments to kwargs (assuming they are in the format: --key value)
    kwargs = {}
    for i in range(0, len(unknown), 2):
        key = unknown[i].lstrip("-")
        value = unknown[i + 1] if i + 1 < len(unknown) else None
        kwargs[key] = value

    # init autogen environment
    init_autogen_environment()

    # Call the function with the kwargs
    return VALIDATE_MODULE[run_type](**kwargs)


if __name__ == "__main__":
    main()
