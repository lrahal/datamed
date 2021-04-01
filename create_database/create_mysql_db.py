import os
from typing import Dict

import pandas as pd
import pymysql
from sqlalchemy import create_engine, types

from .jade_analysis import build_api_fab_sites_dataframe
from .upload_db import upload_cis_cip_from_bdpm

# Credentials to database connection
HOSTNAME = "localhost"
DBNAME = "rs_db"
UNAME = "root"
MYSQL_PWD = os.environ.get("MYSQL_PWD")


def create_db(cursor):
    # Set connection to create new database
    print("Database {} creation...".format(DBNAME))
    cursor.execute("create database " + DBNAME)
    cursor.execute(
        "alter database "
        + DBNAME
        + " character set utf8mb4 collate utf8mb4_unicode_ci;"
    )


def connect_to_engine():
    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD
        ),
        echo=False,
    )

    engine.connect()  # connect to the database
    return engine


def create_table(df: pd.DataFrame, table_name: str, dtype: Dict = None):
    # Connect to database
    engine = connect_to_engine()

    # Convert dataframe to SQL table
    print("Table {} creation...".format(table_name))
    df.to_sql(
        table_name,
        engine,
        schema=None,
        if_exists="append",
        index=False,
        index_label=None,
        chunksize=None,
        dtype=dtype,
        method=None,
    )


def create_atc_table():
    """
    Function for table 'atc' creation in rs_db
    """
    df = pd.read_csv(
        "./create_database/data/ATC.csv",
        names=["cis", "atc", "v3"],
        delimiter=";",
        header=0,
    )

    dtypes_dict = {
        "cis": types.TEXT,
        "atc": types.TEXT,
        "v3": types.TEXT,
    }
    table_name = "atc"
    create_table(df, table_name, dtype=dtypes_dict)


def create_open_medic_table():
    """
    Function for table 'open_medic' creation in rs_db
    Colonnes 'libellé', 'rem' et 'bse' retirées car trop de problèmes d'encoding
    nbc : nb consommants
    rem : montant remboursé
    bse : base de remboursement
    boites : nb boîtes délivrées
    """
    df = pd.read_csv(
        "./create_database/data/NB_2019_cip13.csv",
        names=["cip13", "nbc", "boites"],
        delimiter=";",
        encoding="utf-8",
        header=0,
    )

    dtypes_dict = {
        "cip13": types.TEXT,
        "nbc": types.INTEGER,
        "boites": types.INTEGER,
    }
    table_name = "open_medic"
    create_table(df, table_name, dtype=dtypes_dict)


def create_cis_cip_table():
    """
    Function for table 'cis_cip' creation in rs_db
    """
    df = upload_cis_cip_from_bdpm("./create_database/data/BDPM/CIS_CIP_bdpm.txt")

    dtypes_dict = {
        "cis": types.TEXT,
        "cip7": types.TEXT,
        "libelle_presentation": types.TEXT,
        "statut_admin_presentation": types.TEXT,
        "etat_commercialisation": types.TEXT,
        "date_declaration_commercialisation": types.DATE,
        "cip13": types.TEXT,
        "agrement_collectivites": types.TEXT,
        "taux_remboursement": types.TEXT,
    }
    table_name = "cis_cip"
    create_table(df, table_name, dtype=dtypes_dict)


def main():
    path = "./create_database/data/jade_final/"
    # Load dataframe
    print("Loading dataframe from concatenated Excel files...")
    df = build_api_fab_sites_dataframe(path)

    # Check if rs_db database exists:
    connection = pymysql.connect(
        host=HOSTNAME, user=UNAME, password=MYSQL_PWD, charset="utf8mb4"
    )
    cursor = connection.cursor()
    db_exists = (
        cursor.execute(
            "select schema_name from information_schema.schemata where schema_name = '{}';".format(
                DBNAME
            )
        )
        == 1
    )
    if not db_exists:
        # Create rs_db database
        create_db(cursor)
        print("Database {} created!".format(DBNAME))

    table_name = "fabrication_sites"
    dtypes_dict = {col_name: types.TEXT for col_name in df.columns}
    create_table(df, table_name, dtypes_dict)
    print("Table {} created! Youpiyé!".format(table_name))


if __name__ == "__main__":
    main()
