from argparse import ArgumentParser
from sys import exit

from . import oneary, utils, logger


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="shows debug info, useful for testing",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Oneary v{utils.get_version()}",
        help="show current version and exit",
    )
    args = parser.parse_args()

    oa = oneary.Oneary(args)
    try:
        oa.main()
    except KeyboardInterrupt:
        logger.error("Interrupted")
        exit(1)


if __name__ == "__main__":
    main()
