# Software Systems Laboratory Metrics GitHub Issues Collector

> A `python` tool that lets users download/ collect issues from a GitHub repository

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)
[![DOI](https://zenodo.org/badge/402158914.svg)](https://zenodo.org/badge/latestdoi/402158914)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-github-issues/actions/workflows/release.yml)
![[https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](https://img.shields.io/badge/license-BSD--3-yellow)

## Table of Contents

- [Software Systems Laboratory Metrics GitHub Issues Collector](#software-systems-laboratory-metrics-github-issues-collector)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Issues Collector Project is a `python` tool that lets users download/ collect issues from a GitHub repository.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project and the greater SSL Metrics project, the following software packages are **required**:

### Operating System

All tools developed for the greater SSL Metrics project **must target** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to develop on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip ssl-metrics-meta`
- `pip install --upgrade pip ssl-metrics-github-issues`

### Command Line Arguements

`ssl-metrics-github-issues-collect -h`

```shell
options:
  -h, --help            show this help message and exit
  -p, --pull-request    Flag to enable the collection of pull requests with the other data
  -r REPOSITORY, --repository REPOSITORY
                        GitHub formatted as repository owner/repository
  -o OUTPUT, --output OUTPUT
                        File to save JSON response(s) to
  -t TOKEN, --token TOKEN
                        GitHub personal access token
```

`ssl-metrics-github-issues-graph -h`

```shell
options:
  options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input data file that will be read to create the graphs
  -o OUTPUT, --output OUTPUT
                        The filename to output the graph to
  -r REPOSITORY_NAME, --repository-name REPOSITORY_NAME
                        Name of the repository that is being analyzed. Will be used in the graph title
  --open                Utilize Open Issue data
  --closed              Utilize Closed Issue data
  --graph-data          Graph the raw data. Discrete graph of the data
  --graph-best-fit      Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with
                        `-m`
  --graph-velocity      Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees
                        can be configured with `-m`
  --graph-acceleration  Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial
                        degrees can be configured with `-m`
  --graph-all           Graphs all possible figures of the data onto one chart. Computes the best fit polynomial and takes the first and
                        second derivitve. Polynomial degrees can be configured with `-m`
  --x-min X_MIN         The smallest x value that will be plotted
  --x-max X_MAX         The largest x value that will be plotted
  -m MAXIMUM_POLYNOMIAL_DEGREE, --maximum-polynomial-degree MAXIMUM_POLYNOMIAL_DEGREE
                        Estimated maximum degree of the best fit polynomial
  -s STEPPER, --stepper STEPPER
                        Step through every nth data point
```
