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
df_conso.head(2)


# In[26]:


len(df_conso)


# In[27]:


df.head(1)


# In[28]:


df_fab_cis.head(2)


# In[29]:


df2 = df_fab_cis.merge(df_conso, on='cis', how='left')
df2 = df2[df2.cis.notna()]
df2 = df2.drop_duplicates()


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


import folium
import requests
import json


# In[37]:


r = requests.get(
    'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
)

a = json.loads(r.text)


# In[38]:


#with open('world-countries.json', 'w') as outfile:
#    json.dump(a, outfile)


# In[39]:


c_list = [b['properties']['name'] for b in a['features']]


# In[40]:


for c in df2_countries.country.unique():
    if c not in c_list:
        print(c)


# In[41]:


df2_countries.sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head()
df2_countries.sort_values(
    by=['ventes_total'], ascending=False).drop(
    ['latitude', 'longitude'], axis=1).to_csv('../data/unités_vendues_par_pays_2018.csv', sep=';', index=False)


# In[42]:


# [b['properties']['name'] for b in a['features']]


# In[43]:


df2_countries.ventes_total = df2_countries.ventes_total.apply(lambda x: x/1000000)


# In[44]:


df2_countries[df2_countries.country == 'United States']


# In[45]:


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
    legend_name='Unites (en millions) d API produites (spe vendues en France - 2018)'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## En pondérant par le nombre de substances actives contenues dans uen spécialité

# In[46]:


df_pond = df2.copy()
# df_pond = df_pond.drop_duplicates()


# In[47]:


df_pond.ventes_officine = df_pond.apply(lambda x: x.ventes_officine/len(df_pond[df_pond.cis == x.cis]), axis=1)
df_pond.ventes_hopital = df_pond.apply(lambda x: x.ventes_hopital/len(df_pond[df_pond.cis == x.cis]), axis=1)
df_pond.ventes_total = df_pond.apply(lambda x: x.ventes_total/len(df_pond[df_pond.cis == x.cis]), axis=1)


# In[48]:


df_pond_grouped_by_country = df_pond.groupby(['country']).agg(
    {'ventes_officine': 'sum', 'ventes_hopital': 'sum', 'ventes_total': 'sum'}
).reset_index() # 'substance_active': 'nunique'


# In[49]:


countries = df_pond_grouped_by_country.country.unique()


# In[50]:


df_pond_countries = pd.merge(
    df_pond_grouped_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)


# In[51]:


df_pond_countries.sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1).head()
df_pond_countries.sort_values(
    by=['ventes_total'], ascending=False).drop(
    ['latitude', 'longitude'], axis=1).to_csv('../data/parts_vendues_par_pays_2018.csv', sep=';', index=False)


# In[52]:


df_pond_countries.ventes_total = df_pond_countries.ventes_total.apply(lambda x: x/1000000)


# In[53]:


df_pond_countries[df_pond_countries.country == 'United States']


# In[54]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_pond_countries,
    columns=['country', 'ventes_total'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays pour les spe vendues en France 2018'
).add_to(m)

folium.LayerControl().add_to(m)

m


# In[55]:


# df2[df2.cis == '67705462']


# In[56]:


# df3[df3.cis == '67705462']


# In[57]:


# v = df3.cis.value_counts()
# df3[df3.cis.isin(v.index[v.ge(2)])]


# ## Repartition of API fabrication sites by particular API

# In[58]:


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




