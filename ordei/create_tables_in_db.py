import pandas as pd
from sqlalchemy.orm import sessionmaker

from create_database.models import connect_db
from .models import (
    CorrespProdSub,
    BnpvOpenMedic1418ProdCodex,
    BnpvEffSoclongProdCodexOpen,
    BnpvEffHltProdCodexOpen,
    BnpvNotifProdCodexOpen,
    BnpvOpenMedic1418SaCodex,
    BnpvEffSoclongSaCodexOpen,
    BnpvEffHltSaCodexOpen,
    BnpvNotifSaCodexOpen,
)

engine = connect_db()  # establish connection
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


def save_to_database_orm(session):
    # Création table Corresp_spe_prod
    corresp_spe_prod_subs = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv",
        encoding="ISO-8859-1",
        sep=";",
        dtype={"codeSubstance": str},
    )
    corresp_spe_prod_subs = corresp_spe_prod_subs.drop("Unnamed: 0", axis=1)

    corresp_spe_prod_subs = corresp_spe_prod_subs.rename(
        columns={
            "SPECIALITE_CODEX": "specialite_codex",
            "PRODUIT_CODEX": "produit_codex",
            "SUBSTANCE_CODEX_UNIQUE": "substance_codex_unique",
            "codeSubstance": "code",
        }
    )

    corresp_spe_prod_subs = corresp_spe_prod_subs.where(
        pd.notnull(corresp_spe_prod_subs), None
    )
    corresp_prod_subs = corresp_spe_prod_subs.drop_duplicates(
        subset=["produit_codex", "substance_codex_unique"]
    )
    corresp_prod_subs = corresp_prod_subs[
        ["produit_codex", "substance_codex_unique", "code"]
    ].sort_values(by=["produit_codex"])
    corresp_prod_subs = corresp_prod_subs.dropna()
    corresp_prod_subs.produit_codex = corresp_prod_subs.produit_codex.apply(
        lambda x: " ".join(x.split())
    )
    corresp_prod_subs_list = corresp_prod_subs.to_dict(orient="records")
    for corresp_prod_subs_dict in corresp_prod_subs_list:
        line = CorrespProdSub(**corresp_prod_subs_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_open_medic1418_prod_codex
    bnpv_open_medic1418_prod_codex = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv",
        encoding="ISO-8859-1",
        sep=";",
    )
    bnpv_open_medic1418_prod_codex = bnpv_open_medic1418_prod_codex.drop(
        "Unnamed: 0", axis=1
    )

    bnpv_open_medic1418_prod_codex = bnpv_open_medic1418_prod_codex.rename(
        columns={
            "ANNEE": "annee",
            "SEXE": "sexe",
            "AGE": "age",
            "PRODUIT_CODEX": "produit_codex",
        }
    )

    bnpv_open_medic1418_prod_codex_list = bnpv_open_medic1418_prod_codex.to_dict(
        orient="records"
    )
    for bnpv_open_medic1418_prod_codex_dict in bnpv_open_medic1418_prod_codex_list:
        line = BnpvOpenMedic1418ProdCodex(**bnpv_open_medic1418_prod_codex_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_soclong_prod_codex_open
    bnpv_eff_soclong_prod_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
    )
    bnpv_eff_soclong_prod_codex_open = bnpv_eff_soclong_prod_codex_open.drop(
        "Unnamed: 0", axis=1
    )

    bnpv_eff_soclong_prod_codex_open = bnpv_eff_soclong_prod_codex_open.rename(
        columns={
            "SEXE": "sexe",
            "AGE": "age",
            "SOC_LONG": "soc_long",
            "PRODUIT_CODEX": "produit_codex",
        }
    )

    bnpv_eff_soclong_prod_codex_open_list = bnpv_eff_soclong_prod_codex_open.to_dict(
        orient="records"
    )
    for bnpv_eff_soclong_prod_codex_open_dict in bnpv_eff_soclong_prod_codex_open_list:
        line = BnpvEffSoclongProdCodexOpen(**bnpv_eff_soclong_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_hlt_prod_codex_open
    bnpv_eff_hlt_prod_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
    )
    bnpv_eff_hlt_prod_codex_open = bnpv_eff_hlt_prod_codex_open.drop(
        "Unnamed: 0", axis=1
    )

    bnpv_eff_hlt_prod_codex_open = bnpv_eff_hlt_prod_codex_open.rename(
        columns={
            "SEXE": "sexe",
            "AGE": "age",
            "EFFET_HLT": "effet_hlt",
            "SOC_LONG": "soc_long",
            "PRODUIT_CODEX": "produit_codex",
        }
    )

    bnpv_eff_hlt_prod_codex_open_list = bnpv_eff_hlt_prod_codex_open.to_dict(
        orient="records"
    )
    for bnpv_eff_hlt_prod_codex_open_dict in bnpv_eff_hlt_prod_codex_open_list:
        line = BnpvEffHltProdCodexOpen(**bnpv_eff_hlt_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_notif_prod_codex_open
    bnpv_notif_prod_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
    )
    bnpv_notif_prod_codex_open = bnpv_notif_prod_codex_open.drop("Unnamed: 0", axis=1)

    bnpv_notif_prod_codex_open = bnpv_notif_prod_codex_open.rename(
        columns={
            "TYP_NOTIF": "typ_notif",
            "SEXE": "sexe",
            "AGE": "age",
            "PRODUIT_CODEX": "produit_codex",
        }
    )

    bnpv_notif_prod_codex_open_list = bnpv_notif_prod_codex_open.to_dict(
        orient="records"
    )
    for bnpv_notif_prod_codex_open_dict in bnpv_notif_prod_codex_open_list:
        line = BnpvNotifProdCodexOpen(**bnpv_notif_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_open_medic1418_sa_codex
    bnpv_open_medic1418_sa_codex = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv",
        encoding="ISO-8859-1",
        sep=";",
        dtype={"codeSubstance": str},
    )
    bnpv_open_medic1418_sa_codex = bnpv_open_medic1418_sa_codex.drop(
        "Unnamed: 0", axis=1
    )

    bnpv_open_medic1418_sa_codex = bnpv_open_medic1418_sa_codex.rename(
        columns={
            "ANNEE": "annee",
            "SEXE": "sexe",
            "AGE": "age",
            "SUBSTANCE_CODEX_UNIQUE": "substance_codex_unique",
            "codeSubstance": "code",
        }
    )

    bnpv_open_medic1418_sa_codex_list = bnpv_open_medic1418_sa_codex.to_dict(
        orient="records"
    )
    for bnpv_open_medic1418_sa_codex_dict in bnpv_open_medic1418_sa_codex_list:
        line = BnpvOpenMedic1418SaCodex(**bnpv_open_medic1418_sa_codex_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_soclong_sa_codex_open
    bnpv_eff_soclong_sa_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
        dtype={"codeSubstance": str},
    )
    bnpv_eff_soclong_sa_codex_open = bnpv_eff_soclong_sa_codex_open.drop(
        "Unnamed: 0", axis=1
    )

    bnpv_eff_soclong_sa_codex_open = bnpv_eff_soclong_sa_codex_open.rename(
        columns={
            "SEXE": "sexe",
            "AGE": "age",
            "SOC_LONG": "soc_long",
            "SUBSTANCE_CODEX_UNIQUE": "substance_codex_unique",
            "codeSubstance": "code",
        }
    )

    bnpv_eff_soclong_sa_codex_open_list = bnpv_eff_soclong_sa_codex_open.to_dict(
        orient="records"
    )
    for bnpv_eff_soclong_sa_codex_open_dict in bnpv_eff_soclong_sa_codex_open_list:
        line = BnpvEffSoclongSaCodexOpen(**bnpv_eff_soclong_sa_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_hlt_sa_codex_open
    bnpv_eff_hlt_sa_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
        dtype={"codeSubstance": str},
    )
    bnpv_eff_hlt_sa_codex_open = bnpv_eff_hlt_sa_codex_open.drop("Unnamed: 0", axis=1)

    bnpv_eff_hlt_sa_codex_open = bnpv_eff_hlt_sa_codex_open.rename(
        columns={
            "SEXE": "sexe",
            "AGE": "age",
            "EFFET_HLT": "effet_hlt",
            "SOC_LONG": "soc_long",
            "SUBSTANCE_CODEX_UNIQUE": "substance_codex_unique",
            "codeSubstance": "code",
        }
    )

    bnpv_eff_hlt_sa_codex_open_list = bnpv_eff_hlt_sa_codex_open.to_dict(
        orient="records"
    )
    for bnpv_eff_hlt_sa_codex_open_dict in bnpv_eff_hlt_sa_codex_open_list:
        line = BnpvEffHltSaCodexOpen(**bnpv_eff_hlt_sa_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_notif_sa_codex_open
    bnpv_notif_sa_codex_open = pd.read_csv(
        "/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv",
        encoding="ISO-8859-1",
        sep=";",
        dtype={"codeSubstance": str},
    )
    bnpv_notif_sa_codex_open = bnpv_notif_sa_codex_open.drop("Unnamed: 0", axis=1)

    bnpv_notif_sa_codex_open = bnpv_notif_sa_codex_open.rename(
        columns={
            "TYP_NOTIF": "typ_notif",
            "SEXE": "sexe",
            "AGE": "age",
            "SUBSTANCE_CODEX_UNIQUE": "substance_codex_unique",
            "codeSubstance": "code",
        }
    )

    bnpv_notif_sa_codex_open_list = bnpv_notif_sa_codex_open.to_dict(orient="records")
    for bnpv_notif_sa_codex_open_dict in bnpv_notif_sa_codex_open_list:
        line = BnpvNotifSaCodexOpen(**bnpv_notif_sa_codex_open_dict)
        session.add(line)
        session.commit()
