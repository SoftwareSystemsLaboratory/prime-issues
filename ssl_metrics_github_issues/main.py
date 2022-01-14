from argparse import ArgumentParser, Namespace
from datetime import datetime

import pandas

from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict

from dateutil.parser import parse as dateParse

from common import storeJSON


def getArguements() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GitHub API Client",
        usage="Tool to access specific GitHub endpoints to extract data to be piped into other ssl-metrics applicaitons.",
        description="",
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

    return parser.parse_args()


def getIssueResponse(repo: str, token: str, page: int = 1) -> Response:
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }

    apiURL: str = f"https://api.github.com/repos/{repo}/issues?state=all&sort=created&direction=asc&per_page=100&page={page}"

    return get(url=apiURL, headers=requestHeaders)


def getLastPageOfResponse(response: Response) -> int:
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


def extractDataFromPair(pair: dict, pullRequests: bool, day0: datetime) ->  dict:
    data: dict = {}

    data["number"] = pair["number"]
    data["created_at"] = pair["created_at"]
    data["closed_at"] = pair["closed_at"]
    data["dayOpened"] = (dateParse(pair["created_at"]) - day0).days

    # possible error here
    data["dayClosed"] = (dateParse(pair["closed_at"]) - day0).days

    isPullRequest: bool = testIfPullRequest(dictionary=pair)

    if pullRequests:
        return data
    elif (pullRequests == False) and isPullRequest:
        return None
    else:
        return data

def iterateAPI(
    repo: str,
    token: str,
    pullRequests: bool = False,
) -> DataFrame:

    columnNames: list = ["number", "created_at", "closed_at"]
    df: DataFrame = DataFrame(columns=columnNames)

    print(f"Getting the first page of issues from {repo}")

    response: Response = getIssueResponse(repo, token, page=1)
    numberOfPagesOfIssues: int = getLastPageOfResponse(response)

    if pullRequests is False:
        message: str = (
            f"Removing pull request issues and then storing issue data from {repo}... "
        )
    else:
        message: str = f"Storing issue data from {repo}... "

    with Bar(message, max=numberOfPagesOfIssues):
        json: dict = response.json()

        print(json[0]["created_at"])
        input()
        day0: datetime = dateParse(json[0]["created_at"])

        index: int
        for index in range(len(json)):
            df = df.append(extractDataFromPair(json[index], pullRequests, day0), ignore_index=True)

        df.to_json("test.json")
        print(numberOfPagesOfIssues)
        quit()


    for index in range(len(json)):
        if testIfPullRequest(json[index]) is False:
            data: dict = {}

            data["number"] = json[index]["number"]
            data["openedSinceDay0"] = json[index]["created_at"]
            data["closedSinceDay0"] = json[index]["created_at"]

            df = df.append(data, ignore_index=True)
            print(df)
            quit()

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
                        data: dict = {}
                        if pullRequests is False:
                            if testIfPullRequest(json[index]) is False:
                                data = {
                                    "number": json[index]["number"],
                                    "createdAt": json[index]["created_at"],
                                    "closedAt": json[index]["closed_at"],
                                }
                        else:
                            data = {
                                "number": json[index]["number"],
                                "createdAt": json[index]["created_at"],
                                "closedAt": json[index]["closed_at"],
                            }
                        df.append(data, ignore_index=True)

                    bar.next()
    return df


def testIfPullRequest(dictionary: dict) -> bool:
    try:
        dictionary["pull_request"]
        return True
    except KeyError:
        return False


def main() -> None:
    args: Namespace = getArguements()

    issues: list = iterateAPI(
        repo=args.repository,
        token=args.token,
        pullRequests=args.pull_request,
    )

    print(issues)
    quit()
    storeJSON(
        json=issues,
        filename=args.save_json[0],
    )


if __name__ == "__main__":
    main()
