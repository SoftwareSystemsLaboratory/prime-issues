from argparse import ArgumentParser, Namespace
from json import dumps
from os import sep
from os.path import exists

from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program downloads all issue related data from a GitHub repository",
    )
    parser.add_argument(
        "--comments",
        help="Download the comments of all GitHub issues",
        action="store_true",
        default=False,
        required=False,
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
        "--timeline",
        help="Download the timelines of all GitHub issues",
        action="store_true",
        default=False,
        required=False,
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

    print(f"Getting {repo}'s first issue response to determine iteration amount... '")

    html: Response = get(url=urlTemplate.format(repo, 1), headers=requestHeaders)

    requestIterations: int = getLastPage(response=html)

    json: dict = html.json()
    for index in range(len(json)):
        if testIfPullRequest(json[index]) is False:
            data.append(json[index])

    if pullRequests is False:
        barStr: str = f"Removing pull requests from {repo}... "
    else:
        barStr: str = f"Storing JSON issue data from {repo}... "
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


def getGHIssueComments(
    data: list,
    repo: str,
    token: str,
) -> list:

    # data: list = []
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }

    urls: data = [
        x["comments_url"] + "?&sort=created&direction=asc&per_page=100" for x in data
    ]

    url: str
    for url in urls:
        issueNumber: int = url.split(sep="/")[7]
        print(f"Getting {repo}'s {issueNumber} issue first page of comments response to determine iteration amount... '")

        html: Response = get(url=url, headers=requestHeaders)

        requestIterations: int = getLastPage(response=html)

    json: dict = html.json()
    for index in range(len(json)):
        data.append(json[index])

    barMax: int = requestIterations
    with Bar(f"Downloading remaining comments for issue {issueNumber} in {repo}", max=barMax) as bar:
        bar.next()

        if requestIterations != 1:
            for iteration in range(requestIterations + 1):

                if iteration > 1:
                    apiCall: str = url + f"&page={iteration}"
                    html: Response = get(url=apiCall, headers=requestHeaders)

                    json: dict = html.json()
                    for index in range(len(json)):
                        data.append(json[index])
                    bar.next()
    return data


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


def storeJSON(json: list, filename: str = "issues.json") -> bool:
    data: str = dumps(json)
    with open(file=filename, mode="w") as jsonFile:
        jsonFile.write(data)
    return exists(filename)


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

    if args.comments:
        comments: list = getGHIssueComments(data=issues, repo=args.repository, token=args.token,)
        storeJSON(json=comments, filename="comments.json",)


if __name__ == "__main__":
    main()
