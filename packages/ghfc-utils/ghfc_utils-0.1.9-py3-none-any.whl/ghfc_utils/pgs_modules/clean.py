import argparse
import os

from termcolor import colored


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    """register arguments for this submodule of the argparse

    Args:
        subparsers (argparse._SubParsersAction): the subparsers to register into
    """
    subformat = subparsers.add_parser("clean")
    subformat.add_argument(
        metavar="root",
        dest="root",
        help="collection of summaries to format",
        type=str,
    )
    subformat.add_argument(
        "--slurm",
        dest="slurm",
        help="submit the job to slurm",
        action="store_true",
    )


def run(args):
    list_pgs = []
    # loop over all entity.yaml file in the args.root directory
    for root, _, files in os.walk(args.root):
        if "entity.yaml" in files:
            pgs_name = root[len(args.root) :]
            if pgs_name.startswith("/"):
                pgs_name = pgs_name[1:]
            list_pgs.append(pgs_name)
    list_pgs.sort()

    for p in list_pgs:
        print(f"{colored(p, 'green')}")
