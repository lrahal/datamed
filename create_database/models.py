import os

# from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# load_dotenv(find_dotenv())

# load environment variables
HOSTNAME = 'localhost'
DBNAME = 'rs_db'
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

    # Defining One to Many relationships with the relationship function on the Parent Table
    pres = relationship('Presentation', backref='specialite', lazy=True, cascade='all, delete-orphan')
    prod = relationship('Production', backref='specialite', lazy=True, cascade='all, delete-orphan')


class SubtanceActive(Base):
    __tablename__ = 'substance_active'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Presentation(Base):
    __tablename__ = 'presentation'
    __table_args__ = (
        PrimaryKeyConstraint('cis', 'cis'),
    )

    cis = Column(String(8), ForeignKey('specialite.cis'))
    cip13 = Column(String(13), nullable=False)


class Consommation(Base):
    __tablename__ = 'consommation'
    __table_args__ = (
        PrimaryKeyConstraint('cip13', 'cip13'),
    )

    cip13 = Column(String(13), ForeignKey('presentation.cip13'))
    year = Column(Integer, nullable=False)
    nb_conso = Column(Integer, nullable=False)
    nb_boites = Column(Integer, nullable=False)


class Fabrication(Base):
    __tablename__ = 'fabrication'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(LONGTEXT, nullable=False)
    year = Column(Integer, nullable=False)
    nb_conso = Column(Integer, nullable=False)
    nb_boites = Column(Integer, nullable=False)


class Production(Base):
    __tablename__ = 'production'
    __table_args__ = (
        PrimaryKeyConstraint('cis', 'cis'),
        PrimaryKeyConstraint('id', 'api_id'),
        PrimaryKeyConstraint('id', 'address_id'),
    )

    cis = Column(String(120), ForeignKey('specialite.cis'))
    api_id = Column(Integer, ForeignKey('substance_active.id'))
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('fabrication.id'))
    address = Column(LONGTEXT, nullable=False)


engine = connect_db()
Specialite.__table__.create(bind=engine, checkfirst=True)
SubtanceActive.__table__.create(bind=engine, checkfirst=True)
Presentation.__table__.create(bind=engine, checkfirst=True)
Consommation.__table__.create(bind=engine, checkfirst=True)
Fabrication.__table__.create(bind=engine, checkfirst=True)
Production.__table__.create(bind=engine, checkfirst=True)

