#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db
from create_database.create_tables_in_db import get_excels_df


# # Récupération des données avec géoloc

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()

#metadata = MetaData()
#metadata.reflect(engine)


# In[3]:


#substance_active = metadata.tables['substance_active']
#production = metadata.tables['production']
#j = production.join(substance_active, production.c.substance_active_id == substance_active.c.id)
#sel_st = select([production.c.cis, substance_active.c.name]).select_from(j)
#res = connection.execute(sel_st)
#for row in res:
#    print(row)


# In[4]:


#df_prod = pd.read_sql_table('production', connection)
#df_api = pd.read_sql_table('substance_active', connection)
df_fab = pd.read_sql_table('fabrication', connection)


# In[5]:


df = df_prod.merge(df_api, how='left', left_on='substance_active_id', right_on='id')
df = df.merge(df_fab, how='left', left_on='fabrication_id', right_on='id')
df = df.drop(['id_x', 'id_y', 'id'], axis=1)


# In[ ]:


df = get_excels_df()
df = df.merge(df_fab, how='left', left_on='sites_fabrication_substance_active', right_on='address')
df = df.drop(['denomination_specialite', 'dci', 'type_amm', 'titulaire_amm', 'sites_production',
              'sites_conditionnement_primaire', 'sites_conditionnement_secondaire', 'sites_importation',
              'sites_controle', 'sites_echantillotheque', 'sites_certification', 'substance_active',
              'sites_fabrication_substance_active', 'mitm', 'pgp', 'filename', 'cos_sim', 'id'], axis=1)
df = df.rename(columns={'substance_active_match': 'substance_active'})
df = df.dropna(how='all')
df = df.drop_duplicates()


# In[ ]:


df.head()


# In[ ]:


len(df), len(df.cis.unique())


# In[ ]:


# Keep rows having the right format (8 digits) (88% of all rows)
df = df[~df.country.isna()]
#df = df[~df.cis.isna()]
#df = df[df.cis.apply(lambda x: x.isdigit() and len(x) == 8)]


# In[ ]:


countries = sorted(df.country.unique())


# In[ ]:


europe_countries = ['Germany', 'Belgium', 'Austria', 'Bulgaria', 'Croatia', 'Denmark', 'Spain', 'Estonia', 'Finland',
                    'France', 'French Guiana', 'Martinique', 'Réunion', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
                    'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Czechia', 'Romania', 'Slovakia',
                    'Slovenia', 'Sweden']
oecd_countries = ['Germany', 'Australia', 'Austria', 'Belgium', 'Canada', 'Chile', 'Colombia', 'Czechia', 'Denmark',
                  'Estonia', 'Finland', 'France', 'French Guiana', 'Martinique', 'Réunion', 'Greece', 'Hungary', 'Iceland', 'Ireland',
                  'Israel', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania', 'Luxembourg', 'Mexico', 'Netherlands',
                  'New Zealand', 'Norway', 'Poland', 'Portugal', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 
                  'Switzerland', 'Turkey', 'United Kingdom', 'United States']
third_countries = [c for c in countries if c not in europe_countries]


# In[ ]:


df['europe'] = df.country.isin(europe_countries)
df['oecd'] = df.country.isin(oecd_countries)
df['third'] = df.country.isin(third_countries)


# # Regroupement par code CIS

# In[ ]:


df2 = pd.DataFrame(sorted(df.cis.dropna().unique()), columns=['cis'])


# In[ ]:


df2['europe'] = df2.apply(lambda x: True in df[df.cis == x.cis].europe.to_list(), axis=1)
df2['oecd'] = df2.apply(lambda x: True in df[df.cis == x.cis].oecd.to_list(), axis=1)
df2['third'] = df2.apply(lambda x: True in df[df.cis == x.cis].third.to_list(), axis=1)


# In[ ]:


df[df.cis == '69974276']


# In[ ]:


df2['europe_only'] = df2.apply(lambda x: x.europe and not x.third, axis=1)
df2['third_only'] = df2.apply(lambda x: x.third and not x.europe, axis=1)
df2['mix'] = df2.apply(lambda x: x.europe and x.third, axis=1)


# In[ ]:


df2.head()


# In[ ]:


len(df2[df2.europe_only]) + len(df2[df2.third_only]) + len(df2[df2.mix]), len(df.cis.dropna().unique())


# In[ ]:


def get_category(x):
    if x.europe_only:
        return 'Europe only'
    if x.third_only:
        return 'Third only'
    if x.mix:
        return 'Europe & Third'


# In[ ]:


df2['category'] = df2.apply(lambda x: get_category(x), axis=1)


# In[ ]:


df2.head()


# # Graphiques

# In[ ]:


sns.set_style("white")
sns.set_style("ticks")

plt.figure(figsize=(16, 6))
ax = sns.countplot(x='category',
                   data=df2, 
                   facecolor=(0, 0, 0, 0),
                   linewidth=5,
                   edgecolor=sns.color_palette('dark', 3))


# In[ ]:


corresp_dict = {
    '46': str(len(df2[df2.europe_only])) + ' (' + str(round(len(df2[df2.europe_only])/len(df2) * 100, 2)) +'%)',
    '47': str(len(df2[df2.third_only])) + ' (' + str(round(len(df2[df2.third_only])/len(df2) * 100, 2)) +'%)',
    '6': str(len(df2[df2.mix])) + ' (' + str(round(len(df2[df2.mix])/len(df2) * 100, 2)) +'%)'
}


# In[ ]:


plt.figure(figsize=(15, 10))
df2['category'].value_counts(normalize=True).plot(kind='pie', autopct=lambda x: corresp_dict[str(math.floor(x))])


# # Export dans un csv

# In[ ]:


df_spe = upload_table_from_db('cis_specialite')


# In[ ]:


# Merge both dataframes
df_final = pd.merge(
    df2,
    df_spe[['cis', 'denomination_specialite']], on='cis', how='inner'
)


# In[ ]:


df_final.to_csv('../data/api_fab_sites_repartition.csv', index=False, sep=';')


# In[ ]:




