"""The main entry point for the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from inspect import cleandoc

##############################################################################
# Local imports.
from . import __version__
from .hike import Hike


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The arguments.
    """

    # Build the parser.
    parser = ArgumentParser(
        prog="Hike",
        description="Hike - A Markdown browser for the terminal",
        epilog=f"v{__version__}",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    # Add --license
    parser.add_argument(
        "--license",
        "--licence",
        help="Show license information",
        action="store_true",
    )

    # The remainder is going to be the initial command.
    parser.add_argument(
        "command",
        help=("The initial command; " "can be any valid input to Hike's command line."),
        nargs="*",
    )

    # Finally, parse the command line.
    return parser.parse_args()


##############################################################################
def main() -> None:
    """The main entry point."""
    if (args := get_args()).license:
        print(cleandoc(Hike.HELP_LICENSE))
    else:
        Hike(args).run()


##############################################################################
if __name__ == "__main__":
    main()


### __main__.py ends here
