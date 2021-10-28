import json
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os.path import exists

from dateutil.parser import parse


def get_argparse() -> Namespace:
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
        default=-1
    )
    parser.add_argument(
        "-l",
        "--lower-window-bound",
        help="Argument to specify the start of the window of time to analyze. NOTE: window bounds are inclusive.",
        type=int,
        required=False,
        default=0
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


def getIssueEngagementReport(
    input_json: str,
    low_window: int = None,
    high_window: int = None,
) -> list:

    with open(input_json, "r") as json_file:
        # with open("issues.json") as json_file:
        data = json.load(json_file)
        data = [
            dict(
                issue_number=k1["number"],
                comments=k1["comments"],
                created_at=k1["created_at"],
                closed_at=k1["closed_at"],
                state=k1["state"],
            )
            for k1 in data
        ]
        json_file.close()

    removal_List = []

    begin: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)

    if high_window is None and low_window is not None:

        for issue in data:
            createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
            if low_window > (createdDate - begin).days:
                removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    elif low_window is None and high_window is not None:

        for issue in data:
            if issue["closed_at"] is not None:
                closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
                if high_window < (closedDate - begin).days:
                    removal_List.append(issue)
            else:
                createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
                if high_window < (createdDate - begin).days:
                    removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    elif high_window is not None and low_window is not None:

        for issue in data:
            if issue["closed_at"] is not None:
                closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
                if high_window < (closedDate - begin).days < low_window:
                    removal_List.append(issue)
            else:
                createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
                if high_window < (createdDate - begin).days < low_window:
                    removal_List.append(issue)

        for issue in removal_List:
            data.remove(issue)

    else:

        data = data

    return data


def storeJSON(
    issues: list,
    output_file: str,
) -> bool:
    # json.dump(issues)
    data = json.dumps(issues)
    with open(file=output_file, mode="w") as json_file:
        json_file.write(data)
    return exists(output_file)


def main() -> None:
    args: Namespace = get_argparse()

    issues_json = getIssueEngagementReport(
        input_json=args.input,
        low_window=args.lower_window_bound,
        high_window=args.upper_window_bound,
    )

    storeJSON(
        issues=issues_json,
        output_file=args.save_json,
    )


if __name__ == "__main__":
    main()
