import os
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import sessionmaker

from .jade_analysis import build_api_fab_sites_dataframe
from .models import (connect_db, Specialite, SubstanceActive, Presentation, Consommation, Fabrication, Production,
                     Classification, Ruptures, Ventes)
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
    df = upload_compo_from_rsp('/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/COMPO_RSP.txt')
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
    path = '/Users/ansm/Documents/GitHub/datamed/create_database/data/jade_final/'
    # Load dataframe
    print('Loading dataframe from concatenated Excel files...')
    df = build_api_fab_sites_dataframe(path)

    # Get api by CIS from RSP COMPO.txt file
    api_by_cis = get_api_by_cis()

    # Compute best match api using RSP
    best_match_list = compute_best_matches(df, api_by_cis)
    df_match = pd.DataFrame(best_match_list)
    df_match.to_csv('/Users/ansm/Documents/GitHub/datamed/create_database/data/best_match_api.csv', index=False, sep=';')
    print('best_match_api.csv printed!')

    best_match_dict = {(m['cis'], m['excel']): {'api_rsp': m['rsp'], 'cos_sim': m['cos_sim']} for m in best_match_list}
    df['substance_active_match'] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]['api_rsp']
        if (x.cis, x.substance_active) in best_match_dict else x.substance_active, axis=1)
    df['cos_sim'] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]['cos_sim']
        if (x.cis, x.substance_active) in best_match_dict else None, axis=1)
    df = df.drop(['substance_active'], axis=1)
    df = df.rename(columns={'substance_active_match': 'substance_active'})
    df = df.dropna(subset=['cis', 'substance_active', 'sites_fabrication_substance_active'])
    df = df.drop_duplicates(subset=['cis', 'substance_active', 'sites_fabrication_substance_active'])
    return df


def get_api_list(df: pd.DataFrame) -> List[Dict]:
    """
    Table substance_active
    """
    df_api = upload_compo_from_rsp('/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/COMPO_RSP.txt')

    api_list = [{'name': r['substance_active'], 'code': r['code_substance']} for idx, r in df_api.iterrows()]

    api_not_in_list = [api for api in df.substance_active.unique() if api not in df_api.substance_active.unique()]
    api_list.extend([{'name': api, 'code': None} for api in api_not_in_list])
    api_list = [dict(t) for t in {tuple(d.items()) for d in api_list}]
    return sorted(api_list, key=lambda k: k['name'])


def get_cis_list(df: pd.DataFrame) -> List[Dict]:
    """
    Table specialite, listing all possible CIS codes
    """
    df_cis = upload_cis_from_rsp('./create_database/data/RSP/CIS_RSP.txt')
    df_cis = df_cis.astype({'cis': 'str'})
    records = df_cis.to_dict('records')
    cis_list = df_cis.cis.dropna().unique().tolist()
    values_list = [
        {k: str(v) for k, v in zip(('cis', 'name', 'type_amm', 'etat_commercialisation'),
                                   (r['cis'], r['nom_spe_pharma'], r['type_amm'], r['etat_commercialisation']))}
        for r in records
    ]
    values_list.extend([{'cis': str(cis), 'name': None} for cis in df.cis.dropna().unique() if str(cis) not in cis_list])
    return values_list


def get_pres_list() -> List[Dict]:
    """
    Table listing all possible presentations (CIP13), with corresponding CIS code
    From BDPM
    (In RSP, some CIP13 are linked to multiple CIS, ex: 3400936432826 -> 60197246 & 69553494)
    """
    df = upload_cis_cip_from_bdpm('./create_database/data/BDPM/CIS_CIP_bdpm.txt')
    records = df.to_dict('records')

    return [
        {k: str(v) for k, v in zip(('cis', 'cip13', 'libelle'),
                                   (r['cis'], r['cip13'], r['libelle_presentation']))
         }
        for r in records
    ]


def get_conso_list() -> List[Dict]:
    df = pd.read_excel('./create_database/data/donnees_ventes_2018.xlsx')
    df_grouped = df.groupby(['cis', 'year']).agg(
        {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
    )
    df_grouped = df_grouped.reset_index()
    df_grouped = df_grouped.astype({'cis': str})
    return df_grouped.to_dict(orient='records')


def get_fabrication_list() -> List[Dict]:
    """
    Table fabrication
    Lists for each address, the latitude, longitude and country
    """
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
    df_fab = pd.read_sql_table('fabrication', connection)
    df = df.merge(df_fab, how='left', left_on='sites_fabrication_substance_active', right_on='address')
    df = df.rename(columns={'id': 'fabrication_id'})

    # Replace NaN values with None
    df = df.where(df.notnull(), None)

    return [
        {
            k: v for k, v in zip(('cis', 'substance_active_id', 'fabrication_id', 'substance_active',
                                  'sites_fabrication_substance_active', 'denomination_specialite', 'dci', 'type_amm',
                                  'titulaire_amm', 'sites_production', 'sites_conditionnement_primaire',
                                  'sites_conditionnement_secondaire', 'sites_importation', 'sites_controle',
                                  'sites_echantillotheque', 'sites_certification', 'mitm', 'pgp', 'filename'),
                                 (row['cis'], int(row['substance_active_id']), int(row['fabrication_id']),
                                  row['substance_active'], row['sites_fabrication_substance_active'],
                                  row['denomination_specialite'], row['dci'], row['type_amm'], row['titulaire_amm'],
                                  row['sites_production'], row['sites_conditionnement_primaire'],
                                  row['sites_conditionnement_secondaire'], row['sites_importation'],
                                  row['sites_controle'], row['sites_echantillotheque'], row['sites_certification'],
                                  row['mitm'], row['pgp'], row['filename']))
        }
        for index, row in df.iterrows()
    ]


def get_atc_list() -> List[Dict]:
    """
    Table classification
    Listing all CIS and their possible ATC classification
    """
    df = pd.read_excel('./create_database/data/ATC_new.xlsx', names=['cis', 'atc'], header=0)
    df = df.drop_duplicates()
    df = df.astype({'cis': str})

    # Not allow records having CIS not present in specialite table
    df_cis = pd.read_sql_table('specialite', connection)
    cis_list = df_cis.cis.unique()
    df = df[df.cis.isin(cis_list)]
    return df.to_dict(orient='records')


def get_ruptures() -> List[Dict]:
    """
    Table ruptures
    """
    df = pd.read_excel('analysis/data/decret_stock/décret stock.xlsx', header=0, sheet_name='Raw')

    # Cleaning
    df = df[['ID_Signal', 'Signalement', 'Date Signalement', 'Laboratoire', 'Spécialité', 'Rupture', 'ATC', 'DCI',
             'Date_Signal_Debut_RS', 'Durée_Ville', 'Durée_Hôpital', 'DatePrevi_Ville', 'DatePrevi_Hôpital',
             'Volumes_Ventes_Ville', 'Volumes_Ventes_Hopital']]
    df = df.rename(columns={'ID_Signal': 'id_signal', 'Signalement': 'signalement',
                            'Date Signalement': 'date_signalement', 'Laboratoire': 'laboratoire',
                            'Spécialité': 'specialite', 'Rupture': 'rupture', 'ATC': 'atc', 'DCI': 'dci',
                            'Date_Signal_Debut_RS': 'date_signal_debut_rs', 'Durée_Ville': 'duree_ville',
                            'Durée_Hôpital': 'duree_hopital', 'DatePrevi_Ville': 'date_previ_ville',
                            'DatePrevi_Hôpital': 'date_previ_hopital', 'Volumes_Ventes_Ville': 'volumes_ventes_ville',
                            'Volumes_Ventes_Hopital': 'volumes_ventes_hopital'})
    df.dci = df.dci.str.lower()
    df.laboratoire = df.laboratoire.str.lower()
    df.specialite = df.specialite.str.lower()
    df.rupture = df.rupture.str.lower()
    df.date_signalement = pd.to_datetime(df.date_signalement).apply(lambda x: x.date())
    df.date_signal_debut_rs = pd.to_datetime(df.date_signal_debut_rs).apply(lambda x: x.date())
    df.date_previ_ville = pd.to_datetime(df.date_previ_ville).apply(lambda x: x.date())
    df.date_previ_hopital = pd.to_datetime(df.date_previ_hopital).apply(lambda x: x.date())
    df = df.where(pd.notnull(df), None)
    df.volumes_ventes_ville = df.volumes_ventes_ville.apply(lambda x: get_volumes(x))
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.apply(lambda x: get_volumes(x))
    df.volumes_ventes_ville = df.volumes_ventes_ville.where(pd.notnull(df.volumes_ventes_ville), 0)
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.where(pd.notnull(df.volumes_ventes_hopital), 0)
    df = df.astype({'volumes_ventes_ville': int, 'volumes_ventes_hopital': int})
    df = df.drop_duplicates()
    return df.to_dict(orient='records')


def get_volumes(x):
    if isinstance(x, str):
        x = x.replace(' ', '')
        try:
            x = int(x)
        except ValueError:
            x = 0
    return x


def get_ventes() -> List[Dict]:
    """
    Table ventes
    From OCTAVE database
    """
    df_2018 = pd.read_excel('/Users/ansm/Documents/GitHub/datamed/create_database/data/OCTAVE/Octave_2018_ATC.xlsx')
    df_2018['Nom Labo'] = None
    df_2019 = pd.read_excel('/Users/ansm/Documents/GitHub/datamed/create_database/data/OCTAVE/Octave_2019_ATC.xlsx')
    df = pd.concat([df_2018, df_2019])

    # Cleaning
    df = df.rename(columns={'Année': 'annee', 'code dossier': 'code_dossier', 'code CIS': 'cis',
                            'Identifiant OCTAVE': 'octave_id', 'Code CIP': 'cip13',
                            'Nom spécialité': 'denomination_specialite', 'Présentation': 'libelle',
                            'ClasseATC': 'atc', 'Régime Remb.': 'regime_remb', 'Unités officine': 'unites_officine',
                            'Unités hôpital': 'unites_hopital', 'Nom Labo': 'laboratoire'})
    df = df[['octave_id', 'annee', 'code_dossier', 'laboratoire', 'cis', 'denomination_specialite',
             'cip13', 'libelle', 'atc', 'regime_remb', 'unites_officine', 'unites_hopital']]

    df.cis = df.cis.map(str)
    df.cip13 = df.cip13.map(str)
    df.laboratoire = df.laboratoire.str.lower()
    df.denomination_specialite = df.denomination_specialite.str.lower()

    df = df.where(pd.notnull(df), None)
    df = df.drop_duplicates()
    return df.to_dict(orient='records')


db = connect_db()  # establish connection
connection = db.connect()
Session = sessionmaker(bind=db)
session = Session()


def save_to_database_orm(session):
    df = get_excels_df()

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
    cis_set = set(c['cis'] for c in cis_list)
    for conso_dict in conso_list:
        if conso_dict['cis'] in cis_set:
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

    # Création table Classification
    atc_list = get_atc_list()
    for atc_dict in atc_list:
        atc = Classification(**atc_dict)
        session.add(atc)
        session.commit()

    # Création table Ruptures
    ruptures_list = get_ruptures()
    for ruptures_dict in ruptures_list:
        ruptures = Ruptures(**ruptures_dict)
        session.add(ruptures)
        session.commit()

    # Création table Ventes
    ventes_list = get_ventes()
    for ventes_dict in ventes_list:
        ventes = Ventes(**ventes_dict)
        session.add(ventes)
        session.commit()
