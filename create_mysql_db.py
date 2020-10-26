import os
import pymysql
import jade_analysis as ja
from sqlalchemy import create_engine, exc

# Credentials to database connection
HOSTNAME='localhost'
DBNAME='rs_db'
UNAME='root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def create_db():
    # Set connection to create new database
    connection = pymysql.connect(host=HOSTNAME, user=UNAME, password=MYSQL_PWD, charset='utf8mb4')
    cursor = connection.cursor()
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


def create_table():
    # Create dataframe
    df = ja.get_filtered_dataframe()

    # Create rs_db database
    create_db()

    # Set connection to created database
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Connect to database
    engine = connect_to_engine()

    # Convert dataframe to SQL table
    df.to_sql('api_fab_sites', engine, schema=None, if_exists='append', index=False,
              index_label=None, chunksize=None, dtype=None, method=None)

    # cursor.execute('alter table ' + DBNAME + '.api_fab_sites convert to character set utf8mb4 collate utf8mb4_unicode_ci;')

