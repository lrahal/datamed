import os

import pandas as pd
import pymysql
from sqlalchemy import create_engine, exc

from .jade_analysis import build_api_fab_sites_dataframe

# Credentials to database connection
HOSTNAME='localhost'
DBNAME='rs_db'
UNAME='root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def create_db(cursor):
    # Set connection to create new database
    print('Database {} creation...'.format(DBNAME))
    cursor.execute('create database ' + DBNAME)
    cursor.execute('alter database ' + DBNAME + ' character set utf8mb4 collate utf8mb4_unicode_ci;')


def connect_to_engine():
    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                           .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                           echo=False)

    for _ in range(2):
        # Raise sqlalchemy error once and retry
        # Check why running it 2 times works...
        while True:
            try:
                engine.connect()  # connect to the database
            except exc.InternalError:
                continue
            break
    return engine


def create_table(df: pd.DataFrame, table_name: str):
    # Set connection to created database
    print('Table {} creation...'.format(table_name))
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Connect to database
    engine = connect_to_engine()

    # Convert dataframe to SQL table
    df.to_sql(table_name, engine, schema=None, if_exists='append', index=False,
              index_label=None, chunksize=None, dtype=None, method=None)

    # cursor.execute('alter table ' + DBNAME + '.fabrication_sites convert to character set utf8mb4 collate utf8mb4_unicode_ci;')


def main():
    path = '/Users/linerahal/Documents/GitHub/datamed/create_database/data/jade_final/'
    # Load dataframe
    print('Loading dataframe from concatenated Excel files...')
    df = build_api_fab_sites_dataframe(path)

    # Check if rs_db database exists:
    connection = pymysql.connect(host=HOSTNAME, user=UNAME, password=MYSQL_PWD, charset='utf8mb4')
    cursor = connection.cursor()
    db_exists = cursor.execute(
        "select schema_name from information_schema.schemata where schema_name = '{}';".format(DBNAME)
    ) == 1
    if not db_exists:
        # Create rs_db database
        create_db(cursor)
        print('Database {} created!'.format(DBNAME))

    table_name = 'fabrication_sites'
    create_table(df, table_name)
    print('Table {} created! Youpiyé!'.format(table_name) )


if __name__ == '__main__':
    main()
