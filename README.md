# CLIME Issues

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6478528.svg)](https://doi.org/10.5281/zenodo.6478528)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-issues/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-issues/actions/workflows/release.yml)

> A tool to download issue metadata from online issue trackers

## Table of Contents

- [CLIME Issues](#clime-issues)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Options](#command-line-options)

## About

The Software Systems Laboratory (SSL) CLIME  Issues project is a tool to download issue metadata from online issue trackers. Currently including GitLab, GitHub, and Bugzilla.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip clime-metrics`
- `pip install --upgrade pip clime-issues`

### Command Line Options

`clime-bz-issues`

``` shell
usage: CLIME Bugzilla Issues Downloader (BETA) [-h] -u URL [-i INPUT]
                                               [-o OUTPUT] [-v]

A tool to download all issues from a Bugzilla hosted issue tracker

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Bugzilla repository root url. DEFAULT:
                        https://bugzilla.kernal.org. NOTE: Structure the URL
                        exactly like the DEFAULT or else this will not work.
  -i INPUT, --input INPUT
                        CSV file of exported Bugzilla bugs. DEFAULT:
                        ./bugzilla_issues.csv
  -o OUTPUT, --output OUTPUT
                        File to save JSON response(s) to. DEFAULT:
                        ./bugzilla_issues.json
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Jake Palmer, Rohan Sethi, George K.
Thiruvathukal
```

`clime-gh-issues`

``` shell
usage: CLIME GitHub Issues Downloader [-h] [-p] -r REPOSITORY [-o OUTPUT] -t
                                      TOKEN [--log LOG] [-v]

A tool to download all issues from a GitHub hosted repository

options:
  -h, --help            show this help message and exit
  -p, --pull-request    Flag to enable the collection of pull requests with
                        the other data
  -r REPOSITORY, --repository REPOSITORY
                        GitHub formatted as repository owner/repository
  -o OUTPUT, --output OUTPUT
                        File to save JSON response(s) to. DEFAULT:
                        ./github_issues.json
  -t TOKEN, --token TOKEN
                        GitHub personal access token
  --log LOG             File to store logs in. DEFAULT: github_issues.log
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Jake Palmer, Rohan Sethi, George K.
Thiruvathukal
```

`clime-gl-issues`

``` shell
usage: CLIME Gitlab Issues Downloader [-h] -r REPOSITORY [-o OUTPUT] -t TOKEN
                                      [--log LOG] [-v]

A tool to download all issues from a Gitlab hosted repository

options:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        Gitlab repository ID
  -o OUTPUT, --output OUTPUT
                        File to save JSON response(s) to. DEFAULT:
                        ./gitlab_issues.json
  -t TOKEN, --token TOKEN
                        Gitlab personal access token
  --log LOG             File to store logs in. DEFAULT: gitlab_issues.log
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Jake Palmer, Rohan Sethi, George K.
Thiruvathukal
```

`clime-issues-graph`

``` shell
usage: CLIME GitHub Issues Grapher [-h] [-i INPUT] [-o OUTPUT] [-x X]
                                   [--y-thousandths] [--type TYPE]
                                   [--title TITLE] [--x-label X_LABEL]
                                   [--y-label Y_LABEL]
                                   [--stylesheet STYLESHEET] [-v]

A tool for graphing GitHub issue information from the output of the CLIME
GitHub Issues Downloader

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON export from CLIME GitHub Issues Downloader.
                        DEFAULT: ./github_issues.json
  -o OUTPUT, --output OUTPUT
                        Filename of the graph. DEFAULT: ./github_issues.pdf
  -x X                  Key of the x values to use for graphing. DEFAULT:
                        opened_day_since_0
  --y-thousandths       Flag to divide the y values by 1000
  --type TYPE           Type of figure to plot. DEFAULT: line
  --title TITLE         Title of the figure. DEFAULT: ""
  --x-label X_LABEL     X axis label of the figure. DEFAULT: ""
  --y-label Y_LABEL     Y axis label of the figure. DEFAULT: ""
  --stylesheet STYLESHEET
                        Filepath of matplotlib stylesheet to use. DEFAULT: ""
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Jake Palmer, Rohan Sethi, George K.
Thiruvathukal
```
