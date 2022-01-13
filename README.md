# SSL Metrics GitHub Issues Extractor

> Using the GitHub Issues REST API, provide insight into a specific GitHub repository issue tracker


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5655424.svg)](https://doi.org/10.5281/zenodo.5655424) [![Release to PyPi, GitHub, and Zenodo](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues/actions/workflows/release.yml)

## About

This is a proof of concept demonstrating that it is possible to use the GitHub REST API to extract Issues from a repository and graph various metrics from it.

This software extracts Issues since the project's conception a GitHub repository and stores it within a `.json` file.

This file can then be piped into a bundled graphing utility to graph the following:

* Number of open issues against days
* Number of closed issues against days
* Comparison of number of open and closed issues against days

The graphs can be saved as a `.png`, `.pdf`, or any compatible format that `matplotlib` supports.

## How to Run

### Installation

#### From pip

### From pip

1. Install `Python 3.9.6 +`
2. (Recommended) Create a *virtual environment* with `python3.9 -m venv env` and *activate* it
3. Run `pip install ssl-metrics-github-issues`
4. Generate a JSON data set with `ssl-metrics-github-issues-collect -r REPOSITORY -t GH_TOKEN -s FILENAME.json`
5. Generate graphs with `ssl-metrics-github-issues-graph -i FILENAME.json -o OPEN_ISSUES_GRAPH_FILENAME.* -c CLOSED_ISSUES_GRAPH_FILENAME.* -x JOINT_ISSUES_GRAPH_FILENAME`

### Command Line Arguments

#### ssl-metrics-github-issues-collect

- `-h`, `--help`: Shows the help menu and exits
- `-r`, `--repository`: GitHub repository to be used. Format needs to be "OWNER/REPO". Default is numpy/numpy
- `-t`, `--token`: [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- `-s`, `--save-json`: Save analysis to JSON file

#### ssl-metrics-github-issues-graph

TODO: Add export options

- `-h`, `--help`: Shows the help menu and exits
- `-c`, `--closed-issues-graph-filename`: The filename of the output graph of closed issues
- `-i`, `--input`: The input JSON file that is to be used for graphing
- `-o`, `--open-issues-graph-filename`: The filename of the output graph of open issues
- `-x`, `--joint-issues-graph-filename`: The filename of the output graph of open and closed issues

## Example Outputs

TODO: Add outputs following this format [https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/blob/main/README.md#example-outputs](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/blob/main/README.md#example-outputs)
