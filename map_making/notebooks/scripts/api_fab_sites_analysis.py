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


# # Récupération des données avec géoloc

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df_fab = pd.read_sql_table('fabrication', connection)


# In[4]:


df = pd.read_sql_table('production', connection)

df = df.drop(['denomination_specialite', 'dci', 'type_amm', 'titulaire_amm',
              'sites_production', 'sites_conditionnement_primaire', 'sites_conditionnement_secondaire',
              'sites_importation', 'sites_controle', 'sites_echantillotheque', 'sites_certification',
              'substance_active', 'mitm', 'pgp', 'filename'], axis=1)
df = df.dropna(how='all')

df = df.merge(df_fab, how='left', left_on='fabrication_id', right_on='id')
df = df.rename(columns={'id_x': 'id'})
df = df.drop(columns=['id_y', 'sites_fabrication_substance_active', 'fabrication_id'])

df = df.drop_duplicates()


# In[5]:


df.head()


# In[6]:


len(df), len(df.cis.unique())


# In[7]:


# Keep rows having the right format (8 digits) (88% of all rows)
df = df[~df.country.isna()]
#df = df[~df.cis.isna()]
#df = df[df.cis.apply(lambda x: x.isdigit() and len(x) == 8)]


# In[8]:


countries = sorted(df.country.unique())


# In[9]:


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


# In[10]:


df['europe'] = df.country.isin(europe_countries)
df['oecd'] = df.country.isin(oecd_countries)
df['third'] = df.country.isin(third_countries)


# # Regroupement par code CIS

# In[11]:


df2 = pd.DataFrame(sorted(df.cis.dropna().unique()), columns=['cis'])


# In[12]:


df2['europe'] = df2.apply(lambda x: True in df[df.cis == x.cis].europe.to_list(), axis=1)
df2['oecd'] = df2.apply(lambda x: True in df[df.cis == x.cis].oecd.to_list(), axis=1)
df2['third'] = df2.apply(lambda x: True in df[df.cis == x.cis].third.to_list(), axis=1)


# In[13]:


df2[df2.cis == '69974276']


# In[14]:


df[df.cis == '69974276']


# In[15]:


df2['europe_only'] = df2.apply(lambda x: x.europe and not x.third, axis=1)
df2['third_only'] = df2.apply(lambda x: x.third and not x.europe, axis=1)
df2['mix'] = df2.apply(lambda x: x.europe and x.third, axis=1)


# In[16]:


df2.head()


# In[17]:


len(df2[df2.europe_only]) + len(df2[df2.third_only]) + len(df2[df2.mix]), len(df.cis.dropna().unique())


# In[18]:


def get_category(x):
    if x.europe_only:
        return 'Europe only'
    if x.third_only:
        return 'Third only'
    if x.mix:
        return 'Europe & Third'


# In[19]:


df2['category'] = df2.apply(lambda x: get_category(x), axis=1)


# In[20]:


df2.head()


# # Graphiques

# In[21]:


sns.set_style("white")
sns.set_style("ticks")

plt.figure(figsize=(16, 6))
ax = sns.countplot(x='category',
                   data=df2, 
                   facecolor=(0, 0, 0, 0),
                   linewidth=5,
                   edgecolor=sns.color_palette('dark', 3))


# In[22]:


corresp_dict = {
    '46': str(len(df2[df2.europe_only])) + ' (' + str(round(len(df2[df2.europe_only])/len(df2) * 100, 2)) +'%)',
    '47': str(len(df2[df2.third_only])) + ' (' + str(round(len(df2[df2.third_only])/len(df2) * 100, 2)) +'%)',
    '6': str(len(df2[df2.mix])) + ' (' + str(round(len(df2[df2.mix])/len(df2) * 100, 2)) +'%)'
}


# In[23]:


plt.figure(figsize=(15, 10))
df2['category'].value_counts(normalize=True).plot(kind='pie', autopct=lambda x: corresp_dict[str(math.floor(x))])


# # Proportions des pays fabriquants d'API

# In[24]:


df_repartition = df_fab.copy()


# In[25]:


df_repartition.country = df_fab.country.apply(lambda x: 'Europe' if x in europe_countries else x)


# In[26]:


dfx = df_repartition.groupby('country').count().reset_index()


# In[27]:


dfx['fracs'] = dfx.apply(lambda x: x.id / len(df_repartition) * 100, axis=1)


# In[28]:


dfx = dfx[dfx.fracs > 1.5]


# In[29]:


dfx.country.unique()


# In[30]:


# Some data
labels = dfx.country.tolist()
fracs = dfx.fracs.tolist()

# Make figure and axes
fig, axs = plt.subplots(figsize=(15, 10))

# A standard pie plot
axs.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)

plt.show()


# # Export dans un csv

# In[31]:


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




