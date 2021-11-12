from argparse import ArgumentParser, Namespace
from collections import KeysView  # had to import this
from datetime import datetime
from json import load
from os.path import exists
from typing import Any  # had to import this
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
from intervaltree import IntervalTree
from matplotlib.figure import Figure
from progress.spinner import MoonSpinner


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Graph GitHub Issues",
        usage="This program outputs a series of graphs based on GitHub issue data.",
    )
    parser.add_argument(
        "-u",
        "--upper-window-bound",
        help="Argument to specify the max number of days to look at. NOTE: window bounds are inclusive.",
        type=int,
        required=False,
        default=None,
    )
    parser.add_argument(
        "-l",
        "--lower-window-bound",
        help="Argument to specify the start of the window of time to analyze. NOTE: window bounds are inclusive.",
        type=int,
        required=False,
        default=None,
    )
    parser.add_argument(
        "-c",
        "--closed-issues-graph-filename",
        help="The filename of the output graph of closed issues",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be used for graphing",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--line-of-issues-spoilage-filename",
        help="The filename of the output graph of spoiled issues",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--open-issues-graph-filename",
        help="The filename of the output graph of open issues",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-x",
        "--joint-graph-filename",
        help="The filename of the joint output graph of open and closed issues",
        type=str,
        required=True,
    )

    return parser.parse_args()


def loadJSON(filename: str) -> list:
    try:
        with open(file=filename, mode="r") as jsonFile:
            return load(jsonFile)
    except FileExistsError:
        print(f"{filename} does not exist.")
        quit(1)


def createIntervalTree(data: list, filename: str) -> IntervalTree:
    tree: IntervalTree = IntervalTree()
    # day0: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)

    with MoonSpinner(f"Creating interval tree from {filename}... ") as pb:
        issue: dict
        for issue in data:
            begin: int = issue["created_at_day"]
            end: int = issue["closed_at_day"]

            try:
                issue["endDayOffset"] = 0
                tree.addi(begin=begin, end=end, data=issue)
            except ValueError:
                issue["endDayOffset"] = 1
                tree.addi(begin=begin, end=end + 1, data=issue)

            pb.next()

    return tree


def issue_spoilage_data(
    data: IntervalTree,
):
    # startDay: int = data.begin()
    endDay: int = data.end()
    list_of_spoilage_values = []
    list_of_intervals = []
    for i in range(endDay):
        if i == 1:
            temp_set = data.overlap(0, 1)
            proc_overlap = []
            for issue in temp_set:
                # if issue.data["state"] == "open":
                #     proc_overlap.append(issue)
                if issue.begin != issue.end - 1 and issue.data["endDayOffset"] != 1:
                    proc_overlap.append(issue)
                    # list_of_intervals.append(issue.end - startDay)
            list_of_spoilage_values.append(
                {
                    "day": i + 1,
                    "number_open": len(proc_overlap),
                    "intervals": list_of_intervals,
                }
            )
        else:
            temp_set = data.overlap(i - 1, i)
            proc_overlap = []
            for issue in temp_set:
                # if issue.data["state"] == "open":
                #     proc_overlap.append(issue)
                if issue.begin != issue.end - 1 and issue.data["endDayOffset"] != 1:
                    proc_overlap.append(issue)
                    # list_of_intervals.append(issue.end - startDay)
            list_of_spoilage_values.append(
                {
                    "day": i + 1,
                    "number_open": len(proc_overlap),
                    "intervals": list_of_intervals,
                }
            )
    return list_of_spoilage_values

def shrink_graph(
  keys=None
):
    args: Namespace = getArgparse()
    if args.upper_window_bound != None:
        if args.lower_window_bound != None:
            plt.xlim(args.lower_window_bound, args.upper_window_bound)
        else:
            plt.xlim(0, args.upper_window_bound)
    else:
        if args.lower_window_bound != None:
            plt.xlim(args.lower_window_bound, len(keys))

def plot_IssueSpoilagePerDay(
    pregeneratedData: list,
    filename: str,
):
    figure: Figure = plt.figure()

    plt.title("Number of Spoiled Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: list = pregeneratedData

    keys = list()
    values = list()
    for day in pregeneratedData:
        keys.append(day["day"])
        values.append(day["number_open"])

    plt.plot(keys, values)

    shrink_graph(keys=keys)

    figure.savefig(filename)

    return exists(filename)


def plot_OpenIssuesPerDay_Line(
    pregeneratedData: dict = None,
    filename: str = "open_issues_per_day_line.png",
):
    figure: Figure = plt.figure()

    plt.title("Number of Open Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData

    plt.plot(data.keys(), data.values())
    shrink_graph(keys=data.keys())
    figure.savefig(filename)

    return exists(filename)


def plot_ClosedIssuesPerDay_Line(
    pregeneratedData: dict = None,
    filename: str = "closed_issues_per_day_line.png",
):
    figure: Figure = plt.figure()

    plt.title("Number of Closed Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData

    x_values = [int(i) for i in data.keys()]
    y_values = [int(i) for i in data.values()]
    # z = derivative(x_values, y_values)
    # p = np.poly1d(z)
    plt.plot(data.keys(), data.values(), color="blue", label="discrete")
    # plt.plot(x_values, p(x_values), color="red", label="continuous")

    shrink_graph(keys=data.keys())
    # plt.legend()
    figure.savefig(filename)

    return exists(filename)


def plot_OpenClosedIssuesPerDay_Line(
    pregeneratedData_OpenIssues: dict = None,
    pregeneratedData_ClosedIssues: dict = None,
    filename: str = "open_closed_issues_per_day_line.png",
):
    figure: Figure = plt.figure()

    plt.title("Number of Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    openData: dict = pregeneratedData_OpenIssues
    closedData: dict = pregeneratedData_ClosedIssues

    plt.plot(openData.keys(), openData.values(), color="blue", label="Open Issues")
    plt.plot(closedData.keys(), closedData.values(), color="red", label="Closed Issues")
    plt.legend()
    shrink_graph(keys=openData.keys())
    shrink_graph(keys=closedData.keys())
    shrink_graph(keys=keys)
    figure.savefig(filename)

    return exists(filename)


def fillDictBasedOnKeyValue(
    dictionary: dict, tree: IntervalTree, key: str, value: Any
) -> dict:
    data: dict = {}
    keys: KeysView = dictionary.keys()

    maxKeyValue: int = max(keys)
    minKeyValue: int = min(keys)

    with MoonSpinner(
        f'Getting the total number of "{key} = {value}" issues per day... '
    ) as pb:
        for x in range(minKeyValue, maxKeyValue):
            try:
                data[x] = dictionary[x]
            except KeyError:
                count = 0
                interval: IntervalTree
                for interval in tree.at(x):
                    if interval.data[key] == value:
                        count += 1
                data[x] = count

            pb.next()

    return data

# def derivative(
#     x_values=None,
#     y_values=None,
# ):
#     x = []
#     y = []
#     for i in x_values:
#         x.append(int(i))
#     for i in y_values:
#         y.append(int(i))
#     x1 = np.array(x)
#     y1 = np.array(y)
#     z = np.polyfit(x1, y1, 100)
#     return z
def main() -> None:
    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    jsonData: list = loadJSON(filename=args.input)

    tree: IntervalTree = createIntervalTree(data=jsonData, filename=args.input)

    startDay: int = tree.begin()
    endDay: int = tree.end()

    if len(tree.at(endDay)) == 0:
        endDay -= 1

    baseDict: dict = {startDay: len(tree.at(startDay)), endDay: len(tree.at(endDay))}

    openIssues: dict = fillDictBasedOnKeyValue(
        dictionary=baseDict, tree=tree, key="state", value="open"
    )

    closedIssues: dict = fillDictBasedOnKeyValue(
        dictionary=baseDict, tree=tree, key="state", value="closed"
    )

    plot_OpenIssuesPerDay_Line(
        pregeneratedData=openIssues, filename=args.open_issues_graph_filename
    )

    plot_ClosedIssuesPerDay_Line(
        pregeneratedData=closedIssues, filename=args.closed_issues_graph_filename
    )

    plot_OpenClosedIssuesPerDay_Line(
        pregeneratedData_ClosedIssues=closedIssues,
        pregeneratedData_OpenIssues=openIssues,
        filename=args.joint_graph_filename,
    )

    plot_IssueSpoilagePerDay(
        pregeneratedData=new_list,
        filename=args.line_of_issues_spoilage_filename,
    )


if __name__ == "__main__":
    main()
