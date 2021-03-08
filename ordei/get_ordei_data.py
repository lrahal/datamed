import pandas as pd
from create_database.models import connect_db


engine = connect_db()  # establish connection
connection = engine.connect()
#
# 2. IMPORT DES DONNEES ET PREPARATION ----
# 2.1 Import
bnpv_open_medic1418_prod_codex = pd.read_sql('bnpv_open_medic1418_prod_codex', connection)
bnpv_open_medic1418_sa_codex = pd.read_sql('bnpv_open_medic1418_sa_codex', connection)
bnpv_eff_soclong_prod_codex_open = pd.read_sql('bnpv_eff_soclong_prod_codex_open', connection)
bnpv_eff_soclong_sa_codex_open = pd.read_sql('bnpv_eff_soclong_sa_codex_open', connection)
bnpv_eff_hlt_prod_codex_open = pd.read_sql('bnpv_eff_hlt_prod_codex_open', connection)
bnpv_eff_hlt_sa_codex_open = pd.read_sql('bnpv_eff_hlt_sa_codex_open', connection)
bnpv_notif_prod_codex_open = pd.read_sql('bnpv_notif_prod_codex_open', connection)
bnpv_notif_sa_codex_open = pd.read_sql('bnpv_notif_sa_codex_open', connection)

