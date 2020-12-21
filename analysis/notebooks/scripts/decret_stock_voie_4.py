#!/usr/bin/env python
# coding: utf-8

# # Décret stock
# Définir une métrique pour le choix des classes ATC à prioriser dans le décret stock

# In[1]:


import math
import sys

import numpy as np
import pandas as pd
from collections import defaultdict

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# # Table ruptures

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('ruptures', connection)
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'voie', 'voie_4_classes', 'atc', 'date_signal_debut_rs',
         'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]
df = df[df.date_signalement >= '2018-01-01']
df.atc = df.atc.str.upper()
df.specialite = df.apply(
    lambda x: x.specialite.replace(' /', '/').replace('/ ', '/').replace('intraoculaire', 'intra-oculaire'),
    axis=1)

df.head(2)


# In[4]:


len(df)


# # Avoir toutes les combinaisons (atc, voie_4_classes) possibles

# In[5]:


from itertools import product

# tous les tuples possibles (atc, voie_4_classes)
atc_voie_tuples = list(set(product(df.atc, df.voie_4_classes)))


# In[6]:


df['atc_voie'] = df.apply(lambda x: (x.atc, x.voie_4_classes) if x.atc else None, axis=1)


# # Retrouver le code CIS

# In[7]:


df_cis_1 = pd.read_sql_table('specialite', connection)
df_cis_1 = df_cis_1[df_cis_1.type_amm != "Autorisation d'importation parallèle"]
df_cis_1 = df_cis_1.rename(columns={'name': 'specialite'})


# In[8]:


df_cis_2 = pd.read_excel('../data/decret_stock/correspondance_cis_nom.xlsx', names=['specialite', 'cis'])
df_cis_2 = df_cis_2.drop(df_cis_2.index[0])
df_cis_2.specialite = df_cis_2.specialite.str.lower()
df_cis_2.cis = df_cis_2.cis.map(str)
df_cis_2 = df_cis_2.drop_duplicates()
df_cis_2['type_amm'] = None
df_cis_2['etat_commercialisation'] = None
df_cis_2 = df_cis_2[~df_cis_2.cis.isin(df_cis_1.cis.unique())]


# In[9]:


df_cis = pd.concat([df_cis_1, df_cis_2])
df_cis = df_cis[~df_cis.specialite.isna()]


# In[10]:


df_cis.head()


# In[11]:


df = df.merge(df_cis[['cis', 'specialite']].dropna(), on='specialite', how='left')


# In[12]:


len(df[df.cis.notna()]) / len(df) * 100


# In[13]:


len(df[df.cis.isna()])


# # Ventes

# In[14]:


# Le count ne garde pas les NaN
df_v = pd.read_sql_table('ventes', connection)
df_v['ventes_total'] = df_v['unites_officine'] + df_v['unites_hopital']

df_v.head(1)


# In[15]:


# Compter nb spécialités par classe ATC
df_nb_spe = df_v.groupby('atc').agg({'cis': 'nunique'}).reset_index()
df_nb_spe = df_nb_spe.rename(columns={'cis': 'specialite'})

df_nb_spe.head()


# # Ventes par ATC, CIS, etc.

# In[16]:


# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)


# In[17]:


df_v2 = df_v.groupby(['annee', 'atc']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_atc = df_v2.to_dict(orient='records')
ventes_par_atc = {2018: {ventes_dict['atc']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2018},
                  2019: {ventes_dict['atc']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2018},
                  2020: {ventes_dict['atc']: ventes_dict['ventes_total'] 
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2019}}

df_v3 = df_v.groupby(['annee', 'cis']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_cis = df_v3.to_dict(orient='records')
ventes_par_cis = {2018: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2019: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2020: {ventes_dict['cis']: ventes_dict['ventes_total'] 
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2019}}

df_v4 = df_v.groupby(['annee', 'atc_voie']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_atc_voie = df_v4.to_dict(orient='records')
ventes_par_atc_voie = {2018: {ventes_dict['atc_voie']: ventes_dict['ventes_total']
                              for ventes_dict in ventes_par_atc_voie if ventes_dict['annee'] == 2018},
                       2019: {ventes_dict['atc_voie']: ventes_dict['ventes_total']
                              for ventes_dict in ventes_par_atc_voie if ventes_dict['annee'] == 2018},
                       2020: {ventes_dict['atc_voie']: ventes_dict['ventes_total'] 
                              for ventes_dict in ventes_par_atc_voie if ventes_dict['annee'] == 2019}}


# In[ ]:


for k, v in ventes_par_atc_voie.items():
    break


# In[ ]:


df['ventes_cis'] = df.apply(
    lambda x: ventes_par_cis[x.annee][x.cis] if x.cis in ventes_par_cis[x.annee] else None, axis=1)

df['ventes_atc'] = df.apply(
    lambda x: ventes_par_atc[x.annee][x.atc] if x.atc in ventes_par_atc[x.annee] else None, axis=1)


# In[ ]:


df = df[['id_signal', 'date_signalement', 'annee', 'atc', 'atc_voie', 'cis', 'laboratoire',
         'specialite', 'date_signal_debut_rs', 'duree_ville', 'duree_hopital',
         'date_previ_ville', 'date_previ_hopital', 'ventes_cis', 'ventes_atc']]

df.head(2)


# # Calculer durée rupture

# In[ ]:


def compute_jours(x):
    """
    Nombre de jours entre la date de prévision de fin et la date de début de RS
    """
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    if math.isnan(jours_ville):
        jours_ville = 0
    if math.isnan(jours_hopital):
        jours_hopital = 0
    return max(0, jours_ville), max(0, jours_hopital)

df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)

df.head(1)


# In[ ]:


def get_duree(x):
    """
    Pour chaque signalement, calculer la duree totale de la rupture
    """
    if x.jours_ville and x.jours_hopital:
        return max(x.jours_ville, x.jours_hopital)
    elif x.jours_ville and not x.jours_hopital:
        return x.jours_ville
    elif not x.jours_ville and x.jours_hopital:
        return x.jours_hopital
    else:
        return np.NaN
    
# Durée moyenne des ruptures pour duree_ville ≥ 3 mois
mean_3_months = df[df.duree_ville == '≥ 3 mois'].apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

# Durée moyenne des ruptures sur tout le dataset
mean_all = df.apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

print('Mean 3 months: {} days - Mean all: {} days'.format(round(mean_3_months, 2), round(mean_all, 2)))


# In[ ]:


duree_dict = {
    '≤ 1 semaine': 7,
    'Entre 1 semaine et 1 mois': 21,
    '1 à 3 mois': 70,
    '≥ 3 mois': mean_3_months,
    'Indéterminée': mean_all,
}


# In[ ]:


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
            return max(x.jours_ville, x.jours_hopital)
        
df['nb_jours_rs'] = df.apply(lambda x: compute_duree_rs(x), axis=1)


# In[ ]:


len(df)


# # Retirer les ruptures de moins de 6 jours

# In[ ]:


print('{}% of RS reportings last less than 2 weeks'.format(round(len(df[df.nb_jours_rs <= 14]) / len(df) * 100, 2)))


# In[ ]:


df = df[df.nb_jours_rs > 14]


# # Caper les ruptures supérieures à 4 mois à 4 mois

# In[ ]:


df.nb_jours_rs = df.nb_jours_rs.apply(lambda x: 122 if x > 122 else x)


# # Regrouper par classe atc

# In[ ]:


df_grouped = df.groupby('atc').agg({'nb_jours_rs': 'sum', 'ventes_atc': 'mean'}).reset_index()
df_grouped = df_grouped.merge(df_nb_spe, on='atc', how='left')
df_grouped = df_grouped.rename(columns={'specialite': 'nb_specialites'})

df_grouped.head(3)


# # Calcul d'une métrique

# ## 1) Pondérer par les ventes

# In[ ]:


# Grouper par année et spécialité
df2 = df.groupby(['annee', 'specialite']).agg(
    {'atc': 'first', 'atc_voie': 'first', 'ventes_atc': 'first', 'ventes_cis': 'first', 'nb_jours_rs': 'sum'}
).reset_index()

# Savoir pour combien de CIS on a les chiffres de vente
df2['ventes_exist'] = df2.ventes_cis.apply(lambda x: 0 if pd.isnull(x) else 1)

df2.head()


# In[ ]:


# Trouver, par classe ATC, la spécialité qui a les plus grands chiffres de vente sur 2018-2019
df3 = df_v.groupby(['atc', 'denomination_specialite']).agg({'ventes_total': 'sum'}).reset_index()

records = df3.to_dict(orient='records')
rec_dict = defaultdict(dict)
for atc in df3.atc.unique():
    rec_dict[atc] = {d['denomination_specialite']: d['ventes_total'] for d in records if d['atc'] == atc}
    
max_ventes_dict = {k: max(v, key=v.get) for k, v in rec_dict.items()}


# In[ ]:


# Grouper par année et par classe ATC
df_grouped = df2.groupby(['annee', 'atc']).agg(
    {'ventes_exist': 'sum', 'ventes_atc': 'mean', 'ventes_cis': 'sum', 'nb_jours_rs': 'sum'}).reset_index()
df_grouped = df_grouped.merge(df_nb_spe, on='atc', how='left')

df_grouped = df_grouped.rename(columns={'specialite': 'nb_specialites_atc'})

# Attribuer des ventes au CIS = NaN
df_grouped['ventes_cis_inconnus'] = df_grouped.apply(
    lambda x: (x.ventes_atc - x.ventes_cis) / (x.nb_specialites_atc - x.ventes_exist)
    if (x.nb_specialites_atc - x.ventes_exist) else 0, axis=1)

df_grouped.head()


# In[ ]:


df.ventes_cis = df.apply(
    lambda x: df_grouped[df_grouped.atc == x.atc].iloc[0].ventes_cis_inconnus
    if pd.isnull(x.ventes_cis) and x.atc in df_grouped.atc.unique() else x.ventes_cis, axis=1)

df['nb_specialites_atc'] = df.apply(
    lambda x: df_grouped[df_grouped.atc == x.atc].iloc[0].nb_specialites_atc
    if x.atc in df_grouped.atc.unique() else None, axis=1)


# In[ ]:


def compute_score(atc, df):
    """
    Calcul d'un score pondéré par les ventes
    """
    return sum([
        x.nb_jours_rs * x.ventes_cis / x.ventes_atc 
        for _, x in df[df.atc == atc].iterrows()
    ])

df_score = df_grouped.copy()
df_score['score'] = df_score.atc.apply(lambda x: compute_score(x, df))

df_score = df_score.groupby('atc').agg(
    {'ventes_exist': 'first', 'ventes_atc': 'sum', 'ventes_cis': 'sum', 'nb_specialites_atc': 'first',
     'ventes_cis_inconnus': 'sum', 'nb_jours_rs': 'sum', 'score': 'first'}).reset_index().sort_values(
    by=['score'], ascending=False)

#df_score = df_score.merge(df_names, on='atc', how='left')

df_score['specialite_plus_vendue'] = df_score.atc.apply(
    lambda x: max_ventes_dict[x] if x in max_ventes_dict else None)

df_score = df_score[['atc', 'ventes_atc', 'specialite_plus_vendue', 'nb_jours_rs', 'nb_specialites_atc', 'score']]

df_score.head(10)


# In[ ]:


len(df[df.atc.apply(lambda x: len(x) != 7 if x else True)])


# # Sauvegarder dans csv

# In[ ]:


# df_score.to_csv('../data/decret_stock/classes_atc_score_pondéré_niveau_atc_5.csv', index=False, sep=';')


# # Nombre de ruptures ayant l'ATC complet

# In[ ]:


len(df[df.atc.apply(lambda x: len(x) == 7 if x and isinstance(x, str) else False)]) / len(df) * 100


# In[ ]:




