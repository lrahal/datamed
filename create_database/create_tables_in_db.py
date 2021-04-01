import json
import re
from datetime import datetime as dt
from typing import List, Dict

import pandas as pd
import unicodedata2
from country_list import countries_for_language
from sqlalchemy.orm import sessionmaker

import paths
from map_making.get_geoloc import get_locations
from .jade_analysis import build_api_fab_sites_dataframe
from .models import (
    connect_db,
    Specialite,
    SubstanceActive,
    SpecialiteSubstance,
    RupturesDC,
    Presentation,
    Production,
    Ruptures,
    Ventes,
    Produits,
    ServiceMedicalRendu,
    Pays,
)
from .transform_db import compute_best_matches
from .upload_db import (
    upload_cis_from_rsp,
    upload_compo_from_rsp,
    upload_cis_cip_from_bdpm,
)


def get_api_by_cis() -> Dict:
    """
    Get substance_active (API) list for each CIS
    :return: dict of list
    """
    # Load dataframe
    df = upload_compo_from_rsp(
        "/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/COMPO_RSP.txt"
    )
    # List CIS codes
    cis_list = df.cis.unique()
    return {
        str(cis): list(df[df.cis == cis].substance_active.unique()) for cis in cis_list
    }


def get_excels_df() -> pd.DataFrame:
    """
    Concatenate Excel files
    Compute cosine similarity
    :return:
    """
    path = "/Users/ansm/Documents/GitHub/datamed/create_database/data/jade_final/"
    # Load dataframe
    print("Loading dataframe from concatenated Excel files...")
    df = build_api_fab_sites_dataframe(path)

    # Get api by CIS from RSP COMPO.txt file
    api_by_cis = get_api_by_cis()

    # Compute best match api using RSP
    best_match_list = compute_best_matches(df, api_by_cis)
    df_match = pd.DataFrame(best_match_list)
    df_match.to_csv(
        "/Users/ansm/Documents/GitHub/datamed/create_database/data/best_match_api.csv",
        index=False,
        sep=";",
    )
    print("best_match_api.csv printed!")

    best_match_dict = {
        (m["cis"], m["excel"]): {"api_rsp": m["rsp"], "cos_sim": m["cos_sim"]}
        for m in best_match_list
    }
    df["substance_active_match"] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]["api_rsp"]
        if (x.cis, x.substance_active) in best_match_dict
        else x.substance_active,
        axis=1,
    )
    df["cos_sim"] = df.apply(
        lambda x: best_match_dict[(x.cis, x.substance_active)]["cos_sim"]
        if (x.cis, x.substance_active) in best_match_dict
        else None,
        axis=1,
    )
    df = df.drop(["substance_active"], axis=1)
    df = df.rename(columns={"substance_active_match": "substance_active"})
    df = df.dropna(
        subset=["cis", "substance_active", "sites_fabrication_substance_active"]
    )
    df = df.drop_duplicates(
        subset=["cis", "substance_active", "sites_fabrication_substance_active"]
    )
    return df


def get_api_list(df: pd.DataFrame) -> List[Dict]:
    """
    Table substance_active
    """
    df_api = upload_compo_from_rsp(
        "/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/COMPO_RSP.txt"
    )

    api_list = [
        {"name": r["substance_active"], "code": r["code_substance"]}
        for idx, r in df_api.iterrows()
    ]

    api_not_in_list = [
        api
        for api in df.substance_active.unique()
        if api not in df_api.substance_active.unique()
    ]
    api_list.extend([{"name": api, "code": None} for api in api_not_in_list])
    api_list = [dict(t) for t in {tuple(d.items()) for d in api_list}]
    return sorted(api_list, key=lambda k: k["name"])


def get_cis_api_list() -> List[Dict]:
    """
    Table specialite_substance
    """
    df = upload_compo_from_rsp(paths.P_COMPO_RSP)
    df_api = pd.read_sql_table("substance_active", connection)
    df = df.merge(
        df_api,
        left_on=["code_substance", "substance_active"],
        right_on=["code", "name"],
        how="left",
    )
    df = df[
        [
            "cis",
            "elem_pharma",
            "id",
            "dosage",
            "ref_dosage",
            "nature_composant",
            "num_lien",
        ]
    ]
    df = df.rename(columns={"id": "substance_active_id"})
    df = df.where(pd.notnull(df), None)
    cis_api_list = df.to_dict(orient="records")
    return sorted(cis_api_list, key=lambda k: k["cis"])


def get_cis_list(df: pd.DataFrame) -> List[Dict]:
    """
    Table specialite, listing all possible CIS codes
    """
    df_cis = upload_cis_from_rsp("./create_database/data/RSP/CIS_RSP.txt")

    # Add atc class to df_cis dataframe
    df_atc = pd.read_excel(
        paths.P_CIS_ATC, names=["cis", "atc", "nom_atc"], header=0, dtype={"cis": str}
    )
    df_atc = df_atc.drop_duplicates()

    df_cis = df_cis.merge(df_atc, on="cis", how="left")
    df_atc.nom_atc = df_atc.nom_atc.str.lower()
    df_cis = df_cis.where(pd.notnull(df_cis), None)

    cis_list = df_cis.cis.unique().tolist()
    cis_to_check = df.cis.unique().tolist() + df_atc.cis.unique().tolist()
    cis_not_in_list = [c for c in cis_to_check if c not in cis_list]

    records = df_cis.to_dict("records")

    values_list = [
        {
            k: str(v) if v else None
            for k, v in zip(
                (
                    "cis",
                    "name",
                    "forme_pharma",
                    "voie_admin",
                    "atc",
                    "nom_atc",
                    "type_amm",
                    "etat_commercialisation",
                ),
                (
                    r["cis"],
                    r["nom_spe_pharma"],
                    r["forme_pharma"],
                    r["voie_admin"],
                    r["atc"],
                    r["nom_atc"],
                    r["type_amm"],
                    r["etat_commercialisation"],
                ),
            )
        }
        for r in records
    ]
    values_list.extend([{"cis": cis, "name": None} for cis in cis_not_in_list])
    return values_list


def get_pres_list() -> List[Dict]:
    """
    Table listing all possible presentations (CIP13), with corresponding CIS code
    From BDPM
    (In RSP, some CIP13 are linked to multiple CIS, ex: 3400936432826 -> 60197246 & 69553494)
    """
    df = upload_cis_cip_from_bdpm("./create_database/data/BDPM/CIS_CIP_bdpm.txt")
    df = df.where(pd.notnull(df), None)
    records = df.to_dict("records")

    return [
        {
            k: str(v)
            for k, v in zip(
                ("cis", "cip13", "libelle", "taux_remboursement"),
                (
                    r["cis"],
                    r["cip13"],
                    r["libelle_presentation"],
                    r["taux_remboursement"],
                ),
            )
        }
        for r in records
    ]


def get_country(address: str, country_list: List, country_dict: Dict) -> Dict:
    country_in_address = {}
    for country in country_list:
        if country in address:
            country_in_address[country_dict.get(country, country)] = address.count(
                country
            )
    return country_in_address


def get_countries_list(df: pd.DataFrame, path: str) -> List[Dict]:
    df = df[["sites_fabrication_substance_active"]]
    df = df.drop_duplicates()

    countries_en = [c[1].lower() for c in countries_for_language("en")]
    countries_fr = [c[1].lower() for c in countries_for_language("fr")]

    # json contenant des écritures particulières non listées par les appels ci-dessus
    with open(
        "/Users/ansm/Documents/GitHub/datamed/map_making/data/countries.json"
    ) as json_file:
        country_dict = json.load(json_file)

    all_countries = set(countries_fr + countries_en + list(country_dict.keys()))

    # Ajouter les écritures sans accents
    country_list = []
    for word in all_countries:
        if word not in country_list:
            country_list.append(word)
            word_no_accents = "".join(
                (
                    c
                    for c in unicodedata2.normalize("NFD", word)
                    if unicodedata2.category(c) != "Mn"
                )
            )
            if word_no_accents not in country_list:
                country_list.append(word_no_accents)
    country_list = sorted(country_list)

    # Lister les pays qui apparaissent vraiment dans les adresses de la dataframe
    countries_in_df = []
    addresses = df.sites_fabrication_substance_active.unique()
    for address in addresses:
        countries = get_country(address, country_list, country_dict).keys()
        for country in countries:
            if country not in countries_in_df:
                countries_in_df.append(country)

    df["country"] = df.sites_fabrication_substance_active.apply(
        lambda x: get_country(x, country_list, country_dict)
    )

    for country in countries_in_df:
        df[country_dict.get(country, country)] = df.country.apply(
            lambda x: x.get(country, 0)
        )

    # Pour les adresses pour lesquelles on n'a pas réussi à trouver les pays,
    # on utilise la geocoding API
    not_found_addresses = df[
        df.country == {}
    ].sites_fabrication_substance_active.unique()
    df_not_found_addresses = get_locations(
        not_found_addresses,
        "address_locations_{}.csv".format(dt.now().date().strftime("%d%m%Y")),
    )
    country_by_address = df_not_found_addresses.to_dict(orient="records")
    country_by_address_dict = {c["address"]: c["country"] for c in country_by_address}

    # Résultat de la geocoding injecté dans la dataframe de départ
    df.loc[df.country == {}, "country"] = df.loc[
        df.country == {}, "sites_fabrication_substance_active"
    ].apply(lambda x: country_by_address_dict[x])

    # Replace NaN values with None
    df = df.where(df.notnull(), None)
    df = df.rename(columns={"sites_fabrication_substance_active": "address"})

    cols_keep = [c for c in df.columns if c != "country"]

    return df[cols_keep].to_csv(path, sep=";", index=False)


def get_pays(path: str) -> List[Dict]:
    df = pd.read_csv(path, sep=";")
    countries = sorted([col for col in df.columns if col != "address"])
    df_loc = get_locations(
        countries,
        "countries_locations_{}.csv".format(dt.now().date().strftime("%d%m%Y")),
    )

    # Corrections inde qui donne United States avec la geocoding... #chelou
    df_loc.loc[df_loc.address == "inde", "latitude"] = 20.593684
    df_loc.loc[df_loc.address == "inde", "longitude"] = 78.962880
    df_loc.loc[df_loc.address == "inde", "country"] = "India"
    return df_loc.to_dict(orient="records")


def get_prod_list(df: pd.DataFrame) -> List[Dict]:
    """
    Create table listing all possible occurrences of (cis, substance_active, address)
    """
    # Load substance_active table and join with dataframe
    df_api = pd.read_sql_table("substance_active", connection)
    df = df.merge(df_api, how="left", left_on="substance_active", right_on="name")
    df = df.rename(columns={"id": "substance_active_id"})

    # Replace NaN values with None
    df = df.where(df.notnull(), None)

    return [
        {
            k: v
            for k, v in zip(
                (
                    "cis",
                    "substance_active_id",
                    "substance_active",
                    "sites_fabrication_substance_active",
                    "denomination_specialite",
                    "dci",
                    "type_amm",
                    "titulaire_amm",
                    "sites_production",
                    "sites_conditionnement_primaire",
                    "sites_conditionnement_secondaire",
                    "sites_importation",
                    "sites_controle",
                    "sites_echantillotheque",
                    "sites_certification",
                    "mitm",
                    "pgp",
                    "filename",
                ),
                (
                    row["cis"],
                    int(row["substance_active_id"]),
                    row["substance_active"],
                    row["sites_fabrication_substance_active"],
                    row["denomination_specialite"],
                    row["dci"],
                    row["type_amm"],
                    row["titulaire_amm"],
                    row["sites_production"],
                    row["sites_conditionnement_primaire"],
                    row["sites_conditionnement_secondaire"],
                    row["sites_importation"],
                    row["sites_controle"],
                    row["sites_echantillotheque"],
                    row["sites_certification"],
                    row["mitm"],
                    row["pgp"],
                    row["filename"],
                ),
            )
        }
        for index, row in df.iterrows()
    ]


def get_volumes(x):
    if isinstance(x, str):
        x = x.replace(" ", "")
        try:
            x = int(x)
        except ValueError:
            x = 0
    return x


def get_ruptures() -> List[Dict]:
    """
    Table ruptures
    """
    df = pd.read_excel(paths.P_DECRET, header=0, sheet_name="Raw")

    # Cleaning
    df = df[
        [
            "ID_Signal",
            "Signalement",
            "Date Signalement",
            "Laboratoire",
            "Spécialité",
            "VOIE",
            "VOIE 4 CLASSES",
            "Rupture",
            "Etat dossier",
            "Circuit_Touche_Ville",
            "Circuit_Touche_Hopital",
            "ATC",
            "DCI",
            "Date_Signal_Debut_RS",
            "Durée_Ville",
            "Durée_Hôpital",
            "DatePrevi_Ville",
            "DatePrevi_Hôpital",
            "Volumes_Ventes_Ville",
            "Volumes_Ventes_Hopital",
        ]
    ]
    df = df.rename(
        columns={
            "ID_Signal": "id_signal",
            "Signalement": "signalement",
            "Date Signalement": "date_signalement",
            "Laboratoire": "laboratoire",
            "Spécialité": "specialite",
            "VOIE": "voie",
            "VOIE 4 CLASSES": "voie_4_classes",
            "Rupture": "rupture",
            "Etat dossier": "etat_dossier",
            "Circuit_Touche_Ville": "circuit_touche_ville",
            "Circuit_Touche_Hopital": "circuit_touche_hopital",
            "ATC": "atc",
            "DCI": "dci",
            "Date_Signal_Debut_RS": "date_signal_debut_rs",
            "Durée_Ville": "duree_ville",
            "Durée_Hôpital": "duree_hopital",
            "DatePrevi_Ville": "date_previ_ville",
            "DatePrevi_Hôpital": "date_previ_hopital",
            "Volumes_Ventes_Ville": "volumes_ventes_ville",
            "Volumes_Ventes_Hopital": "volumes_ventes_hopital",
        }
    )

    df.dci = df.dci.str.lower()
    df.laboratoire = df.laboratoire.str.lower()
    df.specialite = df.specialite.str.lower()
    df.voie = df.voie.str.lower()
    df.voie_4_classes = df.voie_4_classes.str.lower()
    df.rupture = df.rupture.str.lower()
    df.etat_dossier = df.etat_dossier.str.lower()
    df.date_signalement = pd.to_datetime(df.date_signalement).dt.date()
    df.date_signal_debut_rs = pd.to_datetime(df.date_signal_debut_rs).dt.date()
    df.date_previ_ville = pd.to_datetime(df.date_previ_ville).dt.date()
    df.date_previ_hopital = pd.to_datetime(df.date_previ_hopital).dt.date()
    df = df.where(pd.notnull(df), None)
    df.volumes_ventes_ville = df.volumes_ventes_ville.apply(lambda x: get_volumes(x))
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.apply(
        lambda x: get_volumes(x)
    )
    df.volumes_ventes_ville = df.volumes_ventes_ville.where(
        pd.notnull(df.volumes_ventes_ville), 0
    )
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.where(
        pd.notnull(df.volumes_ventes_hopital), 0
    )
    df = df.astype({"volumes_ventes_ville": int, "volumes_ventes_hopital": int})
    df = df.drop_duplicates()
    return df.to_dict(orient="records")


def get_ruptures_dc() -> List[Dict]:
    """
    Table ruptures pour le décret stock
    """
    df = pd.read_csv(paths.P_RUPTURES, sep=";")

    df.date_signalement = pd.to_datetime(df.date_signalement).apply(lambda x: x.date())
    df.date_signal_debut_rs = pd.to_datetime(df.date_signal_debut_rs).apply(
        lambda x: x.date()
    )
    df.date_previ_ville = pd.to_datetime(df.date_previ_ville).apply(lambda x: x.date())
    df.date_previ_hopital = pd.to_datetime(df.date_previ_hopital).apply(
        lambda x: x.date()
    )
    df = df.where(pd.notnull(df), None)
    df.volumes_ventes_ville = df.volumes_ventes_ville.apply(lambda x: get_volumes(x))
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.apply(
        lambda x: get_volumes(x)
    )
    df.volumes_ventes_ville = df.volumes_ventes_ville.where(
        pd.notnull(df.volumes_ventes_ville), 0
    )
    df.volumes_ventes_hopital = df.volumes_ventes_hopital.where(
        pd.notnull(df.volumes_ventes_hopital), 0
    )
    df = df.astype({"volumes_ventes_ville": int, "volumes_ventes_hopital": int})
    df = df.drop_duplicates()
    return df.to_dict(orient="records")


def get_ventes() -> List[Dict]:
    """
    Table ventes
    From OCTAVE database
    """
    df_2017 = pd.read_excel(
        paths.P_VENTES_2017,
        dtype={
            "code CIS": str,
            "Code CIP": str,
            "Année": int,
            "Identifiant OCTAVE": int,
        },
    )
    df_2017["Nom Labo"] = None

    df_2018 = pd.read_excel(
        paths.P_VENTES_2018,
        dtype={
            "code CIS": str,
            "Code CIP": str,
            "Année": int,
            "Identifiant OCTAVE": int,
        },
    )
    df_2018["Nom Labo"] = None

    df_2019 = pd.read_excel(
        paths.P_VENTES_2019,
        dtype={
            "code CIS": str,
            "Code CIP": str,
            "Année": int,
            "Identifiant OCTAVE": int,
        },
    )

    df = pd.concat([df_2017, df_2018, df_2019])

    # Cleaning
    df = df.rename(
        columns={
            "Année": "annee",
            "code dossier": "code_dossier",
            "code CIS": "cis",
            "Identifiant OCTAVE": "octave_id",
            "Code CIP": "cip13",
            "Nom spécialité": "denomination_specialite",
            "VOIE 4 classes": "voie_4_classes",
            "VOIE": "voie",
            "Présentation": "libelle",
            "ClasseATC": "atc",
            "Régime Remb.": "regime_remb",
            "Unités officine": "unites_officine",
            "Unités hôpital": "unites_hopital",
            "Nom Labo": "laboratoire",
        }
    )
    df = df[
        [
            "octave_id",
            "annee",
            "code_dossier",
            "laboratoire",
            "cis",
            "denomination_specialite",
            "voie_4_classes",
            "voie",
            "cip13",
            "libelle",
            "atc",
            "regime_remb",
            "unites_officine",
            "unites_hopital",
        ]
    ]

    df.voie = df.voie.str.lower()
    df.voie_4_classes = df.voie_4_classes.str.lower()
    df.laboratoire = df.laboratoire.str.lower()
    df.denomination_specialite = df.denomination_specialite.str.lower()

    df = df.where(pd.notnull(df), None)
    df = df.drop_duplicates()
    return df.to_dict(orient="records")


def get_produits() -> List[Dict]:
    df = pd.read_excel(paths.P_CIS_SPE_PROD, dtype={"cis": str})
    df = df.drop_duplicates()
    return df.to_dict(orient="records")


def get_smr() -> List[Dict]:
    # Read CIS_HAS_SMR_bdpm.txt & CIS_HAS_ASMR_bdpm.txt files and put in dataframes
    col_names_smr = ["cis", "code_dossier", "motif", "date_avis", "smr", "libelle_smr"]
    df_smr = pd.read_csv(
        paths.P_CIS_HAS_SMR,
        sep="\t",
        encoding="latin1",
        names=col_names_smr,
        header=None,
        dtype={"cis": str},
    )
    df_smr.libelle_smr = df_smr.libelle_smr.apply(lambda x: re.sub(r"[\x92]", "'", x))

    col_names_asmr = [
        "cis",
        "code_dossier",
        "motif",
        "date_avis",
        "asmr",
        "libelle_asmr",
    ]
    df_asmr = pd.read_csv(
        paths.P_CIS_HAS_ASMR,
        sep="\t",
        encoding="latin1",
        names=col_names_asmr,
        header=None,
        dtype={"cis": str},
    )
    df_asmr.libelle_asmr = df_asmr.libelle_asmr.apply(
        lambda x: re.sub(r"[\x92]", "'", x)
    )

    # Data cleaning
    df_smr.date_avis = df_smr.date_avis.apply(
        lambda x: pd.to_datetime(x, format="%Y%m%d").date()
    )
    df_asmr.date_avis = df_asmr.date_avis.apply(
        lambda x: pd.to_datetime(x, format="%Y%m%d").date()
    )

    # Attribuer une valeur à chaque SMR et ASMR
    smr_dict = {
        "Commentaires": 0,
        "Non précisé": 1,
        "Insuffisant": 2,
        "Faible": 3,
        "Modéré": 4,
        "Important": 5,
    }
    asmr_dict = {
        "Commentaires sans chiffrage de l'ASMR": 0,
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
    }
    df_smr["valeur_smr"] = df_smr.smr.apply(lambda x: smr_dict[x])
    df_asmr["valeur_asmr"] = df_asmr.asmr.apply(lambda x: asmr_dict[x])

    # Sélectionner le smr avec la date la plus récente
    date_by_cis = (
        df_smr.groupby("cis")
        .agg({"date_avis": "max"})
        .reset_index()
        .to_dict(orient="records")
    )
    date_by_cis = {d["cis"]: d["date_avis"] for d in date_by_cis}
    df_smr = df_smr[df_smr.apply(lambda x: x.date_avis == date_by_cis[x.cis], axis=1)]

    date_by_cis = (
        df_asmr.groupby("cis")
        .agg({"date_avis": "max"})
        .reset_index()
        .to_dict(orient="records")
    )
    date_by_cis = {d["cis"]: d["date_avis"] for d in date_by_cis}
    df_asmr = df_asmr[
        df_asmr.apply(lambda x: x.date_avis == date_by_cis[x.cis], axis=1)
    ]

    # Pour une même date, sélectionner le SMR/ASMR le plus haut
    smr_by_cis = (
        df_smr.groupby("cis")
        .agg({"valeur_smr": "max"})
        .reset_index()
        .to_dict(orient="records")
    )
    smr_by_cis = {d["cis"]: d["valeur_smr"] for d in smr_by_cis}
    df_smr = df_smr[df_smr.apply(lambda x: x.valeur_smr == smr_by_cis[x.cis], axis=1)]

    asmr_by_cis = (
        df_asmr.groupby("cis")
        .agg({"valeur_asmr": "max"})
        .reset_index()
        .to_dict(orient="records")
    )
    asmr_by_cis = {d["cis"]: d["valeur_asmr"] for d in asmr_by_cis}
    df_asmr = df_asmr[
        df_asmr.apply(lambda x: x.valeur_asmr == asmr_by_cis[x.cis], axis=1)
    ]

    # Pour deux SMR/ASMR identiques, garder celui dont l'index est le plus bas
    df_smr = df_smr.drop_duplicates(subset=["cis", "date_avis", "smr"], keep="first")
    df_smr = df_smr.drop(["valeur_smr"], axis=1)

    df_asmr = df_asmr.drop_duplicates(subset=["cis", "date_avis", "asmr"], keep="first")
    df_asmr = df_asmr.drop(["valeur_asmr"], axis=1)

    df = df_smr.merge(
        df_asmr[["cis", "code_dossier", "asmr", "libelle_asmr"]],
        on=["cis", "code_dossier"],
        how="left",
    )
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


engine = connect_db()  # establish connection
connection = engine.connect()
Session = sessionmaker(bind=engine)
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

    # Création table SpecialiteSubstance
    cis_api_list = get_cis_api_list()
    for cis_api_dict in cis_api_list:
        cis_api = SpecialiteSubstance(**cis_api_dict)
        session.add(cis_api)
        session.commit()

    # Création table Presentation
    pres_list = get_pres_list()
    for pres_dict in pres_list:
        pres = Presentation(**pres_dict)
        session.add(pres)
        session.commit()

    # Write countries by address csv file
    path = paths.P_COUNTRIES
    get_countries_list(df, path)

    # Création table Pays
    pays_list = get_pays(path)
    for pays_dict in pays_list:
        pays = Pays(**pays_dict)
        session.add(pays)
        session.commit()

    # Création table Production
    prod_list = get_prod_list(df)
    for prod_dict in prod_list:
        prod = Production(**prod_dict)
        session.add(prod)
        session.commit()

    # Création table Ruptures
    ruptures_list = get_ruptures()
    for ruptures_dict in ruptures_list:
        ruptures = Ruptures(**ruptures_dict)
        session.add(ruptures)
        session.commit()

    # Création table Ruptures DC
    ruptures_list = get_ruptures_dc()
    for ruptures_dict in ruptures_list:
        ruptures = RupturesDC(**ruptures_dict)
        session.add(ruptures)
        session.commit()

    # Création table Ventes
    ventes_list = get_ventes()

    # On ajoute à la table specialite les CIS qui n'y sont pas
    all_cis = [c["cis"] for c in cis_list]
    ventes_cis_dict = {
        v["cis"]: v["denomination_specialite"]
        for v in ventes_list
        if v["cis"] not in all_cis
    }
    for cis, denom in ventes_cis_dict.items():
        cis_dict = {
            "cis": cis,
            "name": denom,
            "type_amm": None,
            "etat_commercialisation": None,
        }
        spe = Specialite(**cis_dict)
        session.add(spe)
        session.commit()

    for ventes_dict in ventes_list:
        ventes = Ventes(**ventes_dict)
        session.add(ventes)
        session.commit()

    # Création table Produit
    produits_list = get_produits()

    # On ajoute à la table specialite les CIS qui n'y sont pas
    all_cis = [c["cis"] for c in cis_list]
    produits_cis_list = [v["cis"] for v in produits_list if v["cis"] not in all_cis]
    for cis in produits_cis_list:
        cis_dict = {
            "cis": cis,
            "name": None,
            "type_amm": None,
            "etat_commercialisation": None,
        }
        spe = Specialite(**cis_dict)
        session.add(spe)
        session.commit()

    for produits_dict in produits_list:
        produits = Produits(**produits_dict)
        session.add(produits)
        session.commit()

    # Création table ServiceMedicalRendu
    smr_list = get_smr()
    for smr_dict in smr_list:
        smr = ServiceMedicalRendu(**smr_dict)
        session.add(smr)
        session.commit()
