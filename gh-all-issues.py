from datetime import datetime, timedelta
from json import load
from os import close
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
    day0: str = data[0]["createdAt"]
    day0: datetime = parse(day0)

    for issue in data:
        closedDate: str = issue["createdAt"]
        closedDate: datetime = parse(closedDate)

        dateDiff: int = (closedDate - day0).days

    tree: IntervalTree = IntervalTree()
    # for issue in data:


getGHIssues(repo="numpy/numpy", limit=10)
data = loadJSON()

createIntervalTree(data)
