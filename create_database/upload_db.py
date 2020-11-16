import os
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine


# Credentials to database connection
HOSTNAME = 'localhost'
DBNAME = 'rs_db'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def upload_table_from_db(table_name: str) -> pd.DataFrame:
    """
    Upload fabrication_sites table
    :param table_name: name of the table ('fabrication_sites' in rs_db database)
    :return: dataframe
    """
    engine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                           .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                           echo=False)

    # Load dataframe from database
    print('Start uploading fabrication_sites table in dataframe...', end='\n')
    df = pd.read_sql('SELECT * FROM {}'.format(table_name), con=engine)
    print('Finished!')
    return df


def clean_columns(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Put column fields in lower case
    """
    df[col_name] = df[col_name].apply(lambda x: x.lower().strip())
    return df


def upload_bdpm() -> pd.DataFrame:
    """
    Upload BDPM compositions database
    In http://base-donnees-publique.medicaments.gouv.fr/telechargement.php
    :return: dataframe
    """
    # Read CIS_COMPO_bdpm.txt file and put in dataframe
    col_names = ['cis', 'elem_pharma', 'code_substance', 'substance_active',
                 'dosage', 'ref_dosage', 'nature_composant', 'num_lien', 'v']
    df = pd.read_csv('./create_database/data/CIS_COMPO_bdpm.txt',
                     sep='\t', encoding='latin1', names=col_names, header=None)
    return df


def get_api_by_cis() -> Dict:
    """
    Get substance_active (API) list for each CIS
    :return: dict of list
    """
    # Load dataframe
    df_bdpm = upload_bdpm()
    # Put substance_active field in lower case
    df_bdpm = clean_columns(df_bdpm, 'substance_active')
    # List CIS codes
    cis_list = df_bdpm.cis.unique()
    # Create dict of list
    api_by_cis = {
        str(cis): list(df_bdpm[df_bdpm.cis == cis].substance_active.unique())
        for cis in cis_list
    }
    return api_by_cis
