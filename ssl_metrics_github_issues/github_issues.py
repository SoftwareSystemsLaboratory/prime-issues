from argparse import ArgumentParser, Namespace
from json import dumps
from os.path import exists

from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program generates an interval tree from a JSON file containing a GitHub repositories issues.",
    )

    parser.add_argument("-p", "--pull-requests", help="Flag to include pull requests in output json file", action="store_true", default=False, required=False,)
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
    filename: str,
    pullRequests: bool = False
) -> int:

    data: list = []
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }
    urlTemplate: str = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=asc&per_page=100&page={}"

    print(f"Getting {repo}'s first issue response to determine iteration amount... '")

    html: Response = get(url=urlTemplate.format(repo, 1), headers=requestHeaders)

    requestIterations: int = getLastPage(response=html)

    json: dict = html.json()
    for index in range(len(json)):
        if testIfPullRequest(json[index]) is False:
            data.append(json[index])

    barMax: int = requestIterations

    with Bar(f"Removing pull requests from {repo}... ", max=barMax) as bar:
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

    if storeJSON(json=data, filename=filename):
        return len(data)
    return 1


def getLastPage(response: Response) -> int:
    responseHeaders: CaseInsensitiveDict = response.headers
    try:
        links: str = responseHeaders["Link"]
    except KeyError:
        return 1

    linksSplit: list = links.split(",")
    lastLink: str = linksSplit[1]

    lastPageIndex: int = lastLink.find("&page=") + 6
    lastPageRightCaretIndex: int = lastLink.find(">;")

    return int(lastLink[lastPageIndex:lastPageRightCaretIndex])


def testIfPullRequest(dictionary: dict) -> bool:
    try:
        dictionary["pull_request"]
        return True
    except KeyError:
        return False


def storeJSON(json: list, filename: str = "issues.json") -> bool:
    data: str = dumps(json)
    with open(file=filename, mode="w") as jsonFile:
        jsonFile.write(data)
    return exists(filename)


def main() -> None:
    args: Namespace = get_argparse()

    getGHIssues(
        repo=args.repository,
        token=args.token,
        filename=args.save_json,
        pullRequests=args.pull_requests
    )


if __name__ == "__main__":
    main()
