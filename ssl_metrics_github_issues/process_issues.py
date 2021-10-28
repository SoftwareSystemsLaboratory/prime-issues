import json
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os.path import exists
from typing import Type

from dateutil.parser import parse


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH Issue Engagement",
        usage="This program generates JSON file containing specific data related to a repositories issue engagement.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Raw repository issues JSON file to be used. These files can be generated using the ssl-metrics-github-issues tool.",
        default="issues.json",
        type=str,
        required=True,
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
        default=0,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Specify name to save analysis to JSON file.",
        default="issue_spoilage.json",
        type=str,
        required=True,
    )
    return parser.parse_args()


def calculateIssueSpoilage(
    data: list,
    lowWindow: int,
    highWindow: int,
) -> list:

    removal_List = []

    begin: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)

    if highWindow is None and lowWindow is not None:

        for issue in data:
            createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
            if lowWindow > (createdDate - begin).days:
                removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    elif lowWindow is None and highWindow is not None:

        for issue in data:
            if issue["closed_at"] is not None:
                closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
                if highWindow < (closedDate - begin).days:
                    removal_List.append(issue)
            else:
                createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
                if highWindow < (createdDate - begin).days:
                    removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    elif highWindow is not None and lowWindow is not None:

        for issue in data:
            if issue["closed_at"] is not None:
                closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
                if highWindow < (closedDate - begin).days < lowWindow:
                    removal_List.append(issue)
            else:
                createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
                if highWindow < (createdDate - begin).days < lowWindow:
                    removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    else:

        data = data

    return data


def extractJSON(inputJSON: str) -> dict:
    try:
        with open(inputJSON, "r") as file:
            issues: list = json.load(file)
            data: list = [
                dict(
                    issue_number=issue["number"],
                    comments=issue["comments"],
                    created_at=issue["created_at"],
                    closed_at=issue["closed_at"],
                    state=issue["state"],
                )
                for issue in issues
            ]
            file.close()
    except FileNotFoundError:
        print(f"{inputJSON} does not exist.")
        quit(3)

    return data


def storeJSON(
    issues: list,
    output_file: str,
) -> bool:
    data = json.dumps(issues)
    with open(file=output_file, mode="w") as json_file:
        json_file.write(data)
    return exists(output_file)


def main() -> None:
    args: Namespace = getArgparse()

    try:
        if args.upper_window_bound <= 0:
            print("Invalid upper window bound. Use integert > 0")
            quit(1)
    except TypeError:
        pass

    if args.lower_window_bound < 0:
        print("Invlaid lower window bound. Use integer >= 0")
        quit(2)

    data: list = extractJSON(inputJSON=args.input)

    issues_json = calculateIssueSpoilage(
        data=data,
        lowWindow=args.lower_window_bound,
        highWindow=args.upper_window_bound,
    )

    storeJSON(
        issues=issues_json,
        output_file=args.save_json,
    )


if __name__ == "__main__":
    main()
