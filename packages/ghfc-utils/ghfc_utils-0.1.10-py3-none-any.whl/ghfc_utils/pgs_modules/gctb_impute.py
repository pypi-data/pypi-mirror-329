import argparse
import os
import subprocess

from simple_slurm import Slurm


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    subformat = subparsers.add_parser(
        "gctb-impute", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
        default="5G",
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
    gctb_impute(
        root=args.root,
        trait_name=args.trait_name,
        matrix=args.matrix,
        threads=args.threads,
        gctb_executable=args.gctb_executable,
        slurm=args.slurm,
        slurm_memory=args.slurm_memory,
        print_only=args.print_only,
        force=args.force,
    )


def gctb_impute(
    root,
    trait_name,
    matrix,
    threads=1,
    gctb_executable="gctb",
    slurm=False,
    slurm_memory="5G",
    print_only=False,
    force=False,
    **kwargs,
):
    if force or not os.path.exists(f"{root}/{trait_name}/summary.cojo.imputed.ma"):
        command_block = f"{gctb_executable} --impute-summary --ldm-eigen {matrix} --thread {threads} --gwas-summary {root}/{trait_name}/summary.cojo.tsv --out {root}/{trait_name}/summary.cojo"
        command_merge = f"{gctb_executable} --gwas-summary summary.cojo --merge-block-gwas-summary --out summary.cojo.imputed"
        if print_only:
            print(command_block)
            print(command_merge)
            return
        if slurm:
            os.makedirs(f"{root}/{trait_name}/logs", exist_ok=True)

            slurm_block = Slurm(
                partition="ghfc",
                qos="ghfc",
                cpus_per_task=threads,
                mem=slurm_memory,
                array=range(1, 592),
                job_name=f"gctb_impute_{trait_name.split('/')[0]}",
                output=f"{root}/{trait_name}/logs/gctb_impute_block%a.txt",
            )
            jobid = slurm_block.sbatch(
                f"{command_block} --block {Slurm.SLURM_ARRAY_TASK_ID}"
            )

            slurm_merge = Slurm(
                partition="ghfc",
                qos="ghfc",
                cpus_per_task=threads,
                mem=slurm_memory,
                dependency=dict(after=jobid),
                job_name=f"gctb_merge_{trait_name.split('/')[0]}",
                output=f"{root}/{trait_name}/logs/gctb_impute_merge.txt",
            )
            slurm_merge.add_cmd(f"cd {root}/{trait_name}")
            slurm_merge.add_cmd("sleep 10")
            slurm_merge.sbatch(command_merge)
        else:
            subprocess.run(command_block, shell=True)
            subprocess.run(command_merge, shell=True)
