from argparse import ArgumentParser, Namespace

import pandas
from matplotlib.figure import Figure
from pandas import DataFrame

from ssl_metrics_github_issues.fileOperations import appendID
from ssl_metrics_github_issues.graphing import graph, graphAll


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="ssl-metrics-github-issues Graph Generator",
        usage="This is a proof of concept demonstrating that it is possible to use the GitHub REST API to compute metrics.",
        description="The default action is to graph all figures of Issue related metrics on a single chart. If multiple data and/or graphing options are choosen the output filename and the title of the figure/chartwill reflect the combination that is being graphed.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The filename to output the graph to",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-r",
        "--repository-name",
        help="Name of the repository that is being analyzed. Will be used in the graph title",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--loc", help="Utilize LOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--dloc", help="Utilize Delta LOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--kloc", help="Utilize KLOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--graph-data",
        help="Graph the raw data. Discrete graph of the data",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-best-fit",
        help="Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-velocity",
        help="Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-acceleration",
        help="Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-all",
        help="Graphs all possible figures of the data onto one chart. Computes the best fit polynomial and takes the first and second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--x-min",
        help="The smallest x value that will be plotted",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "--x-max",
        help="The largest x value that will be plotted",
        type=int,
        required=False,
        default=-1,
    )
    parser.add_argument(
        "-m",
        "--maximum-polynomial-degree",
        help="Estimated maximum degree of the best fit polynomial",
        type=int,
        required=False,
        default=15,
    )
    parser.add_argument(
        "-s",
        "--stepper",
        help="Step through every nth data point",
        type=int,
        required=False,
        default=1,
    )
    return parser.parse_args()


def graphChart(
    figureType: str,
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    filename: str,
    maximumDegree: int = None,
    subplotTitles: list = None,
    yLabelList: list = None,
) -> None:
    if figureType == "data":
        figure: Figure = graph(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
        )
    if figureType == "best_fit":
        figure: Figure = graph(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
            bestFit=True,
        )
    if figureType == "velocity":
        figure: Figure = graph(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
            velocity=True,
        )
    if figureType == "acceleration":
        figure: Figure = graph(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
            acceleration=True,
        )
    if figureType == "all":
        figure: Figure = graphAll(
            title=title,
            xLabel=xLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
            subplotTitles=subplotTitles,
            yLabelList=yLabelList,
        )

    figure.savefig(filename)
    figure.clf()


def main() -> None:
    def _graphDataChart(title: str, yLabel: str, yData: list, filename: str) -> None:
        graphChart(
            figureType="data",
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            filename=filename,
        )

    def _graphBestFitChart(title: str, yLabel: str, yData: list, filename: str) -> None:
        graphChart(
            figureType="best_fit",
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            filename=filename,
            maximumDegree=args.maximum_polynomial_degree,
        )

    def _graphVelocityChart(
        title: str, yLabel: str, yData: list, filename: str
    ) -> None:
        graphChart(
            figureType="velocity",
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            filename=filename,
            maximumDegree=args.maximum_polynomial_degree,
        )

    def _graphAccelerationChart(
        title: str, yLabel: str, yData: list, filename: str
    ) -> None:
        graphChart(
            figureType="acceleration",
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            filename=filename,
            maximumDegree=args.maximum_polynomial_degree,
        )

    def _graphAllCharts(
        title: str, yLabelList: list, yData: list, filename: str
    ) -> None:
        graphChart(
            figureType="all",
            title=title,
            xLabel=xLabel,
            yLabel=None,
            xData=xData,
            yData=yData,
            filename=filename,
            maximumDegree=args.maximum_polynomial_degree,
            subplotTitles=[
                "Data",
                "Best Fit",
                "Velocity",
                "Acceleration",
            ],
            yLabelList=yLabelList,
        )

    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)
    if args.x_min < 0:
        print("Invalid x window min. X window min >= 0")
        quit(2)
    if args.maximum_polynomial_degree < 1:
        print(
            "The maximum degree polynomial is too small. Maximum degree polynomial >= 1"
        )
        quit(3)
    if args.stepper < 1:
        print("The stepper is too small. Stepper >= 1")
        quit(4)

    if (args.loc is False) and (args.dloc is False) and (args.kloc is False):
        print("No data option choosen. Defaulting to --loc")
        args.loc = True
    if (
        (args.graph_data is False)
        and (args.graph_best_fit is False)
        and (args.graph_velocity is False)
        and (args.graph_acceleration is False)
        and (args.graph_all is False)
    ):
        print("No graph option choosen. Defaulting to --graph-all")
        args.graph_all = True

    xLabel: str = f"Every {args.stepper} Commit(s)"
    yLabel0: str = "{}"
    yLabel1: str = "d/dx {}"
    yLabel2: str = "d^2/dx^2 {}"

    df: DataFrame = pandas.read_json(args.input)

    t: str = (
        lambda typeOfGraph, repositoryName, yUnits: f"{typeOfGraph}{repositoryName} {yUnits} / Every {args.stepper} Commits"
    )
    x: list = lambda maxValue: [x for x in range(len(df["loc_sum"]))][
        args.x_min : maxValue : args.stepper
    ]
    y: list = lambda column, maxValue: df[column].tolist()[
        args.x_min : maxValue : args.stepper
    ]

    if args.x_max <= -1:
        xData: list = x(-1)
        yLOC: list = y("loc_sum", -1)
        yDLOC: list = y("delta_loc", -1)
        yKLOC: list = y("kloc", -1)
    else:
        xData: list = x(args.x_max + 1)
        yLOC: list = y("loc_sum", args.x_max + 1)
        yDLOC: list = y("delta_loc", args.x_max + 1)
        yKLOC: list = y("kloc", args.x_max + 1)

    if args.loc:
        if args.graph_data:
            title: str = t("", args.repository_name, "LOC")
            filename: str = appendID(filename=args.output, id="loc_data")
            _graphDataChart(
                title=title,
                yLabel=yLabel0.format("LOC"),
                yData=yLOC,
                filename=filename,
            )

        if args.graph_best_fit:
            title: str = t("Best Fit of ", args.repository_name, "LOC")
            filename: str = appendID(filename=args.output, id="loc_best_fit")
            _graphBestFitChart(
                title=title,
                yLabel=yLabel0.format("LOC"),
                yData=yLOC,
                filename=filename,
            )

        if args.graph_velocity:
            title: str = t("Velocity of ", args.repository_name, "LOC")
            filename: str = appendID(filename=args.output, id="loc_velocity")
            _graphVelocityChart(
                title=title,
                yLabel=yLabel1.format("LOC"),
                yData=yLOC,
                filename=filename,
            )

        if args.graph_acceleration:
            title: str = t("Acceleration of ", args.repository_name, "LOC")
            filename: str = appendID(filename=args.output, id="loc_acceleration")
            _graphAccelerationChart(
                title=title,
                yLabel=yLabel2.format("LOC"),
                yData=yLOC,
                filename=filename,
            )

        if args.graph_all:
            filename: str = appendID(filename=args.output, id="loc_all")
            title = t("", args.repository_name, "LOC")
            yLabelList: list = [
                yLabel0.format("LOC"),
                yLabel0.format("LOC"),
                yLabel1.format("LOC"),
                yLabel2.format("LOC"),
            ]
            _graphAllCharts(
                title=title,
                yLabelList=yLabelList,
                yData=yLOC,
                filename=filename,
            )

    if args.dloc:
        if args.graph_data:
            title: str = t("", args.repository_name, "DLOC")
            filename: str = appendID(filename=args.output, id="dloc_data")
            _graphDataChart(
                title=title,
                yLabel=yLabel0.format("DLOC"),
                yData=yDLOC,
                filename=filename,
            )

        if args.graph_best_fit:
            title: str = t("Best Fit of ", args.repository_name, "DLOC")
            filename: str = appendID(filename=args.output, id="dloc_best_fit")
            _graphBestFitChart(
                title=title,
                yLabel=yLabel0.format("DLOC"),
                yData=yDLOC,
                filename=filename,
            )

        if args.graph_velocity:
            title: str = t("Velocity of ", args.repository_name, "DLOC")
            filename: str = appendID(filename=args.output, id="dloc_velocity")
            _graphVelocityChart(
                title=title,
                yLabel=yLabel1.format("DLOC"),
                yData=yDLOC,
                filename=filename,
            )

        if args.graph_acceleration:
            title: str = t("Acceleration of ", args.repository_name, "DLOC")
            filename: str = appendID(filename=args.output, id="dloc_acceleration")
            _graphAccelerationChart(
                title=title,
                yLabel=yLabel2.format("DLOC"),
                yData=yDLOC,
                filename=filename,
            )

        if args.graph_all:
            title: str = t("", args.repository_name, "DLOC")
            filename: str = appendID(filename=args.output, id="dloc_all")
            yLabelList: list = [
                yLabel0.format("DLOC"),
                yLabel0.format("DLOC"),
                yLabel1.format("DLOC"),
                yLabel2.format("DLOC"),
            ]
            _graphAllCharts(
                title=title,
                yLabelList=yLabelList,
                yData=yDLOC,
                filename=filename,
            )

    if args.kloc:
        if args.graph_data:
            title: str = t("", args.repository_name, "KLOC")
            filename: str = appendID(filename=args.output, id="kloc_data")
            _graphDataChart(
                title=title,
                yLabel=yLabel0.format("KLOC"),
                filename=filename,
            )

        if args.graph_best_fit:
            title: str = t(
                "Best Fit of ",
                args.repository_name,
                "KLOC",
            )
            filename: str = appendID(filename=args.output, id="kloc_best_fit")
            _graphBestFitChart(
                title=title,
                yLabel=yLabel0.format("KLOC"),
                yData=yKLOC,
                filename=filename,
            )

        if args.graph_velocity:
            title: str = t(
                "Velocity of ",
                args.repository_name,
                "KLOC",
            )
            filename: str = appendID(filename=args.output, id="kloc_velocity")
            _graphVelocityChart(
                title=title,
                yLabel=yLabel1.format("KLOC"),
                yData=yKLOC,
                filename=filename,
            )

        if args.graph_acceleration:
            title: str = t("", args.repository_name, "KLOC")
            filename: str = appendID(filename=args.output, id="kloc_acceleration")
            title = title.format(
                "Acceleration of ",
                args.repository_name,
                "KLOC",
                args.stepper,
            )
            _graphAccelerationChart(
                title=title,
                yLabel=yLabel2.format("KLOC"),
                yData=yKLOC,
                filename=filename,
            )

        if args.graph_all:
            title: str = t("", args.repository_name, "KLOC")
            filename: str = appendID(filename=args.output, id="kloc_all")
            yLabelList: list = [
                yLabel0.format("KLOC"),
                yLabel0.format("KLOC"),
                yLabel1.format("KLOC"),
                yLabel2.format("KLOC"),
            ]
            _graphAllCharts(
                title=title,
                yLabelList=yLabelList,
                yData=yKLOC,
                filename=filename,
            )


if __name__ == "__main__":
    main()
