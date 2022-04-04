from argparse import ArgumentParser, Namespace

name: str = "CLIME"
authors: list = [
    "Nicholas M. Synovic",
    "Jake Palmer",
    "Rohan Sethi" "George K. Thiruvathukal",
]


def mainArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} GitHub Issues Downloader",
        description="A tool to download all issues from a GitHub hosted repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-p",
        "--pull-request",
        help="Flag to enable the collection of pull requests with the other data",
        required=False,
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r",
        "--repository",
        help="GitHub formatted as repository owner/repository",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="File to save JSON response(s) to",
        type=str,
        required=False,
        default="github_issues.json",
    )
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub personal access token",
        type=str,
        required=True,
    )

    return parser.parse_args()


def graphArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Git Commit LOC Exploder Grapher",
        description=f"A tool for graphing LOC information from the output of the {name} Commit LOC Exploder",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name} Git Commit Exploder. DEFAULT: ./commits_loc.json",
        type=str,
        required=False,
        default="commits_loc.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./commits_loc.pdf",
        type=str,
        required=False,
        default="commits_loc.pdf",
    )
    parser.add_argument(
        "-x",
        help="Key of the x values to use for graphing. DEFAULT: author_days_since_0",
        type=str,
        required=False,
        default="author_days_since_0",
    )
    parser.add_argument(
        "-y",
        help="Key of the y values to use for graphing. DEFAULT: lines_of_code",
        type=str,
        required=False,
        default="lines_of_code",
    )
    parser.add_argument(
        "--y-thousandths",
        help="Flag to divide the y values by 1000",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot. DEFAULT: line",
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help='Title of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--x-label",
        help='X axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--y-label",
        help='Y axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--stylesheet",
        help="Filepath of matplotlib stylesheet to use. DEFAULT: style.mplstyle. NOTE: This is an internal stylesheet used by the program and doesn't need to be specified/ created by you the user (you)",
        type=str,
        required=False,
        default="style.mplstyle",
    )

    return parser.parse_args()
