from argparse import Namespace, ArgumentParser


def getArguements() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GitHub API Client",
        usage="Tool to access specific GitHub endpoints to extract data to be piped into other ssl-metrics applicaitons.",
        description="",
    )
    subparser = parser.add_subparsers()

    parser.add_argument(
        "-r",
        "--repository",
        help="GitHub formatted as repository owner/repository",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="File to save JSON response(s) to",
        type=str,
        required=True,
        nargs=1,
    )
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub personal access token",
        type=str,
        required=True,
    )

    issuesParser: ArgumentParser = subparser.add_parser(
        "issues",
        prog="",
        usage=False,
        description="",
    )
    issuesParser.add_argument(
        "-p",
        "--pull-request",
        help="Flag to enable the collection of pull requests with the other data",
        type=bool,
        required=False,
        default=False,
    )

    # issueCommentsParser: ArgumentParser = subparser.add_parser(
    #     "comments",
    #     title="",
    #     description="",
    #     required=False,
    #     help="",
    # )
    # issueTimelineParser: ArgumentParser = subparser.add_parser(
    #     "timeline",
    #     title="",
    #     description="",
    #     required=False,
    #     help="",
    # )
    return parser.parse_args()

from pprint import pprint as print
print(getArguements().__dict__)
