import os
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import sessionmaker

from .jade_analysis import build_api_fab_sites_dataframe
from .models import connect_db, Specialite, SubstanceActive, Presentation, Consommation, Fabrication, Production
from .transform_db import compute_best_matches
from .upload_db import upload_table_from_db, upload_cis_from_rsp, upload_compo_from_rsp, upload_cis_cip_from_bdpm

# Credentials to database connection
HOSTNAME = 'localhost'
DBNAME = 'rs_db'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def get_api_by_cis() -> Dict:
    """
    Get substance_active (API) list for each CIS
    :return: dict of list
    """
    # Load dataframe
    df = upload_compo_from_rsp('./create_database/data/RSP/COMPO_RSP.txt')
    # List CIS codes
    cis_list = df.cis.unique()
    return {
        str(cis): list(df[df.cis == cis].substance_active.unique())
        for cis in cis_list
    }


def get_excels_df() -> pd.DataFrame:
    """
    Concatenate Excel files
    Compute cosine similarity
    :return:
    """
    path = './create_database/data/jade_final/'
    # Load dataframe
    print('Loading dataframe from concatenated Excel files...')
    df = build_api_fab_sites_dataframe(path)

    # Get api by CIS from RSP COMPO.txt file
    api_by_cis = get_api_by_cis()

    # Compute best match api using RSP
    best_match_list = compute_best_matches(df, api_by_cis)
    df_match = pd.DataFrame(best_match_list)
    df_match.to_csv('./create_database/data/best_match_api.csv', index=False, sep=';')
    print('best_match_api.csv printed!')

    best_match_dict = {(m['cis'], m['excel']): {'api_rsp': m['rsp'], 'cos_sim': m['cos_sim']} for m in best_match_list}
    df['substance_active_match'] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]['api_rsp']
        if (x.cis, x.substance_active) in best_match_dict else x.substance_active, axis=1)
    df['cos_sim'] = df['substance_active_match'] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]['cos_sim']
        if (x.cis, x.substance_active) in best_match_dict else None, axis=1)
    return df


def get_api_list(df: pd.DataFrame) -> List[Dict]:
    api_list = df.substance_active_match.unique().tolist()

    df_api = upload_compo_from_rsp('./create_database/data/RSP/COMPO_RSP.txt')
    api_list.extend([api for api in df_api.substance_active.unique() if api not in api_list])
    api_list = list(filter(None, api_list))
    api_list = sorted(api_list)
    values_list = [{'name': api} for api in api_list]
    return values_list


def get_cis_list(df: pd.DataFrame) -> List[Dict]:
    cis_list = df.cis.unique().tolist()

    df_cis = upload_cis_from_rsp('./create_database/data/RSP/CIS_RSP.txt')
    cis_list.extend([str(cis) for cis in df_cis.cis.unique() if str(cis) not in cis_list])
    cis_list = list(filter(None, cis_list))
    cis_list = sorted(cis_list)
    values_list = [{'cis': cis} for cis in cis_list]
    return values_list


def get_pres_list() -> List[Dict]:
    """
    CIS/CIP correspondence not found in RSP, but exists in BDPM
    """
    df = upload_cis_cip_from_bdpm('./create_database/data/CIS_CIP_bdpm.txt')
    # df = df[~df.cip13.isna()]
    # df = df.astype({'cip13': int})
    records = df.to_dict('records')

    values_list = [{k: str(v) for k, v in zip(('cis', 'cip13'), (r['cis'], r['cip13']))} for r in records]
    return values_list


def get_conso_list() -> List[Dict]:
    df = pd.read_csv('./create_database/data/NB_2019_cip13.csv',
                     names=['cip13', 'nb_conso', 'nb_boites'], delimiter=';', header=0)
    df['year'] = 2019
    df = df.astype({'cip13': str})
    values_list = df.to_dict(orient='records')
    return values_list


def get_fabrication_list() -> List[Dict]:
    df = upload_table_from_db('api_sites_addresses')
    df = df.where(pd.notnull(df), None)
    values_list = [
        {
            k: v for k, v in zip(('address', 'latitude', 'longitude', 'country'),
                                 (row['input_string'], row['latitude'], row['longitude'], row['country']))
        }
        for index, row in df.iterrows()
    ]
    return [dict(t) for t in {tuple(d.items()) for d in values_list}]


def get_prod_list(df: pd.DataFrame) -> List[Dict]:
    """
    Create table listing all possible occurences of (cis, substance_active, address)
    """
    # Load substance_active table and join with dataframe
    df_api = pd.read_sql_table('substance_active', connection)
    df = df.merge(df_api, how='left', left_on='substance_active', right_on='name')
    df = df.rename(columns={'id': 'substance_active_id'})

    # Load fabrication table and join with dataframe
    # df_fab = pd.read_sql_table('fabrication', connection)
    df = df.merge(df_fab, how='left', left_on='sites_fabrication_substance_active', right_on='address')
    df = df.rename(columns={'id': 'fabrication_id'})

    # Replace NaN values with None
    df = df.where(df.notnull(), None)

    values_list = [
        {
            k: v for k, v in zip(('cis', 'substance_active_id', 'fabrication_id'),
                                 (row['cis'], int(row['substance_active_id']), int(row['fabrication_id'])))
        }
        for index, row in df.iterrows()
        if all((row['cis'], row['substance_active_id'], row['fabrication_id']))
    ]
    return [dict(t) for t in {tuple(d.items()) for d in values_list}]


# def get_atc_list() -> List[Dict]:
#     df = pd.read_csv('./create_database/data/ATC.csv', names=['cis', 'atc', 'v3'], delimiter=';', header=0)
#     df = df.drop_duplicates()



db = connect_db()  # establish connection
connection = db.connect()
Session = sessionmaker(bind=db)
session = Session()


def save_to_database_orm(session):
    # df = get_excels_df()

    df = upload_table_from_db('fabrication_sites')
    df['substance_active_match'] = df.apply(
        lambda x: x.substance_active if not x.substance_active_match else x.substance_active_match, axis=1)

    # Création table Specialite
    cis_list = get_cis_list(df)
    for cis_dict in cis_list:
        spe = Specialite(**cis_dict)
        session.add(spe)
        session.commit()

    # Création table SubstanceActive
    api_list = get_api_list(df)
    for api_dict in api_list:
        api = SubstanceActive(**api_dict)
        session.add(api)
        session.commit()

    # Création table Presentation
    pres_list = get_pres_list()
    for pres_dict in pres_list:
        pres = Presentation(**pres_dict)
        session.add(pres)
        session.commit()

    # Création table Consommation
    conso_list = get_conso_list()
    cip13_set = set(c['cip13'] for c in pres_list)
    for conso_dict in conso_list:
        if conso_dict['cip13'] in cip13_set:
            conso = Consommation(**conso_dict)
            session.add(conso)
            session.commit()

    # Création table Fabrication
    fab_list = get_fabrication_list()
    for fab_dict in fab_list:
        fab = Fabrication(**fab_dict)
        session.add(fab)
        session.commit()

    # Création table Production
    prod_list = get_prod_list(df)
    for prod_dict in prod_list:
        prod = Production(**prod_dict)
        session.add(prod)
        session.commit()
