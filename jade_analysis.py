import os
import pandas as pd

PATH = '/Users/linerahal/Desktop/DataMed/RS/JADE/'


def clean_data(df):
    """
    Data cleaning
    Lower case + remove spaces
    :param df: DataFrame (raw data)
    :return: DataFrame
    """
    # files = os.listdir(PATH)
    # df = pd.read_excel(PATH + files[0])
    df = df[(df['Dénomination de la spécialité'] != 'une ligne par dénomination et par susbtance active')
            & (~df['Dénomination de la spécialité'].isna())]
    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df.apply(lambda x: x.astype(str).str.strip())
    df = df.apply(lambda x: x.astype(str).str.replace('\n', ' '))
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip()
    return df


def get_dataframe():
    """
    List all files in JADE directory
    Create an only DataFrame containing info of all the files
    :return: DataFrame
    """
    files = os.listdir(PATH)
    df = pd.concat((pd.read_excel(PATH + f) for f in files), axis=0, ignore_index=True)
    clean_df = clean_data(df)
    return clean_df