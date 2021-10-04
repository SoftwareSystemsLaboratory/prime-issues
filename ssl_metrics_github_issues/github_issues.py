from argparse import ArgumentParser, Namespace

from libs.common import getLastPage, storeJSON
from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program downloads all issue related data from a GitHub repository",
    )
    parser.add_argument(
        "-p",
        "--pull-requests",
        help="Flag to include pull requests in output json file",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "-r",
        "--repository",
        help='GitHub repository to be used. NOTE: Format needs to be "OWNER/REPO". DEFAULT: numpy/numpy',
        default="numpy/numpy",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file",
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


def getGHIssues(
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
    args: Namespace = get_argparse()

    issues: list = getGHIssues(
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
