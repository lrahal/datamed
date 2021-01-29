import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT, FLOAT, YEAR, DATE, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

# load environment variables
HOSTNAME = 'localhost'
DBNAME = 'fab_sites'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def connect_db():
    # create db create_engine
    return create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                         .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                         echo=False)


Base = declarative_base()


class Specialite(Base):
    __tablename__ = 'specialite'

    cis = Column(String(120), primary_key=True)
    name = Column(LONGTEXT, nullable=True)
    forme_pharma = Column(LONGTEXT, nullable=True)
    voie_admin = Column(LONGTEXT, nullable=True)
    atc = Column(String(120), nullable=True)
    nom_atc = Column(LONGTEXT, nullable=True)
    type_amm = Column(LONGTEXT, nullable=True)
    etat_commercialisation = Column(LONGTEXT, nullable=True)


class SubstanceActive(Base):
    __tablename__ = 'substance_active'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(Integer, nullable=True)


class SpecialiteSubstance(Base):
    __tablename__ = 'specialite_substance'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
        ForeignKeyConstraint(['substance_active_id'], ['substance_active.id']),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cis = Column(String(120), nullable=False)
    elem_pharma = Column(LONGTEXT, nullable=False)
    substance_active_id = Column(Integer, nullable=False)
    dosage = Column(LONGTEXT, nullable=True)
    ref_dosage = Column(LONGTEXT, nullable=True)
    nature_composant = Column(LONGTEXT, nullable=False)
    num_lien = Column(Integer, nullable=False)


class Presentation(Base):
    __tablename__ = 'presentation'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    cip13 = Column(String(13), primary_key=True)
    libelle = Column(LONGTEXT, nullable=True)
    cis = Column(String(8), nullable=False)
    taux_remboursement = Column(String(13), nullable=True)


class Fabrication(Base):
    __tablename__ = 'fabrication'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(LONGTEXT, nullable=False)
    latitude = Column(FLOAT, nullable=True)
    longitude = Column(FLOAT, nullable=True)
    country = Column(LONGTEXT, nullable=True)


class Production(Base):
    __tablename__ = 'production'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
        ForeignKeyConstraint(['substance_active_id'], ['substance_active.id']),
        ForeignKeyConstraint(['fabrication_id'], ['fabrication.id']),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cis = Column(String(120), nullable=False)
    substance_active_id = Column(Integer, nullable=False)
    fabrication_id = Column(Integer, nullable=False)
    substance_active = Column(String(255), nullable=False)
    sites_fabrication_substance_active = Column(LONGTEXT, nullable=False)
    denomination_specialite = Column(LONGTEXT, nullable=True)
    dci = Column(LONGTEXT, nullable=True)
    type_amm = Column(LONGTEXT, nullable=True)
    titulaire_amm = Column(LONGTEXT, nullable=True)
    sites_production = Column(LONGTEXT, nullable=True)
    sites_conditionnement_primaire = Column(LONGTEXT, nullable=True)
    sites_conditionnement_secondaire = Column(LONGTEXT, nullable=True)
    sites_importation = Column(LONGTEXT, nullable=True)
    sites_controle = Column(LONGTEXT, nullable=True)
    sites_echantillotheque = Column(LONGTEXT, nullable=True)
    sites_certification = Column(LONGTEXT, nullable=True)
    mitm = Column(LONGTEXT, nullable=True)
    pgp = Column(LONGTEXT, nullable=True)
    filename = Column(LONGTEXT, nullable=False)


class Ruptures(Base):
    __tablename__ = 'ruptures'
    __table_args__ = ()

    id_signal = Column(Integer, primary_key=True)
    signalement = Column(String(10), nullable=True)
    date_signalement = Column(DATE, nullable=True)
    laboratoire = Column(LONGTEXT, nullable=True)
    specialite = Column(LONGTEXT, nullable=True)
    voie = Column(LONGTEXT, nullable=True)
    voie_4_classes = Column(LONGTEXT, nullable=True)
    rupture = Column(LONGTEXT, nullable=True)
    etat_dossier = Column(LONGTEXT, nullable=False)
    circuit_touche_ville = Column(BOOLEAN, nullable=False)
    circuit_touche_hopital = Column(BOOLEAN, nullable=False)
    atc = Column(String(10), nullable=True)
    dci = Column(LONGTEXT, nullable=True)
    date_signal_debut_rs = Column(DATE, nullable=True)
    duree_ville = Column(LONGTEXT, nullable=True)
    duree_hopital = Column(LONGTEXT, nullable=True)
    date_previ_ville = Column(DATE, nullable=True)
    date_previ_hopital = Column(DATE, nullable=True)
    volumes_ventes_ville = Column(Integer, nullable=True)
    volumes_ventes_hopital = Column(Integer, nullable=True)


class Ventes(Base):
    __tablename__ = 'ventes'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    octave_id = Column(Integer, primary_key=True)
    annee = Column(YEAR, nullable=False)
    code_dossier = Column(LONGTEXT, nullable=False)
    laboratoire = Column(LONGTEXT, nullable=True)
    cis = Column(String(120), nullable=False)
    denomination_specialite = Column(LONGTEXT, nullable=False)
    voie = Column(LONGTEXT, nullable=False)
    voie_4_classes = Column(LONGTEXT, nullable=False)
    cip13 = Column(String(13), nullable=False)
    libelle = Column(LONGTEXT, nullable=True)
    atc = Column(String(120), nullable=False)
    regime_remb = Column(String(120), nullable=False)
    unites_officine = Column(Integer, nullable=False)
    unites_hopital = Column(Integer, nullable=False)


class Produits(Base):
    __tablename__ = 'produits'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    cis = Column(String(120), primary_key=True)
    specialite = Column(LONGTEXT, nullable=False)
    produit_codex = Column(LONGTEXT, nullable=False)


class ServiceMedicalRendu(Base):
    __tablename__ = 'service_medical_rendu'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    cis = Column(String(120), primary_key=True)
    code_dossier = Column(LONGTEXT, nullable=False)
    motif = Column(LONGTEXT, nullable=False)
    date_avis = Column(DATE, nullable=False)
    smr = Column(LONGTEXT, nullable=False)
    libelle_smr = Column(LONGTEXT, nullable=False)
    asmr = Column(LONGTEXT, nullable=True)
    libelle_asmr = Column(LONGTEXT, nullable=True)


engine = connect_db()
Specialite.__table__.create(bind=engine, checkfirst=True)
SubstanceActive.__table__.create(bind=engine, checkfirst=True)
SpecialiteSubstance.__table__.create(bind=engine, checkfirst=True)
Presentation.__table__.create(bind=engine, checkfirst=True)
Production.__table__.create(bind=engine, checkfirst=True)
Ruptures.__table__.create(bind=engine, checkfirst=True)
Ventes.__table__.create(bind=engine, checkfirst=True)
Produits.__table__.create(bind=engine, checkfirst=True)
ServiceMedicalRendu.__table__.create(bind=engine, checkfirst=True)
