import json
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os.path import exists

from dateutil.parser import parse


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH Issue Spoilage Preprocessor",
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
    # parser.add_argument(
    #     "-l",
    #     "--lower-window-bound",
    #     help="Argument to specify the start of the window of time to analyze. NOTE: window bounds are inclusive.",
    #     type=int,
    #     required=False,
    #     default=0,
    # )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Specify name to save analysis to JSON file.",
        default="issue_spoilage.json",
        type=str,
        required=True,
    )
    # parser.add_argument(
    #     "-u",
    #     "--upper-window-bound",
    #     help="Argument to specify the max number of days to look at. NOTE: window bounds are inclusive.",
    #     type=int,
    #     required=False,
    #     default=None,
    # )
    return parser.parse_args()


def extractJSON(inputJSON: str) -> dict:
    issues: list = None

    try:
        with open(inputJSON, "r") as file:
            issues: list = json.load(file)
            file.close()
    except FileNotFoundError:
        print(f"{inputJSON} does not exist.")
        quit(4)

    day0: datetime = parse(issues[0]["created_at"]).replace(tzinfo=None)
    dayN: datetime = datetime.today().replace(tzinfo=None)
    data: list = []

    issue: dict
    for issue in issues:
        value: dict = {
            "issue_number": None,
            "created_at": None,
            "created_at_day": None,
            "closed_at": None,
            "closed_at_day": None,
            "state": None,
        }

        value["issue_number"] = issue["number"]
        value["created_at"] = issue["created_at"]
        value["state"] = issue["state"]

        if issue["closed_at"] is None:
            value["closed_at"] = dayN.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            value["closed_at"] = issue["closed_at"]

        createdAtDay: datetime = parse(issue["created_at"]).replace(tzinfo=None)

        value["created_at_day"] = (createdAtDay - day0).days

        if value["state"] == "open":
            value["closed_at_day"] = (dayN - day0).days
        else:
            value["closed_at_day"] = (
                parse(issue["closed_at"]).replace(tzinfo=None) - day0
            ).days

        data.append(value)

    return data


# def reduceDataSet(
#     data: list,
#     lowWindow: int = 0,
#     highWindow: int = None,
# ) -> list:
#     inBoundsData: list = []
#
#     issue: dict
#     for issue in data:
#
#         if highWindow is None:
#             if lowWindow <= issue["created_at_day"]:
#                 inBoundsData.append(issue)
#         elif lowWindow is None:
#             if highWindow >= issue["created_at_day"]:
#                 if issue["closed_at_day"] > highWindow:
#                     issue["closed_at_day"] = highWindow
#                 inBoundsData.append(issue)
#         else:
#             if (lowWindow <= issue["created_at_day"]) and (
#                 (highWindow >= issue["created_at_day"])
#             ):
#                 if issue["closed_at_day"] > highWindow:
#                     issue["closed_at_day"] = highWindow
#                 inBoundsData.append(issue)
#
#     return inBoundsData


def storeJSON(
    issues: list,
    outputFile: str,
) -> bool:
    data = json.dumps(issues)
    with open(file=outputFile, mode="w") as json_file:
        json_file.write(data)
    return exists(outputFile)


def main() -> None:
    args: Namespace = getArgparse()

    # try:
    #     if args.upper_window_bound <= 0:
    #         print("Invalid upper window bound. Use integer > 0")
    #         quit(1)
    # except TypeError:
    #     pass

    # if args.lower_window_bound < 0:
    #     print("Invlaid lower window bound. Use integer >= 0")
    #     quit(2)
    #
    # if args.lower_window_bound == args.upper_window_bound:
    #     print("Invlaid lower window bound and upper window bound. Use integers >= 0 and different from each other")
    #     quit(3)

    baseData: list = extractJSON(inputJSON=args.input)

    # reducedData: list = reduceDataSet(
    #     data=baseData,
    #     lowWindow=args.lower_window_bound,
    #     highWindow=args.upper_window_bound,
    # )

    storeJSON(
        issues=baseData,
        outputFile=args.save_json,
    )


if __name__ == "__main__":
    main()
