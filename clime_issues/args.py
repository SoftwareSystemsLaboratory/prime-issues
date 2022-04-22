from argparse import ArgumentParser, Namespace

name: str = "CLIME"
authors: list = [
    "Nicholas M. Synovic",
    "Jake Palmer",
    "Rohan Sethi",
    "George K. Thiruvathukal",
]


def bugzillaArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Bugzilla Issues Downloader (BETA)",
        description="A tool to download all issues from a Bugzilla hosted issue tracker",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-u",
        "--url",
        help="Bugzilla repository root url. DEFAULT: https://bugzilla.kernal.org. NOTE: Structure the URL exactly like the DEFAULT or else this will not work.",
        type=str,
        required=True,
        default="https://bugzilla.kernal.org",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="CSV file of exported Bugzilla bugs. DEFAULT: ./bugzilla_issues.csv",
        type=str,
        required=False,
        default="bugzilla_issues.csv",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="File to save JSON response(s) to. DEFAULT: ./bugzilla_issues.json",
        type=str,
        required=False,
        default="bugzilla_issues.json",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def githubArgs() -> Namespace:
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
        help="File to save JSON response(s) to. DEFAULT: ./github_issues.json",
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
    parser.add_argument(
        "--log",
        help="File to store logs in. DEFAULT: github_issues.log",
        type=str,
        required=False,
        default="github_issues.log",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def gitlabArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Gitlab Issues Downloader",
        description="A tool to download all issues from a Gitlab hosted repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-r",
        "--repository",
        help="Gitlab repository ID",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="File to save JSON response(s) to. DEFAULT: ./gitlab_issues.json",
        type=str,
        required=False,
        default="gitlab_issues.json",
    )
    parser.add_argument(
        "-t",
        "--token",
        help="Gitlab personal access token",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--log",
        help="File to store logs in. DEFAULT: gitlab_issues.log",
        type=str,
        required=False,
        default="gitlab_issues.log",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def graphArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} GitHub Issues Grapher",
        description=f"A tool for graphing GitHub issue information from the output of the {name} GitHub Issues Downloader",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name} GitHub Issues Downloader. DEFAULT: ./github_issues.json",
        type=str,
        required=False,
        default="github_issues.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./github_issues.pdf",
        type=str,
        required=False,
        default="github_issues.pdf",
    )
    parser.add_argument(
        "-x",
        help="Key of the x values to use for graphing. DEFAULT: opened_day_since_0",
        type=str,
        required=False,
        default="opened_day_since_0",
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
        help='Filepath of matplotlib stylesheet to use. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )
    return parser.parse_args()
