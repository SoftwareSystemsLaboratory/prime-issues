from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load
from subprocess import call

from dateutil.parser import parse
from intervaltree import IntervalTree


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
        "-o",
        "--order",
        help='The chronological order of which issues are gotten. Supported values are either "asc" or "desc". Default is asc',
        default="asc",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-s",
        "--state",
        help='The state in which an issue is in. Supported values are either "open", "closed", or "all". Default is all',
        default="all",
        type=str,
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
    order: str,
    state: str,
    filename: str,
) -> int:
    if repo == "":
        command: str = f'gh issue list --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-{order}"> {filename}'
    else:
        command: str = f'gh issue list --repo {repo} --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-{order}" > {filename}'

    return call(command, shell=True)


def loadJSON(filename: str = "issues.json") -> list:
    with open(file=filename, mode="r") as json:
        return load(json)


def createIntervalTree(data: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()
    day0: datetime = parse(data[0]["createdAt"])

    for issue in data:
        createdDate: datetime = parse(issue["createdAt"])

        if issue["state"] == "CLOSED":
            closedDate: datetime = parse(issue["closedAt"])
        else:
            closedDate: datetime = parse(datetime.today())

        begin: int = (createdDate - day0).days
        end: int = (closedDate - day0).days

        tree.addi(begin=begin, end=end, data=issue)

    return tree
