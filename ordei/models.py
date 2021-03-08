from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT, YEAR

from create_database.models import connect_db, Base


class CorrespProdSub(Base):
    __tablename__ = "corresp_prod_sub"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_codex = Column(LONGTEXT, nullable=False)
    substance_codex_unique = Column(LONGTEXT, nullable=False)
    code = Column(String(255), nullable=False)


class BnpvOpenMedic1418ProdCodex(Base):
    __tablename__ = "bnpv_open_medic1418_prod_codex"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_codex = Column(LONGTEXT, nullable=False)
    annee = Column(YEAR, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(LONGTEXT, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_conso = Column(Integer, nullable=False)


class BnpvEffSoclongProdCodexOpen(Base):
    __tablename__ = "bnpv_eff_soclong_prod_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_codex = Column(LONGTEXT, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    soc_long = Column(LONGTEXT, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_decla_eff = Column(Integer, nullable=False)


class BnpvEffHltProdCodexOpen(Base):
    __tablename__ = "bnpv_eff_hlt_prod_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_codex = Column(LONGTEXT, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    effet_hlt = Column(LONGTEXT, nullable=False)
    soc_long = Column(LONGTEXT, nullable=False)
    n_decla_eff_hlt = Column(Integer, nullable=False)


class BnpvNotifProdCodexOpen(Base):
    __tablename__ = "bnpv_notif_prod_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_codex = Column(LONGTEXT, nullable=False)
    typ_notif = Column(LONGTEXT, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_decla = Column(Integer, nullable=False)


class BnpvOpenMedic1418SaCodex(Base):
    __tablename__ = "bnpv_open_medic1418_sa_codex"

    id = Column(Integer, primary_key=True, autoincrement=True)
    substance_codex_unique = Column(LONGTEXT, nullable=False)
    code = Column(String(255), nullable=False)
    annee = Column(YEAR, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(LONGTEXT, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_conso = Column(Integer, nullable=False)


class BnpvEffSoclongSaCodexOpen(Base):
    __tablename__ = "bnpv_eff_soclong_sa_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    substance_codex_unique = Column(LONGTEXT, nullable=False)
    code = Column(String(255), nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    soc_long = Column(LONGTEXT, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_decla_eff = Column(Integer, nullable=False)


class BnpvEffHltSaCodexOpen(Base):
    __tablename__ = "bnpv_eff_hlt_sa_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    substance_codex_unique = Column(LONGTEXT, nullable=False)
    code = Column(String(255), nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    effet_hlt = Column(LONGTEXT, nullable=False)
    soc_long = Column(LONGTEXT, nullable=False)
    n_decla_eff_hlt = Column(Integer, nullable=False)


class BnpvNotifSaCodexOpen(Base):
    __tablename__ = "bnpv_notif_sa_codex_open"

    id = Column(Integer, primary_key=True, autoincrement=True)
    substance_codex_unique = Column(LONGTEXT, nullable=False)
    code = Column(String(255), nullable=False)
    typ_notif = Column(LONGTEXT, nullable=False)
    sexe = Column(LONGTEXT, nullable=False)
    age = Column(Integer, nullable=False)
    n_cas = Column(Integer, nullable=False)
    n_decla = Column(Integer, nullable=False)


engine = connect_db()
CorrespProdSub.__table__.create(bind=engine, checkfirst=True)
BnpvOpenMedic1418ProdCodex.__table__.create(bind=engine, checkfirst=True)
BnpvEffSoclongProdCodexOpen.__table__.create(bind=engine, checkfirst=True)
BnpvEffHltProdCodexOpen.__table__.create(bind=engine, checkfirst=True)
BnpvNotifProdCodexOpen.__table__.create(bind=engine, checkfirst=True)
BnpvOpenMedic1418SaCodex.__table__.create(bind=engine, checkfirst=True)
BnpvEffSoclongSaCodexOpen.__table__.create(bind=engine, checkfirst=True)
BnpvEffHltSaCodexOpen.__table__.create(bind=engine, checkfirst=True)
BnpvNotifSaCodexOpen.__table__.create(bind=engine, checkfirst=True)
