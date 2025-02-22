import argparse
import os

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


def status(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.sbayesrc.snpRes"):
        return True
    return False


def print_status(ok):
    if ok:
        return f"[{colored('OK', 'green')}]    "
    return f"[{colored('FAILED', 'red')}]"


def details(root, pgs_name):
    bool_formated, reason = is_formated(root, pgs_name)
    print(f"         >> {reason}")
    if not bool_formated:
        return

    bool_imputed, reason = is_imputed(root, pgs_name)
    print(f"         >> {reason}")
    if not bool_imputed:
        return

    if os.path.isfile(f"{root}/{pgs_name}/summary.sbayesrc.snpRes"):
        print(f"         >> SBayesRC {colored('OK', 'green')}")
    print("         >> SBayesRC missing")


def is_formated(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.cojo.tsv"):
        with open(f"{root}/{pgs_name}/summary.cojo.tsv") as f:
            header = f.readline().strip()
            if header == "SNP\tA1\tA2\tfreq\tb\tse\tp\tN":
                line = f.readline().strip()
                if line.split("\t")[-1] != "0":
                    # check if one of the frist 10 rows starts with "rs"
                    for _ in range(10):
                        line = f.readline().strip()
                        if line.split("\t")[0].startswith("rs"):
                            return True, "Format: OK"
                    return False, "Format: SNP names are not rsIDs"
                else:
                    return False, "Format: N column is 0"
            else:
                return False, "Format: Header is not correct"
    else:
        return False, "Format: Missing file"
    return False, "Format: Unknown error"


def is_imputed(root, pgs_name):
    if os.path.isfile(f"{root}/{pgs_name}/summary.cojo.imputed.ma"):
        return True, "Imputation: OK"
    return False, "Imputation: Missing file"


def run(args):
    list_pgs = []
    for root, _, files in os.walk(args.root):
        if "entity.yaml" in files:
            pgs_name = root[len(args.root) :]
            if pgs_name.startswith("/"):
                pgs_name = pgs_name[1:]
            list_pgs.append(pgs_name)
    list_pgs.sort()

    for p in list_pgs:
        st = status(args.root, p)
        if st and args.hide_ok:
            continue
        print(f"{print_status(st)} {p}")
        if args.details and not st:
            details(args.root, p)
