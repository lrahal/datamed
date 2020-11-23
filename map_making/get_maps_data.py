from typing import Tuple, List, Dict

import pandas as pd

from create_database.upload_db import upload_table_from_db


def get_data(table_name: str, path: str, site_col: str) -> pd.DataFrame:
    """
    Get dataframe listing active substances, fabrication sites, countries, etc.
    :param table_name: should be 'fabrication_sites'
    :param path: 'map_making/data/sites_fabrication_substance_active.csv'
    :param site_col: 'sites_fabrication_substance_active'
    """
    # Upload dataframe from fabrication_sites table
    df_table = upload_table_from_db(table_name)
    df_table.substance_active_match = df_table.apply(
        lambda x: x.substance_active if pd.isnull(x.substance_active_match) else x.substance_active_match, axis=1)

    # Get locations of each address in df_table (from csv)
    df_locations = pd.read_csv(path)
    df_locations = df_locations.drop(columns=['Unnamed: 0'])
    df_locations = df_locations.rename(columns={'input_string': site_col})

    # Merge both dataframes
    df_final = pd.merge(
        df_table[['denomination_specialite', 'cis', 'substance_active_match', site_col]],
        df_locations, on=site_col, how='inner'
    )

    # Rename column substance_active_match
    df_final = df_final.rename(columns={'substance_active_match': 'substance_active'})
    return df_final


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove NaN active substances and NaN countries
    """
    df = df[~df.substance_active.isna()]
    return df[~df['country'].isna()]


def upload_countries_loc(path: str) -> pd.DataFrame:
    """
    Load countries locations csv and put it in dataframe
    :param path: 'map_making/data/countries_locations.csv'
    """
    df_countries_loc = pd.read_csv(path)
    df_countries_loc = df_countries_loc.drop(columns=['Unnamed: 0'])
    return df_countries_loc


def get_api_by_country(df: pd.DataFrame, path: str) -> pd.DataFrame:
    """
    Get number of active substances produced in each country
    :param path: 'map_making/data/countries_locations.csv'
    """
    df_grouped_by_country = df.groupby('country')
    df_grouped_by_country = df_grouped_by_country.agg({'substance_active': 'nunique'})
    df_grouped_by_country = df_grouped_by_country.reset_index()

    df_countries_loc = upload_countries_loc(path)

    df_countries = pd.merge(
        df_grouped_by_country[['substance_active', 'country']], df_countries_loc, on='country', how='inner'
    )
    df_countries = df_countries[~df_countries.country.isna()]
    return df_countries


def get_single_site_api(df: pd.DataFrame) -> List[Dict]:
    """
    Get list of dicts containing active substances
    produced in only one place in the world
    """
    df_grouped_by_api = df.groupby('substance_active')
    df_grouped_by_api = df_grouped_by_api.agg({'formatted_address': 'nunique'})
    df_grouped_by_api = df_grouped_by_api.reset_index()

    single_site_api = df_grouped_by_api[df_grouped_by_api.formatted_address == 1].substance_active.unique()

    single_site_api_list = df[
        df.substance_active.isin(single_site_api)][['substance_active', 'formatted_address', 'country']
    ].to_dict(orient='records')
    return list({v['substance_active']: v for v in single_site_api_list}.values())


def get_final_dataframe() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = get_data('fabrication_sites',
                  'map_making/data/sites_fabrication_substance_active.csv',
                  'sites_fabrication_substance_active')
    df = clean_data(df)

    df_countries = get_api_by_country(df, 'map_making/data/countries_locations.csv')

    return df, df_countries
