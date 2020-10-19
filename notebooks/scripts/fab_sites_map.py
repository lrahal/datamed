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
df_dci = get_filtered_dataframe()


# In[3]:


# Add main production site to dataframe columns
df_dci = add_main_prod_site(df_dci)


# In[4]:


df_dci.main_prod_site = df_dci.main_prod_site.apply(lambda x: re.sub(' +', ' ', x))


# In[5]:


df_dci.head(1)


# In[6]:


def convert_cis(cis_str):
    if cis_str.replace(' ', '').replace('.', '').replace('cis', '').replace(':', '').isdigit():
        cis = int(float(cis_str.replace(' ', '').replace('.', '').replace('cis', '').replace(':', '')))
    else:
        cis = cis_str
    return cis


# In[7]:


df_dci.cis = df_dci.cis.apply(lambda x: convert_cis(x))


# In[8]:


all_cis = df_dci.cis.unique()   # 4982
bad_cis = df_dci[df_dci.cis.apply(lambda x: isinstance(x, str))].cis.unique()   # 381


# In[9]:


df_good_dci = df_dci[df_dci.cis.apply(lambda x: isinstance(x, int))].copy()


# In[10]:


len(df_good_dci)


# In[11]:


nb_addresses = len(df_good_dci.main_prod_site.unique())


# # Get country

# In[12]:


get_countries(df_good_dci, nb_addresses=200)


# In[13]:


df_good_dci_sample = df_good_dci.iloc[:200, :]


# In[14]:


#df_dci['country'] = df_dci.apply(
#    lambda x: get_google_results(x.main_prod_site)['country'], axis=1
#)


# In[15]:


df_good_dci_sample.head(1)


# # Production sites map

# ## Production sites by cis (speciality)

# In[16]:


df_addresses = pd.read_csv('/Users/linerahal/Documents/GitHub/datamed/data/output-addresses.csv')


# In[17]:


df_addresses = df_addresses.drop(columns=['Unnamed: 0'])
df_addresses = df_addresses.rename(columns={'input_string': 'main_prod_site'})


# In[18]:


df = pd.merge(
    df_good_dci_sample[['dénomination de la spécialité', 'cis', 'main_prod_site']],
    df_addresses,
    on='main_prod_site',
    how='inner')


# In[19]:


len(df)


# In[20]:


df.head(1)


# In[21]:


# import the plotly express
import plotly.express as px

# set up the chart from the df dataFrame
fig = px.scatter_geo(df, 
                     # longitude is taken from the df["lon"] columns and latitude from df["lat"]
                     lon='longitude', 
                     lat='latitude',
                     # style
                     color='country',
                     # choose the map chart's projection
                     projection='natural earth',
                     # columns which is in bold in the pop up
                     hover_name = 'cis',
                     # format of the popup not to display these columns' data
                     hover_data = {'cis':False,
                                   'longitude': False,
                                   'latitude': False
                                  }
                     )
#fig.update_traces(marker=dict(size=10, color='red'))
fig.update_traces(marker=dict(size=10))
fig.update_geos(fitbounds='locations', showcountries=True)
fig.update_layout(title = 'Production sites')
fig.show()


# In[ ]:





# In[ ]:




