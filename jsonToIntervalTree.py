from datetime import datetime
from json import load
from math import ceil

from dateutil.parser import parse
from intervaltree import IntervalTree


def loadJSON(filename: str = "issues.json") -> list:
    with open(file=filename, mode="r") as jsonFile:
        return load(jsonFile)


def createIntervalTree(data: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()

    day0: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)
    today: datetime = datetime.now(tz=None)

    for issue in data:
        createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)

        if issue["state"] == "closed":
            closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
        else:
            closedDate: datetime = today

        begin: int = (createdDate - day0).days
        end: int = (closedDate - day0).days

        try:
            issue["endDayOffset"] = 0
            tree.addi(begin=begin, end=end, data=issue)
        except ValueError:
            issue["endDayOffset"] = 1
            tree.addi(begin=begin, end=end + 1, data=issue)

    return tree
