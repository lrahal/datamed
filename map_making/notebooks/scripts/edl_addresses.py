#!/usr/bin/env python
# coding: utf-8

# In[8]:


import re
import sys
import urllib

import pandas as pd
import requests
import seaborn as sns

sys.path.append('/Users/ansm/Documents/GitHub/datamed')
from create_database.models import connect_db
from map_making.get_geoloc import get_google_results


# In[9]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[10]:


df = pd.read_sql_table('production', connection)
df = df[['id', 'substance_active_id', 'sites_fabrication_substance_active']]

df['nb_semicolon'] = df.sites_fabrication_substance_active.str.count(';')
df['address_length'] = df.sites_fabrication_substance_active.apply(lambda x: len(x))

df.head(3)


# In[12]:


sns.scatterplot(data=df, x='address_length', y='nb_semicolon')


# In[18]:


# address = df[df.address_length >= 500].iloc[0].sites_fabrication_substance_active
address = "r0-cep 2016-290-rev 00; divi's laboratories ltd- unit ii annavaram post- chippada village, 531162 bheemunipatnam mandal, andhra pradesh, india r0-cep-2012-338 rev 02; novartis pharma stein ag schaffhauserstrasse 4332 stein switzerland ; divi’s laboratories limited unit-2, chippada (v), annavaram (post) bheemunipatnam (m) visakhapatnam district 531162 andhra pradesh, india ;"


# In[19]:


get_google_results(address)


# In[ ]:


BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'


# In[62]:


address = re.sub(' +', ' ', address)  # Remove multiple spaces
parameters = {'address': address, 'key': API_KEY}
geocode_url = f"{BASE_URL}{urllib.parse.urlencode(parameters)}"


# In[63]:


results = requests.get(geocode_url)
results = results.json()


# In[64]:


results


# In[58]:


df[df.address_length >= 500].iloc[0].sites_fabrication_substance_active.split(';')


# In[59]:


df[df.address_length >= 500].iloc[0].sites_fabrication_substance_active


# In[ ]:




