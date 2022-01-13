from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ssl_metrics_github_issues.polynomialMath import findBestFitLine


def graph(
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    maximumDegree: int = None,
    bestFit: bool = False,
    velocity: bool = False,
    acceleration: bool = False,
) -> Figure:
    figure: Figure = plt.figure()
    plt.title("\n".join(wrap(title, width=60)))
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)

    if type(maximumDegree) is int:
        data: tuple = findBestFitLine(
            x=xData,
            y=yData,
            maximumDegree=maximumDegree,
        )
        bfModel: np.poly1d = data[1]
        line: np.ndarray = np.linspace(0, max(xData), 100)

    if bestFit:
        plt.plot(line, bfModel(line))

    elif velocity:
        velocityModel = np.polyder(p=bfModel, m=1)
        plt.plot(line, velocityModel(line))

    elif acceleration:
        accelerationModel = np.polyder(p=bfModel, m=2)
        plt.plot(line, accelerationModel(line))

    else:
        plt.plot(xData, yData)

    plt.tight_layout()
    return figure


def graphAll(
    title: str,
    xLabel: str,
    yLabelList: list,
    xData: list,
    yData: list,
    maximumDegree: int,
    subplotTitles: list,
) -> Figure:
    figure: Figure = plt.figure()
    plt.suptitle(title)

    # Data
    plt.subplot(2, 2, 1)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabelList[0])
    plt.title(subplotTitles[0])
    plt.plot(xData, yData)
    plt.tight_layout()

    # Best Fit
    plt.subplot(2, 2, 2)
    data: tuple = findBestFitLine(x=xData, y=yData, maximumDegree=maximumDegree)
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[1])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[1])
    plt.plot(line, bfModel(line))
    plt.tight_layout()

    # Velocity
    plt.subplot(2, 2, 3)
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[2])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[2])
    plt.plot(line, velocityModel(line))
    plt.tight_layout()

    # Acceleration
    plt.subplot(2, 2, 4)
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[3])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[3])
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()

    return figure
