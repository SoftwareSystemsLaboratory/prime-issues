from datetime import datetime
from json import load
from subprocess import call

from dateutil.parser import parse
from intervaltree import IntervalTree


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
