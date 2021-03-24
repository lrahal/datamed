#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


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


# In[4]:


ruptures_by_annee = defaultdict()
for a in range(2014, 2021):
    df_annee = df[df.annee == a]
    df_ranked_atc = df_annee.groupby('atc_2').count().reset_index().sort_values(by=['id_signal'], ascending=False)
    df_ranked_atc = df_ranked_atc.rename(columns={'id_signal': 'nb_ruptures'})
    
    ranked_atc_list = df_ranked_atc[['atc_2', 'nb_ruptures']].to_dict(orient='records')
    ruptures_by_annee[a] = {d['atc_2']: d['nb_ruptures'] for d in ranked_atc_list}


# In[6]:


df_ranked_atc = df_ranked_atc.head(10)
fig = go.Figure(
    go.Bar(
        y=df_ranked_atc.atc_2, x=df_ranked_atc.nb_ruptures, orientation='h',
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


# In[ ]:




