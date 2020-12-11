#!/usr/bin/env python
# coding: utf-8

# # Décret stock
# Définir une métrique pour le choix des classes ATC à prioriser dans le décret stock

# In[1]:


import sys
import math
import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db
from create_database.upload_db import upload_compo_from_rsp, upload_cis_from_rsp


# # Base ruptures

# In[2]:


df = pd.read_excel('../data/decret_stock/décret stock.xlsx', header=0, sheet_name='Raw')


# In[3]:


df = df[['ID_Signal', 'Signalement', 'Date Signalement', 'Laboratoire', 'Spécialité', 'Rupture', 'ATC', 'DCI',
         'Date_Signal_Debut_RS', 'Durée_Ville', 'Durée_Hôpital', 'DatePrevi_Ville', 'DatePrevi_Hôpital',
         'Volumes_Ventes_Ville', 'Volumes_Ventes_Hopital']]
df = df[df['Date Signalement'] >= '2018-01-01']
df = df.rename(columns={'ID_Signal': 'id_signal', 'Signalement': 'signalement',
                        'Date Signalement': 'date_signalement', 'Laboratoire': 'laboratoire',
                        'Spécialité': 'specialite', 'Rupture': 'rupture', 'ATC': 'atc', 'DCI': 'dci',
                        'Date_Signal_Debut_RS': 'date_signal_debut_rs', 'Durée_Ville': 'duree_ville', 
                        'Durée_Hôpital': 'duree_hopital', 'DatePrevi_Ville': 'date_previ_ville',
                        'DatePrevi_Hôpital': 'date_previ_hopital', 'Volumes_Ventes_Ville': 'volumes_ventes_ville',
                        'Volumes_Ventes_Hopital': 'volumes_ventes_hopital'})
df['dci'] = df['dci'].str.lower()
df['laboratoire'] = df['laboratoire'].str.lower()
df['specialite'] = df['specialite'].str.lower()
df = df.where(pd.notnull(df), None)
df.volumes_ventes_ville = df.volumes_ventes_ville.where(pd.notnull(df.volumes_ventes_ville), 0)
df.volumes_ventes_hopital = df.volumes_ventes_hopital.where(pd.notnull(df.volumes_ventes_hopital), 0)
df.head(2)


# # ATC3

# In[4]:


df_atc = pd.read_excel('../data/decret_stock/décret stock.xlsx', sheet_name='ATC', names=['specialite', 'atc3'])
df_atc['specialite'] = df_atc['specialite'].str.lower()


# In[5]:


df_atc.head()


# In[6]:


# Le count ne garde pas les NaN
df_nb_spe = df_atc.groupby('atc3').count().reset_index()


# In[7]:


df_nb_spe.head()


# In[8]:


# Ajouter la classe ATC3 pour chaque spécialité
df = df.merge(df_atc.drop_duplicates(), on='specialite', how='left')
df['atc3'] = df.apply(lambda x: x.atc[:5] if pd.isnull(x.atc3) and x.atc else x.atc3, axis=1)


# In[9]:


for i in range(len(df)):
    x = df.iloc[i]
    if pd.isnull(x.atc3) and x.atc:
        a = x.atc[:5]
    else:
        a = x.atc3


# # Calculer durée rupture

# In[10]:


def compute_jours(x):
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    if math.isnan(jours_ville):
        jours_ville = 0
    if math.isnan(jours_hopital):
        jours_hopital = 0
    return jours_ville, jours_hopital


# In[11]:


df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)


# In[12]:


#sum(df[df.duree_ville.isin(
#    ['≤ 1 semaine', 'Entre 1 semaine et 1 mois', '1 à 3 mois', '≥ 3 mois'])].jours_rs) / len(
#    df[df.duree_ville.isin(['≤ 1 semaine', 'Entre 1 semaine et 1 mois', '1 à 3 mois', '≥ 3 mois'])])


# In[13]:


df[df.duree_ville == '≥ 3 mois'].head()


# In[14]:


len(df[df.duree_ville == 'Indéterminée'])


# In[15]:


duree_dict = {
    '≤ 1 semaine': 7,
    'Entre 1 semaine et 1 mois': 21,
    '1 à 3 mois': 70,
    '≥ 3 mois': 178,
    'Indéterminée': 74,
}


# In[16]:


def compute_duree_rs(x):
    duree_ville = 0
    duree_hopital = 0
    if not x.date_signal_debut_rs:
        return duree_dict['Indéterminée']
    else :
        if not x.jours_ville and not x.jours_hopital:
            if x.duree_ville and x.duree_hopital:
                return max(duree_dict[x.duree_ville], duree_dict[x.duree_hopital])
            elif x.duree_ville and not x.duree_hopital:
                return duree_dict[x.duree_ville]
            elif x.duree_hopital and not x.duree_ville:
                return duree_dict[x.duree_hopital]
            else:
                return duree_dict['Indéterminée']
        else:
            return x.jours_ville + x.jours_hopital


# In[17]:


df['nb_jours_rs'] = df.apply(lambda x: compute_duree_rs(x), axis=1)


# In[18]:


df[df.atc3 == 'A01AB']


# In[19]:


# x = df[(df.specialite.str.startswith('buccolam')) & (df.laboratoire == 'shire france')].iloc[0]


# # Regrouper par classe ATC3

# In[20]:


df_grouped = df.groupby('atc3').agg({'nb_jours_rs': 'sum'}).reset_index()
df_grouped = df_grouped.merge(df_nb_spe, on='atc3', how='left')
df_grouped = df_grouped.rename(columns={'specialite': 'nb_specialites'})


# In[21]:


df_grouped.head()


# # Calcul d'une métrique

# ## 1) Diviser le nombre de jours de rupture par le nombre de spécialités dans la classe ATC

# In[22]:


df_grouped['metrique_1'] = df_grouped.apply(lambda x: x.nb_jours_rs / x.nb_specialites, axis=1)


# In[24]:


df_grouped = df_grouped.sort_values(by=['metrique_1'], ascending=False)


# In[26]:


df_grouped.to_csv('../data/metrique_1.csv', index=False, sep=';')


# ## 2) Diviser le nombre de jours de rupture par le nombre de spécialités dans la classe ATC

# In[ ]:




