import pandas as pd

bnpv_open_medic1418_prod_codex = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv', encoding='ISO-8859-1', sep=';')
bnpv_open_medic1418_sa_codex = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv', encoding='ISO-8859-1', sep=';')
corresp_spe_prod_subs = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_soclong_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_soclong_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_hlt_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_eff_hlt_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_notif_prod_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv', encoding='ISO-8859-1', sep=';')
bnpv_notif_sa_codex_open = pd.read_csv('/Users/ansm/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv', encoding='ISO-8859-1', sep=';')


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


def get_json(typ_med: str):
    # typ_med = 'Substance'
    if typ_med == 'Substance':
        data = bnpv_open_medic1418_sa_codex
        data_soclong = bnpv_eff_soclong_sa_codex_open
        data_notif = bnpv_notif_sa_codex_open
        data_hlt = bnpv_eff_hlt_sa_codex_open
        suffix = 'sa'
    else:
        data = bnpv_open_medic1418_prod_codex
        data_soclong = bnpv_eff_soclong_prod_codex_open
        data_notif = bnpv_notif_prod_codex_open
        data_hlt = bnpv_eff_hlt_prod_codex_open
        suffix = 'prod'

    data = data.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
    data_soclong = data_soclong.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
    data_notif = data_notif.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})
    data_hlt = data_hlt.rename(columns={typ_med_dict[typ_med]: 'MEDICAMENT'})

    data_sexe = data.groupby(['MEDICAMENT', 'SEXE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
    data_age = data.groupby(['MEDICAMENT', 'AGE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()
    data_annee = data.groupby(['MEDICAMENT', 'ANNEE']).agg({'n_cas': 'sum', 'n_conso': 'sum'}).reset_index()

    # Age
    temp = data_soclong.groupby(['MEDICAMENT', 'AGE', 'SOC_LONG']).agg({'n_decla_eff': 'sum'}).reset_index()
    temp2 = data_soclong.drop_duplicates(subset=['MEDICAMENT', 'AGE', 'n_cas']).groupby('MEDICAMENT').agg(
        {'n_cas': 'sum'}).reset_index()

    data_soclong_age = temp.merge(temp2, on='MEDICAMENT', how='left')
    data_soclong_age['pour_cas_soclong'] = (data_soclong_age.n_decla_eff / data_soclong_age.n_cas) * 100
    data_soclong_age = data_soclong_age[data_soclong_age.n_decla_eff > 9]
    data_soclong_age = data_soclong_age.sort_values(by=['pour_cas_soclong'], ascending=False)

    data_notif_age = data_notif.groupby(['MEDICAMENT', 'AGE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()
    data_notif_age.TYP_NOTIF = data_notif_age.n_decla.apply(lambda x: 'Notificateur(s) < 10 cas' if x < 10 else x)
    data_notif_age = data_notif_age.groupby(['MEDICAMENT', 'AGE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()

    data_hlt_age = data_hlt.groupby(
        ['MEDICAMENT', 'AGE', 'EFFET_HLT', 'SOC_LONG']).agg({'n_decla_eff_hlt': 'sum'}).reset_index()

    # Sexe
    temp = data_soclong.groupby(['MEDICAMENT', 'SEXE', 'SOC_LONG']).agg({'n_decla_eff': 'sum'}).reset_index()
    temp2 = data_soclong.drop_duplicates(subset=['MEDICAMENT', 'SEXE', 'n_cas']).groupby('MEDICAMENT').agg(
        {'n_cas': 'sum'}).reset_index()

    data_soclong_sexe = temp.merge(temp2, on='MEDICAMENT', how='left')
    data_soclong_sexe['pour_cas_soclong'] = (data_soclong_sexe.n_decla_eff / data_soclong_sexe.n_cas) * 100
    data_soclong_sexe = data_soclong_sexe[data_soclong_sexe.n_decla_eff > 9]
    data_soclong_sexe = data_soclong_sexe.sort_values(by=['pour_cas_soclong'], ascending=False)

    data_notif_sexe = data_notif.groupby(['MEDICAMENT', 'SEXE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()
    data_notif_sexe.TYP_NOTIF = data_notif_age.n_decla.apply(lambda x: 'Notificateur(s) < 10 cas' if x < 10 else x)
    data_notif_sexe = data_notif_sexe.groupby(['MEDICAMENT', 'SEXE', 'TYP_NOTIF']).agg({'n_decla': 'sum'}).reset_index()

    data_hlt_sexe = data_hlt.groupby(
        ['MEDICAMENT', 'SEXE', 'EFFET_HLT', 'SOC_LONG']).agg({'n_decla_eff_hlt': 'sum'}).reset_index()

    data.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data.json'.format(suffix), orient='records')
    data_soclong_age.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_soclong_age.json'.format(suffix), orient='records')
    data_soclong_sexe.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_soclong_sexe.json'.format(suffix), orient='records')
    data_notif_age.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_notif_age.json'.format(suffix), orient='records')
    data_notif_sexe.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_notif_sexe.json'.format(suffix), orient='records')
    data_hlt_age.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_hlt_age.json'.format(suffix), orient='records')
    data_hlt_sexe.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_hlt_sexe.json'.format(suffix), orient='records')
    data_age.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_age.json'.format(suffix), orient='records')
    data_sexe.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_sexe.json'.format(suffix), orient='records')
    data_annee.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/{}_data_annee.json'.format(suffix), orient='records')


def main():
    # Générer données json
    corresp_prod_subs = corresp_spe_prod_subs.drop_duplicates(subset=['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE'])
    corresp_prod_subs = corresp_prod_subs[['PRODUIT_CODEX', 'SUBSTANCE_CODEX_UNIQUE']].sort_values(by=['PRODUIT_CODEX'])
    corresp_prod_subs = corresp_prod_subs.dropna()
    corresp_prod_subs.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/corresp_prod_sa.json', orient='records')

    list_prod = pd.DataFrame(bnpv_open_medic1418_prod_codex.PRODUIT_CODEX.unique(), columns=['MEDICAMENT'])
    list_prod['TYP_MEDICAMENT'] = 'Produit'

    list_sa = pd.DataFrame(bnpv_open_medic1418_sa_codex.SUBSTANCE_CODEX_UNIQUE.unique(), columns=['MEDICAMENT'])
    list_sa['TYP_MEDICAMENT'] = 'Substance'

    frames = [list_prod, list_sa]
    list_prod_sa = pd.concat(frames)
    list_prod_sa = list_prod_sa.sort_values(by=['MEDICAMENT'])
    list_prod_sa.to_json('/Users/ansm/Documents/GitHub/datamed/ordei/data/list_prod_sa.json', orient='records')

    for typ_med in ['Substance', 'Produit']:
        get_json(typ_med)
