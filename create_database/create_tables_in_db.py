import os
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import sessionmaker

from .models import connect_db, Specialite, SubstanceActive, Presentation, Consommation, Fabrication, Production
from .upload_db import (upload_table_from_db, upload_cis_from_rsp, upload_compo_from_rsp, upload_cis_cip_from_bdpm)

# Credentials to database connection
HOSTNAME = 'localhost'
DBNAME = 'rs_db'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def get_api_list(df: pd.DataFrame) -> List[Dict]:
    api_list = df.substance_active_match.unique().tolist()

    df_cis_compo = upload_compo_from_rsp('./create_database/data/COMPO_RSP.txt')
    api_list.extend([api for api in df_cis_compo.substance_active.unique() if api not in api_list])
    api_list = list(filter(None, api_list))
    api_list = sorted(api_list)
    values_list = [{'name': api} for api in api_list]
    return values_list


def get_cis_list(df: pd.DataFrame) -> List[Dict]:
    cis_list = df.cis.unique().tolist()

    df_cis_compo = upload_cis_from_rsp('./create_database/data/CIS_RSP.txt')
    cis_list.extend([str(cis) for cis in df_cis_compo.cis.unique() if str(cis) not in cis_list])
    cis_list = list(filter(None, cis_list))
    cis_list = sorted(cis_list)
    values_list = [{'cis': cis} for cis in cis_list]
    return values_list


def get_pres_list() -> List[Dict]:
    df = upload_cis_cip_from_bdpm('./create_database/data/CIS_CIP_bdpm.txt')
    # df = df[~df.cip13.isna()]
    # df = df.astype({'cip13': int})
    df_records = df.to_dict('records')

    values_list = [{k: str(v) for k, v in zip(('cis', 'cip13'), (d['cis'], d['cip13']))} for d in df_records]
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
    df_records = df.to_dict('records')
    return [
        {
            k: v for k, v in zip(('address', 'latitude', 'longitude', 'country'),
                                 (d['input_string'], d['latitude'], d['longitude'], d['country']))
        }
        for d in df_records
    ]


def get_prod_list(df: pd.DataFrame) -> List[Dict]:
    df_records = df.to_dict('records')
    values_list = [
        {
            k: v for k, v in zip(('cis', 'substance_active', 'address'),
                                 (d['cis'], d['substance_active'], d['sites_fabrication_substance_active']))
        }
        for d in df_records
        if all((d['cis'], d['substance_active'], d['sites_fabrication_substance_active']))
    ]
    return [dict(t) for t in {tuple(d.items()) for d in values_list}]


db = connect_db()  # establish connection
Session = sessionmaker(bind=db)
session = Session()


def save_to_database_ORM(session):
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
