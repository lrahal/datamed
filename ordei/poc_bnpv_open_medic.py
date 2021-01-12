import pandas as pd

# 2. IMPORT DES DONNEES ET PREPARATION ----
# 2.1 Import
bnpv_open_medic1418_prod_codex = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv', encoding='ISO-8859-1', sep=';')
bnpv_open_medic1418_sa_codex = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv', encoding='ISO-8859-1', sep=';')
corresp_spe_prod_subs = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_soclong_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_soclong_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_hlt_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_hlt_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_notif_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_notif_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')

# 2.2 Préparation
# corresp prod_subs
corresp_prod_subs = corresp_spe_prod_subs.drop_duplicates(subset=['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE'])
corresp_prod_subs = corresp_prod_subs[['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE']].sort_values(by=['PRODUIT_CODEX'])
corresp_prod_subs = corresp_prod_subs.dropna()
#corresp_prod_subs <- corresp_spe_prod_subs %>%
#  group_by(PRODUIT_CODEX, SUBSTANCE_CODEX_UNIQUE) %>%
#  summarise(n_prod_subs=n()) %>%
#  select(-n_prod_subs)

#corresp_prod_subs<-na.omit(corresp_prod_subs) # 2 pdts sans substance

# Liste ? produits/substances ? afficher
list_prod = pd.DataFrame(bnpv_open_medic1418_prod_codex.PRODUIT_CODEX.unique(), columns=['MEDICAMENT'])
list_prod['TYP_MEDICAMENT'] = 'Produit'
#list_prod <- as.data.frame(as.character(unique(bnpv_open_medic1418_prod_codex$PRODUIT_CODEX)))
#list_prod$TYP_MEDICAMENT <- 'Produit'
#names(list_prod)[1] <- 'MEDICAMENT'
#list_prod$MEDICAMENT<-as.character(list_prod$MEDICAMENT)

list_sa = pd.DataFrame(bnpv_open_medic1418_sa_codex.SUBSTANCE_CODEX_UNIQUE.unique(), columns=['MEDICAMENT'])
list_sa['TYP_MEDICAMENT'] = 'Substance'
#list_sa <- as.data.frame(as.character(unique(bnpv_open_medic1418_sa_codex$SUBSTANCE_CODEX_UNIQUE)))
#list_sa$TYP_MEDICAMENT <- 'Substance'
#names(list_sa)[1] <- 'MEDICAMENT'
#list_sa$MEDICAMENT<-as.character(list_sa$MEDICAMENT)

frames = [list_prod, list_sa]
list_prod_sa = pd.concat(frames)
list_prod_sa = list_prod_sa.sort_values(by=['MEDICAMENT'])
#list_prod_sa <- rbind(list_prod,list_sa)
#list_prod_sa <- list_prod_sa[order(list_prod_sa$MEDICAMENT),]


# 4.1 Définion paramètres choix utilisateur
med < - input$select_med
typ_med = list_prod_sa[list_prod_sa.MEDICAMENT == med].TYP_MEDICAMENT.values[0]
#typ_med < - list_prod_sa$TYP_MEDICAMENT[list_prod_sa$MEDICAMENT == med]
strat < - input$select_strat

# 4.2 Sélection des données en fonction des paramètres utilisateur (Produit/Substance)
if typ_med == 'Substance':
  data = bnpv_open_medic1418_sa_codex[bnpv_open_medic1418_sa_codex.SUBSTANCE_CODEX_UNIQUE == med]
  data_soclong = bnpv_eff_soclong_sa_codex_open[bnpv_eff_soclong_sa_codex_open.SUBSTANCE_CODEX_UNIQUE == med]
  data_notif = bnpv_notif_sa_codex_open[bnpv_notif_sa_codex_open.SUBSTANCE_CODEX_UNIQUE == med]
  data_soclong = data_soclong.rename(columns={'SUBSTANCE_CODEX_UNIQUE': 'MEDICAMENT'})
  data_notif = data_notif.rename(columns={'SUBSTANCE_CODEX_UNIQUE': 'MEDICAMENT'})
else:
  data = bnpv_open_medic1418_prod_codex[bnpv_open_medic1418_prod_codex.PRODUIT_CODEX == med]
  data_soclong = bnpv_eff_soclong_prod_codex_open[bnpv_eff_soclong_prod_codex_open.PRODUIT_CODEX == med]
  data_notif = bnpv_notif_prod_codex_open[bnpv_notif_prod_codex_open.PRODUIT_CODEX == med]
  data_soclong = data_soclong.rename(columns={'PRODUIT_CODEX': 'MEDICAMENT'})
  data_notif = data_notif.rename(columns={'PRODUIT_CODEX': 'MEDICAMENT'})
#if (typ_med == "Substance"){
#data < - bnpv_open_medic1418_sa_codex[bnpv_open_medic1418_sa_codex$SUBSTANCE_CODEX_UNIQUE == med, ]
#data_soclong < - bnpv_eff_soclong_sa_codex_open[bnpv_eff_soclong_sa_codex_open$SUBSTANCE_CODEX_UNIQUE == med, ]
#data_notif < - bnpv_notif_sa_codex_open[bnpv_notif_sa_codex_open$SUBSTANCE_CODEX_UNIQUE == med, ]
#} else {
#data < - bnpv_open_medic1418_prod_codex[bnpv_open_medic1418_prod_codex$PRODUIT_CODEX == med, ]
#data_soclong < - bnpv_eff_soclong_prod_codex_open[bnpv_eff_soclong_prod_codex_open$PRODUIT_CODEX == med, ]
#data_notif < - bnpv_notif_prod_codex_open[bnpv_notif_prod_codex_open$PRODUIT_CODEX == med, ]
#}

# 4.3 Sélection des données en fonction des paramètres utilisateur (Filtres population)
#names(data_soclong)[2] < - "MEDICAMENT"
#names(data_notif)[3] < - "MEDICAMENT"

# Un dict pour la dataframe data
strat_data_dict = {
  'Hommes': {'value': 'Hommes', 'field': 'SEXE'},
  'Femmes': {'value': 'Femmes', 'field': 'SEXE'},
  'Enfants (0-19 ans)': {'value': '0-19 ans', 'field': 'AGE'},
  'Adultes (20-59 ans)': {'value': '20-59 ans', 'field': 'AGE'},
  'Séniors (60 ans et plus)': {'value': '60 ans et plus', 'field': 'AGE'},
}

# Un dict pour les dataframes data_soclong et data_notif
strat_dict = {
  'Hommes': {'value': 'M', 'field': 'SEXE'},
  'Femmes': {'value': 'F', 'field': 'SEXE'},
  'Enfants (0-19 ans)': {'value': 0, 'field': 'AGE'},
  'Adultes (20-59 ans)': {'value': 20, 'field': 'AGE'},
  'Séniors (60 ans et plus)': {'value': 60, 'field': 'AGE'},
}

data = data[data[strat_data_dict[strat]['field']] == strat_data_dict[strat]['value']]
data_soclong = data_soclong[data_soclong[strat_dict[strat]['field']] == strat_dict[strat]['value']]
data_notif = data_notif[data_notif[strat_dict[strat]['field']] == strat_dict[strat]['value']]
#if (strat == "Ensemble") {
#data < - data
#data_soclong < - data_soclong
#data_notif < - data_notif
#} else if (strat == "Hommes") {
#data < - data[data$SEXE == "Hommes", ]
#data_soclong < - data_soclong[data_soclong$SEXE == "M", ]
#data_notif < - data_notif[data_notif$SEXE == "M", ]
#} else if (strat == "Femmes") {
#data < - data[data$SEXE == "Femmes", ]
#data_soclong < - data_soclong[data_soclong$SEXE == "F", ]
#data_notif < - data_notif[data_notif$SEXE == "F", ]
#} else if (strat == "Enfants (0-19 ans)") {
#data < - data[data$AGE == "0-19 ans", ]
#data_soclong < - data_soclong[data_soclong$AGE == 0, ]
#data_notif < - data_notif[data_notif$AGE == 0, ]
#} else if (strat == "Adultes (20-59 ans)") {
#data < - data[data$AGE == "20-59 ans", ]
#data_soclong < - data_soclong[data_soclong$AGE == 20, ]
#data_notif < - data_notif[data_notif$AGE == 20, ]
#data_hlt < - data_hlt[data_hlt$AGE == 20, ]
#} else if (strat == "S?niors (60 ans et plus)") {
#data < - data[data$AGE == "60 ans et plus", ]
#data_soclong < - data_soclong[data_soclong$AGE == 60, ]
#data_notif < - data_notif[data_notif$AGE == 60, ]
#}

# Consolidation effets soclong
temp = data_soclong.groupby(['MEDICAMENT', 'SOC_LONG']).agg({'n_decla_eff': 'sum'}).reset_index()
#temp < - data_soclong % > %
#group_by(MEDICAMENT, SOC_LONG) % > %
#summarise(n_decla_eff=sum(n_decla_eff))

temp2 = data_soclong.drop_duplicates(subset=['MEDICAMENT', 'AGE', 'SEXE', 'n_cas']).groupby('MEDICAMENT').agg(
  {'n_cas': 'sum'}).reset_index()
#temp2 < - data_soclong % > %
#distinct(MEDICAMENT, AGE, SEXE, n_cas) % > %
#group_by(MEDICAMENT) % > %
#summarise(n_cas=sum(n_cas))

data_soclong = temp.merge(temp2, on='MEDICAMENT', how='left')
data_soclong['pour_cas_soclong'] = (data_soclong.n_decla_eff / data_soclong.n_cas) * 100
data_soclong = data_soclong[data_soclong.n_decla_eff > 9]
data_soclong = data_soclong.sort_values(by=['pour_cas_soclong'], ascending=False)
#data_soclong < - left_join(temp, temp2, by=c("MEDICAMENT"))
#data_soclong$pour_cas_soclong < - (data_soclong$n_decla_eff / data_soclong$n_cas) * 100
#data_soclong < -data_soclong[data_soclong$n_decla_eff > 9,]
#data_soclong < - data_soclong[order(data_soclong$pour_cas_soclong, decreasing = TRUE), ]


# Consolidation notif
data_notif = data_notif.groupby(['MEDICAMENT', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()
data_notif.TYP_NOTIF = data_notif.n_decla.apply(lambda x: 'Notificateur(s) < 10 cas' if x < 10 else x)
data_notif = data_notif.groupby(['MEDICAMENT', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()
#data_notif < - data_notif % > %
#group_by(MEDICAMENT, TYP_NOTIF) % > %
#summarise(n_decla=sum(n_decla))

# Affichage camemberts âge/sexe des cas/patients
data_sexe = data.groupby('SEXE').agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
#data < - data % > %
#group_by(SEXE) % > %
#summarise(n_cas=sum(n_cas))

#data < - data % > %
#group_by(SEXE) % > %
#summarise(n_conso=sum(n_conso))

data_age = data.groupby('AGE').agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
#data < - data % > %
#group_by(AGE) % > %
#summarise(n_cas=sum(n_cas))

#data < - data % > %
#group_by(AGE) % > %
#summarise(n_conso=sum(n_conso))

# Histogramme cas/patients par année
data_annee = data.groupby('ANNEE').agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
#data_annee < - data % > %
#group_by(ANNEE) % > %
#summarise(n_cas=sum(n_cas), n_conso=sum(n_conso))


# 4.4 Affichage fenêtre avec détail HLT par SOC_LONG
# Paramètres (mêmes que précédemment -> mais à redefinir pour l'observeEvent)
med < - input$select_med
typ_med = list_prod_sa[list_prod_sa.MEDICAMENT == med].TYP_MEDICAMENT.values[0]
#typ_med < - list_prod_sa$TYP_MEDICAMENT[list_prod_sa$MEDICAMENT == med]
strat < - input$select_strat

# Données HLT
if typ_med == 'Substance':
  data_hlt = bnpv_eff_hlt_sa_codex_open[bnpv_eff_hlt_sa_codex_open.SUBSTANCE_CODEX_UNIQUE == med]
  data_hlt = data_hlt.rename(columns={'SUBSTANCE_CODEX_UNIQUE': 'MEDICAMENT'})
else:
  data_hlt = bnpv_eff_hlt_prod_codex_open[bnpv_eff_hlt_prod_codex_open.PRODUIT_CODEX == med]
  data_hlt = data_hlt.rename(columns={'PRODUIT_CODEX': 'MEDICAMENT'})
#if (typ_med == "Substance"){
#data_hlt < - bnpv_eff_hlt_sa_codex_open[bnpv_eff_hlt_sa_codex_open$SUBSTANCE_CODEX_UNIQUE == med, ]
#} else {
#data_hlt < - bnpv_eff_hlt_prod_codex_open[bnpv_eff_hlt_prod_codex_open$PRODUIT_CODEX == med, ]
#}

#names(data_hlt)[2] < - "MEDICAMENT"

data_hlt = data_hlt[data_hlt[strat_dict[strat]['field']] == strat_dict[strat_dict[strat]['value']]]
#if (strat == "Ensemble") {
#data_hlt < - data_hlt
#} else if (strat == "Hommes") {
#data_hlt < - data_hlt[data_hlt$SEXE == "M", ]
#} else if (strat == "Femmes") {
#data_hlt < - data_hlt[data_hlt$SEXE == "F", ]
#} else if (strat == "Enfants (0-19 ans)") {
#data_hlt < - data_hlt[data_hlt$AGE == 0, ]
#} else if (strat == "Adultes (20-59 ans)") {
#data_hlt < - data_hlt[data_hlt$AGE == 20, ]
#} else if (strat == "S?niors (60 ans et plus)") {
#data_hlt < - data_hlt[data_hlt$AGE == 60, ]
#}

# Consolidation effets hlt
data_hlt = data_hlt.groupby(['MEDICAMENT', 'EFFET_HLT', 'SOC_LONG']).agg({'n_decla_eff_hlt': 'sum'}).reset_index()

#data_hlt < - data_hlt % > %
#group_by(MEDICAMENT, EFFET_HLT, SOC_LONG) % > %
#summarise(n_decla_eff_hlt=sum(n_decla_eff_hlt))

# Sélection des données pour le SOC_LONG sur lequel l'utilisateur a cliqué
data_soclong_select = data_hlt[data_hlt.SOC_LONG == soc_long_select.y]
#data_soclong_select < - data_hlt[as.character(data_hlt$SOC_LONG) == soc_long_select$y,]

# Stockage de la sortie (liste des HLT correspondants au SOC_LONG) dans une même chaîne
effets_hlt = data_soclong_select.iloc[0].EFFET_HLT
for i in range(1, len(data_soclong_select)):
    effets_hlt = '{}\n'.format(effets_hlt) + data_soclong_select.iloc[i].EFFET_HLT

#for (i in 1 : nrow(data_soclong_select)) {
#if (i == 1){
#effets_hlt < - data_soclong_select$EFFET_HLT[i]
#} else {
#effets_hlt < - paste(effets_hlt, data_soclong_select$EFFET_HLT[i], sep = "<br>")
#}
#}


# Générer données json

corresp_prod_subs = corresp_spe_prod_subs.drop_duplicates(subset=['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE'])
corresp_prod_subs = corresp_prod_subs[['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE']].sort_values(by=['PRODUIT_CODEX'])
corresp_prod_subs = corresp_prod_subs.dropna()

list_prod = pd.DataFrame(bnpv_open_medic1418_prod_codex.PRODUIT_CODEX.unique(), columns=['MEDICAMENT'])
list_prod['TYP_MEDICAMENT'] = 'Produit'

list_sa = pd.DataFrame(bnpv_open_medic1418_sa_codex.SUBSTANCE_CODEX_UNIQUE.unique(), columns=['MEDICAMENT'])
list_sa['TYP_MEDICAMENT'] = 'Substance'

frames = [list_prod, list_sa]
list_prod_sa = pd.concat(frames)
list_prod_sa = list_prod_sa.sort_values(by=['MEDICAMENT'])

# Un dict pour la dataframe data
strat_data_dict = {
  'Hommes': {'value': 'Hommes', 'field': 'SEXE'},
  'Femmes': {'value': 'Femmes', 'field': 'SEXE'},
  'Enfants (0-19 ans)': {'value': '0-19 ans', 'field': 'AGE'},
  'Adultes (20-59 ans)': {'value': '20-59 ans', 'field': 'AGE'},
  'Séniors (60 ans et plus)': {'value': '60 ans et plus', 'field': 'AGE'},
}

# Un dict pour les dataframes data_soclong et data_notif
strat_dict = {
  'Hommes': {'value': 'M', 'field': 'SEXE'},
  'Femmes': {'value': 'F', 'field': 'SEXE'},
  'Enfants (0-19 ans)': {'value': 0, 'field': 'AGE'},
  'Adultes (20-59 ans)': {'value': 20, 'field': 'AGE'},
  'Séniors (60 ans et plus)': {'value': 60, 'field': 'AGE'},
}

typ_med_dict = {'Substance': 'SUBSTANCE_CODEX_UNIQUE', 'Produit': 'PRODUIT_CODEX'}

# typ_med = 'Substance'
typ_med = 'Substance'
data = bnpv_open_medic1418_sa_codex
data_soclong = bnpv_eff_soclong_sa_codex_open
data_notif = bnpv_notif_sa_codex_open
data_hlt = bnpv_eff_hlt_sa_codex_open

data['strat'] = ''
data_soclong['strat'] = ''
data_notif['strat'] = ''
data_hlt['strat'] = ''

data = data.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
data_soclong = data_soclong.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
data_notif = data_notif.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
data_hlt = data_hlt.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})

data_sexe = data.groupby(['MEDICAMENT', 'SEXE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
data_age = data.groupby(['MEDICAMENT', 'AGE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
data_annee = data.groupby(['MEDICAMENT', 'ANNEE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()

frames_data = []
frames_data_soclong = []
frames_data_notif = []
frames_data_hlt = []

for strat in strat_data_dict.keys():
  data_tmp = data[data[strat_data_dict[strat]['field']] == strat_data_dict[strat]['value']]
  data_soclong_tmp = data_soclong[data_soclong[strat_dict[strat]['field']] == strat_dict[strat]['value']]
  data_notif_tmp = data_notif[data_notif[strat_dict[strat]['field']] == strat_dict[strat]['value']]
  data_hlt_tmp = data_hlt[data_hlt[strat_dict[strat]['field']] == strat_dict[strat]['value']]

  temp = data_soclong_tmp.groupby(['MEDICAMENT', 'AGE', 'SEXE', 'SOC_LONG']).agg({'n_decla_eff': 'sum'}).reset_index()
  temp2 = data_soclong_tmp.drop_duplicates(subset=['MEDICAMENT', 'AGE', 'SEXE', 'n_cas']).groupby('MEDICAMENT').agg(
    {'n_cas': 'sum'}).reset_index()

  data_soclong_tmp = temp.merge(temp2, on='MEDICAMENT', how='left')
  data_soclong_tmp['pour_cas_soclong'] = (data_soclong_tmp.n_decla_eff / data_soclong_tmp.n_cas) * 100
  data_soclong_tmp = data_soclong_tmp[data_soclong_tmp.n_decla_eff > 9]
  data_soclong_tmp = data_soclong_tmp.sort_values(by=['pour_cas_soclong'], ascending=False)

  data_notif_tmp = data_notif_tmp.groupby(['MEDICAMENT', 'AGE', 'SEXE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()
  data_notif_tmp.TYP_NOTIF = data_notif_tmp.n_decla.apply(lambda x: 'Notificateur(s) < 10 cas' if x < 10 else x)
  data_notif_tmp = data_notif_tmp.groupby(['MEDICAMENT', 'AGE', 'SEXE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()

  data_hlt_tmp = data_hlt_tmp.groupby(
    ['MEDICAMENT', 'AGE', 'SEXE', 'EFFET_HLT', 'SOC_LONG']).agg({'n_decla_eff_hlt': 'sum'}).reset_index()

  frames_data.append(data_tmp)
  frames_data_soclong.append(data_soclong_tmp)
  frames_data_notif.append(data_notif_tmp)
  frames_data_hlt.append(data_hlt_tmp)


data_final = pd.concat(frames_data)
data_soclong_final = pd.concat(frames_data_soclong)
data_notif_final = pd.concat(frames_data_notif)
data_hlt_final = pd.concat(frames_data_hlt)

data_final.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data.json', orient='records')
data_final.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_soclong.json', orient='records')
data_final.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_notif.json', orient='records')
data_final.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_hlt.json', orient='records')
data_age.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_age.json', orient='records')
data_sexe.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_sexe.json', orient='records')
data_annee.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/sa_data_annee.json', orient='records')