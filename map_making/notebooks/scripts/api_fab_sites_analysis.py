#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
import math

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.upload_db import upload_table_from_db
from map_making.get_maps_data import *


# # Récupération des données avec géoloc

# In[2]:


df = get_data('fabrication_sites',
              '../data/sites_fabrication_substance_active.csv',
              'sites_fabrication_substance_active')
df = clean_data(df)


# In[3]:


len(df), len(df.cis.unique())


# In[4]:


df.head(2)


# In[5]:


# Keep rows having the right format (8 digits) (88% of all rows)
df = df[~df.cis.isna()]
df = df[df.cis.apply(lambda x: x.isdigit() and len(x) == 8)]

len(df)


# In[6]:


countries = sorted(df.country.unique())


# In[7]:


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


# In[8]:


df['europe'] = df.country.isin(europe_countries)
df['oecd'] = df.country.isin(oecd_countries)
df['third'] = df.country.isin(third_countries)


# # Regroupement par code CIS

# In[9]:


df2 = pd.DataFrame(sorted(df.cis.unique()), columns=['cis'])


# In[10]:


df2['europe'] = df2.apply(lambda x: True in df[df.cis == x.cis].europe.to_list(), axis=1)
df2['oecd'] = df2.apply(lambda x: True in df[df.cis == x.cis].oecd.to_list(), axis=1)
df2['third'] = df2.apply(lambda x: True in df[df.cis == x.cis].third.to_list(), axis=1)


# In[11]:


df[df.cis == '69974276']


# In[12]:


df2['europe_only'] = df2.apply(lambda x: x.europe and not x.third, axis=1)
df2['third_only'] = df2.apply(lambda x: x.third and not x.europe, axis=1)
df2['mix'] = df2.apply(lambda x: x.europe and x.third, axis=1)


# In[13]:


df2.head()


# In[14]:


len(df2[df2.europe_only]) + len(df2[df2.third_only]) + len(df2[df2.mix]), len(df.cis.unique())


# In[15]:


df2[(df2.europe == False) & (df2.third == False)]


# In[16]:


def get_category(x):
    if x.europe_only:
        return 'Europe only'
    if x.third_only:
        return 'Third only'
    if x.mix:
        return 'Europe & Third'


# In[17]:


df2['category'] = df2.apply(lambda x: get_category(x), axis=1)


# In[18]:


df2.head()


# # Graphiques

# In[19]:


sns.set_style("white")
sns.set_style("ticks")

plt.figure(figsize=(16, 6))
ax = sns.countplot(x='category',
                   data=df2, 
                   facecolor=(0, 0, 0, 0),
                   linewidth=5,
                   edgecolor=sns.color_palette('dark', 3))


# In[20]:


corresp_dict = {
    '45': str(len(df2[df2.europe_only])) + ' (' + str(round(len(df2[df2.europe_only])/len(df2) * 100, 2)) +'%)',
    '47': str(len(df2[df2.third_only])) + ' (' + str(round(len(df2[df2.third_only])/len(df2) * 100, 2)) +'%)',
    '6': str(len(df2[df2.mix])) + ' (' + str(round(len(df2[df2.mix])/len(df2) * 100, 2)) +'%)'
}


# In[21]:


plt.figure(figsize=(15, 10))
df2['category'].value_counts(normalize=True).plot(kind='pie', autopct=lambda x: corresp_dict[str(math.floor(x))])


# In[22]:


df2


# # Export dans un csv

# In[23]:


df_spe = upload_table_from_db('cis_specialite')


# In[24]:


# Merge both dataframes
df_final = pd.merge(
    df2,
    df_spe[['cis', 'denomination_specialite']], on='cis', how='inner'
)


# In[25]:


df_final.to_csv('../data/api_fab_sites_repartition.csv', index=False, sep=';')


# In[ ]:




