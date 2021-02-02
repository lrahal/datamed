#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import sys
import urllib

import pandas as pd
import requests
import seaborn as sns

sys.path.append('/Users/ansm/Documents/GitHub/datamed')
from create_database.models import connect_db
from map_making.get_geoloc import get_google_results


# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('production', connection)
df = df[['id', 'substance_active_id', 'sites_fabrication_substance_active']]

df['nb_semicolon'] = df.sites_fabrication_substance_active.str.count(';')
df['address_length'] = df.sites_fabrication_substance_active.apply(lambda x: len(x))

df.head(3)


# In[4]:


sns.scatterplot(data=df, x='address_length', y='nb_semicolon')


# In[5]:


address_full = df[df.address_length >= 500].iloc[0].sites_fabrication_substance_active
address = "r0-cep 2016-290-rev 00; divi's laboratories ltd- unit ii annavaram post- chippada village, 531162 bheemunipatnam mandal, andhra pradesh, india r0-cep-2012-338 rev 02; novartis pharma stein ag schaffhauserstrasse 4332 stein switzerland ; divi’s laboratories limited unit-2, chippada (v), annavaram (post) bheemunipatnam (m) visakhapatnam district 531162 andhra pradesh, india ;"


# In[7]:


get_google_results(address_full)


# # Avec geonamescache

# In[49]:


import geonamescache
import spacy

nlp = spacy.load('en_core_web_sm')


# In[50]:


gc = geonamescache.GeonamesCache()
countries = gc.get_countries()


# In[51]:


def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


# In[52]:


countries = [*gen_dict_extract(countries, 'name')]


# In[53]:


address_full


# In[70]:


address_full.title()


# In[72]:


import string

string.capwords(address_full)


# In[91]:


for ent in doc.ents:
    if ent.text == 'Ireland R0-cep':
        print(ent.label_)


# In[92]:


# doc = nlp(address_full)
doc = nlp(string.capwords(address_full))

# Use of NER (engtity recognizer)
for ent in doc.ents:
    if ent.label_ == 'GPE':
        if ent.text in countries:
            print(f"Country : {ent.text}")
        else:
            print(f"Other GPE : {ent.text}")


# In[74]:


# doc = nlp(address_full)
doc = nlp(address_full.title())

# Use of NER (engtity recognizer)
for ent in doc.ents:
    if ent.label_ == 'GPE':
        if ent.text in countries:
            print(f"Country : {ent.text}")
        else:
            print(f"Other GPE : {ent.text}")


# In[65]:


countries_str = ' '.join(countries)


# # Avec du bon gros regex

# In[ ]:





# # Avec la geocoding API

# In[ ]:


# BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'


# In[ ]:


# API_KEY = os.environ.get('GCP_KEY')


# In[ ]:


address_full = re.sub(' +', ' ', address_full)  # Remove multiple spaces
parameters = {'address': address_full, 'key': API_KEY}
geocode_url = f"{BASE_URL}{urllib.parse.urlencode(parameters)}"


# In[ ]:


results = requests.get(geocode_url)
results = results.json()


# In[ ]:


results


# In[ ]:


df[df.address_length >= 500].iloc[0].sites_fabrication_substance_active.split(';')


# In[ ]:




