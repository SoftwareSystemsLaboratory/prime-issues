import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghAllIssues",
    version="0.0.5",
    author="Nicholas M. Synovic",
    author_email="nicholas.synovic@gmail.com",
    description="(Proof of Concept) Using GitHub Issues REST API issues to analyze GitHub issue timeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/NicholasSynovic/mingo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
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
)
