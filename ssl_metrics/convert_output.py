from argparse import ArgumentParser, Namespace

import pandas
from pandas import DataFrame


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be converted",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--csv",
        help="Flag to set the output of the conversion to a .csv file",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--tsv",
        help="Flag to set the output of the conversion to a .tsv file",
        required=False,
        action="store_true",
    )
    return parser


def createDataFrame(filename: str) -> DataFrame:
    return pandas.read_json(filename)


def convertToCSV(df: DataFrame, filename: str) -> None:
    df.to_csv(filename, index=False)


def convertToTSV(df: DataFrame, filename: str) -> None:
    df.to_csv(filename, sep="\t", index=False)

def main():
    args: Namespace = get_argparse().parse_args()

    if args.csv is None and args.tsv is None:
        print('Run "python convertOutput -h" for a full list of arguements...')
        quit(1)

    filename: str = args.input
    df: DataFrame = createDataFrame(filename=filename)

    filenamePrefix: str = filename.split(".json")[0]

    if args.csv:
        convertToCSV(df, filename=filenamePrefix + ".csv")

    if args.tsv:
        convertToTSV(df, filename=filenamePrefix + ".tsv")

if __name__ == "__main__":
    main()

