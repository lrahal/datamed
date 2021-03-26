#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import json
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# In[2]:


# Importer le dict des noms des classes ATC

with open('/Users/ansm/Documents/GitHub/datamed/datamed_dash/data/atc2_names.json') as f:
    atc2_names = json.load(f)


# In[3]:


engine = connect_db()  # establish connection
connection = engine.connect()


# # Ruptures

# In[4]:


# Connexion à la table ruptures
df = pd.read_sql_table('ruptures', connection)
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'etat_dossier', 'circuit_touche_ville',
         'circuit_touche_hopital', 'voie', 'voie_4_classes', 'atc', 'date_signal_debut_rs', 'duree_ville',
         'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]

df = df[df.date_signalement.notna()]

df.atc = df.atc.str.upper()
df.specialite = df.apply(
    lambda x: x.specialite.replace(' /', '/').replace('/ ', '/').replace('intraoculaire', 'intra-oculaire'),
    axis=1)

df['atc_2'] = df.atc.apply(lambda x: x[:3] if x else None)

# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)
df['mois'] = df.date_signalement.apply(lambda x: x.month)

df.head(2)


# In[5]:


ruptures_by_annee = defaultdict()
for a in range(2014, 2021):
    df_annee = df[df.annee == a]
    df_ranked_atc = df_annee.groupby('atc_2').count().reset_index().sort_values(by=['id_signal'], ascending=False)
    df_ranked_atc = df_ranked_atc.rename(columns={'id_signal': 'nb_ruptures'})
    
    ranked_atc_list = df_ranked_atc[['atc_2', 'nb_ruptures']].to_dict(orient='records')
    ruptures_by_annee[a] = {atc2_names.get(d['atc_2'], d['atc_2']): [d['nb_ruptures']] for d in ranked_atc_list}

# Générer le json des ruptures par classe ATC et par année
#with open("../data/ruptures_by_atc_by_annee.json", "w") as outfile: 
#    json.dump(ruptures_by_annee, outfile)


# In[6]:


with open('../data/ruptures_by_atc_by_annee.json') as f:
    RUPTURES_ATC_DICT = json.load(f)


# In[7]:


df_sig_atc = pd.DataFrame.from_dict(
    RUPTURES_ATC_DICT["2020"], orient="index").reset_index().rename(
    columns={"index": "nom_atc", 0: "nb_signal"}
)

df_sig_atc.head(3)


# In[23]:


df_sig_atc_head = df_sig_atc.head(10).sort_values(by="atc_2")
fig = go.Figure(
    go.Bar(
        y=df_sig_atc_head.nom_atc, x=df_sig_atc_head.nb_signal, orientation='h',
        marker=dict(color=['rgba(51,171,102,1)', 'rgba(102,192,140,1)',
                           'rgba(153,213,179,1)', 'rgba(204,234,217,1)',
                           'rgba(191,213,60,1)', 'rgba(207,223,109,1)',
                           'rgba(239,244,206,1)', 'rgba(239,244,206,1)',
                           'rgba(51,194,214,1)', 'rgba(102,209,224,1)'])
    )
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        autorange='reversed',
        ticks="outside", 
        tickcolor='white',
        ticklen=1
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0),
    barmode='group',
    bargap=0.10,
    bargroupgap=0.0,
    font={'size': 14}
)

fig.show()


# # Ventes

# In[9]:


# Connexion à la table ruptures
df_ventes = pd.read_sql_table('ventes', connection)

df_ventes['atc_2'] = df_ventes.atc.apply(lambda x: x[:3] if x else None)


# In[10]:


df_ventes.head(2)


# In[24]:


df_ventes_atc = df_ventes.groupby(['annee', 'atc_2'])[["unites_officine", "unites_hopital"]].sum().reset_index()
df_ventes_atc["total"] = df_ventes_atc.unites_officine + df_ventes_atc.unites_hopital
df_ventes_atc.atc_2 = df_ventes_atc.atc_2.apply(lambda x: atc2_names.get(x, x))
df_ventes_atc.head(3)


# In[16]:


records = df_ventes_atc.to_dict(orient='records')
ventes_atc_annee = {
    a: {
        d['atc_2']: {
            'unites_officine': d['unites_officine'],
            'unites_hopital': d['unites_hopital'],
            'total': d['total']
        }
        for d in records
    }
    for a in [2017, 2018, 2019]
}

# Générer le json des ruptures par classe ATC et par année
with open("../data/ventes_by_atc_by_annee.json", "w") as outfile: 
    json.dump(ventes_atc_annee, outfile)


# In[26]:


df_ventes_atc_2019.sort_values(by=[])


# In[57]:


from plotly.subplots import make_subplots
import math

atc_list = list(df_sig_atc_head.nom_atc.unique())
df_ventes_atc_2019 = df_ventes_atc[(df_ventes_atc.annee == 2019) & (df_ventes_atc.atc_2.isin(atc_list))].sort_values(by="atc_2")
df_sig_atc_head = df_sig_atc.head(10).sort_values(by="nom_atc")

# set up plotly figure
fig = make_subplots(1, 2)

# add first bar trace at row = 1, col = 1
fig.add_trace(go.Bar(
    y=df_sig_atc_head.nom_atc, x=df_sig_atc_head.nb_signal, orientation='h',
    marker=dict(color=['rgba(51,171,102,1)', 'rgba(102,192,140,1)', 'rgba(153,213,179,1)', 'rgba(204,234,217,1)',
                       'rgba(191,213,60,1)', 'rgba(207,223,109,1)', 'rgba(239,244,206,1)', 'rgba(239,244,206,1)',
                       'rgba(51,194,214,1)', 'rgba(102,209,224,1)']),
    name="Nombre de signalements"
)
             )

# add first scatter trace at row = 1, col = 1
fig.add_trace(
    go.Scatter(
        x=df_ventes_atc_2019.total/10000000, y=df_ventes_atc_2019.atc_2,
        line={
            "shape": "spline",
            "smoothing": 1,
            "width": 4,
            "color": "#00B3CC",
        }, mode="lines", name='Volume de ventes (en millions)'),
    row=1, col=1
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        autorange='reversed',
        ticks="outside", 
        tickcolor='white',
        ticklen=1
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0),
    barmode='group',
    bargap=0.10,
    bargroupgap=0.0,
    font={'size': 14}
)

fig.show()


# In[ ]:




