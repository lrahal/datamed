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
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'atc', 'date_signal_debut_rs',
         'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]
df = df[df.date_signalement >= '2018-01-01']
df.atc = df.atc.str.upper()
df.specialite = df.apply(
    lambda x: x.specialite.replace(' /', '/').replace('/ ', '/').replace('intraoculaire', 'intra-oculaire'),
    axis=1)

df.head(2)


# In[4]:


len(df)


# # Retrouver le code CIS

# In[5]:


df_cis_1 = pd.read_sql_table('specialite', connection)
df_cis_1 = df_cis_1[df_cis_1.type_amm != "Autorisation d'importation parallèle"]
df_cis_1 = df_cis_1.rename(columns={'name': 'specialite'})


# In[6]:


df_cis_2 = pd.read_excel('../data/decret_stock/correspondance_cis_nom.xlsx', names=['specialite', 'cis'])
df_cis_2 = df_cis_2.drop(df_cis_2.index[0])
df_cis_2.specialite = df_cis_2.specialite.str.lower()
df_cis_2.cis = df_cis_2.cis.map(str)
df_cis_2 = df_cis_2.drop_duplicates()
df_cis_2['type_amm'] = None
df_cis_2['etat_commercialisation'] = None
df_cis_2 = df_cis_2[~df_cis_2.cis.isin(df_cis_1.cis.unique())]


# In[7]:


df_cis = pd.concat([df_cis_1, df_cis_2])
df_cis = df_cis[~df_cis.specialite.isna()]

# Ne garder que les cis qui sont une bijection cis <-> specialité
# df_cis = df_cis[df_cis.apply(lambda x: len(df_cis[df_cis.specialite == x.specialite].cis.unique()) == 1, axis=1)]

df_cis.head()


# In[8]:


# df = df.merge(df_cis[['cis', 'specialite']].dropna(), on='specialite', how='left')


# In[9]:


# len(df[df.cis.notna()]) / len(df) * 100


# # Ventes

# In[10]:


# Le count ne garde pas les NaN
df_ventes = pd.read_sql_table('ventes', connection)
df_ventes['ventes_total'] = df_ventes['unites_officine'] + df_ventes['unites_hopital']

df_ventes.head(1)


# In[11]:


# Compter nb spécialités par classe ATC
df_nb_spe = df_ventes.groupby('atc').agg({'cis': 'nunique'}).reset_index()
df_nb_spe = df_nb_spe.rename(columns={'cis': 'specialite'})

df_nb_spe.head()


# # Ventes par ATC, CIS, etc.

# In[12]:


# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)


# In[13]:


df_ventes_atc = df_ventes.groupby(['annee', 'atc']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_atc = df_ventes_atc.to_dict(orient='records')
ventes_par_atc = {2018: {ventes_dict['atc']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2018},
                  2019: {ventes_dict['atc']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2018},
                  2020: {ventes_dict['atc']: ventes_dict['ventes_total'] 
                         for ventes_dict in ventes_par_atc if ventes_dict['annee'] == 2019}}

df_ventes_cis = df_ventes.groupby(['annee', 'cis']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_cis = df_ventes_cis.to_dict(orient='records')
ventes_par_cis = {2018: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2019: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2020: {ventes_dict['cis']: ventes_dict['ventes_total'] 
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2019}}


# In[14]:


df = df[['id_signal', 'date_signalement', 'annee', 'atc', 'laboratoire', 'specialite', 'date_signal_debut_rs',
         'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]

df.head(2)


# # Calculer durée rupture

# In[15]:


def compute_jours(x):
    """
    Nombre de jours entre la date de prévision de fin et la date de début de RS
    """
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    return max(0, jours_ville), max(0, jours_hopital)

df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)


# In[16]:


def get_duree(x):
    """
    Pour chaque signalement, calculer la duree totale de la rupture
    """
    return max(x.jours_ville, x.jours_hopital)
    
# Durée moyenne des ruptures pour duree_ville ≥ 3 mois
mean_3_months = df[df.duree_ville == '≥ 3 mois'].apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

# Durée moyenne des ruptures sur tout le dataset
mean_all = df.apply(lambda x: get_duree(x), axis=1).replace(0, np.NaN).mean()

print('Mean 3 months: {} days - Mean all: {} days'.format(round(mean_3_months, 2), round(mean_all, 2)))


# In[17]:


duree_dict = {
    '≤ 1 semaine': 7,
    'Entre 1 semaine et 1 mois': 21,
    '1 à 3 mois': 70,
    '≥ 3 mois': mean_3_months,
    'Indéterminée': mean_all,
}

def compute_duree_rs(x):
    if x.jours_ville or x.jours_hopital:
        return max(x.jours_ville, x.jours_hopital)
    elif x.duree_ville or x.duree_hopital:
        return max(duree_dict.get(x.duree_ville, 0), duree_dict.get(x.duree_hopital, 0))
    else:
        return duree_dict['Indéterminée']
        
df['nb_jours_rs'] = df.apply(lambda x: compute_duree_rs(x), axis=1)


# In[18]:


len(df)


# # Retirer les ruptures de moins de 6 jours

# In[19]:


print('{}% of RS reportings last less than 6 days'.format(round(len(df[df.nb_jours_rs <= 14]) / len(df) * 100, 2)))


# In[20]:


df = df[df.nb_jours_rs > 14]


# # Caper les ruptures supérieures à 4 mois à 4 mois

# In[21]:


df.nb_jours_rs = df.nb_jours_rs.apply(lambda x: 122 if x > 122 else x)


# # Récupérer les noms des classes ATC

# In[22]:


# df_names = pd.read_excel('../data/decret_stock/décret stock.xlsx', sheet_name='BILAN', header=0)
# df_names = df_names[['ATC', 'Nom atc', 'MITM?']]
# df_names = df_names.rename(columns={'ATC': 'atc', 'Nom atc': 'nom_atc', 'MITM?': 'mitm'})
# df_names.head()


# # Calcul d'une métrique

# In[23]:


len(df)


# ## 1) Pondérer par les ventes

# In[24]:


# Trouver, par classe ATC, la spécialité qui a les plus grands chiffres de vente sur 2018-2019
df_spe_max_ventes = df_ventes.groupby(['atc', 'denomination_specialite']).agg({'ventes_total': 'sum'}).reset_index()

records = df_spe_max_ventes.to_dict(orient='records')
rec_dict = defaultdict(dict)
for atc in df_spe_max_ventes.atc.unique():
    rec_dict[atc] = {d['denomination_specialite']: d['ventes_total'] for d in records if d['atc'] == atc}
    
max_ventes_dict = {k: max(v, key=v.get) for k, v in rec_dict.items()}


# In[25]:


# Grouper par année et spécialité
df_ventes_spe = df.groupby(['annee', 'atc', 'specialite']).agg({'nb_jours_rs': 'sum'}).reset_index()
df_ventes_spe = df_ventes_spe.merge(df_cis[['cis', 'specialite']].dropna(), on='specialite', how='left')

df_ventes_spe['ventes_cis'] = df_ventes_spe.apply(lambda x: ventes_par_cis[x.annee].get(x.cis), axis=1)

# Savoir pour combien de CIS on a les chiffres de vente
df_ventes_spe['ventes_exist'] = df_ventes_spe.ventes_cis.apply(lambda x: 0 if pd.isnull(x) else 1)

df_ventes_spe.head()


# In[26]:


# Grouper par année et par classe ATC
df_ventes_annee_atc = df_ventes_spe.groupby(['annee', 'atc']).agg(
    {'ventes_exist': 'sum', 'ventes_cis': 'sum', 'nb_jours_rs': 'sum'}).reset_index()
df_ventes_annee_atc['ventes_atc'] = df_ventes_annee_atc.apply(lambda x: ventes_par_atc[x.annee].get(x.atc), axis=1)

# Rajouter le nombre de spécialités à la dataframe
df_ventes_annee_atc = df_ventes_annee_atc.merge(df_nb_spe, on='atc', how='left')
df_ventes_annee_atc = df_ventes_annee_atc.rename(columns={'specialite': 'nb_specialites_atc'})

# Attribuer des ventes aux CIS = NaN
df_ventes_annee_atc['ventes_cis_inconnus'] = df_ventes_annee_atc.apply(
    lambda x: (x.ventes_atc - x.ventes_cis) / (x.nb_specialites_atc - x.ventes_exist)
    if (x.nb_specialites_atc - x.ventes_exist) else 0, axis=1)

df_ventes_annee_atc.head()


# In[27]:


#df['cis'] = df.specialite.apply(
#    lambda x: df_ventes_spe[df_ventes_spe.specialite == x].iloc[0].cis
#    if x in df_ventes_spe.specialite.unique() else None)

#df['ventes_cis'] = df.apply(lambda x: ventes_par_cis[x.annee].get(x.cis), axis=1)

#df.ventes_cis = df.apply(
#    lambda x: df_ventes_annee_atc[(df_ventes_annee_atc.annee == x.annee) 
#                                  & (df_ventes_annee_atc.atc == x.atc)].iloc[0].ventes_cis_inconnus
#    if pd.isnull(x.ventes_cis) and x.atc in df_ventes_annee_atc.atc.unique() else x.ventes_cis, axis=1)


#df['ventes_atc'] = df.apply(lambda x: ventes_par_atc[x.annee].get(x.atc), axis=1)

#df['nb_specialites_atc'] = df.atc.apply(
#    lambda x: df_ventes_annee_atc[df_ventes_annee_atc.atc == x].iloc[0].nb_specialites_atc
#    if x in df_ventes_annee_atc.atc.unique() else None)

#df.head(2)


# In[28]:


# Ventes des cis de la classe ATC qui n'apparaissent pas dans les ruptures
records = df_ventes_annee_atc.to_dict(orient='records')

ventes_cis_inconnus_dict = {2018: {r['atc']: r['ventes_cis_inconnus'] for r in records if r['annee'] == 2018},
                            2019: {r['atc']: r['ventes_cis_inconnus'] for r in records if r['annee'] == 2019},
                            2020: {r['atc']: r['ventes_cis_inconnus'] for r in records if r['annee'] == 2020}}

nb_spe_par_atc = {r['atc']: r['nb_specialites_atc'] for r in records}


# In[29]:


# Ajouter à la colonne ventes_cis les ventes estimées sur les cis inconnus
df_ventes_spe.ventes_cis = df_ventes_spe.apply(
    lambda x: ventes_cis_inconnus_dict[x.annee].get(x.atc) 
    if pd.isnull(x.ventes_cis) else x.ventes_cis, axis=1)

df_ventes_spe['ventes_atc'] = df_ventes_spe.apply(lambda x: ventes_par_atc[x.annee].get(x.atc), axis=1)
df_ventes_spe['nb_specialites_atc'] = df_ventes_spe.atc.apply(lambda x: nb_spe_par_atc.get(x))

df_ventes_spe.head(2)


# In[30]:


def compute_score(atc, df):
    """
    Calcul d'un score pondéré par les ventes
    """
    return sum([
        x.nb_jours_rs * x.ventes_cis / x.ventes_atc 
        for _, x in df[df.atc == atc].iterrows()
    ])

df_score = df_ventes_annee_atc.groupby('atc').agg(
    {'ventes_atc': 'sum', 'ventes_cis': 'sum', 'nb_specialites_atc': 'first',
     'ventes_cis_inconnus': 'sum', 'nb_jours_rs': 'sum'}).reset_index()

df_score['score'] = df_score.atc.apply(lambda x: compute_score(x, df_ventes_spe))

df_score['specialite_plus_vendue'] = df_score.atc.apply(
    lambda x: max_ventes_dict[x] if x in max_ventes_dict else None)

df_score = df_score[
    ['atc', 'ventes_atc', 'specialite_plus_vendue', 'nb_jours_rs', 'nb_specialites_atc', 'score']
].sort_values(by=['score'], ascending=False)

df_score.head(10)


# In[31]:


len(df[df.atc.apply(lambda x: len(x) != 7 if x else True)])


# # Sauvegarder dans csv

# In[32]:


# df_score.to_csv('../data/decret_stock/classes_atc_score_pondéré_niveau_atc_5.csv', index=False, sep=';')


# # Nombre de ruptures ayant l'ATC complet

# In[33]:


len(df[df.atc.apply(lambda x: len(x) == 7 if x and isinstance(x, str) else False)]) / len(df) * 100


# In[ ]:




