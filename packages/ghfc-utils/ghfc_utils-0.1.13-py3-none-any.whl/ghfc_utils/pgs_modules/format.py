import argparse
import os
import subprocess

import gwaslab as gl
import pkg_resources
import yaml

from .utils import guess_separator


def setup_args(subparsers: "argparse._SubParsersAction") -> None:
    """register arguments for this submodule of the argparse

    Args:
        subparsers (argparse._SubParsersAction): the subparsers to register into
    """
    subformat = subparsers.add_parser("format")
    subformat.add_argument(
        "--root",
        "-r",
        dest="root",
        help="path the the root of the summary statistics directory",
        type=str,
        required=True,
    )
    subformat.add_argument(
        "--name",
        "-n",
        dest="name",
        help="name of the summary, used for path within the root",
        type=str,
        required=True,
    )
    subformat.add_argument(
        "--force",
        "-f",
        dest="force",
        help="force the processing even if file already exists",
        action="store_true",
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
    """Execute the format command with provided arguments.

    Args:
        args: Namespace object containing command line arguments with the following attributes:
            root (str): path the the root of the summary statistics directory
            name (str): Name of the summary, used for path within the root
            force (bool): Force flag to overwrite existing formats

    Returns:
        None

    Raises:
        None
    """
    format(
        root=args.root,
        name=args.name,
        force=args.force,
        dbSNP_vcf=args.dbSNP_vcf,
    )


# function taking teh Zscore, the maf and the N, that will return the SE and the BETA
def zscore_to_se(z, maf, N):
    """
    Compute the standard error from the z-score, the minor allele frequency and the sample size.

    Args:
        z (float): Z-score
        maf (float): Minor allele frequency
        N (int): Sample size

    Returns:
        float: Standard error
    """
    se = 1 / (2 * maf * (1 - maf) * (N + z**2)) ** 0.5
    return se


def format(
    root: str,
    name: str,
    force: bool = False,
    dbSNP_vcf: str = "/pasteur/helix/projects/ghfc_wgs/references/gwaslab/",
) -> None:
    formats = ["cojo"]
    requirements = ["SNPID", "EA", "NEA", "EAF", "BETA", "SE", "P", "N"]
    missing_format = False
    for format in formats:
        if not os.path.exists(f"{root}/{name}/summary.{format}.tsv.gz"):
            missing_format = True
            continue
    if not missing_format and not force:
        return

    gl.options.paths["formatbook"] = pkg_resources.resource_filename(
        "ghfc_utils", "pgs_modules/resources/formatbook.json"
    )

    entity = yaml.safe_load(open(f"{root}/{name}/entity.yaml", "r"))

    mysumstats = gl.Sumstats(
        f"{root}/{name}/{entity['raw']}",
        fmt="auto",
        sep=guess_separator(f"{root}/{name}/{entity['raw']}"),
        verbose=False,
    )

    # check if BETA columns contains something other than NA
    if "BETA" in mysumstats.data.columns and mysumstats.data["BETA"].isnull().all():
        mysumstats.data = mysumstats.data.drop(columns=["BETA"])

    if "Z" in mysumstats.data.columns and "SE" in mysumstats.data.columns:
        mysumstats.data["BETA"] = mysumstats.data["Z"] * mysumstats.data["SE"]

    missing_columns = set(requirements) - set(mysumstats.data.columns)
    mysumstats.fill_data(
        to_fill=missing_columns.intersection({"BETA", "P", "SE"}),
        df=None,
        overwrite=False,
        only_sig=False,
        verbose=False,
    )
    missing_columns = set(requirements) - set(mysumstats.data.columns)
    mysumstats.basic_check(verbose=False)

    if "EAF" in missing_columns:
        print(r"/!\ missing EAF")
        # return
        # mysumstats.infer_build(verbose=False)
        # gl.download_ref(f"1kg_eur_hg{mysumstats.meta['gwaslab']['genome_build']}")
        # # mysumstats.data["EAF"] = ""
        # # print("==", mysumstats.data.columns)
        # mysumstats.infer_af(
        #     ref_infer=gl.get_path(
        #         f"1kg_eur_hg{mysumstats.meta['gwaslab']['genome_build']}"
        #     ),
        #     ref_alt_freq="AF",
        # )
    if "N" in missing_columns:
        if ("N_CASE" in mysumstats.data.columns) and (
            "N_CONTROL" in mysumstats.data.columns
        ):
            mysumstats.data["N"] = (
                mysumstats.data["N_CASE"] + mysumstats.data["N_CONTROL"]
            )
            missing_columns.remove("N")

    # check if "SNPID" columns containts a majority of values starting with "rs"
    if "SNPID" in mysumstats.data.columns:
        if mysumstats.data["SNPID"].str.startswith("rs").mean() < 0.5:
            print("SNPID column does not contain a majority of rsIDs")
            if "rsID" in mysumstats.data.columns:
                if "SNPID" in mysumstats.data.columns:
                    mysumstats.data = mysumstats.data.drop(columns=["SNPID"])
                mysumstats.data = mysumstats.data.rename(columns={"rsID": "SNPID"})
            else:
                print("No rsID column found")
                # mysumstats.data["rsID"] = ""
                status = mysumstats.data["STATUS"].copy()
                mysumstats.infer_build(verbose=False)
                mysumstats.data["STATUS"] = status
                gl.download_ref(
                    f"1kg_dbsnp151_hg{mysumstats.meta['gwaslab']['genome_build']}_auto"
                )
                dbsnp_file = ""
                if mysumstats.meta["gwaslab"]["genome_build"] == "38":
                    dbsnp_file = f"{dbSNP_vcf}/GCF_000001405.40.gz"
                elif mysumstats.meta["gwaslab"]["genome_build"] == "19":
                    dbsnp_file = f"{dbSNP_vcf}/GCF_000001405.25.gz"
                # print(dbsnp_file)
                mysumstats.assign_rsid(
                    ref_rsid_tsv=gl.get_path(
                        f"1kg_dbsnp151_hg{mysumstats.meta['gwaslab']['genome_build']}_auto"
                    ),
                    ref_rsid_vcf=dbsnp_file,
                    chr_dict=gl.get_number_to_NC(
                        build=str(mysumstats.meta["gwaslab"]["genome_build"])
                    ),
                    n_cores=10,
                    overwrite="all",
                )
                mysumstats.data = mysumstats.data.drop(columns=["SNPID"])
                mysumstats.data = mysumstats.data.rename(columns={"rsID": "SNPID"})

    if "SNPID" in mysumstats.data.columns:
        mysumstats.data = mysumstats.data[mysumstats.data["SNPID"].notnull()]

    if (
        "SE" in missing_columns
        and "Z" in mysumstats.data.columns
        and "N" in mysumstats.data.columns
    ):
        mysumstats.data["SE"] = mysumstats.data.apply(
            lambda x: zscore_to_se(x["Z"], x["EAF"], x["N"]), axis=1
        )
        missing_columns.discard("SE")

    if (
        "BETA" in missing_columns
        and "Z" in mysumstats.data.columns
        and "SE" in mysumstats.data.columns
    ):
        mysumstats.data["BETA"] = mysumstats.data["Z"] * mysumstats.data["SE"]
        missing_columns.discard("BETA")

    if "N" in missing_columns:
        if "n" in entity:
            mysumstats.data["N"] = entity["n"]
        else:
            mysumstats.data["N"] = 0
        missing_columns.remove("N")

    if len(missing_columns) > 0:
        print(f"Missing columns: {missing_columns}")

    for format in formats:
        if not os.path.exists(f"{root}/{name}/summary.{format}.tsv") or force:
            mysumstats.to_format(
                f"{root}/{name}/summary",
                fmt=format,
                verbose=False,
            )
            subprocess.run(
                f"gunzip -f {root}/{name}/summary.{format}.tsv.gz", shell=True
            )
