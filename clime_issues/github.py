import logging
import re
from argparse import Namespace
from datetime import datetime

from dateutil.parser import parse as dateParse
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict

from clime_issues.args import githubArgs
from clime_issues.version import version

def getIssueResponse(repo: str, token: str, page: int = 1) -> Response:
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }

    apiURL: str = f"https://api.github.com/repos/{repo}/issues?state=all&sort=created&direction=asc&per_page=100&page={page}"

    logging.debug(f"API endpoint URL: {apiURL}")
    return get(url=apiURL, headers=requestHeaders)


def getPageCount(response: Response) -> int:
    headers: CaseInsensitiveDict = response.headers
    try:
        lastPageString: str = headers["Link"].split(",")[-1].split("&")[4]
        pageCount: int = int(re.search(r"\d+", lastPageString).group())
    except KeyError:
        pageCount: int = 1
    logging.info(f"Number of pages of issues: {pageCount}")
    return pageCount


def iterateAPI(repo: str, token: str) -> list:
    logging.debug("Starting to iterate through issue pages...\n")
    with Bar("Determining number of pages of issues...", max=100) as bar:
        logging.info("Iteration 0")
        resp: Response = getIssueResponse(repo, token, page=1)
        pageCount: int = getPageCount(resp)
        json: list = resp.json()
        logging.debug(f"JSON data:\n{json}")
        bar.message = "Downloading GitHub issues..."
        bar.max = pageCount
        bar.update()
        logging.info("Finished iteration 0\n")
        bar.next()

        for page in range(2, pageCount + 1):
            logging.info(f"Iteration {page}")
            resp: Response = getIssueResponse(repo, token, page)
            json.extend(resp.json())
            logging.info(f"Finished iteration {page}\n")
            bar.next()

    return json


def computeValues(data: list) -> list | None:
    try:
        day0: datetime = dateParse(data[0]["created_at"]).replace(tzinfo=None)
    except IndexError:
        logging.error(f"Invalid JSON formatting. Potentially no JSON data.\n{data}")
        quit(1)
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
    args: Namespace = githubArgs()

    if args.version:
        print(f"clime-gh-issues-collect version {version()}")
        quit(0)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=args.log,
        filemode="a",
        format="%(process)d-%(asctime)s-%(levelname)s: %(message)s",
    )
    logging.info("Started logging...")

    raw: list = iterateAPI(repo=args.repository, token=args.token)
    data: list = computeValues(raw)

    if args.pull_request == False:
        data = [x for x in data if x.get("pull_request") is None]

    df: DataFrame = DataFrame(data)
    df.T.to_json(args.output)


if __name__ == "__main__":
    main()
