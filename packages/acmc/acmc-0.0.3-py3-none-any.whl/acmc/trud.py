import os
import sys
import requests
import argparse
import shutil
import hashlib
import zipfile
import pandas as pd
import simpledbf # type: ignore
import yaml
from pathlib import Path

# setup logging
import acmc.logging_config as lc

logger = lc.setup_logger()

# Constants
FQDN = "isd.digital.nhs.uk"
VOCAB_PATH = Path("./vocab/trud")
VERSION_FILE = "trud_version.yaml"
VERSION_PATH = VOCAB_PATH / VERSION_FILE
DOWNLOADS_PATH = VOCAB_PATH / "downloads"
PROCESSED_PATH = VOCAB_PATH / "processed"


def error_exit(message):
    logger.error(message, "error")
    sys.exit(1)


def get_releases(item_id, API_KEY, latest=False):
    """Retrieve release information for an item from the TRUD API."""
    url = f"https://{FQDN}/trud/api/v1/keys/{API_KEY}/items/{item_id}/releases"
    if latest:
        url += "?latest"

    response = requests.get(url)
    if response.status_code != 200:
        error_exit(
            f"Failed to fetch releases for item {item_id}. Status code: {response.status_code}, error {response.json()['message']}. If no releases found for API key, please ensure you are subscribed to the data release and that it is not pending approval"
        )

    data = response.json()
    if data.get("message") != "OK":
        error_exit(data.get("message", "Unknown error occurred"))

    return data.get("releases", [])


def download_release_file(
    item_id, release_ordinal, release, file_json_prefix, file_type=None
):
    """Download specified file type for a given release of an item."""

    # check folder is a directory
    if not DOWNLOADS_PATH.is_dir():
        raise NotADirectoryError(
            f"Error: '{DOWNLOADS_PATH}' for TRUD resources is not a directory"
        )

    file_type = file_type or file_json_prefix
    file_url = release.get(f"{file_json_prefix}FileUrl")
    file_name = release.get(f"{file_json_prefix}FileName")
    file_destination = DOWNLOADS_PATH / file_name

    if not file_url or not file_name:
        error_exit(
            f"Missing {file_type} file information for release {release_ordinal} of item {item_id}."
        )

    logger.info(
        f"Downloading item {item_id} {file_type} file: {file_name} from {file_url} to {file_destination}"
    )
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        with open(file_destination, "wb") as f:
            f.write(response.content)
        return file_destination
    else:
        error_exit(
            f"Failed to download {file_type} file for item {item_id}. Status code: {response.status_code}"
        )


def validate_download_hash(file_destination: str, item_hash: str):
    with open(file_destination, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    logger.debug(hash)
    if hash.upper() == item_hash.upper():
        logger.debug(f"Verified hash of {file_destination} {hash}")
    else:
        error_exit(
            f"Could not validate origin of {file_destination}. The SHA-256 hash should be: {item_hash}, but got {hash} instead"
        )


def unzip_download(file_destination: str):

    # check folder is a directory
    if not DOWNLOADS_PATH.is_dir():
        raise NotADirectoryError(
            f"Error: '{DOWNLOADS_PATH}' for TRUD resoruces is not a directory"
        )

    with zipfile.ZipFile(file_destination, "r") as zip_ref:
        zip_ref.extractall(DOWNLOADS_PATH)


def extract_icd10():
    # ICD10_edition5
    file_path = (
        DOWNLOADS_PATH
        / "ICD10_Edition5_XML_20160401"
        / "Content"
        / "ICD10_Edition5_CodesAndTitlesAndMetadata_GB_20160401.xml"
    )
    df = pd.read_xml(file_path)
    df = df[["CODE", "ALT_CODE", "DESCRIPTION"]]
    df = df.rename(
        columns={"CODE": "icd10", "ALT_CODE": "icd10_alt", "DESCRIPTION": "description"}
    )
    output_path = PROCESSED_PATH / "icd10.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")


def extract_opsc4():
    file_path = (
        DOWNLOADS_PATH
        / "OPCS410 Data files txt"
        / "OPCS410 CodesAndTitles Nov 2022 V1.0.txt"
    )

    df = pd.read_csv(file_path, sep="\t", dtype=str, header=None)
    df = df.rename(columns={0: "opcs4", 1: "description"})

    output_path = PROCESSED_PATH / "opcs4.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")


def extract_nhs_data_migrations():
    # NHS Data Migrations

    # snomed only
    file_path = (
        DOWNLOADS_PATH
        / "Mapping Tables"
        / "Updated"
        / "Clinically Assured"
        / "sctcremap_uk_20200401000001.txt"
    )
    df = pd.read_csv(file_path, sep="\t")
    df = df[["SCT_CONCEPTID"]]
    df = df.rename(columns={"SCT_CONCEPTID": "snomed"})
    df = df.drop_duplicates()
    df = df.astype(str)

    output_path = PROCESSED_PATH / "snomed.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r2 -> r3
    file_path = (
        DOWNLOADS_PATH
        / "Mapping Tables"
        / "Updated"
        / "Clinically Assured"
        / "rctctv3map_uk_20200401000001.txt"
    )
    df = pd.read_csv(file_path, sep="\t")
    df = df[["V2_CONCEPTID", "CTV3_CONCEPTID"]]
    df = df.rename(columns={"V2_CONCEPTID": "read2", "CTV3_CONCEPTID": "read3"})

    output_path = PROCESSED_PATH / "read2_to_read3.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r3->r2
    file_path = (
        DOWNLOADS_PATH
        / "Mapping Tables"
        / "Updated"
        / "Clinically Assured"
        / "ctv3rctmap_uk_20200401000002.txt"
    )
    df = pd.read_csv(file_path, sep="\t")
    df = df[["CTV3_CONCEPTID", "V2_CONCEPTID"]]
    df = df.rename(columns={"CTV3_CONCEPTID": "read3", "V2_CONCEPTID": "read2"})
    df = df.drop_duplicates()
    df = df[~df["read2"].str.match("^.*_.*$")]  # remove r2 codes with '_'

    output_path = PROCESSED_PATH / "read3_to_read2.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r2 -> snomed
    file_path = (
        DOWNLOADS_PATH
        / "Mapping Tables"
        / "Updated"
        / "Clinically Assured"
        / "rcsctmap2_uk_20200401000001.txt"
    )
    df = pd.read_csv(file_path, sep="\t", dtype=str)
    df = df[["ReadCode", "ConceptId"]]
    df = df.rename(columns={"ReadCode": "read2", "ConceptId": "snomed"})

    output_path = PROCESSED_PATH / "read2_to_snomed.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r3->snomed
    file_path = (
        DOWNLOADS_PATH
        / "Mapping Tables"
        / "Updated"
        / "Clinically Assured"
        / "ctv3sctmap2_uk_20200401000001.txt"
    )
    df = pd.read_csv(file_path, sep="\t", dtype=str)
    df = df[["CTV3_TERMID", "SCT_CONCEPTID"]]
    df = df.rename(columns={"CTV3_TERMID": "read3", "SCT_CONCEPTID": "snomed"})
    df["snomed"] = df["snomed"].astype(str)
    df = df[~df["snomed"].str.match("^.*_.*$")]  # remove snomed codes with '_'

    output_path = PROCESSED_PATH / "read3_to_snomed.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")


def extract_nhs_read_browser():
    # r2 only
    input_path = DOWNLOADS_PATH / "Standard" / "V2" / "ANCESTOR.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = pd.concat([df["READCODE"], df["DESCENDANT"]])
    df = pd.DataFrame(df.drop_duplicates())
    df = df.rename(columns={0: "read2"})
    output_path = PROCESSED_PATH / "read2.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r2 -> atc
    input_path = DOWNLOADS_PATH / "Standard" / "V2" / "ATC.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = df[["READCODE", "ATC"]]
    df = df.rename(columns={"READCODE": "read2", "ATC": "atc"})
    output_path = PROCESSED_PATH / "read2_to_atc.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r2 -> icd10
    input_path = DOWNLOADS_PATH / "Standard" / "V2" / "ICD10.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = df[["READ_CODE", "TARG_CODE"]]
    df = df.rename(columns={"READ_CODE": "read2", "TARG_CODE": "icd10"})
    df = df[~df["icd10"].str.match("^.*-.*$")]  # remove codes with '-'
    df = df[~df["read2"].str.match("^.*-.*$")]  # remove codes with '-'
    output_path = PROCESSED_PATH / "read2_to_icd10.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r2 -> opcs4
    input_path = DOWNLOADS_PATH / "Standard" / "V2" / "OPCS4V3.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = df[["READ_CODE", "TARG_CODE"]]
    df = df.rename(columns={"READ_CODE": "read2", "TARG_CODE": "opcs4"})
    df = df[~df["opcs4"].str.match("^.*-.*$")]  # remove codes with '-'
    df = df[~df["read2"].str.match("^.*-.*$")]  # remove codes with '-'
    output_path = PROCESSED_PATH / "read2_to_opcs4.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r3 only
    input_path = DOWNLOADS_PATH / "Standard" / "V3" / "ANCESTOR.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = pd.concat([df["READCODE"], df["DESCENDANT"]])
    df = pd.DataFrame(df.drop_duplicates())
    df = df.rename(columns={0: "read3"})
    output_path = PROCESSED_PATH / "read3.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r3 -> icd10
    input_path = DOWNLOADS_PATH / "Standard" / "V3" / "ICD10.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = df[["READ_CODE", "TARG_CODE"]]
    df = df.rename(columns={"READ_CODE": "read3", "TARG_CODE": "icd10"})
    df = df[~df["icd10"].str.match("^.*-.*$")]  # remove codes with '-'
    df = df[~df["read3"].str.match("^.*-.*$")]  # remove codes with '-'
    output_path = PROCESSED_PATH / "read3_to_icd10.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")

    # r3 -> icd9
    # dbf = simpledbf.Dbf5('build/maps/downloads/Standard/V3/ICD9V3.DBF')

    # r3 -> opcs4
    input_path = DOWNLOADS_PATH / "Standard" / "V3" / "OPCS4V3.DBF"
    df = simpledbf.Dbf5(input_path).to_dataframe()
    df = df[["READ_CODE", "TARG_CODE"]]
    df = df.rename(columns={"READ_CODE": "read3", "TARG_CODE": "opcs4"})
    df = df[~df["opcs4"].str.match("^.*-.*$")]  # remove codes with '-'
    df = df[~df["read3"].str.match("^.*-.*$")]  # remove codes with '-'
    output_path = PROCESSED_PATH / "read3_to_opcs4.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"Extracted: {output_path}")


def create_map_directories():
    """Create map directories."""

    # Check if build directory exists
    create_map_dirs = False
    if VOCAB_PATH.exists():
        user_input = (
            input(
                f"The map directory {VOCAB_PATH} already exists. Do you want to download and process trud data again? (y/n): "
            )
            .strip()
            .lower()
        )
        if user_input == "y":
            # delete all build files
            shutil.rmtree(VOCAB_PATH)
            create_map_dirs = True
        elif user_input == "n":
            logger.info("Exiting TRUD installation")
            sys.exit(0)
    else:
        create_map_dirs = True

    if create_map_dirs:
        # create maps directories
        VOCAB_PATH.mkdir(parents=True, exist_ok=True)
        DOWNLOADS_PATH.mkdir(parents=True, exist_ok=True)
        PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


def install():
    logger.info(f"Installing TRUD")

    # get TRUD api key from environment variable
    api_key = os.getenv("ACMC_TRUD_API_KEY")
    if not api_key:
        raise ValueError(
            "TRUD API KEY not found. Set the ACMC_TRUD_API_KEY environment variable."
        )

    create_map_directories()

    items_latest = True
    items = [
        {
            "id": 259,
            "name": "NHS ICD-10 5th Edition XML data files",
            "hash": "A4F7BBA6E86349AADD0F4696C5E91152EB99CC06121427FC359160439B9F883F",
            "extract": extract_icd10,
        },
        {
            "id": 119,
            "name": "OPCS-4 data files",
            "hash": "0615A2BF43FFEF94517F1D1E0C05493B627839F323F22C52CBCD8B40BF767CD3",
            "extract": extract_opsc4,
        },
        {
            "id": 9,
            "name": "NHS Data Migration",
            "hash": "D4317B3ADBA6E1247CF17F0B7CD2B8850FD36C0EA2923BF684EA6159F3A54765",
            "extract": extract_nhs_data_migrations,
        },
        {
            "id": 8,
            "name": "NHS Read Browser",
            "hash": "1FFF2CBF11D0E6D7FC6CC6F13DD52D2F459095C3D83A3F754E6C359F16913C5E",
            "extract": extract_nhs_read_browser,
        },
        # TODO: Download BNF from separate site? https://www.nhsbsa.nhs.uk/sites/default/files/2024-10/BNF%20Snomed%20Mapping%20data%2020241016.zip
    ]

    # remove function from items to save versions
    data = [{k: v for k, v in d.items() if k != "extract"} for d in items]
    # save TRUD versions to file to main record of what was downloaded
    with open(VERSION_PATH, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    # Validate and process each item ID
    for item in items:
        item_id = item["id"]
        logger.info(f"--- {item['name']} ---")

        releases = get_releases(item_id, API_KEY=api_key, latest=items_latest)
        if not releases:
            error_exit(f"No releases found for item {item_id}.")

        # Process each release in reverse order
        for release_ordinal, release in enumerate(releases[::-1], 1):
            # Download archive file
            file_destination = download_release_file(
                item_id, release_ordinal, release, "archive"
            )

            # Optional files
            # if items.checksum:
            #     download_release_file(item["id"], release_ordinal, release, "checksum")
            # if items.signature:
            #     download_release_file(item["id"], release_ordinal, release, "signature")
            # if items.public_key:
            #     download_release_file(item["id"], release_ordinal, release, "publicKey", "public key")

            # Verify Hash if available
            if "hash" in item:
                validate_download_hash(file_destination, item["hash"])

            # Unzip downloaded .zip
            unzip_download(file_destination)

            # Extract Tables to parquet
            if "extract" in item:
                item["extract"]()

        logger.info(f"Downloaded {release_ordinal} release(s) for item {item_id}.")

    logger.info(f"TRUD installation completed")
