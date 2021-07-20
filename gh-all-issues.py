from os import popen
from os import system


def getGHIssues(
    repo: str = "",
    limit: int = 10000,
    state: str = "all",
    filename: str = "issues.json",
) -> None:
    filenameSuffix: str = filename.split(".")[-1]
    if filenameSuffix != "json":
        print("Invalid filename. Needs to be a JSON file.")
        quit(1)
    command: str = f'gh issue list --repo {repo} --json "closedAt,createdAt,id,state" --limit {limit} --state {state} > {filename}'
