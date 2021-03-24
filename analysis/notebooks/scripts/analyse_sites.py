#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('production', connection)
df = df.where(pd.notnull(df), None)


# In[4]:


df.head(1)


# In[5]:


columns = ['titulaire_amm', 'sites_fabrication_substance_active', 'sites_production',
           'sites_conditionnement_primaire', 'sites_conditionnement_secondaire', 'sites_importation',
           'sites_controle', 'sites_echantillotheque', 'sites_certification']


# In[6]:


for col in columns:
    a = df[df[col].apply(lambda x: "sii" in x and "tsiic" not in x if x else False)][col].tolist()
    if a :
        print(a)


# In[7]:


for col in columns:
    a = df[df[col].apply(lambda x: "serum institute of india" in x if x else False)][col].tolist()
    if a :
        print(a)


# In[8]:


for col in columns:
    a = df[df[col].apply(lambda x: "legacy" in x if x else False)][col].tolist()
    if a :
        print(a)


# In[9]:


for col in columns:
    print(col)
    print(df[df[col].apply(lambda x: "legacy pharmaceuticals switzerland gmbh" in x if x else False)][col])
    print(df[df[col].apply(lambda x: "legacy pharmaceuticals switzerland gmbh" in x if x else False)].denomination_specialite)
    print('---------------------------------------')


# In[ ]:




