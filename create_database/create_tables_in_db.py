from .upload_db import upload_table_from_db, upload_bdpm_from_csv, upload_cis_cip_from_csv
import pandas as pd
from .create_mysql_db import connect_to_engine
import pymysql
import sqlalchemy as db
import os

# Credentials to database connection
HOSTNAME = 'localhost'
DBNAME = 'rs_db'
UNAME = 'root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def create_api_table(engine, connection, metadata, df):
    api_list = df.substance_active_match.unique().tolist()

    df_cis_compo = upload_bdpm_from_csv('./create_database/data/CIS_COMPO_bdpm.txt')
    api_list.extend([api for api in df_cis_compo.substance_active.unique() if api not in api_list])
    api_list = list(filter(None, api_list))
    api_list = sorted(api_list)
    values_list = [{'name': api} for api in api_list]

    api_table = db.Table('substance_active', metadata,
                         db.Column('Id', db.Integer(), primary_key=True, autoincrement=True),
                         db.Column('name', db.String(255), nullable=False))

    metadata.create_all(engine)  # Creates the table

    query = db.insert(api_table)
    ResultProxy = connection.execute(query, values_list)


def create_specialite_table(engine, connection, metadata, df):
    cis_list = df.cis.unique().tolist()

    df_cis_compo = upload_bdpm_from_csv('./create_database/data/CIS_COMPO_bdpm.txt')
    cis_list.extend([str(cis) for cis in df_cis_compo.cis.unique() if str(cis) not in cis_list])
    cis_list = list(filter(None, cis_list))
    cis_list = sorted(cis_list)
    values_list = [{'cis': cis} for cis in cis_list]
    max_len = len(max(cis_list, key=len))

    cis_table = db.Table('specialite', metadata, db.Column('cis', db.String(max_len), primary_key=True))

    metadata.create_all(engine)  # Creates the table

    query = db.insert(cis_table)
    ResultProxy = connection.execute(query, values_list)


def create_presentation_table(engine, connection, metadata):
    df_cis_cip = upload_cis_cip_from_csv('./create_database/data/CIS_CIP_bdpm.txt')
    df_records = df_cis_cip.to_dict('records')

    values_list = [{str(k): str(v) for k, v in zip(('cis', 'cip13'), (d['cis'], d['cip13']))} for d in df_records]

    cip_table = db.Table('presentation', metadata,
                         db.Column('cis', db.String(8), ForeignKey('points_of_interest.poi_id')),
                         db.Column('cip13', db.String(13), nullable=False))

    metadata.create_all(engine)  # Creates the table

    query = db.insert(cip_table)
    ResultProxy = connection.execute(query, values_list)


def create_consommation_table():
    df_om = pd.read_csv('./create_database/data/NB_2019_cip13.csv',
                        names=['cip13', 'nbc', 'boites'], delimiter=';', header=0)
    df_om['year'] = 2019


def create_fabrication_table():
    df_geo = upload_table_from_db('api_sites_addresses')
    df_records = df_geo.to_dict('records')
    geo_dict = [
        {
            k: v for k, v in zip(('address', 'latitude', 'longitude', 'country'),
                                 (d['input_string'], d['latitude'], d['longitude'], d['country']))
        }
        for d in df_records
    ]


def create_production_table(df):
    df_records = df.to_dict('records')
    df_dict = [
        {
            k: v for k, v in zip(('cis', 'substance_active', 'address'),
                                 (d['cis'], d['substance_active'], d['sites_fabrication_substance_active']))
        }
        for d in df_records
    ]
    df_dict = [dict(t) for t in {tuple(d.items()) for d in df_dict}]


def main():
    df = upload_table_from_db('fabrication_sites')
    df['substance_active_match'] = df.apply(
        lambda x: x.substance_active if not x.substance_active_match else x.substance_active_match, axis=1)

    # Create SQLAlchemy engine to connect to MySQL Database
    engine = db.create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                              .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                              echo=False)
    connection = engine.connect()
    metadata = db.MetaData()

    fab_sites = db.Table('fabrication_sites', metadata, autoload=True, autoload_with=engine)
