from typing import Tuple, List, Dict

import pandas as pd

from create_database.create_tables_in_db import get_excels_df
from create_database.models import connect_db


def get_data() -> pd.DataFrame:
    """
    Get dataframe listing active substances, fabrication sites, countries, etc.
    """
    engine = connect_db()  # establish connection
    connection = engine.connect()

    # Dataframe of concatenated Excels
    df = get_excels_df()

    # Fabrication table
    df_fab = pd.read_sql_table("fabrication", connection)

    # Merge dataframes and clean
    df = df.merge(
        df_fab,
        how="left",
        left_on="sites_fabrication_substance_active",
        right_on="address",
    )
    df = df.drop(
        [
            "dci",
            "type_amm",
            "sites_production",
            "sites_conditionnement_primaire",
            "sites_conditionnement_secondaire",
            "sites_importation",
            "sites_controle",
            "sites_echantillotheque",
            "sites_certification",
            "substance_active",
            "sites_fabrication_substance_active",
            "mitm",
            "pgp",
            "filename",
            "cos_sim",
            "id",
        ],
        axis=1,
    )
    df = df.rename(columns={"substance_active_match": "substance_active"})
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove NaN countries
    """
    return df[~df.country.isna()]


def upload_countries_loc(path: str) -> pd.DataFrame:
    """
    Load countries locations csv and put it in dataframe
    :param path: 'map_making/data/countries_locations.csv'
    """
    df = pd.read_csv(path)
    df = df.drop(columns=["Unnamed: 0"])
    return df


def get_api_by_country(df: pd.DataFrame, path: str) -> pd.DataFrame:
    """
    Get number of active substances produced in each country
    path: 'map_making/data/countries_locations.csv'
    """
    df_grouped_by_country = df.groupby("country")
    df_grouped_by_country = df_grouped_by_country.agg({"substance_active": "nunique"})
    df_grouped_by_country = df_grouped_by_country.reset_index()

    df_countries_loc = upload_countries_loc(path)

    df_countries = pd.merge(
        df_grouped_by_country,
        df_countries_loc[["latitude", "longitude", "country"]],
        on="country",
        how="left",
    )
    df_countries = df_countries[~df_countries.country.isna()]
    return df_countries


def get_single_site_api(df: pd.DataFrame) -> List[Dict]:
    """
    Get list of dicts containing active substances
    produced in only one place in the world
    """
    df_grouped_by_api = df.groupby("substance_active")
    df_grouped_by_api = df_grouped_by_api.agg({"address": "nunique"})
    df_grouped_by_api = df_grouped_by_api.reset_index()

    single_site_api = df_grouped_by_api[
        df_grouped_by_api.address == 1
    ].substance_active.unique()

    single_site_api_list = df[df.substance_active.isin(single_site_api)][
        ["substance_active", "address", "country"]
    ].to_dict(orient="records")
    return list({v["substance_active"]: v for v in single_site_api_list}.values())


def get_final_dataframe() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = get_data()
    df = clean_data(df)

    df_countries = get_api_by_country(df, "map_making/data/countries_locations.csv")

    return df, df_countries
