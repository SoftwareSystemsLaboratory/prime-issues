from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import dumps, load
from math import ceil
from os.path import exists

import dateutil.utils
from dateutil.parser import parse
from intervaltree import IntervalTree
from progress.bar import PixelBar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program generates an interval tree from a JSON file containing a GitHub repositories issues.",
    )
    parser.add_argument(
        "-r",
        "--repository",
        help='GitHub repository to be used. Format needs to be "OWNER/REPO". Default is numpy/numpy',
        default="numpy/numpy",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-p",
        "--page-limit",
        help='The numeric limit of pages of issues to get. Default is "all"',
        default="all",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-t",
        "--token",
        help="GitHub personal access token",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--save-json",
        help="Save analysis to JSON file. EX: --save-json=issues.json",
        default="issues.json",
        type=str,
        required=True,
    )
    return parser


def getGHIssues(
    repo: str,
    token: str,
    pages: str,
    filename: str,
) -> int:
    SKIP_CALL: bool = False

    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }
    urlTemplate: str = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=asc&per_page=100&page={}"
    data: list = []

    if pages == "all":
        SKIP_CALL = 1

        print(
            f"Getting {repo}'s first issue response to determine iteration amount... '"
        )

        html: Response = get(url=urlTemplate.format(repo, 1), headers=requestHeaders)

        requestIterations: int = getLastPage(response=html)
        data += html.json()

    else:
        requestIterations: int = ceil(int(pages) / 100)

    pixelBarMax: int = requestIterations

    if requestIterations < 2:
        requestIterations = 2

    with PixelBar(
        f"Getting issues from {repo}... ", max=pixelBarMax - SKIP_CALL
    ) as bar:

        badPages: int = 0
        if SKIP_CALL:
            badPages += 1
            bar.next()

        for iteration in range(requestIterations):
            apiCall: str = urlTemplate.format(repo, iteration)

            if iteration > badPages:
                html: Response = get(url=apiCall, headers=requestHeaders)
                data += html.json()
                bar.next()

    if storeJSON(json=data, filename=filename):
        return len(data)
    return -1


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


def loadJSON(filename: str = "issues.json") -> list:
    with open(file=filename, mode="r") as jsonFile:
        return load(jsonFile)


def createIntervalTree(data: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()

    day0: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)
    today: datetime = dateutil.utils.today().replace(tzinfo=None)

    for issue in data:
        createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)

        if issue["state"] == "closed":
            closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
        else:
            closedDate: datetime = today

        begin: int = (createdDate - day0).days
        end: int = (closedDate - day0).days

        try:
            tree.addi(begin=begin, end=end, data=issue)
        except ValueError:
            issue["endDayOffset"] = 1
            tree.addi(begin=begin, end=end + 1, data=issue)

    return tree


if __name__ == "__main__":
    args: Namespace = get_argparse().parse_args()

    getGHIssues(
        repo=args.repository,
        pages=args.page_limit,
        token=args.token,
        filename=args.save_json,
    )

    issues: list = loadJSON(filename=args.save_json)

    tree: IntervalTree = createIntervalTree(data=issues)

    print(len(tree))
