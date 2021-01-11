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
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'voie', 'voie_4_classes', 'atc',
         'date_signal_debut_rs', 'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]
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

# Ne garder que les cis qui sont une bijection cis <-> specialité
# df_cis = df_cis[df_cis.apply(lambda x: len(df_cis[df_cis.specialite == x.specialite].cis.unique()) == 1, axis=1)]

df_cis.head()


# # Ventes

# In[10]:


# Le count ne garde pas les NaN
df_ventes = pd.read_sql_table('ventes', connection)
df_ventes['atc_voie'] = df_ventes.apply(lambda x: (x.atc, x.voie_4_classes) if x.atc else None, axis=1)
df_ventes['ventes_total'] = df_ventes['unites_officine'] + df_ventes['unites_hopital']

df_ventes.head(1)


# # MITM oui/non

# In[11]:


df_mitm = pd.read_sql_table('production', connection)
df_mitm = df_mitm[['cis', 'mitm']]
df_mitm = df_mitm[df_mitm.mitm == 'oui']
df_mitm = df_mitm.dropna()
df_mitm = df_mitm.drop_duplicates()
df_mitm.head(1)


# In[12]:


mitm_dict = df_mitm.to_dict(orient='records')


# In[13]:


df_ventes = df_ventes.merge(df_mitm, on='cis', how='left')


# # Grouper par ...

# In[15]:


group = 'atc_voie'


# In[16]:


df_mitm_by_group = df_ventes.groupby([group, 'cis']).agg({'mitm': 'nunique'}).reset_index().groupby(group).sum().reset_index()


# In[17]:


# Compter nb spécialités par classe ATC
df_nb_spe = df_ventes.groupby(group).agg({'cis': 'nunique'}).reset_index()
df_nb_spe = df_nb_spe.rename(columns={'cis': 'nb_specialites_groupe'})
df_nb_spe = df_nb_spe.merge(df_mitm_by_group, on=group, how='left')
df_nb_spe['pourcentage_mitm'] = df_nb_spe.apply(lambda x: x.mitm / x.nb_specialites_groupe * 100 if x.mitm else 0, axis=1)

df_nb_spe.head()


# In[18]:


df_ventes[df_ventes.atc_voie == ('B01AX07', 'iv')]


# # Ventes par ATC, CIS, etc.

# In[19]:


# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)


# In[20]:


df_ventes_groupe = df_ventes.groupby(['annee', group]).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_groupe = df_ventes_groupe.to_dict(orient='records')
ventes_par_groupe = {2018: {ventes_dict[group]: ventes_dict['ventes_total']
                            for ventes_dict in ventes_par_groupe if ventes_dict['annee'] == 2018},
                     2019: {ventes_dict[group]: ventes_dict['ventes_total']
                            for ventes_dict in ventes_par_groupe if ventes_dict['annee'] == 2018},
                     2020: {ventes_dict[group]: ventes_dict['ventes_total'] 
                            for ventes_dict in ventes_par_groupe if ventes_dict['annee'] == 2019}}

df_ventes_cis = df_ventes.groupby(['annee', 'cis']).agg({'ventes_total': 'sum'}).reset_index()
ventes_par_cis = df_ventes_cis.to_dict(orient='records')
ventes_par_cis = {2018: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2019: {ventes_dict['cis']: ventes_dict['ventes_total']
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2018},
                  2020: {ventes_dict['cis']: ventes_dict['ventes_total'] 
                         for ventes_dict in ventes_par_cis if ventes_dict['annee'] == 2019}}


# In[21]:


df = df[['id_signal', 'date_signalement', 'annee', 'atc', 'atc_voie', 'laboratoire', 'specialite',
         'date_signal_debut_rs', 'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]

df.head(2)


# # Calculer durée rupture

# In[22]:


def compute_jours(x):
    """
    Nombre de jours entre la date de prévision de fin et la date de début de RS
    """
    jours_ville = (x.date_previ_ville - x.date_signal_debut_rs).days
    jours_hopital = (x.date_previ_hopital - x.date_signal_debut_rs).days
    return max(0, jours_ville), max(0, jours_hopital)

df['jours_ville'] = df.apply(lambda x: compute_jours(x)[0], axis=1)
df['jours_hopital'] = df.apply(lambda x: compute_jours(x)[1], axis=1)


# In[23]:


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


# In[24]:


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


# In[25]:


len(df)


# # Retirer les ruptures de moins de 6 jours

# In[26]:


print('{}% of RS reportings last less than 2 weeks'.format(round(len(df[df.nb_jours_rs <= 14]) / len(df) * 100, 2)))


# In[27]:


df = df[df.nb_jours_rs > 14]


# # Caper les ruptures supérieures à 4 mois à 4 mois

# In[28]:


df.nb_jours_rs = df.nb_jours_rs.apply(lambda x: 122 if x > 122 else x)


# # Calcul d'une métrique

# In[29]:


len(df)


# ## 1) Pondérer par les ventes

# In[30]:


# Trouver, par classe ATC, la spécialité qui a les plus grands chiffres de vente sur 2018-2019
df_spe_max_ventes = df_ventes.groupby(
    [group, 'denomination_specialite']).agg({'ventes_total': 'sum'}).reset_index()

def get_spe_max_ventes(df_spe_max_ventes):
    """
    Pour chaque groupe, avoir la spécialité la plus vendue, sur toutes les années
    """
    records = df_spe_max_ventes.to_dict(orient='records')
    rec_dict = defaultdict(dict)
    for g in df_spe_max_ventes[group].unique():
        rec_dict[g] = {d['denomination_specialite']: d['ventes_total'] for d in records if d[group] == g}
    return {k: max(v, key=v.get) for k, v in rec_dict.items()}

max_ventes_dict = get_spe_max_ventes(df_spe_max_ventes)


# In[31]:


# Grouper par année et spécialité
df_ventes_spe = df.groupby(['annee', group, 'specialite']).agg({'nb_jours_rs': 'sum'}).reset_index()
df_ventes_spe = df_ventes_spe.merge(df_cis[['cis', 'specialite']].dropna(), on='specialite', how='left')

df_ventes_spe['ventes_cis'] = df_ventes_spe.apply(lambda x: ventes_par_cis[x.annee].get(x.cis), axis=1)

# Savoir pour combien de CIS on a les chiffres de vente
df_ventes_spe['ventes_exist'] = df_ventes_spe.ventes_cis.apply(lambda x: 0 if pd.isnull(x) else 1)

df_ventes_spe.head()


# In[32]:


# Grouper par année et par classe ATC
df_ventes_annee_groupe = df_ventes_spe.groupby(['annee', group]).agg(
    {'ventes_exist': 'sum', 'ventes_cis': 'sum', 'nb_jours_rs': 'sum'}).reset_index()
df_ventes_annee_groupe['ventes_groupe'] = df_ventes_annee_groupe.apply(
    lambda x: ventes_par_groupe[x.annee].get(x[group]), axis=1)

# Rajouter le nombre de spécialités à la dataframe
df_ventes_annee_groupe = df_ventes_annee_groupe.merge(df_nb_spe, on=group, how='left')
df_ventes_annee_groupe = df_ventes_annee_groupe.rename(columns={'specialite': 'nb_specialites_groupe'})

# Attribuer des ventes aux CIS = NaN
df_ventes_annee_groupe['ventes_cis_inconnus'] = df_ventes_annee_groupe.apply(
    lambda x: (x.ventes_groupe - x.ventes_cis) / (x.nb_specialites_groupe - x.ventes_exist)
    if (x.nb_specialites_groupe - x.ventes_exist) else 0, axis=1)

df_ventes_annee_groupe.head()


# In[33]:


# Ventes des cis de la classe ATC qui n'apparaissent pas dans les ruptures
records = df_ventes_annee_groupe.to_dict(orient='records')

ventes_cis_inconnus_dict = {(r['annee'], r[group]): r['ventes_cis_inconnus'] for r in records}

nb_spe_par_groupe = {r[group]: r['nb_specialites_groupe'] for r in records}


# In[34]:


# Ajouter à la colonne ventes_cis les ventes estimées sur les cis inconnus
df_ventes_spe.ventes_cis = df_ventes_spe.apply(
    lambda x: ventes_cis_inconnus_dict.get((x.annee, x[group]))
    if pd.isnull(x.ventes_cis) else x.ventes_cis, axis=1)

df_ventes_spe['ventes_groupe'] = df_ventes_spe.apply(lambda x: ventes_par_groupe[x.annee].get(x[group]), axis=1)

df_ventes_spe.head(2)


# In[35]:


def compute_score(g, df):
    """
    Calcul d'un score pondéré par les ventes
    """
    return sum([
        x.nb_jours_rs * x.ventes_cis / x.ventes_groupe 
        for _, x in df[df[group] == g].iterrows()
    ])

df_score = df_ventes_annee_groupe.groupby(group).agg(
    {'ventes_groupe': 'sum', 'ventes_cis': 'sum', 'ventes_cis_inconnus': 'sum', 'nb_jours_rs': 'sum'}).reset_index()

df_score = df_score.merge(df_nb_spe, on=group, how='left')
df_score['score'] = df_score[group].apply(lambda x: compute_score(x, df_ventes_spe))

df_score['specialite_plus_vendue'] = df_score[group].apply(
    lambda x: max_ventes_dict[x] if x in max_ventes_dict else None)

df_score = df_score[
    [group, 'ventes_groupe', 'specialite_plus_vendue', 'nb_jours_rs', 'nb_specialites_groupe', 'mitm', 'pourcentage_mitm', 'score']
].sort_values(by=['score'], ascending=False)

df_score.head(10)


# In[36]:


# df_score[df_score.atc == 'A06AH01']


# In[37]:


# len(df[df.atc.apply(lambda x: len(x) != 7 if x else True)])


# # Sauvegarder dans csv

# In[47]:


# df_score.to_csv('../data/decret_stock/classes_atc_score_pondéré_niveau_atc5_voie_mitm.csv', index=False, sep=';')


# # Nombre de ruptures ayant l'ATC complet

# In[39]:


# len(df[df.atc.apply(lambda x: len(x) == 7 if x and isinstance(x, str) else False)]) / len(df) * 100


# In[40]:


df_ventes[df_ventes.atc_voie == ('N05CD08', 'orale')]


# In[41]:


df_ventes[df_ventes.denomination_specialite == 'fibrogammin 62,5 ul/ml, poudre et solvant pour solution injectable/perfusion']


# In[42]:


df[df.specialite == 'fibrogammin 62,5 ul/ml, poudre et solvant pour solution injectable/perfusion']


# In[43]:


df[df.atc_voie == ('B02BD07', 'iv')].iloc[0].specialite


# In[44]:


df_ventes_spe[df_ventes_spe.atc_voie == ('B02BD07', 'iv')]


# In[45]:


df_ventes[df_ventes.cis == '66885235']


# In[46]:


df_score[df_score.atc_voie == ('C03DA02', 'iv')]


# In[ ]:




