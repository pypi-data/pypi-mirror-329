import argparse
import os
import subprocess

from simple_slurm import Slurm


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    subformat = subparsers.add_parser(
        "sbayesrc", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    group_exec = subformat.add_argument_group("execution options")

    subformat.add_argument(
        metavar="trait_name",
        dest="trait_name",
        help="name of the trait",
        type=str,
    )
    subformat.add_argument(
        metavar="root",
        dest="root",
        help="path to the summaries root directory",
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
        help="path to the sbayesr executable",
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
        default="30G",
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
    sbayesrc(
        root=args.root,
        trait_name=args.trait_name,
        matrix=args.matrix,
        annot=args.annot,
        gctb_executable=args.gctb_executable,
        threads=args.threads,
        slurm=args.slurm,
        slurm_memory=args.slurm_memory,
        print_only=args.print_only,
        force=args.force,
    )


def sbayesrc(
    root,
    trait_name,
    matrix,
    annot="annot_baseline2.2.txt",
    gctb_executable="gctb",
    threads=1,
    slurm=False,
    slurm_memory="15G",
    print_only=False,
    force=False,
    **kwargs,
):
    # TODO add options for the sbayesr command
    # --exclude-mhc,--impute-n
    if force or not os.path.exists(f"{root}/{trait_name}/summary.sbayesrc.snpRes"):
        command = f"{gctb_executable} --sbayes RC --ldm-eigen {matrix} --annot {annot} --gwas-summary {root}/{trait_name}/summary.cojo.imputed.ma --thread {threads} --out {root}/{trait_name}/summary.sbayesrc"
        if print_only:
            print(command)
            return
        if slurm:
            os.makedirs(f"{root}/{trait_name}/logs", exist_ok=True)

            slurm = Slurm(
                partition="ghfc",
                qos="ghfc",
                cpus_per_task=threads,
                mem=slurm_memory,
                job_name=f"sbayesrc_{trait_name.split('/')[0]}",
                output=f"{root}/{trait_name}/logs/sbayesrc.txt",
            )
            slurm.sbatch(command)
        else:
            subprocess.run(command, shell=True)
