from argparse import ArgumentParser, Namespace
from datetime import datetime

from dateutil.parser import parse as dateParse
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict

from ssl_metrics_github_issues.args import mainArgs


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


def extractDataFromPair(pair: dict, pullRequests: bool, day0: datetime) -> dict:
    data: dict = {}
    day0: datetime = day0.replace(tzinfo=None)
    data["state"] = pair["state"]
    data["number"] = pair["number"]
    data["title"] = pair["title"]
    data["description"] = pair["body"]

    data["created_at"] = pair["created_at"]
    data["closed_at"] = pair["closed_at"]
    data["day_opened"] = (
        dateParse(pair["created_at"]).replace(tzinfo=None) - day0
    ).days
    data["created_at_short"] = (
        dateParse(pair["created_at"]).replace(tzinfo=None).strftime("%Y-%m-%d")
    )

    try:
        data["closed_at_short"] = (
            dateParse(pair["closed_at"]).replace(tzinfo=None).strftime("%Y-%m-%d")
        )
    except TypeError:
        data["closed_at_short"] = (
            datetime.now().replace(tzinfo=None).strftime("%Y-%m-%d")
        )

    try:
        dayClosed: int = (dateParse(pair["closed_at"]).replace(tzinfo=None) - day0).days
    except TypeError:
        dayClosed: int = (datetime.now().replace(tzinfo=None) - day0).days

    data["day_closed"] = dayClosed

    isPullRequest: bool = testIfPullRequest(dictionary=pair)
    data["pull_request"] = isPullRequest

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

    columnNames: list = [
        "number",
        "created_at",
        "closed_at",
        "created_at_short",
        "closed_at_short",
        "day_opened",
        "day_closed",
        "pull_request",
        "state,",
    ]
    df: DataFrame = DataFrame(columns=columnNames)

    response: Response = getIssueResponse(repo, token, page=1)
    numberOfPagesOfIssues: int = getLastPageOfResponse(response)

    if pullRequests is False:
        message: str = (
            f"Removing pull request issues and then storing issue data from {repo}... "
        )
    else:
        message: str = f"Storing issue data from {repo}... "

    with Bar(message, max=numberOfPagesOfIssues) as bar:
        json: dict = response.json()

        day0: datetime = dateParse(json[0]["created_at"])

        index: int
        for index in range(len(json)):
                        df.loc[len(df.index)] = extractDataFromPair(json[index], pullRequests, day0)

        for page in range(numberOfPagesOfIssues):
            if page == 1:
                pass

            response: Response = getIssueResponse(repo, token, page)
            json = response.json()

            index: int
            for index in range(len(json)):
                            df.loc[len(df.index)] = extractDataFromPair(json[index], pullRequests, day0)
            bar.next()

    return df


def testIfPullRequest(dictionary: dict) -> bool:
    try:
        dictionary["pull_request"]
        return True
    except KeyError:
        return False


def main() -> None:
    args: Namespace = mainArgs()

    issues: DataFrame = iterateAPI(
        repo=args.repository,
        token=args.token,
        pullRequests=args.pull_request,
    )

    issues.T.to_json(args.output)
    print(args.output)

if __name__ == "__main__":
    main()
