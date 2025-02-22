import argparse
import os

from simple_slurm import Slurm
from tqdm import tqdm

from . import format


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    """register arguments for this submodule of the argparse

    Args:
        subparsers (argparse._SubParsersAction): the subparsers to register into
    """
    subformat = subparsers.add_parser("format-all")
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
    subformat.add_argument(
        "--format-executable",
        dest="format_executable",
        help="path to the format executable",
        type=str,
        default="pgs format",
    )
    subformat.add_argument(
        "--force", "-f", help="force the processing", action="store_true"
    )
    subformat.add_argument(
        "--dbSNP-vcf-path",
        "-d",
        dest="dbSNP_vcf",
        help="path to the dbSNP vcf file",
        type=str,
        default="/pasteur/helix/projects/ghfc_wgs/references/gwaslab/",
    )


def run(args):
    list_pgs = []
    # loop over all entity.yaml file in the args.root directory
    for root, _, files in os.walk(args.root):
        if ("entity.yaml" in files) and (
            args.force or ("summary.cojo.tsv" not in files)
        ):
            pgs_name = root[len(args.root) :]
            if pgs_name.startswith("/"):
                pgs_name = pgs_name[1:]
            list_pgs.append(pgs_name)
    list_pgs.sort()

    if args.slurm:
        for p in list_pgs:
            command = f"{args.format_executable} --root {args.root} --name {p} {'--force' if args.force else ''}"
            os.makedirs(f"{args.root}/{p}/logs", exist_ok=True)
            slurm = Slurm(
                partition="ghfc",
                qos="ghfc",
                cpus_per_task=1,
                mem="5G",
                job_name=f"format_{p.split('/')[0]}",
                output=f"{args.root}/{p}/logs/ghfc_utils_format.txt",
            )
            slurm.sbatch(command)
    else:
        for p in (pbar := tqdm(list_pgs, desc="processing summaries")):
            pbar.set_description("processing " + p)
            format.format(
                root=args.root, name=p, force=args.force, dbSNP_vcf=args.dbSNP_vcf
            )
