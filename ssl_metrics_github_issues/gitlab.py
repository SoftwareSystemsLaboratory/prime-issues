import re
from datetime import datetime

from dateutil.parser import parse as dateParse
from pandas import DataFrame
from requests import Response, get
from requests.models import CaseInsensitiveDict


def getIssueResponse(repo: str, token: str, page: int = 1) -> Response:
    requestHeaders: dict = {
        "PRIVATE-TOKEN": token,
    }

    apiURL: str = f"https://gitlab.com/api/v4/projects/{repo}/issues?scope=all&order_by=created_at&sort=asc&per_page=100&page={page}"

    return get(url=apiURL, headers=requestHeaders)


def getPageCount(response: Response) -> int:
    headers: CaseInsensitiveDict = response.headers
    try:
        lastPageString: str = headers["link"].split(",")[-1].split("&")[2]
    except KeyError:
        return 1
    return int(re.search(r"\d+", lastPageString).group())


def computeValues(data: list) -> list:
    day0: datetime = dateParse(data[0]["created_at"]).replace(tzinfo=None)

    x: dict
    for x in data:
        x["opened_day_since_0"] = (
            dateParse(x["created_at"]).replace(tzinfo=None) - day0
        ).days
        try:
            x["closed_day_since_0"] = (
                dateParse(x["closed_at"]).replace(tzinfo=None) - day0
            ).days
        except TypeError:
            x["closed_day_since_0"] = (datetime.now().replace(tzinfo=None) - day0).days

    return data


def iterateAPI(repo: str, token: str) -> DataFrame:
    resp: Response = getIssueResponse(repo, token, page=1)
    pageCount: int = getPageCount(resp)
    json: list = resp.json()

    for page in range(2, pageCount + 1):
        resp: Response = getIssueResponse(repo, token, page)
        json.extend(resp.json())

    data: list = computeValues(json)

    return DataFrame(data)


def main() -> None:
    df: DataFrame = iterateAPI(repo="31598236", token="glpat-9W2a5CUryB2_wdu2ruk3")
    df.T.to_json("gitlab.json")

    quit()


if __name__ == "__main__":
    main()
