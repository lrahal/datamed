#!/usr/bin/env python
# coding: utf-8

# # Analyses sur la table des ruptures de stock

# ### Pour les analyses thématiques du dashboard - 7 Janvier 2021

# In[1]:


import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from create_database.models import connect_db

pd.set_option('display.max_rows', None)


# # Importer la table des ruptures

# In[2]:


engine = connect_db()  # establish connection
connection = engine.connect()


# In[3]:


df = pd.read_sql_table('ruptures', connection)
df = df[['id_signal', 'date_signalement', 'laboratoire', 'specialite', 'voie', 'voie_4_classes', 'atc',
         'date_signal_debut_rs', 'duree_ville', 'duree_hopital', 'date_previ_ville', 'date_previ_hopital']]

df = df[df.date_signalement.notna()]

df.atc = df.atc.str.upper()
df.specialite = df.apply(
    lambda x: x.specialite.replace(' /', '/').replace('/ ', '/').replace('intraoculaire', 'intra-oculaire'),
    axis=1)

# Récupérer l'année du signalement
df['annee'] = df.date_signalement.apply(lambda x: x.year)

df.head(2)


# # Evolution du nombre de ruptures au cours des années

# In[4]:


fig_dims = (10, 6)
fig, ax = plt.subplots(figsize=fig_dims)
sns.countplot(x='annee', data=df, ax=ax)
plt.title('Nombre de signalements de ruptures par an')
plt.xlabel('Année')
plt.ylabel('Nombre de signalements')
plt.show()


# In[5]:


len(df[df.date_signalement.apply(lambda x: x.year == 2017)])


# # Classe ATC ayant le plus de ruptures

# In[6]:


df_atc = df.groupby('atc').count().reset_index()
df_atc.head()


# ## ATC ayant eu plus de 20 signalements depuis 2014

# In[7]:


atc_list = df_atc[df_atc.id_signal > 20].atc.unique().tolist()   #.sort_values(by=['id_signal'], ascending=False)


# In[8]:


fig_dims = (20, 6)
fig, ax = plt.subplots(figsize=fig_dims)
sns.countplot(x='atc', data=df[df.atc.isin(atc_list)], ax=ax, order=df[df.atc.isin(atc_list)].atc.value_counts().sort_values().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.title('Nombre de signalements de ruptures par classe ATC depuis 2014')
plt.xlabel('Classe ATC')
plt.ylabel('Nombre de signalements')
plt.show()


# ## Top 10 des ATC ayant le plus de signalements, par année, depuis 2014

# In[9]:


fig_dims = (35, 30)
fig, ax = plt.subplots(3, 3, figsize=fig_dims)

for idx, a in enumerate([2014, 2015, 2016]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc', data=df_annee,
                  order=df_annee.atc.value_counts()[:10].sort_values().index,
                  ax=ax[0][idx])
    ax[0][idx].set_xticklabels(ax[0][idx].get_xticklabels(), rotation=60)
    ax[0][idx].title.set_text(str(a))
    ax[0][idx].set_xlabel('Classe ATC')
    ax[0][idx].set_ylabel('Nombre de signalements')
for idx, a in enumerate([2017, 2018, 2019]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc', data=df_annee,
                  order=df_annee.atc.value_counts()[:10].sort_values().index,
                  ax=ax[1][idx])
    ax[1][idx].set_xticklabels(ax[1][idx].get_xticklabels(), rotation=60)
    ax[1][idx].title.set_text(str(a))
    ax[1][idx].set_xlabel('Classe ATC')
    ax[1][idx].set_ylabel('Nombre de signalements')
df_annee = df[df.annee == 2020]
sns.countplot(x='atc', data=df_annee,
              order=df_annee.atc.value_counts()[:10].sort_values().index,
              ax=ax[2][0])
ax[2][0].set_xticklabels(ax[2][0].get_xticklabels(), rotation=60)
ax[2][0].title.set_text('2020')
ax[2][0].set_xlabel('Classe ATC')
ax[2][0].set_ylabel('Nombre de signalements')

plt.show()


# ## Par grande classe ATC

# In[10]:


df['atc_1'] = df.atc.apply(lambda x: x[:1] if x else None)
df['atc_2'] = df.atc.apply(lambda x: x[:3] if x else None)


# In[11]:


fig_dims = (35, 30)
fig, ax = plt.subplots(3, 3, figsize=fig_dims)

for idx, a in enumerate([2014, 2015, 2016]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc_1', data=df_annee,
                  order=df_annee.atc_1.value_counts()[:10].sort_values().index,
                  ax=ax[0][idx])
    ax[0][idx].set_xticklabels(ax[0][idx].get_xticklabels())
    ax[0][idx].title.set_text(str(a))
    ax[0][idx].set_xlabel('Classe ATC')
    ax[0][idx].set_ylabel('Nombre de signalements')
for idx, a in enumerate([2017, 2018, 2019]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc_1', data=df_annee,
                  order=df_annee.atc_1.value_counts()[:10].sort_values().index,
                  ax=ax[1][idx])
    ax[1][idx].set_xticklabels(ax[1][idx].get_xticklabels())
    ax[1][idx].title.set_text(str(a))
    ax[1][idx].set_xlabel('Classe ATC')
    ax[1][idx].set_ylabel('Nombre de signalements')
df_annee = df[df.annee == 2020]
sns.countplot(x='atc_1', data=df_annee,
              order=df_annee.atc_1.value_counts()[:10].sort_values().index,
              ax=ax[2][0])
ax[2][0].set_xticklabels(ax[2][0].get_xticklabels())
ax[2][0].title.set_text('2020')
ax[2][0].set_xlabel('Classe ATC')
ax[2][0].set_ylabel('Nombre de signalements')

plt.show()


# In[12]:


fig_dims = (35, 30)
fig, ax = plt.subplots(3, 3, figsize=fig_dims)

for idx, a in enumerate([2014, 2015, 2016]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc_2', data=df_annee,
                  order=df_annee.atc_2.value_counts()[:10].sort_values().index,
                  ax=ax[0][idx])
    ax[0][idx].set_xticklabels(ax[0][idx].get_xticklabels())
    ax[0][idx].title.set_text(str(a))
    ax[0][idx].set_xlabel('Classe ATC')
    ax[0][idx].set_ylabel('Nombre de signalements')
for idx, a in enumerate([2017, 2018, 2019]):
    df_annee = df[df.annee == a]
    sns.countplot(x='atc_2', data=df_annee,
                  order=df_annee.atc_2.value_counts()[:10].sort_values().index,
                  ax=ax[1][idx])
    ax[1][idx].set_xticklabels(ax[1][idx].get_xticklabels())
    ax[1][idx].title.set_text(str(a))
    ax[1][idx].set_xlabel('Classe ATC')
    ax[1][idx].set_ylabel('Nombre de signalements')
df_annee = df[df.annee == 2020]
sns.countplot(x='atc_2', data=df_annee,
              order=df_annee.atc_2.value_counts()[:10].sort_values().index,
              ax=ax[2][0])
ax[2][0].set_xticklabels(ax[2][0].get_xticklabels())
ax[2][0].title.set_text('2020')
ax[2][0].set_xlabel('Classe ATC')
ax[2][0].set_ylabel('Nombre de signalements')

plt.show()


# ## Evolution des signalements au cours du temps

# In[34]:


atc_list = []
for a in [2014, 2015, 2016, 2017, 2018, 2019, 2020]:
    df_annee = df[df.annee == a]
    atc_list.extend(df_annee.atc_2.value_counts()[:3].keys())
    
atc_list = list(set(atc_list))


# In[35]:


df_atc = df[(df.atc_2.isin(atc_list)) & (df.annee >= 2014)]


# In[36]:


data_viz = df_atc.groupby(['annee', 'atc_2'], as_index=False).count()


# In[37]:


data_viz.annee.unique()


# In[38]:


data_viz.head()


# In[39]:


fig_dims = (30, 10)
fig, ax = plt.subplots(figsize=fig_dims)
sns.lineplot(data=data_viz, x='annee', y='id_signal', hue='atc_2', linewidth=3)
#sns.scatterplot(data=data_viz, x='annee', y='id_signal', hue='atc_2', s=300)

ax.set_title('Évolution des signalements au cours du temps, pour les classes les plus signalées sur la période 2014 - 2020', fontsize=20)
ax.set_xlabel('Année', fontsize=18)
ax.set_ylabel('Nombre de signalements', fontsize=18)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# # Signalements anti-cancérieux (L) en 2019

# ## En réponse à l'article https://www.ligue-cancer.net/article/59750_penurie-de-medicaments

# In[19]:


# Nombre de signalements
len(df[df.apply(lambda x: x.date_signalement.year == 2019 and x.atc.startswith('L') if x.atc else False, axis=1)])


# In[20]:


# Nombre de spécialités concernées
len(df[
    df.apply(lambda x: x.date_signalement.year == 2019 and x.atc.startswith('L') if x.atc else False, axis=1)
].specialite.unique())


# # Nombre de signalements pour un médicament

# In[21]:


df[df.date_signalement >= '2019'].specialite.value_counts()


# In[22]:


nom_spe = 'paclitaxel ebewe 6 mg/ml, solution à diluer pour perfusion'
annee_start = 2019
annee_end = 2020

nb_sig = len(df[(df.specialite == nom_spe) 
                & (df.date_signalement >= str(annee_start)) 
                & (df.date_signalement < str(annee_end + 1))])


# In[23]:


print('Le nombre de signalements pour le {} sur la période {} - {} est : {}'.format(
    nom_spe, annee_start, annee_end, nb_sig
))


# In[ ]:




