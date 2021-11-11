from argparse import Namespace, ArgumentParser
from requests import Response, get
from progress.bar import Bar
from libs.common import getLastPage, storeJSON


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
        usage="Access the GitHub issues of a repository via the GitHub Issues REST API",
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

def getGitHubIssues(
    repo: str,
    token: str,
    pullRequests: bool = False,
) -> int:

    data: list = []
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }
    urlTemplate: str = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=asc&per_page=100&page={}"

    html: Response = get(url=urlTemplate.format(repo, 1), headers=requestHeaders)

    requestIterations: int = getLastPage(response=html)

    json: dict = html.json()
    for index in range(len(json)):
        if testIfPullRequest(json[index]) is False:
            data.append(json[index])

    if pullRequests is False:
        barStr: str = (
            f"Removing pull request issues and then storing issue data from {repo}... "
        )
    else:
        barStr: str = f"Storing issue data from {repo}... "

    barMax: int = requestIterations
    with Bar(barStr, max=barMax) as bar:
        bar.next()

        if requestIterations != 1:
            for iteration in range(requestIterations + 1):

                if iteration > 1:
                    apiCall: str = urlTemplate.format(repo, iteration)
                    html: Response = get(url=apiCall, headers=requestHeaders)

                    json: dict = html.json()
                    for index in range(len(json)):
                        if pullRequests is False:
                            if testIfPullRequest(json[index]) is False:
                                data.append(json[index])
                        else:
                            data.append(json[index])

                    bar.next()
    return data


def testIfPullRequest(dictionary: dict) -> bool:
    try:
        dictionary["pull_request"]
        return True
    except KeyError:
        return False


def main() -> None:
    args: Namespace = getArguements()

    issues: list = getGitHubIssues(
        repo=args.repository,
        token=args.token,
        pullRequests=args.pull_requests,
    )

    storeJSON(
        json=issues,
        filename=args.save_json,
    )


if __name__ == "__main__":
    main()
