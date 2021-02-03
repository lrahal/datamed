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


# In[6]:


get_google_results(address_full)


# # Avec geonamescache

# In[7]:


import geonamescache
import spacy

nlp = spacy.load('en_core_web_sm')


# In[8]:


gc = geonamescache.GeonamesCache()
countries = gc.get_countries()


# In[9]:


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


# In[10]:


countries = [*gen_dict_extract(countries, 'name')]


# In[11]:


address_full


# In[12]:


address_full.title()


# In[13]:


import string

string.capwords(address_full)


# In[14]:


#for ent in doc.ents:
#    if ent.text == 'Ireland R0-cep':
#        print(ent.label_)


# In[15]:


# doc = nlp(address_full)
doc = nlp(string.capwords(address_full))

# Use of NER (engtity recognizer)
for ent in doc.ents:
    if ent.label_ == 'GPE':
        if ent.text in countries:
            print(f"Country : {ent.text}")
        else:
            print(f"Other GPE : {ent.text}")


# In[16]:


# doc = nlp(address_full)
doc = nlp(address_full.title())

# Use of NER (engtity recognizer)
for ent in doc.ents:
    if ent.label_ == 'GPE':
        if ent.text in countries:
            print(f"Country : {ent.text}")
        else:
            print(f"Other GPE : {ent.text}")


# In[17]:


countries_str = ' '.join(countries)


# # Avec du bon gros regex

# In[18]:


from country_list import available_languages, countries_for_language
import unicodedata2
from tqdm import tqdm
import json
import folium


# In[19]:


df = pd.read_sql_table('production', connection)
df = df[['id', 'substance_active_id', 'sites_fabrication_substance_active', 'filename']]


# In[20]:


df_fab = pd.read_sql_table('fabrication', connection)
countries_fab = [c.lower() for c in df_fab.country.unique() if c]

countries_en = [c[1].lower() for c in countries_for_language('en')]
countries_fr = [c[1].lower() for c in countries_for_language('fr')]
others = ['usa', 'uk', 'england', 'scotland', 'u.s.a.', 'czech republic', 'españa', 'royaume uni', 'macau',
          '(cz)', 'italia', 'corée', '(in)', '(tw)', '(it)', '(us)', '(fr)', 'angleterre', 'etats unis',
          'république tchèque', 'pays bas', '(es)', 'coree', ' us ', 'deutschland', 'gmbh', '(cn)', ' cn ',
         '(ch)', '(fi)', '(gb)', 'lyon', ' douai ', 'korea', '(de)', 'rép. tchèque', 'andhra pradesh',
         'annemasse', 'gentilly', 'bergamo', 'vitry sur seine', 'rép tchèque', 'gennevilliers', '(gr)',
         'tarapur', 'la rochelle', 'românia', 'maharashtra', '(hu)', 'ratlam', 'gujarat', '(pl)', '(nl)']

all_countries = set(countries_fr + countries_en + countries_fab + others)


# In[21]:


country_list = []
for word in all_countries:
    if not word in country_list:
        country_list.append(word)
        word_no_accents = ''.join((c for c in unicodedata2.normalize('NFD', word) if unicodedata2.category(c) !=  'Mn'))
        if not word_no_accents in country_list:
            country_list.append(word_no_accents)

country_list = sorted(country_list)


# In[22]:


with open('/Users/ansm/Documents/GitHub/datamed/map_making/data/countries.json') as json_file:
    country_dict = json.load(json_file)


# In[23]:


def get_country(address, country_list):
    country_in_address = {}
    for country in country_list:
        if country in address:
            country_in_address[country_dict.get(country, country)] = address.count(country)
    return country_in_address

pays_list = []
addresses = df.sites_fabrication_substance_active.unique()
for a in addresses:
    pays = get_country(a, country_list).keys()
    for p in pays:
        if p not in pays_list:
            pays_list.append(p)

df['pays'] = df.sites_fabrication_substance_active.apply(lambda x: get_country(x, country_list))

for country in tqdm(pays_list):
    df[country_dict.get(country, country)] = df.pays.apply(lambda x: x.get(country, 0))


# In[24]:


df.head(3)


# In[25]:


(1 - len(df[df.pays == {}]) / len(df)) * 100


# In[26]:


df.inde.sum(), df.france.sum(), df.chine.sum()


# In[27]:


len(df[df.pays == {}])


# In[28]:


len(df[df.pays.apply(lambda x: len(x) > 1)]) / len(df) * 100


# In[29]:


df[df.pays == {}].iloc[67].sites_fabrication_substance_active


# In[30]:


countries = [col for col in df.columns
             if col not in ['id', 'substance_active_id', 'sites_fabrication_substance_active', 'filename', 'pays']]


# In[31]:


api_by_country = [{'country': col, 'substance_active_id': df[col].sum()} for col in countries]
df_api_by_country = pd.DataFrame(api_by_country, columns=['country', 'substance_active_id'])


# In[32]:


df_api_by_country.head(1)


# In[40]:


df_countries_loc = pd.read_csv('../data/countries_locations_030221.csv', sep=';')
df_countries_loc = df_countries_loc.rename(columns={'country': 'country_en'})
df_countries_loc.head(1)


# In[41]:


df_countries = pd.merge(
    df_api_by_country, df_countries_loc,
    left_on='country', right_on='address', how='left'
)

len(df_countries), len(df_api_by_country)


# In[42]:


df_countries.head()


# In[44]:


state_geo = 'world-countries.json'

m = folium.Map(location=[48, 2], zoom_start=4)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=df_countries,
    columns=['country_en', 'substance_active_id'],
    key_on='feature.properties.name',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Nb de substance actives fabriquees (spe commercialisees en France en 2019)'
).add_to(m)

folium.LayerControl().add_to(m)

m


# In[ ]:





# In[ ]:





# # Avec la geocoding API

# In[37]:


# BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'


# In[38]:


# API_KEY = os.environ.get('GCP_KEY')


# In[39]:


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




