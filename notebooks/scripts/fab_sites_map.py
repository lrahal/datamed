#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
sys.path.append('/Users/linerahal/Documents/GitHub/datamed')

from jade_analysis import *
from get_geoloc import *


# # Load dataframe

# In[2]:


# Get dataframe with only rows containing same columns
df_sites = get_filtered_dataframe()

# Sites possibilities:
# site(s) de production  / sites de production alternatif(s)
# site(s) de conditionnement primaire
# site(s) de conditionnement secondaire
# site d'importation
# site(s) de contrôle
# site(s) d'échantillothèque
# site(s) de certification
# site(s) de fabrication de la substance active
site_name = 'site(s) de fabrication de la substance active'

# Add site to dataframe columns
df_sites = add_selected_site(df_sites, site_name=site_name)


# In[3]:


df_sites.head(1)


# In[ ]:


# all_cis = df_sites.cis.unique()   # 4982
# bad_cis = df_sites[df_sites.cis.apply(lambda x: isinstance(x, str))].cis.unique()   # 381

# Keep rows having integer cis (optional)
# df_sites = df_sites[df_sites.cis.apply(lambda x: isinstance(x, int))].copy()


# In[4]:


len(df_sites)


# In[5]:


nb_addresses = len(df_sites.site_name.unique())
print(nb_addresses)


# # Get country

# In[7]:


# get_locations(df_sites, output_filename='sites_fab_api.csv', nb_addresses=nb_addresses)


# In[8]:


df_sites_sample = df_sites.iloc[:, :]


# # API fabrication sites map

# ## API fabrication sites by cis (speciality)

# In[10]:


df_loc = pd.read_csv('/Users/linerahal/Documents/GitHub/datamed/data/sites_fab_api.csv')


# In[11]:


df_loc = df_loc.drop(columns=['Unnamed: 0'])
df_loc = df_loc.rename(columns={'input_string': 'site_name'})


# In[12]:


df = pd.merge(
    df_sites_sample[['dénomination de la spécialité', 'cis', 'substance active', 'site_name']],
    df_loc,
    on='site_name',
    how='inner')


# In[13]:


df.head(1)


# In[14]:


api_list = df['substance active'].unique().tolist()


# In[15]:


len(api_list)


# In[16]:


df['substance active'].value_counts()


# In[17]:


len(df)


# In[27]:


# Retirer les geocodings qui n'ont pas fonctionné (35 sur 8940)
df = df[(df.status != 'ZERO_RESULTS') & (df.status != 'INVALID_REQUEST') & (~df.country.isna())]
len(df)


# In[ ]:


# list(df['substance active'])
df_api = pd.DataFrame(df['substance active'].unique(), columns=['substance active'])   #.to_csv('substances_actives.csv', index=False)


# In[ ]:


df_api.to_csv('substances_actives.csv', index=False)


# ## API fabrication sites by active substances (api)

# In[28]:


df[df['country'].isna()]


# In[29]:


# import the plotly express
import plotly.express as px

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
                     hover_name = 'substance active',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'substance active': False, 'longitude': False, 'latitude': False}
                    )
#fig.update_traces(marker=dict(size=10, color='red'))
fig.update_traces(marker=dict(size=10))
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Production sites')
fig.show()


# ## Number of api producted by country

# In[30]:


grouped_df = df.groupby('country')
grouped_df = grouped_df.agg({'substance active': 'nunique'})
grouped_df = grouped_df.reset_index()


# In[31]:


grouped_df['site_name'] = grouped_df.country


# In[32]:


# get_locations(grouped_df, output_filename='countries_locations.csv', nb_addresses=len(grouped_df))


# In[33]:


df_countries_loc = pd.read_csv('/Users/linerahal/Documents/GitHub/datamed/data/countries_locations.csv')


# In[34]:


df_countries_loc = df_countries_loc.drop(columns=['Unnamed: 0'])
df_countries_loc = df_countries_loc.rename(columns={'input_string': 'site_name'})


# In[35]:


df_countries = pd.merge(grouped_df[['substance active', 'site_name']], df_countries_loc, on='site_name', how='inner')


# In[36]:


df_countries = df_countries[~df_countries.country.isna()]


# In[44]:


# import the plotly express
import plotly.express as px

# set up the chart from the df dataFrame
fig = px.scatter_geo(df_countries, 
                     # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     size='substance active',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop-up
                     hover_name = 'country',
                     # format of the pop-up not to display these columns' data
                     hover_data = {'country': False, 'longitude': False, 'latitude': False}
                    )
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Active substances fabrication sites')
fig.show()


# ## Repartition of API fabrication sites by particular API

# In[41]:


# import the plotly express
import plotly.express as px

# set up the chart from the df dataFrame
fig = px.scatter_geo(df[df['substance active'] == 'hydrochlorothiazide'], 
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




