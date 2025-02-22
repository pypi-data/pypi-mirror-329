import argparse
import os
import sys

from cf_remote import log
from cfengine_cli import version
from cfengine_cli import commands
from cfengine_cli.utils import UserError


def print_version_info():
    print("CFEngine CLI version %s" % version.string())


def _get_arg_parser():
    ap = argparse.ArgumentParser(
        description="Human-oriented CLI for interacting with CFEngine tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    ap.add_argument(
        "--log-level",
        help="Specify level of logging: DEBUG, INFO, WARNING, ERROR, or CRITICAL",
        type=str,
        default="WARNING",
    )
    ap.add_argument(
        "--version",
        "-V",
        help="Print or specify version",
        nargs="?",
        type=str,
        const=True,
    )

    command_help_hint = (
        "Commands (use %s COMMAND --help to get more info)"
        % os.path.basename(sys.argv[0])
    )
    subp = ap.add_subparsers(dest="command", title=command_help_hint)

    subp.add_parser("help", help="Print help information")

    subp.add_parser(
        "run", help="Run the CFEngine agent, fetching, evaluating, and enforcing policy"
    )

    subp.add_parser(
        "report",
        help="Run the agent and hub commands necessary to get new reporting data",
    )

    return ap


def get_args():
    ap = _get_arg_parser()
    args = ap.parse_args()
    return args


def run_command_with_args(command, _) -> int:
    if command == "run":
        return commands.run()
    if command == "report":
        return commands.report()
    if command == "help":
        return commands.help()
    raise UserError("Unknown command: '{}'".format(command))


def validate_command(_command, _args):
    pass


def main():
    try:
        args = get_args()
        if args.log_level:
            log.set_level(args.log_level)
        validate_command(args.command, args)

        exit_code = run_command_with_args(args.command, args)
        assert type(exit_code) is int
        sys.exit(exit_code)
    except AssertionError as e:
        print(f"Error: {str(e)} (programmer error, please file a bug)")
        sys.exit(-1)
    except UserError as e:
        print(str(e))
        sys.exit(-1)


if __name__ == "__main__":
    main()
