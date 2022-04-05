import pandas
from pandas import DataFrame
from requests import Response, get
from progress.bar import Bar

def getIssueResponse(url: str, bug: int) -> Response:
    apiURL: str = f"{url}/rest/bug/{bug}"
    return get(url=apiURL)

def main()  ->  None:
    df: DataFrame = pandas.read_csv("bugs.csv")
    bugIDs: list = df["Bug ID"].tolist()

    json: list = []

    with Bar("Downloading Bugzilla issues...", max=len(bugIDs)) as bar:
        id: int
        for id in bugIDs:
            resp: Response = getIssueResponse("https://bugzilla.kernel.org", bug=id)
            json.append(resp.json())
            bar.next()

    data: DataFrame = DataFrame(json)
    data.to_json("bugzilla_issues.json")




if __name__ == "__main__":
    main()
