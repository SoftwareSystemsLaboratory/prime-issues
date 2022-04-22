# CLIME Issues

> A tool to download issue metadata from online issue trackers

## Table of Contents

- [CLIME Issues](#clime-issues)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) CLIME  Issues project is a tool to download issue metadata from online issue trackers. Currently including GitLab, GitHub, and Bugzilla.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip clime-metrics`
- `pip install --upgrade pip clime-issues`

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
