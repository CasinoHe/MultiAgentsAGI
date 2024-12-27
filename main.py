import argparse
import os
import sys
import importlib
from utils import path_helper


TEST_COMMAND = "test"
SETUP_COMMAND = "setup"


class ArgParser(object):
    def __init__(self, args):
        self.args = args

        self.parser = argparse.ArgumentParser(description="Run Multi-Agents AGI",
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.subparser = self.parser.add_subparsers(dest="Commands", help="Run specific commands")

        self.add_test_subparser()
        self.add_setup_subparser()

    def add_test_subparser(self):
        parser = self.subparser.add_parser(TEST_COMMAND, help=f"example: python main.py {TEST_COMMAND} --filename two_agents")
        parser.add_argument("-f", "--filename", type=str, required=True, help="The filename of the test script under the test folder, for example: two_agents")
        parser.add_argument("--without_autogen_ext", action="store_true", default=False, help="Run the test without autogen-ext")
        parser.add_argument("--without_openai", action="store_true", default=False, help="Run the test without OpenAI API")
        parser.add_argument("--openai_key", type=str, default="", help="OpenAI API key")

    def add_setup_subparser(self):
        parser = self.subparser.add_parser(SETUP_COMMAND, help="Set up individual modules for AutoGen")
        parser.add_argument("--without_core", action="store_true", default=False, help="Ensure autogen-core is installed")
        parser.add_argument("--without_agentchat", action="store_true", default=False, help="Ensure autogen-agentchat is installed")
        parser.add_argument("--without_ext", action="store_true", default=False, help="Ensure autogen-ext is installed")

    def __call__(self, *args, **kwds):
        args = self.parser.parse_args(self.args, **kwds)
        return args


def install_autogen_environment(args):
    path_helper.ensure_core()
    path_helper.ensure_agentchat()

    if not args.without_autogen_ext:
        path_helper.ensure_ext()


def setup_modules(args):
    if not args.without_core:
        path_helper.ensure_core()
    if not args.without_agentchat:
        path_helper.ensure_agentchat()
    if not args.without_ext:
        path_helper.ensure_ext()


def test(args):
    """
    Starting test under the test directory simply by running the script directly
    """
    filename = args.filename

    # strip the ".py" extension and space
    filename = filename.strip().replace(".py", "")
    # check the existence of the file
    if not os.path.exists(f"test/{filename}.py"):
        raise FileNotFoundError(f"File not found: test/{filename}.py")

    if args.openai_key:
        os.environ["OPENAI_API_KEY"] = args.openai_key

    # load module from test folder, and run the module
    importlib.import_module(f".{filename}", package="test")
    return True


def main():
    parser = ArgParser(args=sys.argv[1:])
    args = parser()

    if args.Commands == "test":
        install_autogen_environment(args)
        test(args)
    elif args.Commands == "setup":
        setup_modules(args)
    else:
        parser.parser.print_help()

    sys.exit(0)


if __name__ == "__main__":
    main()
