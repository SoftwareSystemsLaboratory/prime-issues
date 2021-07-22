from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load
from os.path import exists
from typing import KeysView

import matplotlib.pyplot as plt
from dateutil.parser import parse
from intervaltree import IntervalTree
from matplotlib.figure import Figure


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Graph GitHub Issues",
        usage="This program outputs a series of graphs based on GitHub issue data.",
    )

    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be used for graphing",
        type=str,
        required=True,
    )

    return parser.parse_args()


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


def plot_OpenIssuesPerDay_Bar(
    tree: IntervalTree, filename: str = "open_issues_per_day_bar.png"
):
    figure: Figure = plt.figure()

    plt.title("Number of Open Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    startDay: int = tree.begin()
    endDay: int = tree.end()

    if len(tree.at(endDay)) == 0:
        endDay -= 1

    tempData: dict = {startDay: len(tree.at(startDay)), endDay: len(tree.at(endDay))}

    data: dict = fillDict(dictionary=tempData, tree=tree)

    plt.bar(data.keys(), data.values())
    figure.savefig(filename)

    return exists(filename)


def fillDict(dictionary: dict, tree: IntervalTree) -> dict:
    data: dict = {}
    keys: KeysView = dictionary.keys()

    maxKeyValue: int = max(keys)
    minKeyValue: int = min(keys)

    for x in range(minKeyValue, maxKeyValue):
        try:
            data[x] = dictionary[x]
        except KeyError:
            count = 0
            interval: IntervalTree
            for interval in tree.at(x):
                if interval.data["state"] == "open":
                    count += 1
            data[x] = count

    return data


if __name__ == "__main__":

    args = get_argparse()

    jsonData: list = loadJSON(filename=args.input)

    tree: IntervalTree = createIntervalTree(data=jsonData)

    plot_OpenIssuesPerDay_Bar(tree=tree)
