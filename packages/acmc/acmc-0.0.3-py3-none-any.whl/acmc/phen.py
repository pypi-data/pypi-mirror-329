import argparse
import pandas as pd
import numpy as np
import json
import os
import sqlite3
import sys
import shutil
import git
import re
import logging
import requests
import yaml
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import acmc
from acmc import trud, omop, parse

# setup logging
import acmc.logging_config as lc

logger = lc.setup_logger()

pd.set_option("mode.chained_assignment", None)

PHEN_DIR = "phen"
DEFAULT_PHEN_PATH = Path("./workspace") / PHEN_DIR

CODES_DIR = "codes"
MAP_DIR = "map"
CONCEPT_SET_DIR = "concept-set"
OMOP_DIR = "omop"
DEFAULT_PHEN_DIR_LIST = [CODES_DIR, MAP_DIR, CONCEPT_SET_DIR, OMOP_DIR]
CONFIG_FILE = "config.yaml"
VOCAB_VERSION_FILE = "vocab_version.yaml"

DEFAULT_GIT_BRANCH = "main"

SPLIT_COL_ACTION = "split_col"
CODES_COL_ACTION = "codes_col"
DIVIDE_COL_ACTION = "divide_col"
COL_ACTIONS = [SPLIT_COL_ACTION, CODES_COL_ACTION, DIVIDE_COL_ACTION]

CODE_FILE_TYPES = [".xlsx", ".xls", ".csv"]


class PhenValidationException(Exception):
    """Custom exception class raised when validation errors in phenotype configuration file"""

    def __init__(self, message, validation_errors=None):
        super().__init__(message)
        self.validation_errors = validation_errors


def construct_git_url(remote_url):
    """Constructs a git url for github or gitlab including a PAT token environment variable"""
    # check the url
    parsed_url = urlparse(remote_url)

    # if github in the URL otherwise assume it's gitlab, if we want to use others such as codeberg we'd
    # need to update this function if the URL scheme is different.
    if "github.com" in parsed_url.netloc:
        # get GitHub PAT from environment variable
        auth = os.getenv("ACMC_GITHUB_PAT")
        if not auth:
            raise ValueError(
                "GitHub PAT not found. Set the ACMC_GITHUB_PAT environment variable."
            )
    else:
        # get GitLab PAT from environment variable
        auth = os.getenv("ACMC_GITLAB_PAT")
        if not auth:
            raise ValueError(
                "GitLab PAT not found. Set the ACMC_GITLAB_PAT environment variable."
            )
        auth = f"oauth2:{auth}"

    # Construct the new URL with credentials
    new_netloc = f"{auth}@{parsed_url.netloc}"
    return urlunparse(
        (
            parsed_url.scheme,
            new_netloc,
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment,
        )
    )


def create_empty_git_dir(path):
    """Creates a directory with a .gitkeep file so that it's tracked in git"""
    path.mkdir(exist_ok=True)
    keep_path = path / ".gitkeep"
    keep_path.touch(exist_ok=True)


def init(phen_dir, remote_url):
    """Initial phenotype directory as git repo with standard structure"""
    logger.info(f"Initialising Phenotype in directory: {phen_dir}")
    phen_path = Path(phen_dir)

    # check if directory already exists and ask user if they want to recreate it
    configure = False
    if (
        phen_path.exists() and phen_path.is_dir()
    ):  # Check if it exists and is a directory
        user_input = (
            input(
                f"The phen directory already exists. Do you want to reinitialise? (yes/no): "
            )
            .strip()
            .lower()
        )
        if user_input in ["yes", "y"]:
            shutil.rmtree(phen_path)
            configure = True
        else:
            logger.info("Phen directory was not recreated.")
    else:
        configure = True

    if not configure:
        logger.info(f"Exiting, phenotype not initiatised")
        return

    # Initialise repo from local or remote
    repo = None
    # if remote then clone the repo otherwise init a local repo
    if remote_url != None:
        # add PAT token to the URL
        git_url = construct_git_url(remote_url)

        # clone the repo
        repo = git.cmd.Git()
        repo.clone(git_url, phen_path)
        # open repo
        repo = git.Repo(phen_path)
        # check if there are any commits (new repo has no commits)
        if (
            len(repo.branches) == 0 or repo.head.is_detached
        ):  # Handle detached HEAD (e.g., after init)
            logger.debug("The phen repository has no commits yet.")
            commit_count = 0
        else:
            # Get the total number of commits in the default branch
            commit_count = sum(1 for _ in repo.iter_commits())
            logger.debug(f"Repo has previous commits: {commit_count}")
    else:
        # local repo, create the directories and init
        phen_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Phen directory '{phen_path}' has been created.")
        repo = git.Repo.init(phen_path)
        commit_count = 0

    # initialise empty repos
    if commit_count == 0:
        # create initial commit
        initial_file_path = phen_path / "README.md"
        with open(initial_file_path, "w") as file:
            file.write(
                "# Initial commit\nThis is the first commit in the phen repository.\n"
            )
        repo.index.add([initial_file_path])
        repo.index.commit("Initial commit")
        commit_count = 1

    # Checkout the phens default branch, creating it if it does not exist
    if DEFAULT_GIT_BRANCH in repo.branches:
        main_branch = repo.heads[DEFAULT_GIT_BRANCH]
        main_branch.checkout()
    else:
        main_branch = repo.create_head(DEFAULT_GIT_BRANCH)
        main_branch.checkout()

    # if the phen path does not contain the config file then initialise the phen type
    config_path = phen_path / CONFIG_FILE
    if config_path.exists():
        logger.debug(f"Phenotype configuration files already exist")
        return

    logger.info("Creating phen directory structure and config files")
    for d in DEFAULT_PHEN_DIR_LIST:
        create_empty_git_dir(phen_path / d)

    # set initial version based on the number of commits in the repo, depending on how the repo was created
    # e.g., with a README.md, then there will be some initial commits before the phen config is added
    next_commit_count = commit_count + 1
    initial_version = f"v1.0.{next_commit_count}"

    # create empty phen config file
    config = {
        "phenotype": {
            "version": initial_version,
            "omop": {
                "vocabulary_id": "",
                "vocabulary_name": "",
                "vocabulary_reference": "",
            },
            "concept_sets": [],
        }
    }

    with open(phen_path / CONFIG_FILE, "w") as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)

    # add git ignore
    ignore_content = """# Ignore SQLite database files
 *.db
 *.sqlite3
 
 # Ignore SQLite journal and metadata files
 *.db-journal
 *.sqlite3-journal
 """
    ignore_path = phen_path / ".gitignore"
    with open(ignore_path, "w") as file:
        file.write(ignore_content)

    # add to git repo and commit
    for d in DEFAULT_PHEN_DIR_LIST:
        repo.git.add(phen_path / d)
    repo.git.add(all=True)
    repo.index.commit("initialised the phen git repo.")

    logger.info(f"Phenotype initialised successfully")


def validate(phen_dir):
    """Validates the phenotype directory is a git repo with standard structure"""
    logger.info(f"Validating phenotype: {phen_dir}")
    phen_path = Path(phen_dir)
    if not phen_path.is_dir():
        raise NotADirectoryError(
            f"Error: '{str(phen_path.resolve())}' is not a directory"
        )

    config_path = phen_path / CONFIG_FILE
    if not config_path.is_file():
        raise FileNotFoundError(
            f"Error: phen configuration file '{config_path}' does not exist."
        )

    codes_path = phen_path / CODES_DIR
    if not codes_path.is_dir():
        raise FileNotFoundError(
            f"Error: source codes directory {source_codes_dir} does not exist."
        )

    # Calidate the directory is a git repo
    try:
        git.Repo(phen_path)
    except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
        raise Exception(f"Phen directory {phen_path} is not a git repo")

    # Load configuration File
    if config_path.suffix == ".yaml":
        with config_path.open("r") as file:
            phenotype = yaml.safe_load(file)
    else:
        raise Exception(
            f"Unsupported configuration filetype: {str(config_path.resolve())}"
        )

    # initiatise
    validation_errors = []
    phenotype = phenotype["phenotype"]
    code_types = parse.CodeTypeParser().code_types

    # check the version number is of the format vn.n.n
    match = re.match(r"v(\d+\.\d+\.\d+)", phenotype["version"])
    if not match:
        validation_errors.append(
            f"Invalid version format in configuration file: {phenotype['version']}"
        )

    # create a list of all the concept set names defined in the concept set configuration
    concept_set_names = []
    for item in phenotype["concept_sets"]:
        if item["name"] in concept_set_names:
            validation_errors.append(
                f"Duplicate concept set defined in concept sets {item['name'] }"
            )
        else:
            concept_set_names.append(item["name"])

    # TODO: change this to some sort of yaml schema validation
    required_keys = {"name", "file", "metadata"}

    # check codes definition
    for item in phenotype["concept_sets"]:

        if required_keys.issubset(item.keys()):

            # check concepte code file exists
            concept_code_file_path = codes_path / item["file"]["path"]
            if not concept_code_file_path.exists():
                validation_errors.append(
                    f"Coding file {str(concept_code_file_path.resolve())} does not exist"
                )

            # check concepte code file is not empty
            if concept_code_file_path.stat().st_size == 0:
                validation_errors.append(
                    f"Coding file {str(concept_code_file_path.resolve())} is an empty file"
                )

            # check code file type is supported
            if concept_code_file_path.suffix not in CODE_FILE_TYPES:
                raise ValueError(
                    f"Unsupported filetype {concept_code_file_path.suffix}, only support csv, xlsx, xls code file types"
                )

            # check columns specified are a supported medical coding type
            for column in item["file"]["columns"]:
                if column not in code_types:
                    validation_errors.append(
                        f"Column type {column} for file {concept_code_file_path} is not supported"
                    )

            # check the actions are supported
            if "actions" in item["file"]:
                for action in item["file"]["actions"]:
                    if action not in COL_ACTIONS:
                        validation_errors.append(f"Action {action} is not supported")

        else:
            validation_errors.append(
                f"Missing required elements {required_keys} in concept set {item}"
            )

    if len(validation_errors) > 0:
        logger.error(validation_errors)
        raise PhenValidationException(
            f"Configuration file {str(config_path.resolve())} failed validation",
            validation_errors,
        )

    logger.info(f"Phenotype validated successfully")


def read_table_file(path, excel_sheet=None):
    """
    Load Code List File
    """

    path = path.resolve()
    if path.suffix == ".csv":
        df = pd.read_csv(path, dtype=str)
    elif path.suffix == ".xlsx" or path.suffix == ".xls":
        if excel_sheet:
            df = pd.read_excel(path, sheet_name=excel_sheet, dtype=str)
        else:
            df = pd.read_excel(path, dtype=str)
    elif path.suffix == ".dta":
        df = pd.read_stata(path, dtype=str)
    else:
        raise ValueError(
            f"Unsupported filetype {codes_file_path.suffix}, only support{CODE_FILE_TYPES} code file types"
        )

    return df


def process_actions(df, concept_set):
    # Perform Structural Changes to file before preprocessing
    logger.debug("Processing file structural actions")
    if (
        "actions" in concept_set["file"]
        and "split_col" in concept_set["file"]["actions"]
        and "codes_col" in concept_set["file"]["actions"]
    ):
        split_col = concept_set["file"]["actions"]["split_col"]
        codes_col = concept_set["file"]["actions"]["codes_col"]
        logger.debug(
            "Action: Splitting",
            split_col,
            "column into:",
            df[split_col].unique(),
        )
        codes = df[codes_col]
        oh = pd.get_dummies(df[split_col], dtype=bool)  # one hot encode
        oh = oh.where((oh != True), codes, axis=0)  # fill in 1s with codes
        oh[oh == False] = np.nan  # replace 0s with None
        df = pd.concat([df, oh], axis=1)  # merge in new columns

    return df


# Perform QA Checks on columns individually and append to df
def preprocess_codes(df, concept_set, code_file_path, target_code_type=None):
    """Parses each column individually - Order and length will not be preserved!"""
    out = pd.DataFrame([])  # create output df to append to
    code_errors = []  # list of errors from processing

    # TODO: Is there a better way of processing this action as it's distributed across
    # different parts of the programme.
    if (
        "actions" in concept_set["file"]
        and "divide_col" in concept_set["file"]["actions"]
    ):
        divide_col_df = df[concept_set["file"]["actions"]["divide_col"]]
    else:
        divide_col_df = pd.DataFrame()

    # Preprocess codes
    code_types = parse.CodeTypeParser().code_types
    for code_type in concept_set["file"]["columns"]:
        parser = code_types[code_type]
        logger.info(f"Processing {code_type} codes...")

        # get code types
        codes = df[concept_set["file"]["columns"][code_type]].dropna()
        codes = codes.astype(str)  # convert to string
        codes = codes.str.strip()  # remove excess spaces

        # process codes, validating them using parser and returning the errors
        codes, errors = parser.process(codes, code_file_path)
        if len(errors) > 0:
            code_errors.extend(errors)
            logger.warning(f"Codes validation failed with {len(errors)} errors")

        # append to output dataframe
        out = pd.concat(
            [out, pd.DataFrame({code_type: codes}).join(divide_col_df)],
            ignore_index=True,
        )

    return out, code_errors


# Translate Df with multiple codes into single code type Series
def translate_codes(df, target_code_type):
    codes = pd.Series([], dtype=str)

    # Convert codes to target type
    logger.info(f"Converting to target code type {target_code_type}")
    for col_name in df.columns:
        # if target code type is the same as thet source code type, no translation, just appending source as target
        if col_name == target_code_type:
            logger.debug(
                f"Target code type {target_code_type} has source code types {len(df)}, copying rather than translating"
            )
            codes = pd.concat([codes, df[target_code_type]])
        else:
            filename = f"{col_name}_to_{target_code_type}.parquet"
            map_path = trud.PROCESSED_PATH / filename
            if map_path.exists():
                col = df[col_name]
                df_map = pd.read_parquet(map_path)
                # merge on corresponding codes and take target column
                translated = pd.merge(col, df_map, how="left")[target_code_type]
                # TODO: BUG mask does not match column
                codes = pd.concat([codes, translated])  # merge to output
            else:
                logger.warning(
                    f"No mapping from {col_name} to {target_code_type}, file {str(map_path.resolve())} does not exist"
                )

    return codes


# Append file's codes to output Df with concept
def map_file(df, target_code_type, out, concept_name):

    # translate codes
    codes = translate_codes(df, target_code_type)
    codes = codes.dropna()  # delete NaNs

    # Append to output if translated
    if len(codes) > 0:
        codes = pd.DataFrame({"CONCEPT": codes})
        codes["CONCEPT_SET"] = np.repeat(concept_name.strip(), len(codes))
        out = pd.concat([out, codes])
    else:
        logger.debug(f"No codes converted with target code type {target_code_type}")

    return out


def sql_row_exist(conn, table, column, value):
    # Execute and check if a result exists
    cur = conn.cursor()
    query = f"SELECT 1 FROM {table} WHERE {column} = ? LIMIT 1;"
    cur.execute(query, (value,))
    exists = cur.fetchone() is not None

    return exists


def write_code_errors(code_errors, code_errors_path):
    err_df = pd.DataFrame(
        [
            {
                "CONCEPT": ", ".join(err.codes[~err.mask].tolist()),
                "VOCABULARY": err.code_type,
                "SOURCE": err.codes_file,
                "CAUSE": err.message,
            }
            for err in code_errors
        ]
    )

    err_df = err_df.drop_duplicates()  # Remove Duplicates from Error file
    err_df = err_df.sort_values(by=["SOURCE", "VOCABULARY", "CONCEPT"])
    err_df.to_csv(code_errors_path, index=False, mode="w")


def write_vocab_version(phen_path):
    # write the vocab version files

    if not trud.VERSION_PATH.exists():
        raise FileNotFoundError(
            f"TRUD version path {trud.VERSION_PATH} does not exist, please check TRUD is installed"
        )

    if not omop.VERSION_PATH.exists():
        raise FileNotFoundError(
            f"OMOP version path {omop.VERSION_PATH} does not exist, please check OMOP is installed"
        )

    with trud.VERSION_PATH.open("r") as file:
        trud_version = yaml.safe_load(file)

    with omop.VERSION_PATH.open("r") as file:
        omop_version = yaml.safe_load(file)

    # Create the combined YAML structure
    version_data = {
        "versions": {
            "acmc": acmc.__version__,
            "trud": trud_version,
            "omop": omop_version,
        }
    }

    with open(phen_path / VOCAB_VERSION_FILE, "w") as file:
        yaml.dump(version_data, file, default_flow_style=False, sort_keys=False)


def map(phen_dir, target_code_type):
    logger.info(f"Processing phenotype: {phen_dir}")
    logger.debug(f"Target coding format: {target_code_type}")

    # Validate configuration
    validate(phen_dir)

    # initialise paths
    phen_path = Path(phen_dir)
    config_path = phen_path / CONFIG_FILE
    codes_path = phen_path / CODES_DIR

    # load configuration
    with config_path.open("r") as file:
        config = yaml.safe_load(file)
    phenotype = config["phenotype"]

    # Create output dataframe
    out = pd.DataFrame([])
    code_errors = []

    # Process each folder in codes section
    for concept_set in phenotype["concept_sets"]:
        logger.debug(f"--- {concept_set['file']} ---")

        # Load code file
        codes_file_path = Path(codes_path / concept_set["file"]["path"])
        df = read_table_file(codes_file_path)

        # process structural actions
        df = process_actions(df, concept_set)

        # Preprocessing & Validation Checks
        logger.debug("Processing and validating code formats")
        df, errors = preprocess_codes(
            df,
            concept_set,
            codes_file_path,
            target_code_type=target_code_type,
        )

        logger.debug(f"Length of errors from preprocess {len(errors)}")
        if len(errors) > 0:
            code_errors.extend(errors)
        logger.debug(f" Length of code_errors {len(code_errors)}")

        # Map
        # if processing a source coding list with categorical data
        if (
            "actions" in concept_set["file"]
            and "divide_col" in concept_set["file"]["actions"]
            and len(df) > 0
        ):
            divide_col = concept_set["file"]["actions"]["divide_col"]
            logger.debug(f"Action: Dividing Table by {divide_col}")
            logger.debug(f"column into: {df[divide_col].unique()}")
            df_grp = df.groupby(divide_col)
            for cat, grp in df_grp:
                if cat == concept_set["file"]["category"]:
                    grp = grp.drop(columns=[divide_col])  # delete categorical column
                    out = map_file(
                        grp, target_code_type, out, concept_name=concept_set["name"]
                    )
        else:
            out = map_file(df, target_code_type, out, concept_name=concept_set["name"])

    if len(code_errors) > 0:
        logger.error(f"The map processing has {len(code_errors)} errors")
        error_path = phen_path / MAP_DIR / "errors"
        error_path.mkdir(parents=True, exist_ok=True)
        error_filename = f"{target_code_type}-code-errors.csv"
        write_code_errors(code_errors, error_path / error_filename)

    # Check there is output from processing
    if len(out.index) == 0:
        logger.error(f"No output after map processing")
        raise Exception(
            f"No output after map processing, check config {str(config_path.resolve())}"
        )

    # Final processing
    out = out.reset_index(drop=True)
    out = out.drop_duplicates(subset=["CONCEPT_SET", "CONCEPT"])
    out = out.sort_values(by=["CONCEPT_SET", "CONCEPT"])

    # Save output to map directory
    output_filename = target_code_type + ".csv"
    map_path = phen_path / MAP_DIR / output_filename
    out.to_csv(map_path, index=False)
    logger.info(f"Saved mapped concepts to {str(map_path.resolve())}")

    # save concept sets as separate files
    concept_set_path = phen_path / CONCEPT_SET_DIR / target_code_type

    # empty the concept-set directory if it exists but keep the .git file
    git_items = [".git", ".gitkeep"]
    if concept_set_path.exists():
        for item in concept_set_path.iterdir():
            if item not in git_items:
                item.unlink()
    else:
        concept_set_path.mkdir(parents=True, exist_ok=True)

    # write each concept as a separate file
    for name, concept in out.groupby("CONCEPT_SET"):
        concept = concept.sort_values(by="CONCEPT")  # sort rows
        concept = concept.dropna(how="all", axis=1)  # remove empty cols
        concept = concept.reindex(
            sorted(concept.columns), axis=1
        )  # sort cols alphabetically
        filename = f"{name}.csv"
        concept_path = concept_set_path / filename
        concept.to_csv(concept_path, index=False)

    write_vocab_version(phen_path)

    logger.info(f"Phenotype processed successfully")


def publish(phen_dir):
    """Publishes updates to the phenotype by commiting all changes to the repo directory"""

    # Validate config
    validate(phen_dir)
    phen_path = Path(phen_dir)

    # load git repo and set the branch
    repo = git.Repo(phen_path)
    if DEFAULT_GIT_BRANCH in repo.branches:
        main_branch = repo.heads[DEFAULT_GIT_BRANCH]
        main_branch.checkout()
    else:
        raise AttributeError(
            f"Phen repo does not contain the default branch {DEFAULT_GIT_BRANCH}"
        )

    # check if any changes to publish
    if not repo.is_dirty() and not repo.untracked_files:
        logger.info("Nothing to publish, no changes to the repo")
        return

    # get major version from configuration file
    config_path = phen_path / CONFIG_FILE
    with config_path.open("r") as file:
        config = yaml.safe_load(file)
    match = re.match(r"v(\d+\.\d+)", config["phenotype"]["version"])
    major_version = match.group(1)

    # get latest minor version from git commit count
    commit_count = len(list(repo.iter_commits("HEAD")))

    # set version and write to config file so consistent with repo version
    next_minor_version = commit_count + 1
    version = f"v{major_version}.{next_minor_version}"
    logger.debug(f"New version: {version}")
    config["phenotype"]["version"] = version
    with open(config_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)

    # Add and commit changes to repo
    commit_message = f"Committing updates to phenotype {phen_path}"
    repo.git.add("--all")
    repo.index.commit(commit_message)

    # Create and push the tag
    if version in repo.tags:
        raise Exception(f"Tag {version} already exists in repo {phen_path}")
    repo.create_tag(version, message=f"Release {version}")
    logger.info(f"New version: {version}")

    # push to origin if a remote repo
    try:
        origin = repo.remotes.origin
        origin.push("main")
        origin.push(tags=True)
        logger.debug("Changes pushed to 'origin'.")
    except AttributeError:
        logger.debug("No remote named 'origin' found, local repo.")

    logger.info(f"Phenotype published successfully")


def export(phen_dir, version):
    """Exports a phen repo at a specific tagged version into a target directory"""
    logger.info(f"Exporting phenotype {phen_dir} at version {version}")

    # validate configuration
    validate(phen_dir)
    phen_path = Path(phen_dir)

    # load configuration
    config_path = phen_path / CONFIG_FILE
    with config_path.open("r") as file:
        config = yaml.safe_load(file)

    map_path = phen_path / MAP_DIR
    if not map_path.exists():
        logger.warning(f"Map path does not exist '{map_path}'")

    export_path = phen_path / OMOP_DIR
    # check export directory exists and if not create it
    if not export_path.exists():
        export_path.mkdir(parents=True)
        logger.debug(f"OMOP export directory '{export_path}' created.")

    # omop export db
    export_db_path = omop.export(
        map_path,
        export_path,
        config["phenotype"]["version"],
        config["phenotype"]["omop"],
    )

    # write to tables
    # export as csv
    logger.info(f"Phenotype exported successfully")


def copy(phen_dir, target_dir, version):
    """Copys a phen repo at a specific tagged version into a target directory"""

    # Validate
    validate(phen_dir)
    phen_path = Path(phen_dir)

    # Check target directory exists
    target_path = Path(target_dir)
    if not target_path.exists():
        raise FileNotFoundError(f"The target directory {target_path} does not exist")

    # Set copy directory
    copy_path = target_path / version
    logger.info(f"Copying repo {phen_path} to {copy_path}")

    if not copy_path.exists():
        # If copy directory doesn't exist, clone the repo
        logger.debug(f"Cloning repo from {phen_path} into {copy_path}...")
        repo = git.Repo.clone_from(phen_path, copy_path)
    else:
        # If copy directory exists, open the repo
        logger.debug(
            f"Copy of repository already exists in {copy_path}. Opening the repo..."
        )
        repo = git.Repo(copy_path)

    # Check out the latest commit or specified version
    if version:
        # Checkout a specific version (e.g., branch, tag, or commit hash)
        logger.info(f"Checking out version {version}...")
        repo.git.checkout(version)
    else:
        # Checkout the latest commit (HEAD)
        logger.info(f"Checking out the latest commit...")
        repo.git.checkout("HEAD")

    logger.debug(f"Copied {phen_path} {repo.head.commit.hexsha[:7]} in {copy_path}")

    logger.info(f"Phenotype copied successfully")


def diff(phen_dir, phen_old_dir):
    """Compare the differences between two versions of a phenotype"""

    # validate phenotype directories
    validate(phen_old_dir)
    validate(phen_dir)

    old_phen_path = Path(phen_old_dir)
    new_phen_path = Path(phen_dir)

    # Load report (FOR SOME REASON THIS WAS APPEND SO SET TO w for NOW)
    report_file_name = old_phen_path.name + "_diff.md"
    report_path = new_phen_path / report_file_name
    report = open(report_path, "w")
    logger.debug(f"Writing to report file {str(report_path.resolve())}")

    # Get maps files from phenotype
    old_map_path = old_phen_path / MAP_DIR
    new_map_path = new_phen_path / MAP_DIR

    # List files from output directories
    old_output_files = [
        file.name
        for file in old_map_path.iterdir()
        if file.is_file() and not file.name.startswith(".")
    ]
    new_output_files = [
        file.name
        for file in new_map_path.iterdir()
        if file.is_file() and not file.name.startswith(".")
    ]

    # Convert the lists to sets for easy comparison
    old_output_set = set(old_output_files)
    new_output_set = set(new_output_files)

    # Outputs that are in old_output_set but not in new_output_set (removed files)
    removed_outputs = old_output_set - new_output_set
    # Outputs that are in new_output_set but not in old_output_set (added files)
    added_outputs = new_output_set - old_output_set
    # Outputs that are the intersection of old_output_set and new_output_set
    common_outputs = old_output_set & new_output_set

    # Write outputs report
    new_config = new_phen_path / CONFIG_FILE
    with new_config.open("r") as file:
        new_config = yaml.safe_load(file)
    report.write(f"\n\n# Report for version {new_config['phenotype']['version']}\n\n")
    report.write(f"- Removed outputs: {list(removed_outputs)}\n")
    report.write(f"- Added outputs: {list(added_outputs)}\n")
    report.write(f"- Common outputs: {list(common_outputs)}\n")

    report.write(
        f"\n\n## Compare concepts {str(old_phen_path.resolve())} to {str(new_phen_path.resolve())}\n\n"
    )
    # Compare common outputs between versions
    for file in common_outputs:
        old_output = old_map_path / file
        new_output = new_map_path / file

        logger.debug(f"Old ouptput: {str(old_output.resolve())}")
        logger.debug(f"New ouptput: {str(new_output.resolve())}")

        df1 = pd.read_csv(old_output)
        df1 = df1[["CONCEPT", "CONCEPT_SET"]].groupby("CONCEPT_SET").count()
        df2 = pd.read_csv(new_output)
        df2 = df2[["CONCEPT", "CONCEPT_SET"]].groupby("CONCEPT_SET").count()

        # Check for added and removed concepts
        report.write(
            "- Removed concepts {}\n".format(list(set(df1.index) - set(df2.index)))
        )
        report.write(
            "- Added concepts {}\n".format(list(set(df2.index) - set(df1.index)))
        )

        # Check for changed concepts
        diff = df2 - df1  # diff in counts
        diff = diff[
            (~(diff["CONCEPT"] == 0.0)) & diff["CONCEPT"].notna()
        ]  # get non-zero counts
        s = "\n"
        if len(diff.index) > 0:
            for concept, row in diff.iterrows():
                s += "\t - {} {}\n".format(concept, row["CONCEPT"])
            report.write(f"- Changed concepts {s}\n\n")
        else:
            report.write(f"- Changed concepts []\n\n")

    logger.info(f"Phenotypes diff'd successfully")
