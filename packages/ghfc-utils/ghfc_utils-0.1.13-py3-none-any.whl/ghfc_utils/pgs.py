import argparse

from .pgs_modules import (
    clean,
    format,
    format_all,
    gctb_impute,
    gctb_impute_all,
    sbayesrc,
    sbayesrc_all,
    status,
)


def parse_app_args(args=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="cmd",
        help="pgs subcommand to run. for additional help, run `pgs <subcommand> -h`",
    )
    subparsers.required = True
    format.setup_args(subparsers)
    format_all.setup_args(subparsers)
    gctb_impute.setup_args(subparsers)
    gctb_impute_all.setup_args(subparsers)
    sbayesrc.setup_args(subparsers)
    sbayesrc_all.setup_args(subparsers)
    status.setup_args(subparsers)
    clean.setup_args(subparsers)

    return parser.parse_args(args)


def main() -> None:
    parsed_args = parse_app_args()
    command_map = {
        "format": format.run,
        "format-all": format_all.run,
        "gctb-impute": gctb_impute.run,
        "gctb-impute-all": gctb_impute_all.run,
        "sbayesrc": sbayesrc.run,
        "sbayesrc-all": sbayesrc_all.run,
        "status": status.run,
        "clean": clean.run,
    }
    command_map[parsed_args.cmd](parsed_args)


if __name__ == "__main__":
    main()
