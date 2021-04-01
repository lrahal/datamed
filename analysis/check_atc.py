import pandas as pd

from create_database.models import connect_db

engine = connect_db()  # establish connection
connection = engine.connect()


def get_diff_atc():
    """
    Lister les classes ATC qui ne sont pas identiques
    pour une même spécialité dans la table ruptures_dc et dans la table ventes
    :return: génère un csvc
    """
    dfr = pd.read_sql_table("ruptures_dc", connection)
    dfv = pd.read_sql_table("ventes", connection)

    a = dfr.groupby(["specialite", "atc"]).count().reset_index()[["specialite", "atc"]]
    a = a.rename(columns={"atc": "atc_ruptures"})

    b = (
        dfv.groupby(["cis", "denomination_specialite", "atc"])
        .count()
        .reset_index()[["cis", "denomination_specialite", "atc"]]
    )
    b = b.rename(
        columns={"denomination_specialite": "specialite_ventes", "atc": "atc_ventes"}
    )

    c = pd.merge(a, b, left_on="specialite", right_on="specialite_ventes", how="outer")
    c = c.where(pd.notnull(c), None)

    d = c[
        c.apply(
            lambda x: x.atc_ruptures != x.atc_ventes
            if (x.atc_ruptures and x.atc_ventes and x.specialite_ventes)
            else False,
            axis=1,
        )
    ]
    d = d.drop(["specialite_ventes"], axis=1)
    d = d[["cis", "specialite", "atc_ruptures", "atc_ventes"]]
    d.to_csv("/Users/ansm/Desktop/diff_atc_ruptures_ventes.csv", sep=";")
