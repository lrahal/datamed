#!/usr/bin/env python
# coding: utf-8

# # Réunion avec le LEEM - 8 Décembre 2020
# Sortir un jeu de données pour la réunion du 8 Décembre 2020 avec le LEEM sur le sujet du décret stocks.<br/>
# On a une liste de classes ATC, il faut lister les spécialités, présentations et DCI concernées, ainsi que l'info MITM

# In[1]:


import sys
import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db
from create_database.upload_db import upload_compo_from_rsp, upload_cis_from_rsp


# # Load ATC data

# In[2]:


df_xls = pd.read_excel('../data/leem/Projet de liste - Durée de stock étendue v18-09-2020.xlsx', header=0)


# In[3]:


df_xls.head(1)


# In[4]:


# Classes ATC qui nous intéressent
atc_list = df_xls.ATC.unique()
len(atc_list)


# # Upload dataframes and join them

# In[5]:


# Get substance_active info
df_api = upload_compo_from_rsp('/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/COMPO_RSP.txt')
df_api = df_api[df_api.nature_composant == 'SA']
df_api = df_api.drop(columns=['v', 'elem_pharma', 'dosage', 'ref_dosage', 'num_lien', 'nature_composant'])
df_api = df_api.astype({'cis': 'str'})


# In[6]:


# Get spécialité info
df_cis = upload_cis_from_rsp('/Users/ansm/Documents/GitHub/datamed/create_database/data/RSP/CIS_RSP.txt')
df_cis = df_cis.astype({'cis': 'str'})


# In[7]:


# Merge df_api et df_cis
df_api = df_api.merge(df_cis[['cis', 'etat_commercialisation']], on='cis', how='left')


# In[8]:


df_api.head()


# In[9]:


# df_api[df_api.substance_active == 'sulfate de ciprofloxacine']


# In[10]:


# df_api[df_api.substance_active == 'chlorhydrate de ciprofloxacine']


# # Join avec ATC

# In[11]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[12]:


# Upload classification table
df_atc = pd.read_sql_table('classification', connection)


# In[13]:


df = df_api[['cis', 'code_substance', 'substance_active', 'etat_commercialisation']].merge(
    df_atc, on='cis', how='left')
df = df.drop(['id'], axis=1)


# In[14]:


def check_atc_in_list(a):
    for atc in atc_list:
        if a.startswith(atc):
            return True
    else:
        return False


# In[15]:


df['atc_in_list'] = df.atc.apply(lambda x: check_atc_in_list(x) if not pd.isnull(x) else False)


# In[16]:


# Keep only ATC that are listed and état is "commercialisée"
df = df[(df.atc_in_list) & (df.etat_commercialisation == 'Commercialisée')]
df = df.drop_duplicates()


# In[17]:


df.head(1)


# In[18]:


#pd.DataFrame(df[(df.atc.isna()) & (df.etat_commercialisation == 'Commercialisée')].cis.unique()).to_csv(
#    'cis_list.txt', index=False)


# ## Retrouver nom spécialité

# In[19]:


df_cis = pd.read_sql_table('specialite', connection)


# In[20]:


df = df.merge(df_cis, on='cis', how='left')
df = df.rename(columns={'name': 'denomination'})


# ## Retrouver présentation

# In[21]:


# Upload presentation table
df_pres = pd.read_sql_table('presentation', connection)


# In[22]:


df = df.merge(df_pres, on='cis', how='left')


# In[23]:


df.head(1)


# # MITM oui/non

# In[24]:


# Get dataframe from table
df_table = pd.read_sql_table('production', connection)
df_table = df_table.drop(['id', 'dci', 'type_amm', 'sites_production', 'sites_conditionnement_primaire',
                          'sites_conditionnement_secondaire', 'sites_importation', 'sites_controle',
                          'sites_echantillotheque', 'sites_certification', 'pgp', 'filename',
                          'substance_active_id', 'fabrication_id', 'substance_active',
                          'sites_fabrication_substance_active', 'denomination_specialite', 'titulaire_amm'],
                         axis=1)


# In[25]:


# Ne garder que la colonne MITMs avec les valeurs valant oui ou non
df_table = df_table.drop_duplicates()
df_table = df_table.where(pd.notnull(df_table), None)
df_table = df_table[df_table.mitm.isin(['oui', 'non'])]


# In[26]:


df_x = df.merge(df_table, on='cis', how='left')
df_x = df_x.where(pd.notnull(df_x), None)

# Merge substance_active and code_substance in one line
df_x.code_substance = df_x.apply(
    lambda x: ', '.join(map(str, df_x[df_x.cis == x.cis].code_substance.unique())), axis=1)
df_x.substance_active = df_x.apply(
    lambda x: ', '.join(df_x[df_x.cis == x.cis].substance_active.unique()), axis=1)

# Remove duplicates
df_x = df_x.drop_duplicates()


# In[27]:


# Reordering columns
df_x = df_x[['atc', 'cis', 'denomination', 'cip13', 'libelle', 'substance_active', 
             'code_substance', 'etat_commercialisation', 'mitm']]


# In[28]:


df_x.sort_values(by=['atc']).head()


# In[29]:


len(df), len(df_x)


# # INCA

# Ajouter les données de l'INCa

# In[30]:


df_cis_inca = pd.read_excel('../data/leem/IncaCSIS  Réponse.xlsx')
df_cis_inca.denomination = df_cis_inca.denomination.str.lower()


# In[31]:


df_cis_inca.head(1)


# In[32]:


denom_not_in_df = [d for d in df_cis_inca.denomination.unique() if d not in df_x.denomination.unique()]


# In[33]:


df_cis[df_cis.name.isin(denom_not_in_df)].head()


# In[34]:


df_inca = df_cis[df_cis.name.isin(denom_not_in_df)]
len(df_inca)


# In[35]:


df_inca = df_inca.merge(df_atc, on='cis', how='left')
df_inca = df_inca.rename(columns={'name': 'denomination'})
df_inca = df_inca.drop(['id', 'v3'], axis=1)


# In[36]:


df_inca = df_inca.merge(df_pres, on='cis', how='left')
df_inca = df_inca.merge(df_api[['cis', 'code_substance', 'substance_active', 'etat_commercialisation']],
                        on='cis', how='left')


# In[37]:


df_y = df_inca.merge(df_table, on='cis', how='left')
df_y = df_y.where(pd.notnull(df_y), None)
df_y = df_y.drop_duplicates()
df_y.code_substance = df_y.apply(
    lambda x: ', '.join(map(str, df_y[df_y.cis == x.cis].code_substance.unique())), axis=1)
df_y.substance_active = df_y.apply(
    lambda x: ', '.join(df_y[df_y.cis == x.cis].substance_active.unique()), axis=1)
df_y = df_y.drop_duplicates()


# In[38]:


len(df_inca), len(df_y)


# In[39]:


df_y.head()


# In[40]:


df_y = df_y[df_y.etat_commercialisation == 'Commercialisée']
df_y = df_y[['atc', 'cis', 'denomination', 'cip13', 'libelle', 'substance_active',
             'code_substance', 'etat_commercialisation', 'mitm']]


# In[41]:


df_y.sort_values(by=['atc']).head()


# In[42]:


df_end = pd.concat([df_x, df_y], axis=0)


# In[43]:


cis_x_list = df_x.cis.unique()
cis_y_list = df_y.cis.unique()


# In[44]:


df_end.sort_values(by=['atc']).to_csv(
    '../data/leem/reunion_leem_decret_stocks_atc_details.csv', sep=';', encoding='utf-8', index=False)


# In[ ]:




