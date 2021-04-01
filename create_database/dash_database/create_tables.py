import json
import zipfile
from datetime import datetime as dt
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import sessionmaker

import paths
from models import (
    connect_db,
    Specialite,
    Substance,
    SpecialiteSubstance,
    Presentation,
    Produit,
    Notice,
)

with zipfile.ZipFile(paths.P_MED, "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        MED_DICT = json.loads(data.decode("utf-8"))

with zipfile.ZipFile(paths.P_NOTICE, "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        NOTICE = json.loads(data.decode("utf-8"))


def clean_columns(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Put column fields in lower case
    """
    df[col_name] = df[col_name].apply(lambda x: x.lower().strip())
    return df


def upload_cis_from_rsp(path: str) -> pd.DataFrame:
    """
    Upload RSP CIS table
    In http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/telecharger.php
    :return: dataframe
    """
    # Read CIS_RSP.txt file and put in dataframe
    col_names = [
        "cis",
        "nom_spe_pharma",
        "forme_pharma",
        "voie_admin",
        "statut_amm",
        "type_amm",
        "etat_commercialisation",
        "code_doc",
    ]
    df = pd.read_csv(
        path,
        sep="\t",
        encoding="latin1",
        names=col_names,
        header=None,
        dtype={"cis": str},
    )
    # Put substance_active field in lower case
    df = clean_columns(df, "nom_spe_pharma")
    return df


def upload_compo_from_rsp(path: str) -> pd.DataFrame:
    """
    Upload RSP COMPO table
    In http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/telecharger.php
    :return: dataframe
    """
    # Read COMPO_RSP.txt file and put in dataframe
    col_names = [
        "cis",
        "elem_pharma",
        "code_substance",
        "substance_active",
        "dosage",
        "ref_dosage",
        "nature_composant",
        "num_lien",
        "v",
    ]
    df = pd.read_csv(
        path,
        sep="\t",
        encoding="latin1",
        names=col_names,
        header=None,
        dtype={"cis": str, "code_substance": str},
    )
    df = df[~df.substance_active.isna()]
    # Put substance_active field in lower case
    df = clean_columns(df, "substance_active")
    return df


def upload_cis_cip_from_bdpm(path: str) -> pd.DataFrame:
    """
    Upload BDPM compositions database
    In http://base-donnees-publique.medicaments.gouv.fr/telechargement.php
    Attention : 4 dernière colonnes retirées car pb d'écriture des nombres
    ex : comment transformer 4,768,73 en 4768,73 ?
    :return: dataframe
    """
    # Read CIS_CIP_bdpm.txt file and put in dataframe
    col_names = [
        "cis",
        "cip7",
        "libelle_presentation",
        "statut_admin_presentation",
        "etat_commercialisation",
        "date_declaration_commercialisation",
        "cip13",
        "agrement_collectivites",
        "taux_remboursement",
        "prix_medicament_euro",
        "chelou_1",
        "chelou_2",
        "indications_remboursement",
    ]
    df = pd.read_csv(path, sep="\t", encoding="latin1", names=col_names, header=None)
    # Retirer les 4 dernières colonnes
    df = df.drop(
        ["prix_medicament_euro", "chelou_1", "chelou_2", "indications_remboursement"],
        axis=1,
    )
    # Convertir les dates en format datetime
    df.date_declaration_commercialisation = df.date_declaration_commercialisation.apply(
        lambda x: dt.strptime(x, "%d/%m/%Y")
    )
    return df


def get_specialite() -> List[Dict]:
    """
    Table specialite, listing all possible CIS codes
    """
    df_cis = upload_cis_from_rsp(paths.P_CIS_RSP)

    # Add atc class to df_cis dataframe
    df_atc = pd.read_excel(
        paths.P_CIS_ATC, names=["cis", "atc", "nom_atc"], header=0, dtype={"cis": str}
    )
    df_atc = df_atc.drop_duplicates()

    df_cis = df_cis.merge(df_atc, on="cis", how="left")
    df_atc.nom_atc = df_atc.nom_atc.str.lower()
    df_cis = df_cis.where(pd.notnull(df_cis), None)

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
    return values_list


def get_substance() -> List[Dict]:
    """
    Table substance_active
    """
    df_api = upload_compo_from_rsp(paths.P_COMPO_RSP)

    api_list = [
        {"name": r["substance_active"], "code": r["code_substance"]}
        for idx, r in df_api.iterrows()
    ]
    api_list = [dict(t) for t in {tuple(d.items()) for d in api_list}]
    return sorted(api_list, key=lambda k: k["name"])


def get_spe_substance() -> List[Dict]:
    """
    Table specialite_substance
    """
    df = upload_compo_from_rsp(paths.P_COMPO_RSP)
    df_api = pd.read_sql_table("substance", connection)
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
    df = df.rename(columns={"id": "substance_id"})
    df = df.where(pd.notnull(df), None)
    cis_api_list = df.to_dict(orient="records")
    return sorted(cis_api_list, key=lambda k: k["cis"])


def get_produit() -> List[Dict]:
    df_cis = pd.read_csv(
        "data/corresp_cis_spe_prod_subs_utf8.csv",
        sep=";",
        dtype={"codeCIS": str, "codeSubstance": str},
    )
    df_cis = df_cis.where(pd.notnull(df_cis), None)

    df_cis.SPECIALITE_CODEX = df_cis.SPECIALITE_CODEX.str.lower()
    df_cis.PRODUIT_CODEX = df_cis.PRODUIT_CODEX.str.lower()

    df_cis = df_cis.rename(
        columns={
            "codeCIS": "cis",
            "SPECIALITE_CODEX": "specialite",
            "PRODUIT_CODEX": "produit",
        }
    )

    df_produit = df_cis[["cis", "specialite", "produit"]].drop_duplicates()
    values_list = df_produit.to_dict(orient="records")

    keys_ok = [med.lower() for med in MED_DICT.keys()]
    return [v for v in values_list if v["produit"] in keys_ok]


def get_notice() -> List[Dict]:
    return NOTICE


def get_presentation() -> List[Dict]:
    """
    Table listing all possible presentations (CIP13), with corresponding CIS code
    From BDPM
    (In RSP, some CIP13 are linked to multiple CIS, ex: 3400936432826 -> 60197246 & 69553494)
    """
    df = upload_cis_cip_from_bdpm(paths.P_CIS_CIP_BDPM)
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


engine = connect_db()  # establish connection
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


def save_to_database_orm(session):

    # Création table Specialite
    cis_list = get_specialite()
    for cis_dict in cis_list:
        spe = Specialite(**cis_dict)
        session.add(spe)
        session.commit()

    # Création table Substance
    api_list = get_substance()
    for api_dict in api_list:
        api = Substance(**api_dict)
        session.add(api)
        session.commit()

    # Création table SpecialiteSubstance
    spe_api_list = get_spe_substance()
    for spe_api_dict in spe_api_list:
        spe_api = SpecialiteSubstance(**spe_api_dict)
        session.add(spe_api)
        session.commit()

    # Création table Presentation
    pres_list = get_presentation()
    for pres_dict in pres_list:
        pres = Presentation(**pres_dict)
        session.add(pres)
        session.commit()

    # Création table Produit
    produit_list = get_produit()
    for produit_dict in produit_list:
        produit = Produit(**produit_dict)
        session.add(produit)
        session.commit()

    # Création table Notice
    notice_list = get_notice()
    for notice_dict in notice_list:
        notice = Notice(**notice_dict)
        session.add(notice)
        session.commit()
