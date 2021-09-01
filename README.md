# SSL Metrics Github Issues

> (Proof of Concept) Using GitHub Issues REST API  issues to analyze GitHub issue timeline

## Reasoning Behind the Project

We're interested in classical metrics, which often require us to look more longtudinally at project history.

In this example, we're looking at issues over time, starting from the first issue of a project's history.

The present implementation assumes a GitHub hosted project.

## How to Execute the Program

> It is reccomended to use `Python 3.9+` to execute this program

### From Source

1. Install the requirements via `pip install -r requirements.txt`
2. Execute `python3 gh-all-issues.py --repo <OWNER/REPO> --page-limit <all | int> --token <PERSONAL ACCESS TOKEN> --save-json <filename.json>`

**Availible arguements**
* `-r, --repository`: GitHub repository to be used. Format needs to be "OWNER/REPO". Default is numpy/numpy
* `-p, --page-limit`: The numeric limit of pages of issues to get. Default is "all"
* `-t, --token`: GitHub personal access token
* `-s, --save-json`: Save analysis to JSON file

. *(Optional Step)* To convert the data non-destructively to a `CSV` or `TSV`, run `python convertOutput --input <filename.json> --csv --tsv`

**Availible arguements**
* `-i, --input`: The input `json` file to be converted
* `--csv`: Flag to output a `CSV` file with the filename. EX: `filename.csv`
* * `--tsv`: Flag to output a `TSV` file with the filename. EX: `filename.tsv`

## What You'll See

### Exported JSON file from `gh-all-issues.py`

* Every issue or a subset of the set of all issues and all of the JSON metadata associated with it.

## TODOs

* Support some of the derived metrics from our Metrics Pipeline project at https://ssl.cs.luc.edu.
