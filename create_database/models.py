import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT, FLOAT, YEAR
from sqlalchemy.ext.declarative import declarative_base

# load environment variables
HOSTNAME = 'localhost'
DBNAME = 'fab_sites'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def connect_db():
    # create db create_engine
    db = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                       .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                       echo=False)
    return db


Base = declarative_base()


class Specialite(Base):
    __tablename__ = 'specialite'

    cis = Column(String(120), primary_key=True)
    name = Column(LONGTEXT, nullable=True)


class SubstanceActive(Base):
    __tablename__ = 'substance_active'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Presentation(Base):
    __tablename__ = 'presentation'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    cip13 = Column(String(13), primary_key=True)
    libelle = Column(LONGTEXT, nullable=True)
    cis = Column(String(8), nullable=False)


class Consommation(Base):
    __tablename__ = 'consommation'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    cis = Column(String(120), primary_key=True)
    year = Column(YEAR, nullable=False)
    ventes_officine = Column(Integer, nullable=False)
    ventes_hopital = Column(Integer, nullable=False)
    ventes_total = Column(Integer, nullable=False)


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


class Classification(Base):
    __tablename__ = 'classification'
    __table_args__ = (
        ForeignKeyConstraint(['cis'], ['specialite.cis']),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cis = Column(String(120), nullable=False)
    atc = Column(String(120), nullable=False)
    v3 = Column(String(120), nullable=False)


engine = connect_db()
Specialite.__table__.create(bind=engine, checkfirst=True)
SubstanceActive.__table__.create(bind=engine, checkfirst=True)
Presentation.__table__.create(bind=engine, checkfirst=True)
Consommation.__table__.create(bind=engine, checkfirst=True)
Fabrication.__table__.create(bind=engine, checkfirst=True)
Production.__table__.create(bind=engine, checkfirst=True)
Classification.__table__.create(bind=engine, checkfirst=True)
