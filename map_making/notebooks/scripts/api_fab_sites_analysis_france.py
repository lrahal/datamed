#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db
from create_database.create_tables_in_db import get_excels_df


# # Récupération des données avec géoloc

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


#df_prod = pd.read_sql_table('production', connection)
#df_api = pd.read_sql_table('substance_active', connection)
df_fab = pd.read_sql_table('fabrication', connection)


# In[4]:


df = get_excels_df()
df = df.merge(df_fab, how='left', left_on='sites_fabrication_substance_active', right_on='address')
df = df.drop(['denomination_specialite', 'dci', 'type_amm', 'titulaire_amm', 'sites_production',
              'sites_conditionnement_primaire', 'sites_conditionnement_secondaire', 'sites_importation',
              'sites_controle', 'sites_echantillotheque', 'sites_certification', 'substance_active',
              'sites_fabrication_substance_active', 'mitm', 'pgp', 'filename', 'cos_sim', 'id'], axis=1)
df = df.rename(columns={'substance_active_match': 'substance_active'})
df = df.dropna(how='all')
df = df.drop_duplicates()


# In[5]:


#df = df_prod.merge(df_api, how='left', left_on='substance_active_id', right_on='id')
#df = df.merge(df_fab, how='left', left_on='fabrication_id', right_on='id')
#df = df.drop(['id_x', 'id_y', 'id'], axis=1)


# In[6]:


len(df), len(df.cis.unique())


# In[7]:


# df[df.duplicated(subset=None, keep='first')]


# In[8]:


df.head(2)


# In[9]:


# Keep rows having the right format (8 digits) (88% of all rows)
df = df[~df.country.isna()]
len(df)


# In[10]:


# Liste des pays listés dans le dataset
countries = sorted(df.country.unique())


# In[11]:


# Listes de pays pour chaque catégorie
france_countries = ['France', 'French Guiana', 'Martinique', 'Réunion'] 
europe_countries = ['Germany', 'Belgium', 'Austria', 'Bulgaria', 'Croatia', 'Denmark', 'Spain', 'Estonia',
                    'Finland', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                    'Malta', 'Netherlands', 'Poland', 'Portugal', 'Czechia', 'Romania', 'Slovakia', 'Slovenia',
                    'Sweden'] + france_countries
mutual_rec_countries = europe_countries + ['Australia', 'Canada', 'Israel', 'Japan',
                                           'New Zealand', 'Switzerland', 'United States']
china_countries = ['China']
india_countries = ['India']

union_list = list(set(europe_countries) | set(mutual_rec_countries) | set(china_countries) | set(india_countries))

third_countries = [c for c in countries if c not in union_list]


# In[12]:


len(df[df.country == 'China']) / len(df) * 100


# In[13]:


len(df[df.country == 'India']) / len(df) * 100


# In[14]:


df['france'] = df.country.isin(france_countries)
df['europe'] = df.country.isin(europe_countries)
df['mutual_rec'] = df.country.isin(mutual_rec_countries)

df['china'] = df.country.isin(china_countries)
df['india'] = df.country.isin(india_countries)

df['third'] = df.country.isin(third_countries)


# In[15]:


df[df.country == 'Martinique'].head(3)


# # Regroupement par code CIS

# On représente les données par code CIS et non plus par substance active

# In[16]:


df2 = pd.DataFrame(df.cis.dropna().unique(), columns=['cis'])
df2 = df2.dropna()


# In[17]:


df2['france'] = df2.apply(lambda x: True in df[df.cis == x.cis].france.to_list(), axis=1)
df2['europe'] = df2.apply(lambda x: True in df[df.cis == x.cis].europe.to_list(), axis=1)
df2['mutual_rec'] = df2.apply(lambda x: True in df[df.cis == x.cis].mutual_rec.to_list(), axis=1)
df2['china'] = df2.apply(lambda x: True in df[df.cis == x.cis].china.to_list(), axis=1)
df2['india'] = df2.apply(lambda x: True in df[df.cis == x.cis].india.to_list(), axis=1)
df2['third'] = df2.apply(lambda x: True in df[df.cis == x.cis].third.to_list(), axis=1)


# In[18]:


df2[(df2.europe == True) & (df2.china == True)].head()


# In[19]:


df2['france_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].france.to_list()), axis=1)
df2['europe_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].europe.to_list()), axis=1)
df2['mutual_rec_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].mutual_rec.to_list()), axis=1)
df2['china_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].china.to_list()), axis=1)
df2['india_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].india.to_list()), axis=1)
df2['third_only'] = df2.apply(lambda x: not (False in df[df.cis == x.cis].third.to_list()), axis=1)


# In[20]:


df2['nothing_in_france'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].france.to_list()), axis=1)
df2['nothing_in_europe'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].europe.to_list()), axis=1)
df2['nothing_in_mutual_rec'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].mutual_rec.to_list()), axis=1)
df2['nothing_in_china'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].china.to_list()), axis=1)
df2['nothing_in_india'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].india.to_list()), axis=1)
df2['nothing_in_third'] = df2.apply(lambda x: not (True in df[df.cis == x.cis].third.to_list()), axis=1)


# In[21]:


df2[df2.france_only].head()


# In[22]:


#df[~df.cis.apply(lambda x: x.isdigit() if isinstance(x, str) else False)].cis.unique()


# ## Calcul des stats

# In[23]:


def get_stat(label, df):
    print(label + ': ' + str(len(df[df[label]])) + ' (' + str(len(df[df[label]]) / len(df) * 100) + '%)')


# In[24]:


get_stat('france_only', df2)
get_stat('europe_only', df2)
get_stat('mutual_rec_only', df2)
get_stat('china_only', df2)
get_stat('india_only', df2)
get_stat('third_only', df2)

get_stat('nothing_in_france', df2)
get_stat('nothing_in_europe', df2)
get_stat('nothing_in_mutual_rec', df2)
get_stat('nothing_in_china', df2)
get_stat('nothing_in_india', df2)
get_stat('nothing_in_third', df2)


# In[25]:


df2[df2.france_only].head()


# In[26]:


# Vérification rapide que les calculs concordent
len(df2[df2.france_only]) + len(df2[df2.nothing_in_france]) + len(df2[(df2.france) & (~df2.france_only)]) == len(df2)


# In[27]:


only_dict = {
    'France only': len(df2[df2.france_only]),
    'Europe only': len(df2[df2.europe_only]),
    'Mutual Rec only': len(df2[df2.mutual_rec_only]),
    'China only': len(df2[df2.china_only]),
    'India only': len(df2[df2.india_only]),
    'Third only': len(df2[df2.third_only]),
}


# In[28]:


fig, ax = plt.subplots(figsize=(12, 6))
plot1 = ax.bar(range(len(only_dict)), list(only_dict.values()), align='center')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(plot1)

plt.xticks(range(len(only_dict)), list(only_dict.keys()))
None


# In[29]:


nothing_dict = {
    'nothing in France': len(df2[df2.nothing_in_france]),
    'nothing in Europe': len(df2[df2.nothing_in_europe]),
    'nothing in Mutual Rec': len(df2[df2.nothing_in_mutual_rec]),
    'nothing in China': len(df2[df2.nothing_in_china]),
    'nothing in India': len(df2[df2.nothing_in_india]),
    'nothing in Third': len(df2[df2.nothing_in_third]),
}


# In[30]:


fig, ax = plt.subplots(figsize=(12, 6))
plot2 = ax.bar(range(len(nothing_dict)), list(nothing_dict.values()), align='center')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(plot2)

plt.xticks(range(len(nothing_dict)), list(nothing_dict.keys()))
None


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[31]:


def get_category(x):
    if x.france_only:
        return 'France only'
    if x.europe_only:
        return 'Europe only'
    if x.mutual_rec_only:
        return 'Mutual Rec only'
    if x.third_only:
        return 'Third only'
    if x.china_only:
        return 'China only'
    if x.india_only:
        return 'India only'


# In[32]:


x = df2.iloc[217]


# In[33]:


cols = [c for c in df2.columns if c != 'cis']


# In[34]:


def get_col_true(x, cols):
    col_str = ''
    for col in cols:
        if x[col]:
            col_str = str(col) + ', ' + col_str
    col_str = col_str[:-2]
    col_str = col_str.replace('_', ' ')
    return col_str


# In[35]:


df2['category'] = df2.apply(lambda x: get_category(x), axis=1)
df2['category'] = df2.apply(lambda x: get_col_true(x, cols) if not x.category else x.category, axis=1)


# In[36]:


df2.head(3)


# In[37]:


sns.set_style("white")
sns.set_style("ticks")

plt.figure(figsize=(16, 6))
ax = sns.countplot(x='category',
                   data=df2,
                   order = df2.category.value_counts().index,
                   facecolor=(0, 0, 0, 0),
                   linewidth=5,
                   edgecolor=sns.color_palette('dark', 3))

for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2.,
            height + 50,
            '{:1.2f}'.format(height/(len(df2)) * 100),
            ha='center') 

ax.set_xticklabels(ax.get_xticklabels(), rotation=45,  horizontalalignment='right')
None


# In[ ]:





# In[ ]:




