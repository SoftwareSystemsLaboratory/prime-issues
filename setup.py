from setuptools import setup
from sssl_metrics_github_issues import version

setup(
    name="ssl-metrics-github-issues",
    packages=["ssl_metrics_github_issues"],
    version=version.version(),
    description="SSL Metrics - GitHub Issues Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="Apache License 2.0",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
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
