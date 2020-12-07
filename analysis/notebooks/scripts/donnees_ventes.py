#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import folium
import requests
import json
import pandas as pd
import plotly.express as px

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.create_tables_in_db import get_excels_df
from create_database.models import connect_db


# # Load dataframe

# In[2]:


# Get dataframe from table
df = get_excels_df()
df = df.drop(['dci', 'type_amm', 'sites_production', 'sites_conditionnement_primaire',
              'sites_conditionnement_secondaire', 'sites_importation', 'sites_controle',
              'sites_echantillotheque', 'sites_certification', 'substance_active', 'pgp',
              'filename', 'cos_sim'], axis=1)
df = df.rename(columns={'substance_active_match': 'substance_active'})
df = df.dropna(how='all')
df = df.drop_duplicates()


# In[4]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[5]:


df_fab = pd.read_sql_table('fabrication', connection)
df_atc = pd.read_sql_table('classification', connection)


# In[6]:


df_fab_cis = pd.merge(
    df[['cis', 'substance_active', 'sites_fabrication_substance_active', 'mitm']], df_fab,
    left_on='sites_fabrication_substance_active', right_on='address', how='outer')
df_fab_cis = df_fab_cis.merge(df_atc[['cis', 'atc', 'v3']], on='cis', how='left')

df_fab_cis = df_fab_cis.drop(['id', 'sites_fabrication_substance_active'], axis=1)
df_fab_cis.head(1)


# In[7]:


# Retirer les geocodings qui n'ont pas fonctionné
df_fab_cis = df_fab_cis[~df_fab_cis.country.isna()]
len(df_fab_cis)


# In[8]:


df_conso = pd.read_sql_table('consommation', connection)
df_conso.head(2)


# In[66]:


df_pond = df_fab_cis.merge(df_conso, on='cis', how='left')
df_pond = df_pond[df_pond.cis.notna()]
df_pond = df_pond.drop_duplicates()


# In[10]:


df_pond.ventes_officine = df_pond.apply(lambda x: x.ventes_officine/len(df_pond[df_pond.cis == x.cis]), axis=1)
df_pond.ventes_hopital = df_pond.apply(lambda x: x.ventes_hopital/len(df_pond[df_pond.cis == x.cis]), axis=1)
df_pond.ventes_total = df_pond.apply(lambda x: x.ventes_total/len(df_pond[df_pond.cis == x.cis]), axis=1)


# In[11]:


df_pond_grouped_by_country = df_pond.groupby(['country']).agg(
    {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
).reset_index() # 'substance_active': 'nunique'


# In[12]:


countries = df_pond_grouped_by_country.country.unique()


# In[13]:


df_countries_loc = pd.read_csv('../../map_making/data/countries_locations.csv')


# In[14]:


df_pond_countries = pd.merge(
    df_pond_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[15]:


df_pond_countries.sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head()
df_pond_countries.sort_values(
    by=['ventes_total'], ascending=False).drop(
    ['latitude', 'longitude'], axis=1).to_csv('../data/parts_vendues_par_pays_2018.csv', sep=';', index=False)


# In[16]:


df_pond_countries['ventes_total_millions'] = df_pond_countries.ventes_total.apply(lambda x: x/1000000)


# In[17]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_pond_countries,
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays pour les spe vendues en France 2018'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## MITM only

# In[18]:


df_pond_mitm = df_pond[df_pond.mitm == 'oui']


# In[19]:


df_pond_mitm_grouped_by_country = df_pond_mitm.groupby(['country']).agg(
    {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
).reset_index()


# In[20]:


countries_mitm = df_pond_mitm_grouped_by_country.country.dropna().unique()


# In[21]:


df_pond_mitm_countries = pd.merge(
    df_pond_mitm_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[22]:


df_pond_mitm_countries.sort_values(
    by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head(7)


# In[23]:


df_pond_mitm_countries.sort_values(by=['ventes_total'], ascending=False).drop(
    ['latitude', 'longitude'], axis=1).to_csv('../data/parts_mitm_vendues_par_pays_2018.csv', sep=';', index=False)


# In[24]:


df_pond_mitm_countries['ventes_total_millions'] = df_pond_mitm_countries.ventes_total.apply(lambda x: x/1000000)


# In[25]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_pond_mitm_countries,
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays pour les spe MITM vendues en France 2018'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## Etude sur les classes ATC

# Curares : M03AA<br/>
# Anti-infectieux : J<br/>
# Antineoplastiques : L<br/>
# Système nerveux : N<br/>

# Voir : https://www.ameli.fr/fileadmin/user_upload/documents/ald_bizone_atc.pdf et https://fr.wikipedia.org/wiki/Classe_ATC_M03

# In[139]:


df_curares = df_pond[df_pond.atc.notna()]


# In[140]:


df_curares = df_curares[df_curares.atc.str.startswith('N')]


# In[141]:


len(df_curares)


# In[142]:


df_curares_grouped_by_country = df_curares.groupby(['country']).agg(
    {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
).reset_index()


# In[143]:


countries = df_curares_grouped_by_country.country.unique()


# In[144]:


df_curares_countries = pd.merge(
    df_curares_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[149]:


df_curares_countries.sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head(6)


# In[146]:


df_curares_countries['ventes_total_millions'] = df_curares_countries.ventes_total.apply(lambda x: x/1000000)


# In[148]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_curares_countries,
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays - Systeme nerveux - France 2018'
).add_to(m)

folium.LayerControl().add_to(m)

m


# In[ ]:





# In[ ]:





# In[ ]:




