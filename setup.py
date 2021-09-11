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
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues",
    },
    keywords=["github", "software engineering", "metrics", "issues"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
    install_requires=[
        "intervaltree",
        "numpy",
        "matplotlib",
        "pandas",
        "progress",
        "python-dateutil",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ssl-metrics-github-issues-collect = ssl_metrics_github_issues.github_issues:main",
            "ssl-metrics-github-issues-graph = ssl_metrics_github_issues.create_graph:main",
        ]
    },
)
