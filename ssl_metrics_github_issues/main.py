import re
from argparse import Namespace
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


def getPageCount(response: Response) -> int:
    headers: CaseInsensitiveDict = response.headers
    try:
        lastPageString: str = headers["Link"].split(",")[-1].split("&")[4]
    except KeyError:
        return 1
    return int(re.search(r"\d+", lastPageString).group())


def iterateAPI(repo: str, token: str) -> list:
    with Bar("Determining number of pages of issues...", max=100) as bar:
        resp: Response = getIssueResponse(repo, token, page=1)
        pageCount: int = getPageCount(resp)
        json: list = resp.json()

        bar.message = "Downloading GitHub issues..."
        bar.max = pageCount
        bar.update()
        bar.next()

        for page in range(2, pageCount + 1):
            resp: Response = getIssueResponse(repo, token, page)
            json.extend(resp.json())
            bar.next()

    return json


def computeValues(data: list) -> list:
    day0: datetime = dateParse(data[0]["created_at"]).replace(tzinfo=None)

    x: dict
    for x in data:
        x["opened_day_since_0"] = (
            dateParse(x["created_at"]).replace(tzinfo=None) - day0
        ).days
        try:
            x["closed_day_since_0"] = (
                dateParse(x["closed_at"]).replace(tzinfo=None) - day0
            ).days
        except TypeError:
            x["closed_day_since_0"] = (datetime.now().replace(tzinfo=None) - day0).days

    return data


def main() -> None:
    args: Namespace = mainArgs()

    raw: list = iterateAPI(repo=args.repository, token=args.token)
    data: list = computeValues(raw)

    if args.pull_request == False:
        data = [x for x in data if x.get("pull_request") is None]

    df: DataFrame = DataFrame(data)
    df.T.to_json(args.output)


if __name__ == "__main__":
    main()
