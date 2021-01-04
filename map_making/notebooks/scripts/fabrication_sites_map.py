#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import sys

import folium
import pandas as pd
import plotly.express as px
import requests

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db


# # Load dataframe

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('production', connection)

df = df.drop(['dci', 'type_amm', 'sites_production', 'sites_conditionnement_primaire',
              'sites_conditionnement_secondaire', 'sites_importation', 'sites_controle',
              'sites_echantillotheque', 'sites_certification', 'substance_active', 'pgp',
              'filename'], axis=1)

df = df.dropna(how='all')
df = df.drop_duplicates()

df.head(2)


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


df_fab = pd.read_sql_table('fabrication', connection)

df_fab.head(1)


# In[8]:


df = df.merge(df_fab, left_on='fabrication_id', right_on='id', how='left')
df = df.rename(columns={'id_x': 'id'})
df = df.drop(['id_y', 'sites_fabrication_substance_active', 'fabrication_id'], axis=1)

df.head(2)


# In[9]:


# Retirer les geocodings qui n'ont pas fonctionné
df = df[~df.country.isna()]
len(df)


# In[10]:


# list(df.substance_active)
# df_api = pd.DataFrame(df_fab_cis.substance_active.unique(), columns=['substance_active'])


# ## API fabrication sites by active substances (api)

# In[11]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'substance_active_id',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'substance_active_id': False, 'longitude': False, 'latitude': False}
                    )
#fig.update_traces(marker=dict(size=10, color='red'))
fig.update_traces(marker=dict(size=10))
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Active substance fabrication sites')
fig.show()


# ## Number of api produced by country

# In[12]:


df_fab.head()


# In[13]:


df_api_by_country = df.groupby(['country']).agg({'substance_active_id': 'nunique'}).reset_index()


# In[14]:


countries = df_api_by_country.country.unique()


# In[15]:


# get_locations(countries, output_filename='countries_locations.csv')


# In[16]:


df_countries_loc = pd.read_csv('../data/countries_locations.csv')
df_countries_loc.head()


# In[17]:


df_countries = pd.merge(
    df_api_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
)

len(df_countries), len(df_api_by_country)


# In[18]:


df_countries.head(1)


# In[19]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_countries, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     size='substance_active_id',
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


# In[56]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_countries,
    columns=['country', 'substance_active_id'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Nb de substance actives fabriquees (spe commercialisees en France en 2019)'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## Number of boxes sold in France which api have been produced in specific country

# In[20]:


df_ventes = pd.read_sql_table('ventes', connection)
df_ventes['ventes_total'] = df_ventes.unites_officine + df_ventes.unites_hopital
df_ventes.head(2)


# In[21]:


df.head(2)


# In[22]:


# Calculer les ventes par année et par CIS (somme sur les présentations)
df_ventes_by_cis = df_ventes.groupby(['annee', 'cis']).agg({'ventes_total': 'sum'}).reset_index()


# In[23]:


# Calculer les ventes par CIS
year = 2019

df2 = df.merge(df_ventes_by_cis[df_ventes_by_cis.annee == year], on='cis', how='left')
df2 = df2[df2.cis.notna()]
df2 = df2.drop(columns=['titulaire_amm', 'denomination_specialite'])
df2 = df2.drop_duplicates()


# In[24]:


df2[df2.cis == '60349519']


# In[25]:


# Calculer les ventes par pays
df2_ventes_by_country = df2.groupby('country').agg({'ventes_total': 'sum'}).reset_index()

df2_ventes_by_country.head(2)


# In[26]:


countries = df2_ventes_by_country.country.dropna().unique()


# In[27]:


df2_countries = pd.merge(
    df2_ventes_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
).sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1)

df2_countries.to_csv('../data/unités_vendues_par_pays_' + str(year) + '.csv', sep=';', index=False)

df2_countries['ventes_total_millions'] = df2_countries.ventes_total.apply(lambda x: x/10**6)

df2_countries.head(2)


# In[28]:


r = requests.get(
    'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
)

a = json.loads(r.text)


# In[29]:


# with open('world-countries.json', 'w') as outfile:
#    json.dump(a, outfile)


# In[30]:


c_list = [b['properties']['name'] for b in a['features']]

for c in df2_countries.country.unique():
    if c not in c_list:
        print(c)


# In[31]:


# [b['properties']['name'] for b in a['features']]


# In[32]:


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
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Unites (en millions) d API produites (spe vendues en France - ' + str(year) + ')'
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## En pondérant par le nombre de substances actives contenues dans une spécialité

# In[33]:


df_pond = df2.copy()
# df_pond = df_pond.drop_duplicates()

df_pond.head()


# In[34]:


df_pond.ventes_total = df_pond.apply(lambda x: x.ventes_total/len(df_pond[df_pond.cis == x.cis]), axis=1)


# In[35]:


df_ventes_pond_by_country = df_pond.groupby(['country']).agg({'ventes_total': 'sum'}).reset_index()


# In[36]:


countries = df_ventes_pond_by_country.country.unique()


# In[37]:


df_ventes_pond_countries = pd.merge(
    df_ventes_pond_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
).sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1)

# Save into csv
df_ventes_pond_countries.to_csv('../data/parts_vendues_par_pays_' + str(year) + '.csv', sep=';', index=False)

df_ventes_pond_countries['ventes_total_millions'] = df_ventes_pond_countries.ventes_total.apply(lambda x: x/10**6)

df_ventes_pond_countries.head(3)


# In[38]:


df_ventes_pond_countries[df_ventes_pond_countries.country == 'United States']


# In[39]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_ventes_pond_countries,
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays pour les spe vendues en France ' + str(year)
).add_to(m)

folium.LayerControl().add_to(m)

m


# ## MITM only

# In[40]:


df_pond_mitm = df_pond[df_pond.mitm == 'oui']


# In[41]:


df_ventes_pond_mitm_by_country = df_pond_mitm.groupby(['country']).agg({'ventes_total': 'sum'}).reset_index()


# In[42]:


countries_mitm = df_ventes_pond_mitm_by_country.country.dropna().unique()


# In[43]:


df_ventes_pond_mitm_countries = pd.merge(
    df_ventes_pond_mitm_by_country, df_countries_loc[['latitude', 'longitude', 'country']],
    on='country', how='left'
).sort_values(by=['ventes_total'], ascending=False).drop(['latitude', 'longitude'], axis=1)

df_ventes_pond_mitm_countries.to_csv('../data/parts_mitm_vendues_par_pays_' + str(year) + '.csv',
                                     sep=';', index=False)

df_ventes_pond_mitm_countries['ventes_total_millions'] = df_ventes_pond_mitm_countries.ventes_total.apply(
    lambda x: x/10**6)


# In[44]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_ventes_pond_mitm_countries,
    columns=['country', 'ventes_total_millions'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Parts (millions) des API fabriquees / pays pour les spe MITM vendues en France ' + str(year)
).add_to(m)

folium.LayerControl().add_to(m)

m


# In[45]:


# df2[df2.cis == '67705462']


# In[46]:


# df3[df3.cis == '67705462']


# In[47]:


# v = df3.cis.value_counts()
# df3[df3.cis.isin(v.index[v.ge(2)])]


# ## Repartition of API fabrication sites by particular API

# In[48]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df[df.substance_active_id == 3297], 
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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




