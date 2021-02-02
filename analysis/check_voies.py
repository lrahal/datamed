import pandas as pd


def get_diff_voies():
    """
    Trouver les CIS des ventes 2017 qui n'ont pas d'équivalent dans les ventes 2018 et 2019
    :return:
    """
    df_2017 = pd.read_excel(
        '/Users/ansm/Documents/GitHub/datamed/create_database/data/OCTAVE/Données OCTAVE 2017.xlsx',
        dtype={'code CIS': str, 'Code CIP': str, 'Année': int, 'Identifiant OCTAVE': int})
    df_2017['Nom Labo'] = None

    df_2018 = pd.read_excel(
        '/Users/ansm/Documents/GitHub/datamed/create_database/data/OCTAVE/Octave_2018_ATC_voie.xlsx',
        dtype={'code CIS': str, 'Code CIP': str, 'Année': int, 'Identifiant OCTAVE': int})
    df_2018['Nom Labo'] = None

    df_2019 = pd.read_excel(
        '/Users/ansm/Documents/GitHub/datamed/create_database/data/OCTAVE/Octave_2019_ATC_voie.xlsx',
        dtype={'code CIS': str, 'Code CIP': str, 'Année': int, 'Identifiant OCTAVE': int})
    df = pd.concat([df_2018, df_2019])

    records = df.to_dict(orient='records')
    r = {d['cis']: {d['annee']: d['voie_4_classes']} for d in records}
    cis_list = df.cis.unique().tolist()


    bad_voie = []
    for c in cis_list:
        if r[c].get(2018, '') and r[c].get(2019, '') and r[c].get(2018, '') != r[c].get(2019, ''):
            bad_voie.append({'cis': c, '2018': r[c].get(2018, ''), '2019': r[c].get(2019, '')})

    cis_list_2017 = df_2017['code CIS'].unique().tolist()
    all_cis = set(cis_list + cis_list_2017)

    voie_by_cis = {d['code CIS']: d['VOIE'] for d in records}
    voie_4_by_cis = {d['code CIS']: d['VOIE 4 classes'] for d in records}

    df_2017['VOIE'] = df_2017['code CIS'].apply(lambda x: voie_by_cis.get(x, None))
    df_2017['VOIE 4 classes'] = df_2017['code CIS'].apply(lambda x: voie_4_by_cis.get(x, None))

    # CIS qui n'ont pas d'équivalent dans les ventes 2018 et 2019
    cis_not_matched = df_2017[df_2017.voie_4_classes.isnull()]['code CIS'].unique()

    df_2017['matched'] = df_2017['code CIS'].apply(lambda x: 'NOK' if x in cis_not_matched else 'OK')
