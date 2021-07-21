from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load
from subprocess import call

from dateutil.parser import parse
from intervaltree import IntervalTree

def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Git All Python (CLI Only)",
        usage="This program outputs the lines of code (LOC) per commit and the delta LOC of a Git repository in JSON format.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containing repository root folder (.git)",
        default=".",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="Default branch for analysis to be ran on",
        default="main",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file (EX: --save-json=output.json)",
        type=str,
        required=True,
    )
    return parser

def getGHIssues(
    repo: str = "",
    limit: int = 10000,
    state: str = "all",
    filename: str = "issues.json",
) -> int:
    if repo == "":
        command: str = f'gh issue list --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-asc"> {filename}'
    else:
        command: str = f'gh issue list --repo {repo} --json "closedAt,createdAt,id,number,state" --limit {limit} --state {state} --search "sort:created-asc" > {filename}'

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

if __name__ == "__main__":
