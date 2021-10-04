from argparse import ArgumentParser, Namespace
from json import dumps
from os import sep
from os.path import exists

from progress.bar import Bar
from requests import Response, get
from requests.models import CaseInsensitiveDict


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH All issues",
        usage="This program downloads all issue related data from a GitHub repository",
    )
    parser.add_argument(
        "--comments",
        help="Download the comments of all GitHub issues",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file",
        default="issues.json",
        type=str,
        required=True,
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


def getLastPage(response: Response) -> int:
    responseHeaders: CaseInsensitiveDict = response.headers
    try:
        links: str = responseHeaders["Link"]
    except KeyError:
        return 1

    linksSplit: list = links.split(",")
    lastLink: str = linksSplit[1]

    lastPageIndex: int = lastLink.find("&page=") + 6
    lastPageRightCaretIndex: int = lastLink.find(">;")

    return int(lastLink[lastPageIndex:lastPageRightCaretIndex])


def storeJSON(json: list, filename: str = "issues.json") -> bool:
    data: str = dumps(json)
    with open(file=filename, mode="w") as jsonFile:
        jsonFile.write(data)
    return exists(filename)


def main():
    args: Namespace = get_argparse()

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
