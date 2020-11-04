# coding: utf-8

import csv
import string
from collections import defaultdict
from typing import Tuple, List, Dict, DefaultDict

import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import unidecode
from helpers import files_explorer
from mysql.connector import errorcode
from nltk.corpus import stopwords
from tqdm import tqdm

from .compute_similarity import get_similarity
from .create_mysql_db import connect_to_engine, HOSTNAME, DBNAME, UNAME, MYSQL_PWD
from .upload_db import upload_table_from_db, get_api_by_cis

STOPWORDS = stopwords.words('french')


def get_api_correspondence(df: pd.DataFrame, api_by_cis: Dict) -> Tuple[DefaultDict, List]:
    """
    Excel database: CIS -> api
    BDPM: CIS -> [api1, api2, ...] (referential)
    Make the correspondence api (Excel) -> api (BDPM) in order to put the good syntax
    in the MySQL database
    :return: dict of list
    """
    cis_list = df.cis.unique()
    bad_cis = []
    api_corresp_dict = defaultdict(list)  # {api_excel: [api_bdpm]}
    for cis in tqdm(cis_list):
        for api in df[df.cis == cis].substance_active:
            try:
                api_corresp_dict[api] = api_by_cis[cis]
            except KeyError:
                if cis not in bad_cis:
                    bad_cis.append(cis)
                continue
    return api_corresp_dict, bad_cis


def clean_string(text: str) -> str:
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    text = unidecode.unidecode(text)
    return text


def get_api_similarities(api_corresp_dict: DefaultDict, ndigits: int) -> DefaultDict:
    """
    Get for each api_excel, its similarity with the corresponding api
    contained in the api_bdpm_list
    :return:  dict of dict
    """
    api_sim_dict = defaultdict(dict)
    for api_excel, api_bdpm in tqdm(api_corresp_dict.items()):
        for api in api_bdpm:
            # Create sentences tuple
            api_tuple = (api_excel, api)
            # Clean the words in api_tuple
            cleaned_api_tuple = tuple(map(clean_string, api_tuple))
            # Compute cosine similarity between the 2 words in tuple
            api_sim_dict[api_excel][api] = get_similarity(cleaned_api_tuple, ndigits)
    return api_sim_dict


def get_most_sim_api(api_sim_dict: DefaultDict) -> Dict:
    """
    Pick the api_bdpm with the highest similarity score
    :return: dict
    """
    return {
        api_excel: max(api_sim_dict[api_excel], key=api_sim_dict[api_excel].get, default=None)
        for api_excel in api_sim_dict.keys()
    }


def compute_best_matches(df: pd.DataFrame, api_by_cis: Dict) -> Dict:
    # Find correspondence between Excel api and BDPM api
    # 1 -> N
    print('Finding correspondences between Excels api and BDPM api...')
    api_corresp_dict, bad_cis = get_api_correspondence(df, api_by_cis)
    print('{} CIS codes over {} are not referenced in the BDPM'.format(
        len(bad_cis), len(df.cis.unique())), end='\n')

    # Save bad_cis list in file
    files_explorer.write_txt_file('./create_database/data/bad_cis.txt', bad_cis)

    # Get the cosine similarity score for each couple (api_excel, api_bdpm)
    print('Computing similarity scores...', end='\n')
    api_sim_dict = get_api_similarities(api_corresp_dict, ndigits=2)

    # Select the one with the highest score
    print('Selecting best matches...', end='\n')
    best_match_api = get_most_sim_api(api_sim_dict)
    return best_match_api


def add_best_match_api_to_table(best_match_api: Dict, table_name: str, col_name: str):
    """
    Add new substance_active field to table using best_match_api dict
    :return: Update table in database
    """
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Create new column for best match api
    try:
        # If column doesn't exist
        cursor.execute(
            'ALTER TABLE {} ADD {} VARCHAR(1000) NULL AFTER substance_active;'.format(table_name, col_name)
        )
    except pymysql.Error as e:
        if e.args[0] == 1060:
            print(e.args[1])
        else:
            print(e)

    # Fill new column with values from dict
    for old_api, new_api in tqdm(best_match_api.items()):
        cursor.execute(
            'UPDATE {} SET {} = "{}" WHERE substance_active = "{}"'.format(
                table_name, col_name, new_api, old_api)
        )
    cursor.close()


def main():
    # Upload dataframe from fabrication_sites table
    table_name = 'fabrication_sites'
    df = upload_table_from_db(table_name)

    # Get api by CIS from BDPM CIS_COMPO_bdpm.txt file
    api_by_cis = get_api_by_cis()

    best_match_api = compute_best_matches(df, api_by_cis)
    files_explorer.write_csv(
        best_match_api,
        path='./create_database/data/best_match_api.csv',
        fieldnames=['substance_active_excel', 'substance_active_bdpm']
    )
    print('best_match_api.csv printed!')

    # Add new substance_active field to table using best_match_api dict
    add_best_match_api_to_table(best_match_api, table_name, 'substance_active_new')
    print('substance_active_new column created!')



if __name__ == '__main__':
    main()