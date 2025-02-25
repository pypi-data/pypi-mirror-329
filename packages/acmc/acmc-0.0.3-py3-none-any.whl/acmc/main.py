import argparse
import logging
from pathlib import Path

import acmc
from acmc import trud, omop, phen, logging_config as lc

# setup logging
logger = lc.setup_logger()

DEFAULT_WORKING_PATH = Path("./workspace")


def trud_install(args):
    """Handle the `trud install` command."""
    trud.install()


def omop_install(args):
    """Handle the `omop install` command."""
    omop.install(args.omop_zip_file, args.version)


def omop_clear(args):
    """Handle the `omop clear` command."""
    omop.clear(omop.DB_PATH)


def omop_delete(args):
    """Handle the `omop delete` command."""
    omop.delete(omop.DB_PATH)


def phen_init(args):
    """Handle the `phen init` command."""
    phen.init(args.phen_dir, args.remote_url)


def phen_validate(args):
    """Handle the `phen validate` command."""
    phen.validate(args.phen_dir)


def phen_map(args):
    """Handle the `phen map` command."""
    phen.map(args.phen_dir, args.target_coding)


def phen_export(args):
    """Handle the `phen copy` command."""
    phen.export(args.phen_dir, args.version)


def phen_publish(args):
    """Handle the `phen publish` command."""
    phen.publish(args.phen_dir)


def phen_copy(args):
    """Handle the `phen copy` command."""
    phen.copy(args.phen_dir, args.target_dir, args.version)


def phen_diff(args):
    """Handle the `phen diff` command."""
    phen.diff(args.phen_dir, args.phen_dir_old)


def main():
    parser = argparse.ArgumentParser(description="ACMC command-line tool")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--version", action="version", version=f"acmc {acmc.__version__}"
    )

    # Top-level commands
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    ### TRUD Command ###
    trud_parser = subparsers.add_parser("trud", help="TRUD commands")
    trud_subparsers = trud_parser.add_subparsers(
        dest="subcommand", required=True, help="TRUD subcommands"
    )

    # trud install
    trud_install_parser = trud_subparsers.add_parser(
        "install", help="Install TRUD components"
    )
    trud_install_parser.set_defaults(func=trud_install)

    ### OMOP Command ###
    omop_parser = subparsers.add_parser("omop", help="OMOP commands")
    omop_subparsers = omop_parser.add_subparsers(
        dest="subcommand", required=True, help="OMOP subcommands"
    )

    # omop install
    omop_install_parser = omop_subparsers.add_parser(
        "install", help="Install OMOP codes within database"
    )
    omop_install_parser.add_argument(
        "-f", "--omop-zip-file", required=True, help="Path to downloaded OMOP zip file"
    )
    omop_install_parser.add_argument(
        "-v", "--version", required=True, help="OMOP vocabularies release version"
    )
    omop_install_parser.set_defaults(func=omop_install)

    # omop clear
    omop_clear_parser = omop_subparsers.add_parser(
        "clear", help="Clear OMOP data from database"
    )
    omop_clear_parser.set_defaults(func=omop_clear)

    # omop delete
    omop_delete_parser = omop_subparsers.add_parser(
        "delete", help="Delete OMOP database"
    )
    omop_delete_parser.set_defaults(func=omop_delete)

    ### PHEN Command ###
    phen_parser = subparsers.add_parser("phen", help="Phen commands")
    phen_subparsers = phen_parser.add_subparsers(
        dest="subcommand", required=True, help="Phen subcommands"
    )

    # phen init
    phen_init_parser = phen_subparsers.add_parser(
        "init", help="Initiatise phenotype directory"
    )
    phen_init_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_init_parser.add_argument(
        "-r", "--remote_url", help="URL to remote git repository"
    )
    phen_init_parser.set_defaults(func=phen_init)

    # phen validate
    phen_validate_parser = phen_subparsers.add_parser(
        "validate", help="Validate phenotype configuration"
    )
    phen_validate_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_validate_parser.set_defaults(func=phen_validate)

    # phen map
    phen_map_parser = phen_subparsers.add_parser("map", help="Process phen mapping")
    phen_map_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_map_parser.add_argument(
        "-t",
        "--target-coding",
        required=True,
        choices=["read2", "read3", "icd10", "snomed", "opcs4"],
        help="Specify the target coding (read2, read3, icd10, snomed, opcs4)",
    )
    phen_map_parser.add_argument(
        "-o",
        "--output",
        choices=["csv", "omop"],
        nargs="+",  # allows one or more values
        default=["csv"],  # default to CSV if not specified
        help="Specify output format(s): 'csv', 'omop', or both (default: csv)",
    )
    phen_map_parser.set_defaults(func=phen_map)

    # phen export
    phen_export_parser = phen_subparsers.add_parser(
        "export", help="Export phen to OMOP database"
    )
    phen_export_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_export_parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="latest",
        help="Phenotype version to export, defaults to the latest version",
    )
    phen_export_parser.set_defaults(func=phen_export)

    # phen publish
    phen_publish_parser = phen_subparsers.add_parser(
        "publish", help="Publish phenotype configuration"
    )
    phen_publish_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_publish_parser.set_defaults(func=phen_publish)

    # phen copy
    phen_copy_parser = phen_subparsers.add_parser(
        "copy", help="Publish phenotype configuration"
    )
    phen_copy_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Phenotype workspace directory",
    )
    phen_copy_parser.add_argument(
        "-td",
        "--target-dir",
        type=str,
        default=str(DEFAULT_WORKING_PATH.resolve()),
        help="Target directory for the copy",
    )
    phen_copy_parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="latest",
        help="Phenotype version to copy, defaults to the latest version",
    )
    phen_copy_parser.set_defaults(func=phen_copy)

    # phen diff
    phen_diff_parser = phen_subparsers.add_parser(
        "diff", help="Publish phenotype configuration"
    )
    phen_diff_parser.add_argument(
        "-d",
        "--phen-dir",
        type=str,
        default=str(phen.DEFAULT_PHEN_PATH.resolve()),
        help="Directory for the new phenotype version",
    )
    phen_diff_parser.add_argument(
        "-old",
        "--phen-dir-old",
        required=True,
        help="Directory of the old phenotype version that is compared to the new one",
    )
    phen_diff_parser.set_defaults(func=phen_diff)

    # Parse arguments
    args = parser.parse_args()

    # setup logging
    if args.debug:
        lc.set_log_level(logging.DEBUG)

    # Call the function associated with the command
    args.func(args)


if __name__ == "__main__":
    main()
