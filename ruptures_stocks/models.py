import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT, DATE, YEAR
from sqlalchemy.ext.declarative import declarative_base

# load environment variables
HOSTNAME = 'localhost'
DBNAME = 'ruptures_stocks'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def connect_db():
    # create db create_engine
    db = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                       .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                       echo=False)
    return db


Base = declarative_base()


class Classification(Base):
    __tablename__ = 'atc3'
    __table_args__ = ()

    id = Column(Integer, primary_key=True, autoincrement=True)
    specialite = Column(LONGTEXT, nullable=False)
    atc3 = Column(String(10), nullable=True)


class Rupture(Base):
    __tablename__ = 'rupture'
    __table_args__ = ()

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_signal = Column(Integer, nullable=False)
    signalement = Column(String(10), nullable=False)
    date_signalement = Column(DATE, nullable=False)
    laboratoire = Column(LONGTEXT, nullable=True)
    specialite = Column(LONGTEXT, nullable=False)
    rupture = Column(LONGTEXT, nullable=True)
    atc = Column(String(10), nullable=True)
    dci = Column(LONGTEXT, nullable=True)
    date_signal_debut_rs = Column(DATE, nullable=True)
    duree_ville = Column(Integer, nullable=True)
    duree_hopital = Column(Integer, nullable=True)
    date_previ_ville = Column(DATE, nullable=True)
    date_previ_hopital = Column(DATE, nullable=True)
    volumes_ventes_ville = Column(Integer, nullable=True)
    volumes_ventes_hopital = Column(Integer, nullable=True)


class Ventes(Base):
    __tablename__ = 'ventes'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    year = Column(YEAR, nullable=False)
    code_dossier = Column(String(10), nullable=False)
    cis = Column(String(120), primary_key=False)
    cip13 = Column(String(13), primary_key=False)
    specialite = Column(LONGTEXT, nullable=False)
    presentation = Column(LONGTEXT, nullable=True)
    atc = Column(String(120), nullable=False)
    regime_remb = Column(String(120), nullable=False)
    ventes_officine = Column(Integer, nullable=False)
    ventes_hopital = Column(Integer, nullable=False)
