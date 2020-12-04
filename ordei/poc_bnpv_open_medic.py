import pandas as pd

# 2. IMPORT DES DONNEES ET PREPARATION ----
# 2.1 Import
bnpv_open_medic1418_prod_codex = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv")
bnpv_open_medic1418_sa_codex = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv")
corresp_spe_prod_subs = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv")
bnpv_eff_soclong_prod_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv")
bnpv_eff_soclong_sa_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv")
bnpv_eff_hlt_prod_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv")
bnpv_eff_hlt_sa_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv")
bnpv_notif_prod_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv")
bnpv_notif_sa_codex_open = pd.read_csv("C:/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv")

# 2.2 Pr?paration
# corresp prod_subs
corresp_prod_subs <- corresp_spe_prod_subs %>%
  group_by(PRODUIT_CODEX, SUBSTANCE_CODEX_UNIQUE) %>%
  summarise(n_prod_subs=n()) %>%
  select(-n_prod_subs)

corresp_prod_subs<-na.omit(corresp_prod_subs) # 2 pdts sans substance

# Liste ? produits/substances ? afficher
list_prod <- as.data.frame(as.character(unique(bnpv_open_medic1418_prod_codex$PRODUIT_CODEX)))
list_prod$TYP_MEDICAMENT <- "Produit"
names(list_prod)[1] <- "MEDICAMENT"
list_prod$MEDICAMENT<-as.character(list_prod$MEDICAMENT)

list_sa <- as.data.frame(as.character(unique(bnpv_open_medic1418_sa_codex$SUBSTANCE_CODEX_UNIQUE)))
list_sa$TYP_MEDICAMENT <- "Substance"
names(list_sa)[1] <- "MEDICAMENT"
list_sa$MEDICAMENT<-as.character(list_sa$MEDICAMENT)

list_prod_sa <- rbind(list_prod,list_sa)
list_prod_sa <- list_prod_sa[order(list_prod_sa$MEDICAMENT),]