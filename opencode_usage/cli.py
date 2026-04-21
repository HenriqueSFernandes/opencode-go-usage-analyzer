import argparse

from .app import logout, run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show OpenCode workspace usage.")
    parser.add_argument(
        "--no-remember",
        action="store_true",
        help="Do not read or write local session credentials.",
    )
    parser.add_argument(
        "--logout",
        action="store_true",
        help="Delete the saved local session and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.logout:
        logout()
    else:
        run(remember=not args.no_remember)
