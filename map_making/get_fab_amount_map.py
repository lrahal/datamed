import pymysql

from create_database.create_mysql_db import HOSTNAME, DBNAME, UNAME, MYSQL_PWD


def create_fab_sites_api_amount_table():
    """
    Create table fab_sites_api_amount
    Containing, by CIS code:
    - substance_active (which active substances are present in the speciality)
    - sites_fabrication_substance_active
    - boites : nb of boxes sold
    - latitude
    - longitude
    - country
    """
    connection = pymysql.connect(host=HOSTNAME, db=DBNAME, user=UNAME, password=MYSQL_PWD,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    cursor = connection.cursor()

    sql = 'CREATE TABLE fab_sites_api_amount AS ' \
          'SELECT t2.cis, t2.substance_active, t2.sites_fabrication_substance_active, t2.boites, ' \
          'afsg.latitude, afsg.longitude, afsg.country ' \
          'FROM api_fab_sites_geocode AS afsg ' \
          'LEFT JOIN ' \
          '(SELECT fs.cis, fs.substance_active, fs.sites_fabrication_substance_active, t1.boites ' \
          'FROM fabrication_sites AS fs ' \
          'LEFT JOIN ' \
          '(SELECT cis_cip.cis as cis, SUM(open_medic.boites) AS boites ' \
          'FROM open_medic ' \
          'LEFT JOIN cis_cip ON open_medic.cip13 = cis_cip.cip13 ' \
          'GROUP BY cis) as t1 ' \
          'ON fs.cis = t1.cis ' \
          'GROUP BY fs.cis, fs.substance_active, fs.sites_fabrication_substance_active, t1.boites) ' \
          'AS t2 ' \
          'ON t2.sites_fabrication_substance_active = afsg.input_string'
    cursor.execute(sql)


