from argparse import ArgumentParser, Namespace

from libs.common import getLastPage, readJSON, storeJSON
from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program downloads all issue related data from a GitHub repository",
    )
    parser.add_argument(
        "-c",
        "--comments-output",
        help="JSON file to store issue comments",
        type=str,
        default="comments.json",
        required=False,
    )
    parser.add_argument(
        "--comments",
        help="Download the comments of all GitHub issues",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="JSON file to load issue to collect extra information",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-to",
        "--timeline-output",
        help="JSON file to store issue timelines",
        type=str,
        default="timelines.json",
        required=False,
    )
    parser.add_argument(
        "--timeline",
        help="Download the timelines of all GitHub issues",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub personal access token",
        type=str,
        required=True,
    )

    return parser.parse_args()


def getGHRESTAPIFromKey(
    key: str,
    data: list,
    repo: str,
    token: str,
) -> list:

    out: list = []
    requestHeaders: dict = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gh-all-issues",
        "Authorization": f"token {token}",
    }

    urls: data = [x[key] + "?&sort=created&direction=asc&per_page=100" for x in data]

    url: str
    for url in urls:
        issueNumber: str = url.split(sep="/")[7]

        html: Response = get(url=url, headers=requestHeaders)

        requestIterations: int = getLastPage(response=html)

        json: dict = html.json()
        for index in range(len(json)):
            out.append(json[index])

        if key == "comments_url":
            barStr: str = f"Storing issue {issueNumber} comments data from {repo}... "
        elif key == "timeline_url":
            barStr: str = f"Storing issue {issueNumber} timeline data from {repo}... "
        else:
            barStr: str = f"Storing issue {issueNumber} data from {repo}... "

        barMax: int = requestIterations
        with Bar(barStr, max=barMax) as bar:
            bar.next()

            if requestIterations != 1:
                for iteration in range(requestIterations + 1):

                    if iteration > 1:
                        apiCall: str = url + f"&page={iteration}"
                        html: Response = get(url=apiCall, headers=requestHeaders)

                        json: dict = html.json()
                        for index in range(len(json)):
                            out.append(json[index])
                        bar.next()
    return out


def main():
    args: Namespace = get_argparse()

    issues: list = readJSON(filename=args.input)

    if args.comments:
        comments: list = getGHRESTAPIFromKey(
            key="comments_url",
            data=issues,
            repo=args.repository,
            token=args.token,
        )
        storeJSON(
            json=comments,
            filename="comments.json",
        )

    if args.timeline:
        timeline: list = getGHRESTAPIFromKey(
            key="timeline_url",
            data=issues,
            repo=args.repository,
            token=args.token,
        )
        storeJSON(
            json=timeline,
            filename="timeline.json",
        )


if __name__ == "__main__":
    main()
