import argparse
import os

from tqdm import tqdm

from . import sbayesrc


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    """register arguments for this submodule of the argparse

    Args:
        subparsers (argparse._SubParsersAction): the subparsers to register into
    """
    subformat = subparsers.add_parser("sbayesrc-all")
    subformat.add_argument(
        metavar="root",
        dest="root",
        help="collection of summaries to run SBayesRC on",
        type=str,
    )
    subformat.add_argument(
        metavar="mldm",
        dest="matrix",
        help="path to the matrix of LD scores",
        type=str,
    )
    subformat.add_argument(
        "--annot",
        dest="annot",
        help="annotation file for SBayesRC",
        type=str,
        default="annot_baseline2.2.txt",
    )

    group_exec = subformat.add_argument_group("execution options")

    group_exec.add_argument(
        "--threads",
        dest="threads",
        help="number of threads to use",
        type=int,
        default=1,
    )
    group_exec.add_argument(
        "--gctb-executable",
        dest="gctb_executable",
        help="path to the gctb executable",
        type=str,
        default="gctb",
    )
    group_exec.add_argument(
        "--slurm",
        dest="slurm",
        help="submit the job to slurm",
        action="store_true",
    )
    group_exec.add_argument(
        "--slurm-memory",
        dest="slurm_memory",
        help="memory for the slurm job",
        type=str,
        default="15G",
    )
    group_exec.add_argument(
        "--print-only",
        dest="print_only",
        help="print the command only",
        action="store_true",
    )
    group_exec.add_argument(
        "--force",
        "-f",
        help="force the processing even if file already exists",
        action="store_true",
    )


def run(args):
    list_pgs = []
    for root, _, files in os.walk(args.root):
        if "summary.cojo.imputed.ma" in files:
            pgs_name = root[len(args.root) :]
            if pgs_name.startswith("/"):
                pgs_name = pgs_name[1:]
            list_pgs.append(pgs_name)
    list_pgs.sort()

    for p in (
        pbar := tqdm(
            list_pgs, desc="running SBayesRC", disable=(args.print_only or args.slurm)
        )
    ):
        pbar.set_description("running SBayesRC on " + p)
        sbayesrc.sbayesrc(trait_name=p, **vars(args))
