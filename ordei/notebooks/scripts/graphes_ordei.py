#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import zipfile

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.append('/Users/ansm/Documents/GitHub/datamed')

from ordei.get_ordei_data import *

pd.set_option('display.max_rows', None)


# In[2]:


#with open('../data/med_dict.json.zip') as jsonfile:
#    med_dict = json.load(jsonfile.decode("utf-8"))


# In[2]:


with zipfile.ZipFile('../data/med_dict.json.zip', "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        med_dict = json.loads(data.decode("utf-8"))


# In[3]:


PROD_SUBS = pd.read_csv("../data/liste_produits_substances.csv", sep=';').to_dict(orient='records')
type_med_dict = {d['medicament']: d['typ_medicament'] for d in PROD_SUBS}


# In[4]:


med = "CLARADOL"


# In[5]:


ordei_colors = ['#DFD4E5', '#BFAACB', '#5E2A7E']


# # Indicateurs

# In[7]:


df_annee = pd.DataFrame(med_dict[med]["annee"])


# In[8]:


df_annee.n_conso.mean()


# In[9]:


df_annee.n_cas.sum() * 100000 / df_annee.n_conso.sum()


# In[10]:


df_annee.n_cas.sum()


# In[11]:


df_annee.head()


# # Camembert

# ## Sexe

# In[12]:


df_sexe = pd.DataFrame(med_dict[med]["sexe"])
df_sexe.head()


# In[13]:


fig_sexe = go.Pie(labels=df_sexe.sexe, values=df_sexe.n_cas,
                  name='Répartition par sexe des patients traités',
                  marker_colors=ordei_colors)
fig_sexe = go.Figure(fig_sexe)
fig_sexe.show()


# In[14]:


fig_sexe = go.Pie(labels=df_sexe.sexe, values=df_sexe.n_conso,
                  name='Répartition par sexe des patients traités',
                  marker_colors=ordei_colors)
fig_sexe = go.Figure(fig_sexe)
fig_sexe.show()


# ## âge

# In[15]:


df_age = pd.DataFrame(med_dict[med]["age"])
df_age.head()


# In[16]:


fig_age = go.Pie(labels=df_age.age, values=df_age.n_cas,
             name='Répartition par âge des patients traités',
             marker_colors=ordei_colors)
fig_age = go.Figure(fig_age)
fig_age.show()


# In[17]:


fig_age = go.Pie(labels=df_age.age, values=df_age.n_conso,
             name='Répartition par âge des patients traités',
             marker_colors=ordei_colors)
fig_age = go.Figure(fig_age)
fig_age.show()


# # Sunburst

# In[18]:


dd = defaultdict(dict)
for d in med_dict["DOLIPRANE"]["sexe"]:
    dd[d['sexe']] = {'n_cas': d['n_cas'], 'n_conso': d['n_conso']}


# In[19]:


med_dict["DOLIPRANE"]["sexe"]


# In[20]:


104550066 + 79613426


# In[21]:


fig = go.Figure(go.Sunburst(
    labels=['n_cas', 'n_conso', 'Femmes', 'Hommes', 'Femmes', 'Hommes'],
    parents=['', '', 'n_cas', 'n_cas', 'n_conso', 'n_conso'],
    values=[4654, 184163492, 2848, 104550066, 1806, 79613426],
))
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

fig.show()


# # Courbes

# In[22]:


df_annee = pd.DataFrame(med_dict[med]["annee"])


# In[23]:


df_annee.head()


# In[24]:


df_annee.n_cas.min()


# In[25]:


fig = make_subplots(specs=[[{"secondary_y": True}]])

if df_annee.n_cas.min() >= 10:
    fig.add_trace(go.Scatter(x=df_annee.annee, y=df_annee.n_cas,
                             mode='lines',
                             name='Cas déclarés',
                             line={'shape': 'spline', 'smoothing': 1, 'width': 4, 'color': "#BFAACB"}),
                  secondary_y=False)

fig.add_trace(go.Scatter(x=df_annee.annee, y=df_annee.n_conso,
                         mode='lines',
                         name='Patients traités',
                         line={'shape': 'spline', 'smoothing': 1, 'width': 4, 'color': "#5E2A7E"}),
              secondary_y=True)

fig.update_yaxes(
    title_text="Nombre de cas déclarés", 
    secondary_y=False)
fig.update_yaxes(
    title_text="Nombre de patients traités", 
    secondary_y=True)

fig.update_xaxes(nticks=len(df_annee))
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=True, yaxis2_showgrid=False, plot_bgcolor='rgba(0,0,0,0)')
fig.show()


# # Histogrammes

# In[74]:


med = "DOLIPRANE"


# In[75]:


med_dict[med].keys()


# In[76]:


df_notif = pd.DataFrame(med_dict[med]["notif"])
df_notif.head(3)


# In[77]:


fig = px.bar(df_notif, y='typ_notif', x='n_decla', orientation='h')

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        #showticklabels=False,
        zeroline=False,
    ),
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=120, r=10, t=140, b=80),
    showlegend=False,
)

fig.show()


# In[97]:


fig = go.Figure(
    go.Bar(
        y=df_notif.typ_notif, x=df_notif.n_decla, orientation='h',
        marker=dict(color=['rgba(51,171,102,1)', 'rgba(102,192,140,1)',
                           'rgba(153,213,179,1)', 'rgba(204,234,217,1)',
                           'rgba(191,213,60,1)', 'rgba(207,223,109,1)', 'rgba(207,223,109,1)'])
    )
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        #showticklabels=False,
        zeroline=False,
        autorange='reversed',
        ticks="outside", 
        tickcolor='white',
        ticklen=1
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0),
    barmode='group',
    bargap=0.10,
    bargroupgap=0.0,
    font={'size': 14}
)

fig.show()


# In[ ]:





# In[98]:


df_soc = pd.DataFrame(med_dict[med]["soclong"])
df_soc.head(3)


# In[101]:


df_soc = df_soc.head(10)
fig = go.Figure(
    go.Bar(
        y=df_soc.soc_long, x=df_soc.n_decla_eff, orientation='h',
        marker=dict(color=['rgba(51,171,102,1)', 'rgba(102,192,140,1)',
                           'rgba(153,213,179,1)', 'rgba(204,234,217,1)',
                           'rgba(191,213,60,1)', 'rgba(207,223,109,1)',
                           'rgba(239,244,206,1)', 'rgba(239,244,206,1)',
                           'rgba(51,194,214,1)', 'rgba(102,209,224,1)'])
    )
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        #showticklabels=False,
        zeroline=False,
        autorange='reversed',
        ticks="outside", 
        tickcolor='white',
        ticklen=1
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0),
    barmode='group',
    bargap=0.10,
    bargroupgap=0.0,
    font={'size': 14}
)

fig.show()


# In[ ]:




