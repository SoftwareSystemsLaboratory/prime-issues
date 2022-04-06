from argparse import Namespace

import pandas
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get

from ssl_metrics_github_issues.args import bugzillaArgs


def getIssueResponse(url: str, bug: int) -> Response:
    apiURL: str = f"{url}/rest/bug/{bug}"
    return get(url=apiURL)


def main() -> None:
    args: Namespace = bugzillaArgs()

    df: DataFrame = pandas.read_csv(args.input)
    bugIDs: list = df["Bug ID"].tolist()

    json: list = []

    with Bar("Downloading Bugzilla issues...", max=len(bugIDs)) as bar:
        id: int
        for id in bugIDs:
            resp: Response = getIssueResponse(args.url, bug=id)
            json.append(resp.json())
            bar.next()

    data: DataFrame = DataFrame(json)
    data.to_json(args.output)


if __name__ == "__main__":
    main()
