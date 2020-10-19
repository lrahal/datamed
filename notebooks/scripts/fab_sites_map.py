#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('/Users/linerahal/Documents/GitHub/datamed')

from jade_analysis import *
from get_geoloc import *


# # Load dataframe

# In[2]:


# Get dataframe with only rows containing same columns
df = get_filtered_dataframe()


# In[3]:


# Add main production site to dataframe columns
df = add_main_prod_site(df)


# In[4]:


df.head(1)


# # Get country

# In[5]:


# get_countries(df, nb_countries=20)


# In[6]:


df = df.iloc[:10, :]


# In[7]:


df['country'] = df.apply(
    lambda x: get_google_results(x.main_prod_site)['country'] if 'country' not in df.columns else x, axis=1
)


# In[8]:


df.country

