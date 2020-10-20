import os
import re
import pandas as pd

PATH = '/Users/linerahal/Desktop/DataMed/RS/JADE/'


def clean_data(df):
    """
    Data cleaning
    Lower case + remove spaces
    :param df: DataFrame (raw data)
    :return: DataFrame
    """
    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df.apply(lambda x: x.astype(str).str.strip())
    df = df.apply(lambda x: x.astype(str).str.replace('\n', ' '))
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('\n', ' ')
    return df


def get_dataframe():
    """
    List all files in JADE directory
    Create an only DataFrame containing info of all the files
    :return: DataFrame
    """
    files = os.listdir(PATH)
    files = files[1:]   # Remove DS_Store file
    df = pd.concat((pd.read_excel(PATH + f) for f in files), axis=0, ignore_index=True)
    clean_df = clean_data(df)
    return clean_df


def get_dataset_columns():
    files = os.listdir(PATH)
    files = files[1:]   # Remove DS_Store file
    columns_list = []
    for f in files:
        df_file = pd.read_excel(PATH + f)
        df_file = clean_data(df_file)
        file_dict = {'filename': f}
        file_dict.update({'col_' + str(i+1): col for i, col in enumerate(df_file.columns)})
        columns_list.append(file_dict)
    df = pd.DataFrame(columns_list)
    return df


def convert_cis(cis_str):
    """
    Keep only integer cis codes
    """
    if cis_str.replace(' ', '').replace('.', '').replace('cis', '').replace(':', '').isdigit():
        cis_int = int(float(cis_str.replace(' ', '').replace('.', '').replace('cis', '').replace(':', '')))
    else:
        cis_int = cis_str
    return cis_int


def get_filtered_dataframe():
    """
    Choose interesting columns (corresponding to most recent files)
    Filter on files containing those columns
    Create big dataframe with all those files
    Clean the dataframe
    :return: DataFrame
    """
    cols = ['dénomination de la spécialité', 'cis', 'dénomination commune (dci)', "type d'amm", "titulaire de l'amm",
            'site(s) de production  / sites de production alternatif(s)', 'site(s) de conditionnement primaire',
            'site(s) de conditionnement secondaire', "site d'importation", 'site(s) de contrôle',
            "site(s) d'échantillothèque", 'site(s) de certification', 'substance active',
            'site(s) de fabrication de la substance active', 'mitm (oui/non)', 'pgp (oui/non)']

    df_cols = get_dataset_columns()
    df_cols['cols_ok'] = df_cols.apply(lambda x: list(x)[1:17] == cols, axis=1)

    filenames = list(df_cols[df_cols.cols_ok].filename)
    df_data = pd.concat((pd.read_excel(PATH + f) for f in filenames), axis=0, ignore_index=True)
    df_data = df_data[
        (~df_data['Dénomination de la spécialité'].isna())
        & (df_data['Dénomination de la spécialité'] != 'une ligne par dénomination et par susbtance active')
    ]
    clean_df = clean_data(df_data)
    clean_df = clean_df.iloc[:, :-23]
    clean_df.cis = clean_df.cis.apply(lambda x: convert_cis(x))
    return clean_df


def add_selected_site(df, site_name='site(s) de production  / sites de production alternatif(s)'):
    """
    Retrieve the first address mentioned for site name
    :param df: DataFame (= clean DataFrame)
    :return: DataFrame
    ex: site_name = 'site(s) de production  / sites de production alternatif(s)'
    """
    df['site_name'] = df.apply(lambda x: re.sub(' +', ' ', x[site_name].split(';')[0]), axis=1)
    return df



