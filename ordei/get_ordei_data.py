import pandas as pd
from create_database.models import connect_db
from collections import defaultdict


engine = connect_db()  # establish connection
connection = engine.connect()
#
# 2. IMPORT DES DONNEES ET PREPARATION ----
# 2.1 Import
bnpv_open_medic1418_prod_codex = pd.read_sql(
    "bnpv_open_medic1418_prod_codex", connection
)
bnpv_open_medic1418_sa_codex = pd.read_sql("bnpv_open_medic1418_sa_codex", connection)
bnpv_eff_soclong_prod_codex_open = pd.read_sql(
    "bnpv_eff_soclong_prod_codex_open", connection
)
bnpv_eff_soclong_sa_codex_open = pd.read_sql(
    "bnpv_eff_soclong_sa_codex_open", connection
)
bnpv_eff_hlt_prod_codex_open = pd.read_sql("bnpv_eff_hlt_prod_codex_open", connection)
bnpv_eff_hlt_sa_codex_open = pd.read_sql("bnpv_eff_hlt_sa_codex_open", connection)
bnpv_notif_prod_codex_open = pd.read_sql("bnpv_notif_prod_codex_open", connection)
bnpv_notif_sa_codex_open = pd.read_sql("bnpv_notif_sa_codex_open", connection)

corresp_prod_subs = pd.read_sql("corresp_spe_prod", connection)

# Liste produits/substances à afficher
list_prod = pd.DataFrame(
    bnpv_open_medic1418_prod_codex.produit_codex.unique(), columns=["medicament"]
)
list_prod["typ_medicament"] = "Produit"

list_sa = pd.DataFrame(
    bnpv_open_medic1418_sa_codex.substance_codex_unique.unique(), columns=["medicament"]
)
list_sa["typ_medicament"] = "Substance"

frames = [list_prod, list_sa]
list_prod_sa = pd.concat(frames)
list_prod_sa = list_prod_sa.sort_values(by=["medicament"])

# Un dict pour la dataframe data
strat_data_dict = {
    "Hommes": {"value": "Hommes", "field": "sexe"},
    "Femmes": {"value": "Femmes", "field": "sexe"},
    "Enfants (0-19 ans)": {"value": "0-19 ans", "field": "age"},
    "Adultes (20-59 ans)": {"value": "20-59 ans", "field": "age"},
    "Séniors (60 ans et plus)": {"value": "60 ans et plus", "field": "age"},
}

# Un dict pour les dataframes data_soclong et data_notif
strat_dict = {
    "Hommes": {"value": "M", "field": "sexe"},
    "Femmes": {"value": "F", "field": "sexe"},
    "Enfants (0-19 ans)": {"value": 0, "field": "age"},
    "Adultes (20-59 ans)": {"value": 20, "field": "age"},
    "Séniors (60 ans et plus)": {"value": 60, "field": "age"},
}

med_dict = defaultdict(dict)
for med in tqdm(list_prod_sa.medicament.unique()):
    typ_med = list_prod_sa[list_prod_sa.medicament == med].typ_medicament.values[0]
    for strat in [
        "Ensemble",
        "Hommes",
        "Femmes",
        "Enfants (0-19 ans)",
        "Adultes (20-59 ans)",
        "Séniors (60 ans et plus)",
    ]:
        if typ_med == "Substance":
            data = bnpv_open_medic1418_sa_codex[
                bnpv_open_medic1418_sa_codex.substance_codex_unique == med
            ]
            data_soclong = bnpv_eff_soclong_sa_codex_open[
                bnpv_eff_soclong_sa_codex_open.substance_codex_unique == med
            ]
            data_notif = bnpv_notif_sa_codex_open[
                bnpv_notif_sa_codex_open.substance_codex_unique == med
            ]
            data_soclong = data_soclong.rename(
                columns={"substance_codex_unique": "medicament"}
            )
            data_notif = data_notif.rename(columns={"substance_codex_unique": "medicament"})
            data_hlt = bnpv_eff_hlt_sa_codex_open[
                bnpv_eff_hlt_sa_codex_open.substance_codex_unique == med
            ]
            data_hlt = data_hlt.rename(columns={"substance_codex_unique": "medicament"})
        else:
            data = bnpv_open_medic1418_prod_codex[
                bnpv_open_medic1418_prod_codex.produit_codex == med
            ]
            data_soclong = bnpv_eff_soclong_prod_codex_open[
                bnpv_eff_soclong_prod_codex_open.produit_codex == med
            ]
            data_notif = bnpv_notif_prod_codex_open[
                bnpv_notif_prod_codex_open.produit_codex == med
            ]
            data_soclong = data_soclong.rename(columns={"produit_codex": "medicament"})
            data_notif = data_notif.rename(columns={"produit_codex": "medicament"})
            data_hlt = bnpv_eff_hlt_prod_codex_open[
                bnpv_eff_hlt_prod_codex_open.produit_codex == med
            ]
            data_hlt = data_hlt.rename(columns={"produit_codex": "medicament"})

        if strat != "Ensemble":
            data = data[
                data[strat_data_dict[strat]["field"]] == strat_data_dict[strat]["value"]
            ]
            data_soclong = data_soclong[
                data_soclong[strat_dict[strat]["field"]] == strat_dict[strat]["value"]
            ]
            data_notif = data_notif[
                data_notif[strat_dict[strat]["field"]] == strat_dict[strat]["value"]
            ]
            data_hlt = data_hlt[
                data_hlt[strat_dict[strat]["field"]] == strat_dict[strat]["value"]
            ]

        temp = (
            data_soclong.groupby(["medicament", "soc_long"])
            .agg({"n_decla_eff": "sum"})
            .reset_index()
        )
        temp2 = (
            data_soclong.drop_duplicates(subset=["medicament", "age", "sexe", "n_cas"])
            .groupby("medicament")
            .agg({"n_cas": "sum"})
            .reset_index()
        )

        try:
            data_soclong = temp.merge(temp2, on="medicament", how="left")
            data_soclong["pour_cas_soclong"] = (
                data_soclong.n_decla_eff / data_soclong.n_cas
            ) * 100
            data_soclong = data_soclong[data_soclong.n_decla_eff > 9]
            data_soclong = data_soclong.sort_values(
                by=["pour_cas_soclong"], ascending=False
            )
        except ValueError:
            data_soclong = pd.DataFrame(columns=['medicament', 'soc_long', 'n_decla_eff', 'n_cas', 'pour_cas_soclong'])

        data_notif = (
            data_notif.groupby(["medicament", "typ_notif"])
            .agg({"n_decla": "sum"})
            .reset_index()
        )
        data_notif.typ_notif = data_notif.apply(
            lambda x: "Notificateur(s) < 10 cas" if x.n_decla < 10 else x.typ_notif,
            axis=1,
        )
        data_notif = (
            data_notif.groupby(["medicament", "typ_notif"])
            .agg({"n_decla": "sum"})
            .reset_index()
            .sort_values(by="n_decla", ascending=False)
        )

        data_hlt = (
            data_hlt.groupby(["medicament", "effet_hlt", "soc_long"])
            .agg({"n_decla_eff_hlt": "sum"})
            .reset_index()
            .sort_values(by="n_decla_eff_hlt", ascending=False)
        )

        data_sexe = (
            data.groupby("sexe").agg({"n_cas": "sum", "n_conso": "sum"}).reset_index()
        )

        data_age = (
            data.groupby("age").agg({"n_cas": "sum", "n_conso": "sum"}).reset_index()
        )

        data_annee = (
            data.groupby("annee").agg({"n_cas": "sum", "n_conso": "sum"}).reset_index()
        )

        med_dict[med][strat] = {
            "soclong": [
                {k: v for k, v in d.items() if k != "medicament"}
                for d in data_soclong.to_dict(orient="records")
            ],
            "notif": [
                {k: v for k, v in d.items() if k != "medicament"}
                for d in data_notif.to_dict(orient="records")
            ],
            "hlt": [
                {k: v for k, v in d.items() if k != "medicament"}
                for d in data_hlt.to_dict(orient="records")
            ],
            "sexe": data_sexe.to_dict(orient="records"),
            "age": data_age.to_dict(orient="records"),
            "annee": data_annee.to_dict(orient="records"),
        }
