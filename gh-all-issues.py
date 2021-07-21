from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load
from subprocess import call

import dateutil.utils
from dateutil.parser import parse
from intervaltree import IntervalTree
from progress.spinner import MoonSpinner


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
        help="The limit of how many issues to get. Default is 100",
        default=100,
        type=int,
        required=False,
    )

    parser.add_argument(
        "--save-json",
        help="Save analysis to JSON file (EX: --save-json=output.json)",
        type=str,
        required=True,
    )
    return parser


def getGHIssues(
    repo: str,
    limit: int,
    state: str,
    filename: str,
) -> int:

    if repo == "":
        command: str = f'gh issue list --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-asc"> {filename}'
    else:
        command: str = f'gh issue list --repo {repo} --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-asc" > {filename}'

    print(f"Getting the first {limit} issues for {repo}... ")
    return call(command, shell=True)


def loadJSON(filename: str = "issues.json") -> list:
    with open(file=filename, mode="r") as json:
        return load(json)


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
        order=args.order,
        state=args.state,
        filename=args.save_json,
    )

    issues: list = loadJSON(filename=args.save_json)

    tree: IntervalTree = createIntervalTree(data=issues)

    print(len(tree))
