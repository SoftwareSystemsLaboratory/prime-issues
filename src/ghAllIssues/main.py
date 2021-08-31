from argparse import ArgumentParser, Namespace

from ghAllIssues.libs.ghAllIssues import getGHIssues
from ghAllIssues.libs.graph import main as graphMain


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program generates an interval tree from a JSON file containing a GitHub repositories issues.",
    )
    parser.add_argument(
        "-r",
        "--repository",
        help='GitHub repository to be used. Format needs to be "OWNER/REPO". Default is numpy/numpy',
        default="numpy/numpy",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file. EX: --save-json=issues.json",
        default="issues.json",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-t",
        "--token",
        help="GitHub personal access token",
        type=str,
        required=True,
    )

    return parser.parse_args()


def main() -> None:
    args: Namespace = get_argparse()

    print(
        getGHIssues(
            repo=args.repository,
            token=args.token,
            filename=args.save_json,
        )
    )

    graphMain(jsonFile=args.save_json)


if __name__ == "__main__":
    main()
