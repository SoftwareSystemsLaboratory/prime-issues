from setuptools import setup

from clime_issues import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clime-issues",
    packages=["clime_issues"],
    version=version.version(),
    description="CLIME - Issues",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/clime-issues/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/clime-issues",
    },
    keywords=[
        "bugzilla",
        "bus factor",
        "bus factor",
        "cloc",
        "commits",
        "commits",
        "delta lines of code",
        "engineering",
        "git",
        "git",
        "github",
        "github",
        "gitlab",
        "installable",
        "issue density",
        "issue density",
        "issue spoilage",
        "issues",
        "issues",
        "kloc",
        "lines of code",
        "longitudinal graphs",
        "loyola university chicago",
        "loyola",
        "luc",
        "metrics",
        "metrics",
        "mining",
        "productivity",
        "python",
        "repository mining",
        "repository",
        "simple",
        "sloccount",
        "software engineering",
        "software metrics",
        "software systems laboratory",
        "software",
        "ssl",
        "thousands of lines of code",
        "tool",
        "vcs"
    ],
    python_requires=">=3.9",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "progress",
        "python-dateutil",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "clime-bz-issues = clime_issues.bugzilla:main",
            "clime-gh-issues = clime_issues.github:main",
            "clime-gl-issues = clime_issues.gitlab:main",
            "clime-issues-graph = clime_issues.graph:main",
        ]
    },
)
