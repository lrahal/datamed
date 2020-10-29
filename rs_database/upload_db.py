import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from jade_analysis import convert_cis

# Credentials to database connection
HOSTNAME='localhost'
DBNAME='rs_db'
UNAME='root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def upload_fab_sites(table_name='fabrication_sites'):
    """
    Upload fabrication_sites table
    :param table_name: name of the table ('fabrication_sites' in rs_db database)
    :return: dataframe
    """
    engine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                           .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                           echo=False)

    # Load dataframe from database
    print('Loading dataframe from database...')
    df = pd.read_sql('SELECT * FROM ' + table_name, con=engine)
    df.cis = df.cis.apply(lambda x: convert_cis(x))
    return df


def upload_bdpm():
    """
    Upload BDPM compositions database
    In http://base-donnees-publique.medicaments.gouv.fr/telechargement.php
    :return: dataframe
    """
    # Read CIS_COMPO_bdpm.txt file and put in dataframe
    col_names = ['cis', 'elem_pharma', 'code_substance', 'substance_active',
                 'dosage', 'ref_dosage', 'nature_composant', 'num_lien', 'v']
    df = pd.read_csv('~/Documents/GitHub/datamed/data/CIS_COMPO_bdpm.txt',
                     sep='\t', encoding='latin1', names=col_names, header=None)

    # Put substance_active field in lower case
    df.substance_active = df.substance_active.apply(lambda x: x.lower().strip())
    return df


def get_api_by_cis():
    """
    Get substance_active (API) list for each CIS
    :return: dict of list
    """
    # Load dataframe
    df = upload_bdpm()
    # List CIS codes
    cis_list = set(df.cis.unique())
    # Create dict of list
    api_by_cis = {str(cis): list(df[df.cis == cis].substance_active.unique()) for cis in cis_list}
    return api_by_cis
