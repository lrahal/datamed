#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db
from create_database.create_tables_in_db import get_excels_df


# # Récupérer les spécialités de la classe ATC N06AA (MITM oui/non)

# ## 4 Décembre 2020

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = get_excels_df()


# In[4]:


df = df.drop(['type_amm', 'sites_production', 'sites_conditionnement_primaire', 'sites_conditionnement_secondaire',
              'sites_importation', 'sites_controle', 'sites_echantillotheque', 'sites_certification',
              'substance_active', 'substance_active_match', 'sites_fabrication_substance_active', 'filename',
              'cos_sim'], axis=1)
df = df.dropna(how='all')
df = df.drop_duplicates()


# In[5]:


df.head(2)


# In[6]:


df_atc = pd.read_sql_table('classification', connection)


# In[7]:


df_atc.head(2)


# In[24]:


df_atc[df_atc.cis == '60528874']


# In[8]:


cis_list = df_atc[df_atc.atc.str.startswith('N06AA')].cis.unique()


# In[27]:


df2 = df[df.cis.isin(cis_list)].merge(df_atc, on='cis', how='left')
df2 = df2.drop(['id'], axis=1)


# In[28]:


df2


# In[29]:


df2.to_csv('../data/atc_N06AA_mitm.csv', sep=';', index=False)


# In[ ]:




