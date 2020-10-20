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
site_name = 'site(s) de production  / sites de production alternatif(s)'

# Add site to dataframe columns
df_sites = add_selected_site(df_sites, site_name=site_name)


# In[3]:


df_sites.head(1)


# In[4]:


all_cis = df_sites.cis.unique()   # 4982
bad_cis = df_sites[df_sites.cis.apply(lambda x: isinstance(x, str))].cis.unique()   # 381


# In[5]:


# Keep rows having integer cis (optional)
# df_sites = df_sites[df_sites.cis.apply(lambda x: isinstance(x, int))].copy()


# In[6]:


len(df_sites)


# In[7]:


nb_addresses = len(df_sites.site_name.unique())


# # Get country

# In[8]:


get_countries(df_sites, nb_addresses=200)


# In[9]:


df_sites_sample = df_sites.iloc[:200, :]


# In[10]:


#df_sites['country'] = df_sites.apply(
#    lambda x: get_google_results(x.site_name)['country'], axis=1
#)


# In[11]:


df_sites_sample.head(1)


# # Production sites map

# ## Production sites by cis (speciality)

# In[18]:


df_addresses = pd.read_csv('/Users/linerahal/Documents/GitHub/datamed/data/output-addresses.csv')


# In[19]:


df_addresses = df_addresses.drop(columns=['Unnamed: 0'])
df_addresses = df_addresses.rename(columns={'input_string': 'site_name'})


# In[35]:


df = pd.merge(
    df_sites_sample[['dénomination de la spécialité', 'cis', 'substance active', 'site_name']],
    df_addresses,
    on='site_name',
    how='inner')


# In[36]:


len(df)


# In[37]:


df.head(1)


# In[38]:


api_list = df['substance active'].unique().tolist()


# In[39]:


len(api_list)


# In[40]:


df['substance active'].value_counts()


# In[45]:


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
fig.update_layout(title = 'Production sites')
fig.show()


# In[ ]:





# In[ ]:




