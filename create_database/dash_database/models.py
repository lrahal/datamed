import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

# load environment variables
HOSTNAME = "localhost"
DBNAME = "dash_database"
UNAME = "root"
MYSQL_PWD = os.environ.get("MYSQL_PWD")


def connect_db():
    # create db create_engine
    return create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD
        ),
        echo=False,
    )


Base = declarative_base()


class Specialite(Base):
    __tablename__ = "specialite"

    cis = Column(String(120), primary_key=True)
    name = Column(LONGTEXT, nullable=True)
    forme_pharma = Column(LONGTEXT, nullable=True)
    voie_admin = Column(LONGTEXT, nullable=True)
    atc = Column(String(120), nullable=True)
    nom_atc = Column(LONGTEXT, nullable=True)
    type_amm = Column(LONGTEXT, nullable=True)
    etat_commercialisation = Column(LONGTEXT, nullable=True)


class Substance(Base):
    __tablename__ = "substance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=True)


class SpecialiteSubstance(Base):
    __tablename__ = "specialite_substance"
    __table_args__ = (
        ForeignKeyConstraint(["cis"], ["specialite.cis"]),
        ForeignKeyConstraint(["substance_id"], ["substance.id"]),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cis = Column(String(120), nullable=False)
    elem_pharma = Column(LONGTEXT, nullable=False)
    substance_id = Column(Integer, nullable=False)
    dosage = Column(LONGTEXT, nullable=True)
    ref_dosage = Column(LONGTEXT, nullable=True)
    nature_composant = Column(LONGTEXT, nullable=False)
    num_lien = Column(Integer, nullable=False)


class Produit(Base):
    __tablename__ = "produit"
    __table_args__ = (ForeignKeyConstraint(["cis"], ["specialite.cis"]),)

    cis = Column(String(120), primary_key=True)
    specialite = Column(LONGTEXT, nullable=False)
    produit = Column(LONGTEXT, nullable=False)


class Notice(Base):
    __tablename__ = "notice"
    __table_args__ = (ForeignKeyConstraint(["cis"], ["specialite.cis"]),)

    cis = Column(String(120), primary_key=True)
    specialite = Column(VARCHAR(255), nullable=False)
    notice = Column(LONGTEXT, nullable=True)


class Presentation(Base):
    __tablename__ = "presentation"
    __table_args__ = (ForeignKeyConstraint(["cis"], ["specialite.cis"]),)

    cip13 = Column(String(13), primary_key=True)
    libelle = Column(LONGTEXT, nullable=True)
    cis = Column(String(8), nullable=False)
    taux_remboursement = Column(String(13), nullable=True)


engine = connect_db()
Specialite.__table__.create(bind=engine, checkfirst=True)
Substance.__table__.create(bind=engine, checkfirst=True)
SpecialiteSubstance.__table__.create(bind=engine, checkfirst=True)
Produit.__table__.create(bind=engine, checkfirst=True)
Notice.__table__.create(bind=engine, checkfirst=True)
Presentation.__table__.create(bind=engine, checkfirst=True)
