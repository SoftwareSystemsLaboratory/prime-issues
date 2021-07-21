from subprocess import call


def getGHIssues(
    repo: str = "",
    limit: int = 10000,
    state: str = "all",
    filename: str = "issues.json",
) -> int:
    if repo == "":
        command: str = f'gh issue list --json "closedAt,createdAt,id,state" --limit {limit} --state {state} > {filename}'
    else:
        command: str = f'gh issue list --repo {repo} --json "closedAt,createdAt,id,state" --limit {limit} --state {state} > {filename}'

    return call(command, shell=True)
