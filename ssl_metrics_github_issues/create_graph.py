from argparse import ArgumentParser, Namespace
<<<<<<< HEAD
from operator import itemgetter
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame
from sklearn.metrics import r2_score
=======
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
>>>>>>> main


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
<<<<<<< HEAD
        prog="ssl-metrics-git-bus-factor Graph Generator",
        usage="This is a proof of concept demonstrating that it is possible to use git to compute the bus factor of a project.",
        description="The only required arguement of this program is -i/--input. The default action is to do nothing until a filename for the graph is inputted.",
=======
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
>>>>>>> main
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
<<<<<<< HEAD
=======
    parser.add_argument(
        "-d",
        "--line-of-issues-spoilage-filename",
        help="The filename of the output graph of spoiled issues",
        type=str,
        required=True,
    )
>>>>>>> main
    parser.add_argument(
        "-o",
        "--output",
        help="The filename to output the bus factor graph to",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-m",
        "--maximum-degree-polynomial",
        help="Estimated maximum degree of polynomial",
        type=int,
        required=False,
        default=15,
    )
    parser.add_argument(
        "-r",
        "--repository-name",
        help="Name of the repository that is being analyzed",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--x-window-min",
        help="The smallest x value that will be plotted",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "--x-window-max",
        help="The largest x value that will be plotted",
        type=int,
        required=False,
        default=-1,
    )

    return parser.parse_args()


<<<<<<< HEAD
def __findBestFitLine(x: list, y: list, maximumDegrees: int) -> tuple:
    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []
=======
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
>>>>>>> main

    degree: int
    for degree in range(maximumDegrees):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))

<<<<<<< HEAD

def _graphFigure(
    repositoryName: str,
    xLabel: str,
    yLabel: str,
    title: str,
    x: list,
    y: list,
    maximumDegree: int,
    filename: str,
) -> None:
    figure: Figure = plt.figure()
    plt.suptitle(repositoryName)

    # Actual Data
    plt.subplot(2, 2, 1)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    # Best Fit
    plt.subplot(2, 2, 2)
    data: tuple = __findBestFitLine(x=x, y=y, maximumDegrees=maximumDegree)
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title("Best Fit Line")
    plt.plot(line, bfModel(line))
    plt.tight_layout()

    # Velocity of Best Fit
    plt.subplot(2, 2, 3)
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Velocity Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Velocity")
    plt.plot(line, velocityModel(line))
    plt.tight_layout()

    # Acceleration of Best Fit
    plt.subplot(2, 2, 4)
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Acceleration Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Acceleration")
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()

=======
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
>>>>>>> main
    figure.savefig(filename)
    figure.clf()


<<<<<<< HEAD
def plot(
    x: list,
    y: list,
    xLabel: str,
    yLabel: str,
    title: str,
    maximumDegree: int,
    repositoryName: str,
    filename: str,
) -> tuple:
    _graphFigure(
        repositoryName=repositoryName,
        xLabel=xLabel,
        yLabel=yLabel,
        title=title,
        x=x,
        y=y,
        maximumDegree=maximumDegree,
        filename=filename,
    )
    return (x, y)
=======
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
>>>>>>> main

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
    if args.x_window_min < 0:
        print("Invalid x window min. X window min >= 0")
        quit(2)

    locXLabel: str = "Commit"
    locYLabel: str = "LOC"
    locTitle: str = "Lines of Code (LOC) / Commits"

    dlocXLabel: str = locXLabel
    dlocYLabel: str = "ΔLOC"
    dlocTitle: str = "Change of Lines of Code (ΔLOC) / Days"

    klocXLabel: str = locXLabel
    klocYLabel: str = "KLOC"
    klocTitle: str = "Thousands of Lines of Code (KLOC) / Days"

    df: DataFrame = pandas.read_json(args.input)

    if args.x_window_max <= -1:
        x: list = [x for x in range(len(df["kloc"]))][args.x_window_min :]
        yLoc: list = df["loc_sum"].tolist()[args.x_window_min :]
        yDLoc: list = df["delta_loc"].tolist()[args.x_window_min :]
        yKLoc: list = df["kloc"].to_list()[args.x_window_min :]
    else:
        x: list = [x for x in range(len(df["kloc"]))][
            args.x_window_min : args.x_window_max + 1
        ]
        yLoc: list = df["loc_sum"].tolist()[args.x_window_min : args.x_window_max + 1]
        yDLoc: list = df["delta_loc"].tolist()[
            args.x_window_min : args.x_window_max + 1
        ]
        yKLoc: list = df["kloc"].to_list()[args.x_window_min : args.x_window_max + 1]

    if args.graph_loc_filename != None:
        # LOC
        plot(
            x=x,
            y=yLoc,
            xLabel=locXLabel,
            yLabel=locYLabel,
            title=locTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_loc_filename,
        )

    if args.graph_delta_loc_filename != None:
        # DLOC
        plot(
            x=x,
            y=yDLoc,
            xLabel=dlocXLabel,
            yLabel=dlocYLabel,
            title=dlocTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_delta_loc_filename,
        )

    if args.graph_k_loc_filename != None:
        # KLOC
        plot(
            x=x,
            y=yKLoc,
            xLabel=klocXLabel,
            yLabel=klocYLabel,
            title=klocTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_k_loc_filename,
        )


if __name__ == "__main__":
    main()
