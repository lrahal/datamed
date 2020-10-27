import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine

# Credentials to database connection
HOSTNAME='localhost'
DBNAME='rs_db'
UNAME='root'
MYSQL_PWD = os.environ.get('MYSQL_PWD')


def upload_data(table_name='fabrication_sites'):
    engine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'
                           .format(host=HOSTNAME, db=DBNAME, user=UNAME, pw=MYSQL_PWD),
                           echo=False)

    # Load dataframe from database
    print('Loading dataframe from database...')
    df = pd.read_sql('SELECT * FROM ' + table_name, con=engine)