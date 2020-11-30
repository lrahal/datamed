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

    sql = 'CREATE TABLE fabrication_sites_boites AS ' \
          'SELECT t2.cis, t2.api, t2.sites_fabrication_substance_active, t2.boites, ' \
          'asa.latitude, asa.longitude, asa.country ' \
          'FROM ' \
          '(SELECT fs.cis, ' \
          'CASE WHEN substance_active_match IS NULL THEN fs.substance_active ELSE substance_active_match END ' \
          'AS api, fs.sites_fabrication_substance_active, t1.boites ' \
          'FROM fabrication_sites AS fs ' \
          'LEFT JOIN ' \
          '(SELECT cis_cip.cis as cis, SUM(open_medic.boites) AS boites ' \
          'FROM open_medic ' \
          'LEFT JOIN cis_cip ON open_medic.cip13 = cis_cip.cip13 ' \
          'GROUP BY cis) as t1 ' \
          'ON fs.cis = t1.cis) AS t2 ' \
          'LEFT JOIN api_sites_addresses AS asa ' \
          'ON t2.sites_fabrication_substance_active = asa.input_string'
    cursor.execute(sql)


    sql = 'CREATE TABLE prout AS ' \
          'SELECT fs.cis, ' \
          'CASE WHEN substance_active_match IS NULL THEN fs.substance_active ELSE substance_active_match END ' \
          'AS api, fs.sites_fabrication_substance_active, t1.boites ' \
          'FROM fabrication_sites AS fs ' \
          'LEFT JOIN ' \
          '(SELECT cis_cip.cis as cis, SUM(open_medic.boites) AS boites ' \
          'FROM open_medic ' \
          'LEFT JOIN cis_cip ON open_medic.cip13 = cis_cip.cip13 ' \
          'GROUP BY cis) as t1 ' \
          'ON fs.cis = t1.cis'
    cursor.execute(sql)


    sql = 'CREATE TABLE fab_sites_api_amount AS ' \
          'SELECT t2.cis, t2.api, t2.sites_fabrication_substance_active, t2.boites, ' \
          '    asa.latitude, asa.longitude, asa.country ' \
          '    FROM api_sites_addresses AS asa ' \
          'LEFT JOIN ' \
          '(SELECT fs.cis, ' \
          'CASE WHEN substance_active_match IS NULL THEN fs.substance_active ELSE substance_active_match END ' \
          'AS api, fs.sites_fabrication_substance_active, t1.boites ' \
          'FROM fabrication_sites AS fs ' \
          'LEFT JOIN ' \
          '(SELECT cis_cip.cis as cis, SUM(open_medic.boites) AS boites ' \
          'FROM open_medic ' \
          'LEFT JOIN cis_cip ON open_medic.cip13 = cis_cip.cip13 ' \
          'GROUP BY cis) as t1 ' \
          'ON fs.cis = t1.cis ' \
          'GROUP BY fs.cis, api, fs.sites_fabrication_substance_active, t1.boites) ' \
          'AS t2 ' \
          'ON t2.sites_fabrication_substance_active = asa.input_string'
    cursor.execute(sql)


