from json import dumps, load
from os import sep
from os.path import exists

from requests import Response
from requests.models import CaseInsensitiveDict


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


def readJSON(filename: str = "issues.json") -> list:
    data: list = []
    with open(file=filename, mode="r") as jsonFile:
        data = load(jsonFile)
        jsonFile.close()
    return exists(filename)


def storeJSON(json: list, filename: str = "issues.json") -> bool:
    data: str = dumps(json)
    with open(file=filename, mode="w") as jsonFile:
        jsonFile.write(data)
        jsonFile.close()
    return exists(filename)
