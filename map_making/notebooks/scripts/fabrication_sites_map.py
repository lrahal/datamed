#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys

import pandas as pd
import plotly.express as px

sys.path.append('/Users/linerahal/Documents/GitHub/datamed')

from create_database.upload_db import upload_table_from_db
from map_making.get_geoloc import get_locations


# # Load dataframe

# In[2]:


# Get dataframe from table
table_name = 'fabrication_sites'
df = upload_table_from_db(table_name)


# In[3]:


df.head(1)


# In[4]:


len(df)


# In[5]:


nb_addresses = len(df.sites_fabrication_substance_active.unique())
print(nb_addresses)


# # Get country

# In[6]:


addresses = df.sites_fabrication_substance_active.unique()


# In[7]:


# get_locations(addresses, output_filename='sites_fabrication_substance_active.csv')


# In[8]:


# df_sites_sample = df.iloc[:, :]


# # API fabrication sites map

# ## API fabrication sites by cis (speciality)

# In[9]:


df_locations = pd.read_csv('../data/sites_fabrication_substance_active.csv')


# In[10]:


site_col = 'sites_fabrication_substance_active'


# In[11]:


df_locations = df_locations.drop(columns=['Unnamed: 0'])
df_locations = df_locations.rename(columns={'input_string': site_col})


# In[12]:


df_locations.head(1)


# In[13]:


df_final = pd.merge(
    df[['denomination_specialite', 'cis', 'substance_active', site_col]], df_locations, on=site_col, how='inner'
)
df_final.head(1)


# In[14]:


api_list = df_final.substance_active.unique()
len(api_list)


# In[15]:


#df_final.substance_active.value_counts()


# In[16]:


len(df_final)


# In[17]:


# Retirer les geocodings qui n'ont pas fonctionné (35 sur 8940)
#df_final = df_final[
#    (df_final.status != 'ZERO_RESULTS') & (df_final.status != 'INVALID_REQUEST') & (~df_final.country.isna())
#]
df_final = df_final[df_final.status == 'OK']
len(df_final)


# In[18]:


# list(df.substance_active)
df_api = pd.DataFrame(df_final.substance_active.unique(), columns=['substance_active'])


# In[19]:


df_api.to_csv('../data/substances_actives.csv', index=False)


# ## API fabrication sites by active substances (api)

# In[20]:


df_final = df_final[~df_final['country'].isna()]


# In[21]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_final, 
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


# ## Number of api producted by country

# In[22]:


df_grouped_by_country = df_final.groupby('country')
df_grouped_by_country = df_grouped_by_country.agg({'substance_active': 'nunique'})
df_grouped_by_country = df_grouped_by_country.reset_index()


# In[23]:


countries = df_grouped_by_country.country.unique()


# In[24]:


# get_locations(countries, output_filename='countries_locations.csv')


# In[25]:


df_countries_loc = pd.read_csv('../data/countries_locations.csv')


# In[26]:


df_countries_loc.head(1)


# In[27]:


df_countries_loc = df_countries_loc.drop(columns=['Unnamed: 0'])


# In[28]:


df_countries = pd.merge(
    df_grouped_by_country[['substance_active', 'country']], df_countries_loc, on='country', how='inner'
)


# In[29]:


df_countries.head(1)


# In[30]:


df_countries = df_countries[~df_countries.country.isna()]


# In[31]:


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


# ## Repartition of API fabrication sites by particular API

# In[32]:


# set up the chart from the df dataFrame
fig = px.scatter_geo(df_final[df_final.substance_active == 'hydrochlorothiazide'], 
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




