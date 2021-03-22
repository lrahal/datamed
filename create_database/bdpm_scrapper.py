import json
from collections import defaultdict
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

file_liste_spe = open("./datamed_dash/data/liste_specialites.json", "r")
SPE_DICT = json.loads(file_liste_spe.read())


def get_cis_list() -> List:
    cis_list = []
    for k, v in SPE_DICT.items():
        cis_list.extend(v)
    return list(set(cis_list))


def get_spe_by_cis():
    spe_by_cis = defaultdict()
    for k, values in SPE_DICT.items():
        for v in values:
            spe_by_cis[v] = k
    return spe_by_cis


def scrap_bdpm(cis_list: List, spe_by_cis: Dict) -> Dict:
    notice_dict = defaultdict()
    for cis in tqdm(cis_list):
        page = requests.get(
            "http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid={}".format(
                cis
            )
        )

        # Fetch webpage
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify())

        notice_elements = soup.find_all("p", {"class": "AmmCorpsTexte"})
        notice = ""
        for ele in notice_elements:
            if (
                ele.text.replace("\n", "")
                .strip()
                .startswith("Classe pharmacothérapeutique")
            ):
                continue
            else:
                notice += ele.text.replace("\n", "").strip()
        notice_dict[spe_by_cis[cis]] = notice
    return notice_dict


def __main__():
    cis_list = get_cis_list()
    spe_by_cis = get_spe_by_cis()
    notice_dict = scrap_bdpm(cis_list, spe_by_cis)
    with open("./datamed_dash/data/notice_by_cis.json", "w") as outfile:
        json.dump(notice_dict, outfile)
