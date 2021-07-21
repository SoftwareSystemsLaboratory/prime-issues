from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load, dumps
from math import ceil

from os.path import isfile

import dateutil.utils
from dateutil.parser import parse
from intervaltree import IntervalTree
from progress.bar import PixelBar
from requests import get
from requests.models import Response


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
        "-l",
        "--limit",
        help='The numeric limit of how many issues to get. Default is "all"',
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
    limit: int,
    filename: str,
) -> int:

    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Metrics-Dashboard",
        "Authorization": f"token {token}",
    }
    urlTemplate: str = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=asc&per_page=100&page={}"
    data = []

    requestIterations: int = ceil(limit / 100)

    with PixelBar(f"Getting issues from {repo}... ", max=requestIterations) as bar:
        for iteration in range(requestIterations + 1):
            if iteration != 0:
                html: Response = get(
                    url=urlTemplate.format(repo, iteration), headers=requestHeaders
                )
                data += html.json()
                bar.next()

    if storeJSON(json=data, filename=filename):
        return len(data)
    return -1


def storeJSON(json: list, filename: str = "issues.json") -> bool:
    data: str = dumps(json)
    with open(file=filename, mode="w") as jsonFile:
        jsonFile.write(data)
    return isfile(filename)


def loadJSON(filename: str = "issues.json") -> list:
    with open(file=filename, mode="r") as jsonFile:
        return load(jsonFile)


def createIntervalTree(data: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()
    day0: datetime = parse(data[0]["createdAt"]).replace(tzinfo=None)
    today: datetime = dateutil.utils.today().replace(tzinfo=None)

    for issue in data:
        createdDate: datetime = parse(issue["createdAt"]).replace(tzinfo=None)

        if issue["state"] == "CLOSED":
            closedDate: datetime = parse(issue["closedAt"]).replace(tzinfo=None)
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
        limit=args.limit,
        token=args.token,
        filename=args.save_json,
    )

    issues: list = loadJSON(filename=args.save_json)

    tree: IntervalTree = createIntervalTree(data=issues)

    print(len(tree))
