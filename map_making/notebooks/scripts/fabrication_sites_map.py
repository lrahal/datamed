#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

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
              'sites_echantillotheque', 'sites_certification', 'substance_active', 'mitm',
              'pgp', 'filename', 'cos_sim'], axis=1)
df = df.rename(columns={'substance_active_match': 'substance_active'})
df = df.dropna(how='all')
df = df.drop_duplicates()


# In[3]:


len(df)


# In[4]:


nb_addresses = len(df.sites_fabrication_substance_active.unique())
print(nb_addresses)


# # Get country

# In[5]:


addresses = df.sites_fabrication_substance_active.unique()


# In[6]:


# get_locations(addresses, output_filename='../data/sites_fabrication_substance_active.csv')


# # API fabrication sites map

# ## API fabrication sites by cis (speciality)

# In[7]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[8]:


df_fab = pd.read_sql_table('fabrication', connection)


# In[9]:


df_fab.head(1)


# In[10]:


df_fab_cis = pd.merge(
    df[['cis', 'substance_active', 'sites_fabrication_substance_active']], df_fab,
    left_on='sites_fabrication_substance_active', right_on='address', how='outer')

df_fab_cis = df_fab_cis.drop(['id', 'sites_fabrication_substance_active'], axis=1)
df_fab_cis.head(1)


# In[11]:


len(df), len(df_fab_cis)


# In[12]:


# Retirer les geocodings qui n'ont pas fonctionné
df_fab_cis = df_fab_cis[~df_fab_cis.country.isna()]
len(df_fab_cis)


# In[13]:


# list(df.substance_active)
# df_api = pd.DataFrame(df_fab_cis.substance_active.unique(), columns=['substance_active'])


# ## API fabrication sites by active substances (api)

# In[14]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_fab_cis, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'substance_active',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'substance_active': False, 'longitude': False, 'latitude': False}
                    )
#fig.update_traces(marker=dict(size=10, color='red'))
fig.update_traces(marker=dict(size=10))
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Active substance fabrication sites')
fig.show()


# ## Number of api produced by country

# In[15]:


df_grouped_by_country = df_fab_cis.groupby(['country']).agg({'substance_active': 'nunique'}).reset_index()


# In[16]:


countries = df_grouped_by_country.country.unique()


# In[17]:


# get_locations(countries, output_filename='countries_locations.csv')


# In[18]:


df_countries_loc = pd.read_csv('../data/countries_locations.csv')


# In[19]:


df_countries_loc.head()


# In[20]:


df_countries = pd.merge(
    df_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[21]:


len(df_countries), len(df_grouped_by_country)


# In[22]:


df_countries.head(1)


# In[23]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_countries, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     size='substance_active',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'country',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'country': False, 'longitude': False, 'latitude': False}
                    )
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Amount of active substances produced countries')
fig.show()


# ## Number of boxes sold in France which api have been produced in specific country

# In[24]:


db = connect_db()  # establish connection
connection = db.connect()


# In[25]:


df_conso = pd.read_sql_table('consommation', connection)


# In[26]:


df_conso.head(2)


# In[27]:


df.head(1)


# In[28]:


df_fab_cis.head(2)


# In[29]:


df2 = df_fab_cis.merge(df_conso, on='cis', how='left')


# In[30]:


len(df2), len(df_fab_cis)


# In[31]:


df2.head(2)


# In[32]:


df2_grouped_by_country = df2.groupby(['country']).agg(
    {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
).reset_index() # 'substance_active': 'nunique'


# In[33]:


countries = df2_grouped_by_country.country.dropna().unique()


# In[34]:


df2_countries = pd.merge(
    df2_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[35]:


df2_countries.head(2)


# In[36]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df2_countries, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     size='ventes_total',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'country',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'country': False, 'longitude': False, 'latitude': False}
                    )
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Amount of active substances produced countries')
fig.show()


# In[37]:


import folium
import requests
import json


# In[38]:


r = requests.get(
    'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
)

a = json.loads(r.text)


# In[39]:


#with open('world-countries.json', 'w') as outfile:
#    json.dump(a, outfile)


# In[40]:


c_list = [b['properties']['name'] for b in a['features']]


# In[41]:


for c in df2_countries.country.unique():
    if c not in c_list:
        print(c)


# In[42]:


df2_countries.sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head()
df2_countries.sort_values(
    by=['ventes_total'], ascending=False).drop(
    ['latitude', 'longitude'], axis=1).to_csv('../data/ventes_par_pays_2018.csv', sep=';', index=False)


# In[43]:


# [b['properties']['name'] for b in a['features']]


# In[44]:


df2_countries.ventes_total = df2_countries.ventes_total.apply(lambda x: x/1000000)


# In[45]:


df2_countries[df2_countries.country == 'United States']


# In[46]:


# https://github.com/python-visualization/folium/blob/master/examples/data/world-countries.json#
# url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
# state_geo = f'{url}/world-countries.json'
state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df2_countries,
    columns=['country', 'ventes_total'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Boxes sold in France in 2018 (in millions)'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## Repartition of API fabrication sites by particular API

# In[47]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_fab_cis[df_fab_cis.substance_active == 'hydrochlorothiazide'], 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'cis',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'cis': False, 'longitude': False, 'latitude': False}
                    )
#fig.update_traces(marker=dict(size=10, color='red'))
fig.update_traces(marker=dict(size=10))
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Fabrication sites of hydrochlorothiazide')
fig.show()


# In[ ]:




