# coding: utf-8

import string
from collections import defaultdict
from typing import List, Dict, DefaultDict, Set

import pandas as pd
import pymysql
import unidecode
from nltk.corpus import stopwords
from tqdm import tqdm

from .compute_similarity import get_similarity
from .create_mysql_db import HOSTNAME, DBNAME, UNAME, MYSQL_PWD
from .upload_db import upload_table_from_db, get_api_by_cis

STOPWORDS = stopwords.words('french')


def get_cis_not_in_bdpm(df: pd.DataFrame, cis_not_in_bdpm: Set, path: str):
    # Get cis not in BDPM and correspond file
    cis_not_in_bdpm_by_filename = [
        {'cis': c, 'filename': f}
        for c in cis_not_in_bdpm
        for f in df[df.cis == c].filename.unique()
    ]
    # Save it into csv
    df_cis = pd.DataFrame(cis_not_in_bdpm_by_filename)
    df_cis.to_csv(path, sep=';', index=False)


def get_api_correspondence(df: pd.DataFrame, api_by_cis: Dict) -> DefaultDict:
    """
    - Excel database: CIS -> api
    - BDPM: CIS -> [api1, api2, ...] (frame of reference)
    - Make the correspondence api (Excel) -> api (BDPM) in order to put the good syntax
    in the MySQL database
    - API = Active Pharmaceutical Ingredient (shortcut for "active substance")
    :return: dict of list
    """
    cis_table = set(df.cis.unique())             # CIS in fabrication_sites table
    cis_bdpm = set(api_by_cis.keys())            # CIS in cis_compo (= BDPM)
    cis_set = cis_table.intersection(cis_bdpm)   # CIS in both fabrication_sites and cis_compo
    cis_not_in_bdpm = cis_table - cis_set        # CIS that are in fabrication_sites but not in cis_compo
    print('{} CIS codes over {} are not referenced in the BDPM'.format(
        len(cis_not_in_bdpm), len(df.cis.unique())), end='\n')

    # Write cis_not_in_bdpm in csv
    get_cis_not_in_bdpm(df, cis_not_in_bdpm, path='./create_database/data/cis_not_in_bdpm.csv')

    # Get api correspondence dict: {api_excel: [api_bdpm]}
    api_corresp_dict = defaultdict(list)
    for cis in tqdm(cis_set):
        for api in df[df.cis == cis].substance_active:
            if not api:
                continue
            else:
                api_corresp_dict[(api, cis)] = api_by_cis[cis]
    return api_corresp_dict


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
            api_tuple = (api_excel[0], api)
            # Clean the words in api_tuple
            cleaned_api_tuple = tuple(map(clean_string, api_tuple))
            # Compute cosine similarity between the 2 words in tuple
            api_sim_dict[api_excel][api] = get_similarity(cleaned_api_tuple, ndigits)
    return api_sim_dict


def get_most_sim_api(api_sim_dict: DefaultDict) -> List[Dict]:
    """
    Pick the api_bdpm with the highest similarity score
    :return: dict
    """
    return [
        {
            'cis': api_excel[1],
            'excel': api_excel[0],
            'bdpm': max(api_bdpm_dict, key=api_bdpm_dict.get, default=None),
            'cos_sim': api_bdpm_dict[max(api_bdpm_dict, key=api_bdpm_dict.get, default=None)]
        }
        for api_excel, api_bdpm_dict in api_sim_dict.items()
    ]


def compute_best_matches(df: pd.DataFrame, api_by_cis: Dict) -> List[Dict]:
    # Find correspondence between Excel api and BDPM api
    # 1 -> N
    print('Finding correspondences between Excels api and BDPM api...')
    api_corresp_dict = get_api_correspondence(df, api_by_cis)

    # Get the cosine similarity score for each couple (api_excel, api_bdpm)
    print('Computing similarity scores...', end='\n')
    api_sim_dict = get_api_similarities(api_corresp_dict, ndigits=2)

    # Select the one with the highest score
    print('Selecting best matches...', end='\n')
    best_match_api = get_most_sim_api(api_sim_dict)
    return best_match_api


def create_columns(cursor, table_name: str, col_name: str):
    """
    Create substance_active match and cosine_similarity columns
    """
    try:
        # If column doesn't exist, create column
        cursor.execute(
            'ALTER TABLE {} ADD {} TEXT NULL AFTER substance_active;'.format(table_name, col_name)
        )
        cursor.execute(
            'ALTER TABLE {} ADD {} FLOAT NULL AFTER {};'.format(table_name, 'cosine_similarity', col_name)
        )
    except pymysql.Error as e:
        # If column already exists, print error
        if e.args[0] == 1060:
            print(e.args[1])

            # Delete columns and then recreate them
            print('Columns already exist: deleting them...')
            cursor.execute(
                'ALTER TABLE {} DROP COLUMN {}, DROP COLUMN {};'.format(table_name, col_name, 'cosine_similarity')
            )

            print('Recreate columns')
            create_columns(cursor, table_name, col_name)

        # If other error, print error
        else:
            print(e)


def add_best_match_api_to_table(best_match_api: List[Dict], table_name: str, col_name: str):
    """
    Add new substance_active field to table using best_match_api dict
    :return: Update table in database
    """
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    cursor = connection.cursor()

    # Create new column for best match api
    create_columns(cursor, table_name, col_name)

    # Fill new column with values from dict
    for api_matching_couple in tqdm(best_match_api):
        cursor.execute(
            'UPDATE {} SET {} = "{}", cosine_similarity = {} WHERE substance_active = "{}" AND cis = "{}"'.format(
                table_name,
                col_name,
                api_matching_couple['bdpm'],
                api_matching_couple['cos_sim'],
                api_matching_couple['excel'],
                api_matching_couple['cis'])
        )
    connection.close()


def join_tables(table_name_1: str = 'fabrication_sites', table_name_2: str = 'atc'):
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    cursor = connection.cursor()

    try:
        cursor.execute(
            'ALTER TABLE {} ADD {} TEXT NULL AFTER {};'.format(table_name_1, 'atc', 'cis')
        )
    except pymysql.Error as e:
        if e.args[0] == 1060:
            print(e.args[1])
            cursor.execute(
                'ALTER TABLE {} DROP COLUMN {};'.format(table_name_1, 'atc')
            )
        else:
            print(e)

    cursor.execute(
        'UPDATE {} INNER JOIN atc ON {}.cis = {}.cis SET {}.atc = {}.atc'.format(
            table_name_1, table_name_1, table_name_2, table_name_1, table_name_2
        )
    )
    connection.close()


def main():
    # Upload dataframe from fabrication_sites table
    table_name = 'fabrication_sites'
    df = upload_table_from_db(table_name)

    # Get api by CIS from BDPM CIS_COMPO_bdpm.txt file
    api_by_cis = get_api_by_cis()

    # Compute best match api using BDPM
    best_match_api = compute_best_matches(df, api_by_cis)
    df_match = pd.DataFrame(best_match_api)
    df_match.to_csv('./create_database/data/best_match_api.csv', index=False, sep=';')
    print('best_match_api.csv printed!')

    # Add new substance_active field to table using best_match_api list
    add_best_match_api_to_table(best_match_api, table_name, 'substance_active_match')
    print('substance_active_match column created!')

    print('Add ATC code to table')
    join_tables('fabrication_sites', 'atc')


if __name__ == '__main__':
    main()
