import pandas as pd
from sqlalchemy.orm import sessionmaker

from create_database.models import connect_db
from .models import (CorrespSpeProd, BnpvOpenMedic1418ProdCodex, BnpvEffSoclongProdCodexOpen,
                     BnpvEffHltProdCodexOpen, BnpvNotifProdCodexOpen, BnpvOpenMedic1418SaCodex,
                     BnpvEffSoclongSaCodexOpen, BnpvEffHltSaCodexOpen, BnpvNotifSaCodexOpen)

engine = connect_db()  # establish connection
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


def save_to_database_orm(session):
    # Création table Corresp_spe_prod
    corresp_spe_prod_subs = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv',
                                        encoding='ISO-8859-1', sep=';')
    corresp_spe_prod_subs = corresp_spe_prod_subs.where(pd.notnull(corresp_spe_prod_subs), None)
    corresp_spe_prod_subs_list = corresp_spe_prod_subs.to_dict(orient='records')
    for corresp_spe_prod_subs_dict in corresp_spe_prod_subs_list:
        line = CorrespSpeProd(**corresp_spe_prod_subs_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_open_medic1418_prod_codex
    bnpv_open_medic1418_prod_codex = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_open_medic1418_prod_codex_list = bnpv_open_medic1418_prod_codex.to_dict(orient='records')
    for bnpv_open_medic1418_prod_codex_dict in bnpv_open_medic1418_prod_codex_list:
        line = BnpvOpenMedic1418ProdCodex(**bnpv_open_medic1418_prod_codex_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_soclong_prod_codex_open
    bnpv_eff_soclong_prod_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_eff_soclong_prod_codex_open_list = bnpv_eff_soclong_prod_codex_open.to_dict(orient='records')
    for bnpv_eff_soclong_prod_codex_open_dict in bnpv_eff_soclong_prod_codex_open_list:
        line = BnpvEffSoclongProdCodexOpen(**bnpv_eff_soclong_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_hlt_prod_codex_open
    bnpv_eff_hlt_prod_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv',
        encoding='ISO-8859-1', sep=';')
    bnpv_eff_hlt_prod_codex_open_list = bnpv_eff_hlt_prod_codex_open.to_dict(orient='records')
    for bnpv_eff_hlt_prod_codex_open_dict in bnpv_eff_hlt_prod_codex_open_list:
        line = BnpvEffHltProdCodexOpen(**bnpv_eff_hlt_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_notif_prod_codex_open
    bnpv_notif_prod_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_notif_prod_codex_open_list = bnpv_notif_prod_codex_open.to_dict(orient='records')
    for bnpv_notif_prod_codex_open_dict in bnpv_notif_prod_codex_open_list:
        line = BnpvNotifProdCodexOpen(**bnpv_notif_prod_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_open_medic1418_sa_codex
    bnpv_open_medic1418_sa_codex = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_open_medic1418_sa_codex_list = bnpv_open_medic1418_sa_codex.to_dict(orient='records')
    for bnpv_open_medic1418_sa_codex_dict in bnpv_open_medic1418_sa_codex_list:
        line = BnpvOpenMedic1418SaCodex(**bnpv_open_medic1418_sa_codex_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_soclong_sa_codex_open
    bnpv_eff_soclong_sa_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_eff_soclong_sa_codex_open_list = bnpv_eff_soclong_sa_codex_open.to_dict(orient='records')
    for bnpv_eff_soclong_sa_codex_open_dict in bnpv_eff_soclong_sa_codex_open_list:
        line = BnpvEffSoclongSaCodexOpen(**bnpv_eff_soclong_sa_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_eff_hlt_sa_codex_open
    bnpv_eff_hlt_sa_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv', encoding='ISO-8859-1',
        sep=';')
    bnpv_eff_hlt_sa_codex_open_list = bnpv_eff_hlt_sa_codex_open.to_dict(orient='records')
    for bnpv_eff_hlt_sa_codex_open_dict in bnpv_eff_hlt_sa_codex_open_list:
        line = BnpvEffHltSaCodexOpen(**bnpv_eff_hlt_sa_codex_open_dict)
        session.add(line)
        session.commit()

    # Création table Bnpv_notif_sa_codex_open
    bnpv_notif_sa_codex_open = pd.read_csv(
        '/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')
    bnpv_notif_sa_codex_open_list = bnpv_notif_sa_codex_open.to_dict(orient='records')
    for bnpv_notif_sa_codex_open_dict in bnpv_notif_sa_codex_open_list:
        line = BnpvNotifSaCodexOpen(**bnpv_notif_sa_codex_open_dict)
        session.add(line)
        session.commit()
