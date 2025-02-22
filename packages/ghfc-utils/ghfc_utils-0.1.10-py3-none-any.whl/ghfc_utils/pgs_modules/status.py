import argparse
import glob
import os

import pandas as pd
from termcolor import colored


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    """register arguments for this submodule of the argparse

    Args:
        subparsers (argparse._SubParsersAction): the subparsers to register into
    """
    subformat = subparsers.add_parser("status")
    subformat.add_argument(
        "--root",
        dest="root",
        help="collection of summaries to get the status on",
        type=str,
        default=".",
    )
    subformat.add_argument(
        "--details",
        "-d",
        dest="details",
        help="show details",
        action="store_true",
    )
    subformat.add_argument(
        "--hide-ok",
        "-H",
        dest="hide_ok",
        help="hide OK status",
        action="store_true",
    )


def is_processed_sbayesrc(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.sbayesrc.snpRes"):
        return f"{colored('done', 'green')}"
    return f"{colored('not done', 'red')}"


def is_formated(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.cojo.tsv"):
        with open(f"{root}/{pgs_name}/summary.cojo.tsv") as f:
            header = f.readline().strip()
            if header == "SNP\tA1\tA2\tfreq\tb\tse\tp\tN":
                line = f.readline().strip()
                if line.split("\t")[-1] != "0":
                    # check if one of the frist 10 rows starts with "rs"
                    for _ in range(20):
                        line = f.readline().strip()
                        if line.split("\t")[0].startswith("rs"):
                            return f"{colored('done', 'green')}"
                    return f"{colored('PB', 'red')}: SNP are not rsIDs"
                else:
                    return f"{colored('PB', 'red')}: N column is 0"
            else:
                return f"{colored('PB', 'red')}: header problem"
    else:
        return f"{colored('not done', 'red')}"
    return f"{colored('unknown problem', 'red')}"


def get_nb_imputed_blocks(root, pgs_name):
    return len(glob.glob(f"{root}/{pgs_name}/summary.cojo.block*.imputed.ma"))


def get_nb_merged_blocks(root, pgs_name):
    # if f"{root}/{pgs_name}/logs/gctb_impute_merge.txt") does not exist, return -1
    if not os.path.isfile(f"{root}/{pgs_name}/logs/gctb_impute_merge.txt"):
        return -1
    # grep "Merging GWAS summary statistics files across" from the gctb_impute_merge.txt log file
    with open(f"{root}/{pgs_name}/logs/gctb_impute_merge.txt") as f:
        for line in f:
            if "Merging GWAS summary statistics files across" in line:
                return int(line.split()[6])


def is_imputed(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.cojo.imputed.ma"):
        # need to check if all the blocks were merged together
        nb_imputed_blocks = get_nb_imputed_blocks(root, pgs_name)
        nb_merged_blocks = get_nb_merged_blocks(root, pgs_name)
        if nb_merged_blocks == -1:
            return f"{colored('PB', 'red')}: missing log file"
        if nb_imputed_blocks == nb_merged_blocks:
            return f"{colored('done', 'green')} ({nb_imputed_blocks} imputed blocks)"
        return f"{colored('PB', 'red')}: missing {nb_imputed_blocks - nb_merged_blocks} blocks"
    return f"{colored('not done', 'red')}"


def run(args):
    list_pgs = []
    for root, dirs, files in os.walk(args.root):
        if "logs" in dirs:
            dirs.remove("logs")
        if "entity.yaml" in files:
            pgs_name = root[len(args.root) :]
            if pgs_name.startswith("/"):
                pgs_name = pgs_name[1:]
            list_pgs.append(pgs_name)
    list_pgs.sort()

    t_report = []

    for p in list_pgs:
        reason = is_formated(args.root, p)
        reason_2 = is_imputed(args.root, p)
        reason_3 = is_processed_sbayesrc(args.root, p)
        t_report.append([p, reason, reason_2, reason_3])

    if args.hide_ok:
        t_report = [
            r
            for r in t_report
            if (
                (r[3] != colored("done", "green")) or (r[1] != colored("done", "green"))
            )
        ]

    print(
        pd.DataFrame(
            t_report, columns=["PGS", "formating", "imputation", "SBayesRC"]
        ).to_markdown(index=False)
    )
