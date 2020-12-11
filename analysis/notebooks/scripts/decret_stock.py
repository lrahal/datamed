#!/usr/bin/env python
# coding: utf-8

# # Décret stock
# Définir une métrique pour le choix des classes ATC à prioriser dans le décret stock

# In[1]:


import math
import sys

import numpy as np
import pandas as pd

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

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
df['atc3'] = df['atc3'].str.upper()


# # Calculer durée rupture

# In[9]:


def compute_jours(x):
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    if math.isnan(jours_ville):
        jours_ville = 0
    if math.isnan(jours_hopital):
        jours_hopital = 0
    return max(0, jours_ville), max(0, jours_hopital)


# In[10]:


df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)


# In[11]:


df.head(1)


# In[12]:


def get_duree(x):
    """
    Pour chaque signalement, calculer la duree totale de la rupture
    """
    if x.jours_ville and x.jours_hopital:
        return x.jours_ville + x.jours_hopital
    elif x.jours_ville and not x.jours_hopital:
        return x.jours_ville
    elif not x.jours_ville and x.jours_hopital:
        return x.jours_hopital
    else:
        return np.NaN


# In[13]:


# Durée moyenne des ruptures pour duree_ville ≥ 3 mois
mean_3_months = df[df.duree_ville == '≥ 3 mois'].apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()
mean_3_months


# In[14]:


# Durée moyenne des ruptures sur tout le dataset
mean_all = df.apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()
mean_all


# In[15]:


duree_dict = {
    '≤ 1 semaine': 7,
    'Entre 1 semaine et 1 mois': 21,
    '1 à 3 mois': 70,
    '≥ 3 mois': mean_3_months,
    'Indéterminée': mean_all,
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


# x = df[(df.specialite.str.startswith('buccolam')) & (df.laboratoire == 'shire france')].iloc[0]


# # Retirer les ruptures de moins de 6 jours

# In[19]:


len(df)


# In[20]:


df6 = df[df.nb_jours_rs <= 6]


# In[21]:


len(df6)


# # Caper les ruptures supérieures à 4 mois à 4 mois

# In[22]:


df.nb_jours_rs = df.nb_jours_rs.apply(lambda x: 122 if x > 122 else x)


# # Regrouper par classe ATC3

# In[23]:


df_grouped = df.groupby('atc3').agg({'nb_jours_rs': 'sum'}).reset_index()
df_grouped = df_grouped.merge(df_nb_spe, on='atc3', how='left')
df_grouped = df_grouped.rename(columns={'specialite': 'nb_specialites'})


# In[24]:


df_grouped.head(3)


# # Calcul d'une métrique

# ## 1) Diviser le nombre de jours de rupture par le nombre de spécialités dans la classe ATC

# In[25]:


df_grouped['metrique_1'] = df_grouped.apply(lambda x: x.nb_jours_rs / x.nb_specialites, axis=1)


# In[26]:


df_grouped = df_grouped.sort_values(by=['metrique_1'], ascending=False)


# In[27]:


# atc3_list = df_grouped[df_grouped.nb_specialites.isna()].atc3.unique()


# In[28]:


# df[df.atc3.isin(atc3_list)]    #.to_csv('../data/ruptures_atc3_nan.csv', index=False, sep=';')


# In[34]:


# df_grouped[df_grouped.nb_specialites.isna()]     #.to_csv('../data/atc3_nan.csv', index=False, sep=';')


# In[30]:


len(df_grouped)


# ## 2) Diviser le nombre de jours de rupture par le nombre de spécialités dans la classe ATC

# In[31]:


df_grouped['metrique_2'] = df_grouped.apply(lambda x: math.log(x.nb_jours_rs) / (x.nb_specialites) ** 2, axis=1)


# In[32]:


df_grouped = df_grouped.sort_values(by=['metrique_2'], ascending=False)


# # Sauvegarder dans csv

# In[33]:


df_grouped.to_csv('../data/metriques.csv', index=False, sep=';')


# In[ ]:




