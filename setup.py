# setup.py - placeholder for eventual setup script

from setuptools import setup

from ssl_metrics import version

setup(
    name="ssl-metrics-github-issues",
    packages=["ssl_metrics"],
    version=version.version(),
    description="SSL Metrics - GitHub Issues Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    keywords=["github", "software engineering", "metrics", "issues"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3",
    install_requires=[
        "intervaltree",
        "numpy",
        "matplotlib",
        "pandas",
        "progress",
        "python-dateutil",
        "requests",
    ],
    entry_points={"console_scripts": []},
)
