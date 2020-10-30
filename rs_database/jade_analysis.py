import os
import re
import pandas as pd
from typing import List
from xlrd import XLRDError

PATH = '/Users/linerahal/Desktop/DataMed/RS/JADE/'


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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning
    Lower case + remove spaces
    :param df: DataFrame (raw data)
    :return: DataFrame
    """
    # Global cleaning
    df[df.columns] = df[df.columns].apply(clean_column)
    df = df.applymap(lambda x: re.sub(' +', ' ', x) if isinstance(x, str) else x)
    df.columns = df.columns.str.lower().str.strip().str.replace('\n', ' ')
    df.cis = df.cis.apply(lambda x: convert_cis(x))

    # Select only 17 first columns
    df = df.iloc[:, :-23]
    df = df.rename(
        columns={'dénomination de la spécialité': 'denomination_specialite',
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
                 'pgp (oui/non)': 'pgp'
                 })
    return df


def get_good_filenames() -> List:
    """
    Get the list of files sharing the same structure (given in cols list)
    Upgrade: should find a way to load only the header of the Excel file
    :return: list
    """
    files = os.listdir(PATH)
    files = files[1:]   # Remove DS_Store file

    cols = ['dénomination de la spécialité', 'cis', 'dénomination commune (dci)', "type d'amm", "titulaire de l'amm",
            'site(s) de production  / sites de production alternatif(s)', 'site(s) de conditionnement primaire',
            'site(s) de conditionnement secondaire', "site d'importation", 'site(s) de contrôle',
            "site(s) d'échantillothèque", 'site(s) de certification', 'substance active',
            'site(s) de fabrication de la substance active', 'mitm (oui/non)', 'pgp (oui/non)']

    filenames = []
    for f in files:
        try:
            df_file = pd.read_excel(PATH + f)
            df_file.columns = df_file.columns.str.lower().str.strip().str.replace('\n', ' ')   # Clean column title
            if list(df_file.columns)[:16] == cols:
                filenames.append(f)
        except XLRDError:
            print('File {} corrupted'.format(f))
            continue
    return filenames


def get_filtered_dataframe() -> pd.DataFrame:
    """
    Choose interesting columns (corresponding to most recent files)
    Filter on files containing those columns
    Create big dataframe with all those files
    Clean the dataframe
    :return: DataFrame
    """
    # Get filenames having good structure
    filenames = get_good_filenames()
    # Create dataframe
    df_data = pd.concat((pd.read_excel(PATH + f) for f in filenames), axis=0, ignore_index=True, sort=False)
    # Remove rows having bad information
    df_data = df_data[
        (~df_data['Dénomination de la spécialité'].isna())
        & (df_data['Dénomination de la spécialité'] != 'une ligne par dénomination et par susbtance active')
    ]
    # Clean dataframe
    clean_df = clean_data(df_data)
    return clean_df


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



