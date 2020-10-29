import string
import unidecode
import numpy as np
from nltk.corpus import stopwords
from typing import Tuple, List, Dict, DefaultDict
from upload_db import upload_fab_sites, get_api_by_cis
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

STOPWORDS = stopwords.words('french')


class FabricationSites:
    def __init__(self):
        self.df = upload_fab_sites()
        self.api_by_cis = get_api_by_cis()
        self.api_corresp_dict = get_api_correspondance()


def get_api_correspondance() -> [DefaultDict, List]:
    """
    Excel database: CIS -> api
    BDPM: CIS -> [api1, api2, ...] (referential)
    Make the correspondance api (Excel) -> api (BDPM) in order to put the good syntax
    in the MySQL database
    :return: dict of list
    """
    cis_list = df.cis.unique()
    bad_cis = []
    api_corresp_dict = defaultdict(list)  # {api_excel: [api_bdpm]}
    for cis in tqdm(cis_list):
        for api in df[df.cis == cis].substance_active:
            try:
                api_corresp_dict[api] = api_by_cis[cis]
            except KeyError:
                if cis not in bad_cis:
                    bad_cis.append(cis)
                continue
    return api_corresp_dict, bad_cis


def clean_string(text: str) -> str:
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    text = unidecode.unidecode(text)
    return text


def get_vectors(sentences: Tuple[str]) -> np.ndarray:
    """
    Convert a collection of sentences to a matrix of token counts
    :param sentences: text
    :return:
    """
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    vectors = X.toarray()
    return vectors


def cosine_sim_vectors(vec1: np.ndarray, vec2: np.ndarray) -> np.float64:
    """
    Compute the similarity between two vectors
    :param vec1: api (Excel)
    :param vec2: api (BDPM)
    :return: similarity measure (between 0 and 1)
    """
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def get_api_similarities() -> DefaultDict:
    """
    Get for each api_excel, its similarity with the corresponding api
    contained in the api_bdpm_list
    :return:  dict of dict
    """
    api_sim_dict = defaultdict(dict)
    for api_excel, api_bdpm in tqdm(api_corresp_dict.items()):
        for api in api_bdpm:
            # Create sentences tuple
            api_tuple = (api_excel, api)
            # Clean the words in api_tuple
            cleaned = tuple(map(clean_string, api_tuple))
            # Vectorize
            vectors = get_vectors(cleaned)
            # Compute cosine similarity between the 2 words in tuple
            api_sim_dict[api_excel][api] = cosine_sim_vectors(vectors[0], vectors[1])
    return api_sim_dict


def get_most_sim_api(api_sim_dict: DefaultDict) -> Dict:
    """
    Pick the api_bdpm with the highest similarity score
    :return: dict
    """
    return {
        api_excel: max(api_sim_dict[api_excel], key=api_sim[api_excel].get)
        for api_excel in api_corresp_dict.keys()
    }
