import os
import argparse
import sqlite3
import pandas as pd
import logging
import zipfile
import shutil
import json
import yaml
from pathlib import Path

from acmc import logging_config

# setup logging
logger = logging_config.setup_logger()

# constants
VOCAB_PATH = Path("./vocab/omop")
DB_PATH = VOCAB_PATH / "omop_54.sqlite"
VERSION_FILE = "omop_version.yaml"
VERSION_PATH = VOCAB_PATH / VERSION_FILE
EXPORT_FILE = "omop_export.db"

vocabularies = {
    "source": "OHDSI Athena",
    "url": "https://athena.ohdsi.org/vocabulary/list",
    "version": "",
    "vocabularies": [
        {"id": 1, "name": "SNOMED"},
        {"id": 2, "name": "ICD9CM"},
        {"id": 17, "name": "Readv2"},
        {"id": 21, "name": "ATC"},
        {"id": 55, "name": "OPCS4"},
        {"id": 57, "name": "HES Specialty"},
        {"id": 70, "name": "ICD10CM"},
        {"id": 75, "name": "dm+d"},
        {"id": 144, "name": "UK Biobank"},
        {"id": 154, "name": "NHS Ethnic Category"},
        {"id": 155, "name": "NHS Place of Service"},
    ],
    "tables": [],
}

omop_vocab_types = {
    "read2": "Read",
    "read3": None,
    "icd10": "ICD10CM",
    "snomed": "SNOMED",
    "opcs4": "OPCS4",
    "atc": "ATC",
    "med": None,
    "cprd": None,
}


# Populate SQLite3 Database with default OMOP CONCEPTS
def install(omop_zip_file, version):
    """Installs the OMOP release csv files in a file-based sql database"""
    logger.info(f"Installing OMOP from zip file: {omop_zip_file}")
    omop_zip_path = Path(omop_zip_file)

    # Check if the file exists and is a ZIP file
    if not omop_zip_path.exists():
        msg = f"{omop_zip_path} does not exist."
        logger.error(msg)
        raise ValueError(msg)
    if not zipfile.is_zipfile(omop_zip_path):
        msg = f"Error: {omop_zip_path} is not a valid ZIP file."
        logger.error(msg)
        raise ValueError(msg)

    # check codes directory exists and if not create it
    if not VOCAB_PATH.exists():
        VOCAB_PATH.mkdir(parents=True)
        logger.debug(f"OMOP directory '{VOCAB_PATH}' created.")
    else:
        # removing existing OMOP files
        csv_files = list(VOCAB_PATH.glob("*.csv"))
        for file in csv_files:
            file.unlink()
            logger.debug(f"Deleted OMOP csv file: {file}")

    # Extract ZIP contents
    with zipfile.ZipFile(omop_zip_path, "r") as zip_ref:
        zip_ref.extractall(VOCAB_PATH)
        logger.info(f"Extracted OMOP zip file {omop_zip_path} to {VOCAB_PATH}/")

    # connect to database, if it does not exist it will be created
    conn = sqlite3.connect(DB_PATH)
    # Iterate through files in the folder
    csv_files = list(VOCAB_PATH.glob("*.csv"))
    total_tables_count = len(csv_files)
    table_count = 1
    for filename in csv_files:
        try:
            logger.info(
                f"Processing {table_count} of {total_tables_count} tables: {filename}"
            )
            # read the CSV file with the specified delimiter
            df = pd.read_csv(filename, delimiter="\t", low_memory=False)

            # export Table to sqlite db
            df.to_sql(filename.stem, conn, if_exists="replace", index=False)

            # add to the metadata
            vocabularies["tables"].append(filename.stem)
            table_count = table_count + 1
        except Exception as e:
            raise Exception(f"Error reading file {filename}: {e}")

    conn.close()

    # write version file
    write_version_file(version)

    logger.info(f"OMOP installation completed")


def write_version_file(version):
    """Writes the OMOP vocaburaries and version to a file"""
    vocabularies["version"] = version
    with open(VERSION_PATH, "w") as file:
        yaml.dump(vocabularies, file, default_flow_style=False, sort_keys=False)


def clear(db_path):
    """Clears the OMOP sql database"""
    logger.info(f"Clearing OMOP data from database")
    omop_db_path = Path(db_path)
    if not omop_db_path.is_file():
        raise FileNotFoundError(f"Error: OMOP DB file '{omop_db_path}' does not exist.")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch and print table names
    tables = cur.fetchall()
    logger.debug("Tables in database:", [table[0] for table in tables])

    # cur.execute("DROP TABLE CONCEPT_SET;")
    # cur.execute("DROP TABLE CONCEPT_SET_ITEM;")

    conn.close()
    logger.info(f"OMOP database cleared")


def delete(db_path):
    """Deletes the OMOP sql database"""
    logger.info(f"Deleting OMOP database")
    omop_db_path = Path(db_path)
    if not omop_db_path.is_file():
        raise FileNotFoundError(f"Error: OMOP DB file '{omop_db_path}' does not exist.")

    omop_db_path.unlink()
    logger.info(f"OMOP database deleted")


def table_exists(cursor, table_name):
    # Query to check if the table exists
    cursor.execute(
        """
		SELECT name
		FROM sqlite_master
		WHERE type='table' AND name=?
		""",
        (table_name,),
    )

    # Fetch the result
    result = cursor.fetchone()

    return result is not None


def vocab_exists(cursor, vocab_id):
    # Query to check if the table exists
    cursor.execute(
        """
		SELECT vocabulary_id 
		FROM VOCABULARY
		WHERE vocabulary_id=?
		""",
        (vocab_id,),
    )

    # Fetch the result
    result = cursor.fetchone()

    return result is not None


def concept_set_exist(cursor, concept_set_name):

    query = f"SELECT EXISTS (SELECT 1 FROM CONCEPT_SET WHERE concept_set_name = ?)"
    cursor.execute(query, (concept_set_name,))

    # 1 if exists, 0 otherwise
    return cursor.fetchone()[0] == 1


def export(map_path, export_path, version, omop_metadata):
    logger.debug(f"exporting with metadata {omop_metadata} at version {version}")

    # copy the baseline omop database
    export_db_path = export_path / EXPORT_FILE
    shutil.copy(DB_PATH, export_db_path)

    # connect to db
    conn = sqlite3.connect(export_db_path)
    cur = conn.cursor()

    # Create VOCABULARY
    df_test = pd.DataFrame(
        [
            {
                "vocabulary_id": omop_metadata["vocabulary_id"],
                "vocabulary_name": omop_metadata["vocabulary_name"],
                "vocabulary_reference": omop_metadata["vocabulary_reference"],
                "vocabulary_version": version,
                # "vocabulary_concept_id": 0,
            }
        ]
    )
    df_test.to_sql("VOCABULARY", conn, if_exists="append", index=False)

    # Create CONCEPT_SET
    cur.execute(
        """
	CREATE TABLE CONCEPT_SET (
		concept_set_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for each concept set
		atlas_id INTEGER,                                -- Unique identifier generated by ATLAS
		concept_set_name TEXT,                           -- Optional name for the concept set
		concept_set_description TEXT,                    -- Optional description for the concept set
		vocabulary_id TEXT NOT NULL,                     -- Foreign key to VOCABULARY table
		FOREIGN KEY (vocabulary_id) REFERENCES VOCABULARY(vocabulary_id)
	);"""
    )

    # Create CONCEPT_SET_ITEM
    cur.execute(
        """
	CREATE TABLE CONCEPT_SET_ITEM (
		concept_set_item_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for each mapping
		concept_set_id INTEGER NOT NULL,                      -- Foreign key to CONCEPT_SET table
		concept_id INTEGER NOT NULL,                          -- Foreign key to CONCEPT table
		FOREIGN KEY (concept_set_id) REFERENCES CONCEPT_SET(concept_set_id),
		FOREIGN KEY (concept_id) REFERENCES CONCEPT(concept_id)
	);"""
    )

    # read map files
    map_files = list(map_path.glob("*.csv"))
    total = len(map_files)
    logger.info(f"Exporting {total} map files")
    for index, map_file in enumerate(map_files):
        logger.info(f"Processing {index+1} of {total}: {map_file}")
        df = pd.read_csv(map_file)

        for concept_set_name, grp in df.groupby("CONCEPT_SET"):

            # create Concept_Set
            if not concept_set_exist(cur, concept_set_name):
                cur.execute(
                    f"INSERT INTO CONCEPT_SET (concept_set_name, vocabulary_id) VALUES ('{concept_set_name}', '{omop_metadata['vocabulary_id']}');"
                )
            else:
                logger.debug(f"Concept_set {concept_set_name} already exists")
                # TODO: ask to remove old concept_set?

            # get Concept_set_Id
            query = "SELECT concept_set_id FROM CONCEPT_SET WHERE concept_set_name = ? AND vocabulary_id = ?;"
            target_code_type = map_file.stem
            cur.execute(
                query,
                (
                    concept_set_name,
                    omop_metadata["vocabulary_id"],
                ),
            )
            # FAILS HERE WITH NONE REUR
            logger.debug(f"target code type {target_code_type}")
            logger.debug(f"omop code type {omop_vocab_types[target_code_type]}")
            concept_set_id = cur.fetchone()[0]
            logger.debug(f"concept set id {concept_set_id}")

            # get corresponing Concept_id (OMOP) for each Concept_code (e.g. SNOMED)
            concept_codes = "'" + "', '".join(list(grp["CONCEPT"].astype(str))) + "'"
            query = f"SELECT concept_id FROM CONCEPT WHERE vocabulary_id = ? AND concept_code IN ({concept_codes});"
            cur.execute(query, (omop_vocab_types[target_code_type],))
            df_out = pd.DataFrame(cur.fetchall(), columns=["concept_id"])

            if not len(grp) == len(df_out):
                logger.error(
                    f"ERROR: Some {omop_vocab_types[target_code_type]} Codes do not exist in OMOP Database"
                )

            # Create Concept_set_item
            df_out["concept_set_id"] = concept_set_id
            df_out.to_sql("CONCEPT_SET_ITEM", conn, if_exists="append", index=False)

    # Output all tables to CSV
    # Get the list of all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()  # List of tables

    # Export each table to a separate CSV file
    for table in tables:
        table_name = table[0]  # Extract table name
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        output_file = f"{table_name}.csv"
        output_path = export_path / output_file
        df.to_csv(output_path, index=False)  # Save as CSV
        logger.info(f"Exported {table_name} to {table_name}.csv")

    conn.close()

    logger.debug(f"Created export db successfully")

    return export_db_path

    return export_db_path
