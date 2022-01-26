from setuptools import setup

from ssl_metrics_github_issues import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ssl-metrics-github-issues",
    packages=["ssl_metrics_github_issues"],
    version=version.version(),
    description="SSL Metrics - GitHub Issues Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues",
    },
    keywords=[
        "bus factor",
        "commits",
        "engineering",
        "git",
        "github",
        "issue density",
        "issues",
        "kloc",
        "loyola",
        "loyola university chicago",
        "luc",
        "mining",
        "metrics",
        "repository",
        "repository mining",
        "simple",
        "software",
        "software engineering",
        "software metrics",
        "software systems laboratory",
        "ssl"
    ],
    python_requires=">=3.9",
    install_requires=[
        "intervaltree>=3.1.0",
        "numpy>1.21.2",
        "matplotlib>=3.4.3",
        "pandas>=1.3.3",
        "progress>=1.6",
        "python-dateutil>=2.8.2",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "ssl-metrics-github-issues-collect = ssl_metrics_github_issues.main:main",
            "ssl-metrics-github-issues-graph = ssl_metrics_github_issues.create_graph:main",
        ]
    },
)
