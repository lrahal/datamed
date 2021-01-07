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
corresp_prod_subs = corresp_spe_prod_subs.groupby(['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE']).count().reset_index()

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
else:
  data = bnpv_open_medic1418_prod_codex[bnpv_open_medic1418_prod_codex.PRODUIT_CODEX == med]
  data_soclong = bnpv_eff_soclong_prod_codex_open[bnpv_eff_soclong_prod_codex_open.PRODUIT_CODEX == med]
  data_notif = bnpv_notif_prod_codex_open[bnpv_notif_prod_codex_open.PRODUIT_CODEX == med]

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
data_soclong = data_soclong.rename(columns={'SUBSTANCE_CODEX_UNIQUE': 'MEDICAMENT'})
data_notif = data_notif.rename(columns={'SUBSTANCE_CODEX_UNIQUE': 'MEDICAMENT'})

#names(data_soclong)[2] < - "MEDICAMENT"
#names(data_notif)[3] < - "MEDICAMENT"

if strat == 'Hommes':
  data = data[data.SEXE == 'Hommes']
  data_soclong = data_soclong[data_soclong.SEXE == 'M']
  data_notif = data_notif[data_notif.SEXE == 'M']
elif strat == 'Femmes':
  data = data[data.SEXE == 'Femmes']
  data_soclong = data_soclong[data_soclong.SEXE == 'F']
  data_notif = data_notif[data_notif.SEXE == 'F']
elif strat == 'Enfants (0-19 ans)':
  data = data[data.AGE == '0-19 ans']
  data_soclong = data_soclong[data_soclong.AGE == 0]
  data_notif = data_notif[data_notif.AGE == 0]
elif strat == 'Adultes (20-59 ans)':
  data = data[data.AGE == '20-59 ans']
  data_soclong = data_soclong[data_soclong.AGE == 20]
  data_notif = data_notif[data_notif.AGE == 20]
elif strat == 'Séniors (60 ans et plus)':
  data = data[data.AGE == '60 ans et plus']
  data_soclong = data_soclong[data_soclong.AGE == 60]
  data_notif = data_notif[data_notif.AGE == 60]

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

#data_notif < - data_notif % > %
#group_by(MEDICAMENT, TYP_NOTIF) % > %
#summarise(n_decla=sum(n_decla))


# 4.4 Affichage fenêtre avec détail HLT par SOC_LONG
# Paramètres (mêmes que précédemment -> mais à redefinr pour l'observeEvent)
med < - input$select_med
typ_med = list_prod_sa[list_prod_sa.MEDICAMENT == med].TYP_MEDICAMENT.values[0]
#typ_med < - list_prod_sa$TYP_MEDICAMENT[list_prod_sa$MEDICAMENT == med]
strat < - input$select_strat

# Données HLT
if (typ_med == "Substance"){
data_hlt < - bnpv_eff_hlt_sa_codex_open[bnpv_eff_hlt_sa_codex_open$SUBSTANCE_CODEX_UNIQUE == med, ]
} else {
data_hlt < - bnpv_eff_hlt_prod_codex_open[bnpv_eff_hlt_prod_codex_open$PRODUIT_CODEX == med, ]
}

names(data_hlt)[2] < - "MEDICAMENT"

if (strat == "Ensemble") {
data_hlt < - data_hlt
} else if (strat == "Hommes") {
data_hlt < - data_hlt[data_hlt$SEXE == "M", ]
} else if (strat == "Femmes") {
data_hlt < - data_hlt[data_hlt$SEXE == "F", ]
} else if (strat == "Enfants (0-19 ans)") {
data_hlt < - data_hlt[data_hlt$AGE == 0, ]
} else if (strat == "Adultes (20-59 ans)") {
data_hlt < - data_hlt[data_hlt$AGE == 20, ]
} else if (strat == "S?niors (60 ans et plus)") {
data_hlt < - data_hlt[data_hlt$AGE == 60, ]
}

# Consolidation effets hlt
data_hlt < - data_hlt % > %
group_by(MEDICAMENT, EFFET_HLT, SOC_LONG) % > %
summarise(n_decla_eff_hlt=sum(n_decla_eff_hlt))

# S?lection des données pour le SOC_LONG sur lequel l'utilisateur a cliqué
data_soclong_select < - data_hlt[as.character(data_hlt$SOC_LONG) == soc_long_select$y,]

# Stockage de la sortie (liste des HLT correspondants au SOC_LONG) dans une même chaîne
for (i in 1 : nrow(data_soclong_select)) {
if (i == 1){
effets_hlt < - data_soclong_select$EFFET_HLT[i]
} else {
effets_hlt < - paste(effets_hlt, data_soclong_select$EFFET_HLT[i], sep = "<br>")
}
}