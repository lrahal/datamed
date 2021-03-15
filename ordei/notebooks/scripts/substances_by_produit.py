#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import json
import zipfile

import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('corresp_spe_prod', connection)
df = df.where(pd.notnull(df), None)


# In[4]:


df.produit_codex = df.produit_codex.str.lower()
df.substance_codex_unique = df.substance_codex_unique.str.lower()


# In[5]:


prod_sub = pd.read_csv("../data/liste_produits_substances.csv", sep=";")
prod_sub.medicament = prod_sub.medicament.str.lower()


# In[6]:


prod_sub.head()


# In[7]:


df = df[df.produit_codex.isin(prod_sub.medicament.unique())]


# In[8]:


len(df)


# In[9]:


df.head()


# In[10]:


records = df.to_dict(orient='records')


# In[11]:


sub_by_prod = {
    prod: df[df.produit_codex == prod].substance_codex_unique.unique().tolist() for prod in df.produit_codex.unique()
}


# In[12]:


with open('../data/substance_by_produit.json', 'w') as outfile:
    json.dump(sub_by_prod, outfile)


# # Liste CIS - Spé - Substance

# In[13]:


df_cis = pd.read_csv('../data/corresp_cis_spe_prod_subs_utf8.csv', sep=';',
                     dtype={"codeCIS": str})

df_cis = df_cis.where(pd.notnull(df_cis), None)

df_cis.SPECIALITE_CODEX = df_cis.SPECIALITE_CODEX.str.lower().str.capitalize()
df_cis.PRODUIT_CODEX = df_cis.PRODUIT_CODEX.str.lower().str.capitalize()
df_cis.SUBSTANCE_CODEX_UNIQUE = df_cis.SUBSTANCE_CODEX_UNIQUE.str.lower().str.capitalize()


# In[14]:


df_cis.head()


# # Substance by spécialité

# In[15]:


with zipfile.ZipFile("../data/med_dict.json.zip", "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        med_dict = json.loads(data.decode("utf-8"))

keys_ok = med_dict.keys()

sub_by_spe = {
    spe: {
        'cis': df_cis[df_cis.SPECIALITE_CODEX == spe].codeCIS.unique().tolist(), 
        'produit': df_cis[df_cis.SPECIALITE_CODEX == spe].PRODUIT_CODEX.values[0],
        'substances': df_cis[df_cis.SPECIALITE_CODEX == spe].SUBSTANCE_CODEX_UNIQUE.unique().tolist()
    }
    for spe in df_cis.SPECIALITE_CODEX.unique()
    if df_cis[df_cis.SPECIALITE_CODEX == spe].PRODUIT_CODEX.values[0] in keys_ok
}

with open('../data/substance_by_specialite.json', 'w') as outfile:
    json.dump(sub_by_spe, outfile)


# # Liste spécialités

# In[16]:


spe_dict = {spe: v['cis'] for spe, v in sub_by_spe.items()}

with open('../data/liste_specialites.json', 'w') as outfile:
    json.dump(spe_dict, outfile)


# In[17]:


df_cis[df_cis.SPECIALITE_CODEX == 'Coveram 10 mg/5 mg, comprimé']


# # ATC

# In[23]:


df_atc = pd.read_sql_table('specialite', connection)
df_atc = df_atc.where(pd.notnull(df_atc), None)

df_atc.head(1)


# In[27]:


cis_list = list(df_cis.codeCIS.unique())


# In[51]:


atc_by_spe = {
    df_cis[df_cis.codeCIS == cis].SPECIALITE_CODEX.values[0]: {
        'code_atc': df_atc[df_atc.cis == cis].atc.values[0],
        'nom_atc': df_atc[df_atc.cis == cis].nom_atc.apply(
            lambda x: x.lower().capitalize() if x else None).values[0],
    }
    for cis in cis_list
}


# In[55]:


with open('../data/atc_by_spe.json', 'w') as outfile:
    json.dump(atc_by_spe, outfile)


# In[ ]:




