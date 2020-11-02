import os
import re
import pandas as pd
from typing import List
from xlrd import XLRDError
from helpers import files_explorer


SCHEMA = {
    'dénomination de la spécialité': 'denomination_specialite',
    'cis': 'cis',
    'dénomination commune (dci)': 'dci',
    "type d'amm": 'type_amm',
    "titulaire de l'amm": 'titulaire_amm',
    'site(s) de production  / sites de production alternatif(s)': 'sites_production',
    'site(s) de conditionnement primaire': 'sites_conditionnement_primaire',
    'site(s) de conditionnement secondaire': 'sites_conditionnement_secondaire',
    "site d'importation": 'sites_importation',
    'site(s) de contrôle': 'sites_controle',
    "site(s) d'échantillothèque": 'sites_echantillotheque',
    'site(s) de certification': 'sites_certification',
    'substance active': 'substance_active',
    'site(s) de fabrication de la substance active': 'sites_fabrication_substance_active',
    'mitm (oui/non)': 'mitm',
    'pgp (oui/non)': 'pgp',
}


def clean_column(col):
    """
    Clean dataframe columns content
    :param col: DataFrame column
    :return: cleaned column
    """
    return col.astype(str).str.lower().str.strip().str.replace('\n', ' ')


def convert_cis(cis_str: str) -> str:
    """
    Convert cis codes in int type if possible
    """
    cis_tmp = cis_str.replace(' ', '').replace('cis', '').replace(':', '').replace(u'\xa0', u'').replace('.', '')[:8]
    if cis_tmp.isdigit():
        return cis_tmp
    else:
        return cis_str


def global_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning
    Lower case + remove spaces + remove all NaN rows
    :param df: DataFrame (raw data)
    :return: DataFrame
    """
    # Global cleaning
    df = df.dropna(how='all')
    df[df.columns] = df[df.columns].apply(clean_column)
    df = df.applymap(lambda x: re.sub(' +', ' ', x) if isinstance(x, str) else x)
    df.columns = df.columns.str.lower().str.strip().str.replace('\n', ' ')
    return df


def columns_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    # Select only 17 first columns
    df = df.iloc[:, :len(SCHEMA)]
    df = df.rename(columns=SCHEMA)
    # Correct CIS codes
    df.cis = df.cis.apply(lambda x: convert_cis(x))
    # Remove rows having bad information
    df = df[df.denomination_specialite != 'une ligne par dénomination et par susbtance active']
    return df


def get_filenames(path: str) -> List:
    """
    Get the list of files sharing the same structure (given in cols list)
    Upgrade: should find a way to load only the header of the Excel file
    :return: list
    """
    # List all files in directory
    # (avoid .DS_Store files for macos)
    files = list(files_explorer.listdir_nohidden(path))

    for f in files:
        try:
            df_file = pd.read_excel(path + f)
            df_file.columns = df_file.columns.str.lower().str.strip().str.replace('\n', ' ')   # Clean column title
            if list(df_file.columns)[:len(SCHEMA)] == list(SCHEMA.keys()):
                yield f
        except XLRDError:
            print('File {} is corrupted'.format(f))
            continue


def build_api_fab_sites_dataframe(path: str) -> pd.DataFrame:
    """
    Choose interesting columns (corresponding to most recent files)
    Filter on files containing those columns
    Create big dataframe with all those files
    Clean the dataframe
    :return: DataFrame
    """
    # Get filenames having good structure
    filenames = list(get_filenames(path))
    # Create dataframe
    df_data = pd.concat((pd.read_excel(path + f) for f in filenames),
                        axis=0, ignore_index=True, sort=False)
    # Clean dataframe
    df_tmp = global_cleaning(df_data)
    df_cleaned = columns_cleaning(df_tmp)
    return df_cleaned


def add_selected_site(df: pd.DataFrame, site_name: str) -> pd.DataFrame:
    """
    Retrieve the first address mentioned for site name
    Multiple addresses are separated by ';'
    :param df: DataFame (= clean DataFrame)
    :return: DataFrame
    ex: site_name = 'site(s) de production  / sites de production alternatif(s)'
    """
    df['site_name'] = df.apply(lambda x: x[site_name].split(';')[0], axis=1)
    return df



