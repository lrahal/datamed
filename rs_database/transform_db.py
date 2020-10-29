import nltk
import string
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from upload_db import upload_fab_sites, get_api_by_cis

STOPWORDS = nltk.corpus.stopwords.words('french')


class FabricationSites:
    def __init__(self):
        self.df = upload_fab_sites()
        self.api_by_cis = get_api_by_cis()


def get_api_correspondance():
    """
    Excel database: CIS -> api
    BDPM: CIS -> [api1, api2, ...] (referential)
    Make the correspondance api (Excel) -> api (BDPM) in order to put the good syntax
    in the MySQL database
    :return: dict of list
    """
    cis_list = df.cis.unique()
    bad_cis = []
    api_corresp_dict = defaultdict(list)  # {api_df: [api_bdpm]}
    for cis in tqdm(cis_list):
        for api in df[df.cis == cis].substance_active:
            try:
                api_corresp_dict[api] = api_by_cis[cis]
            except KeyError:
                if cis not in bad_cis:
                    bad_cis.append(cis)
                continue
    return api_corresp_dict


def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    return text


def get_vectors(sentences):
    """
    Convert a collection of sentences to a matrix of token counts
    :param sentences: text
    :return:
    """
    cleaned = list(map(clean_string, sentences))
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(cleaned)
    vectors = X.toarray()
    return vectors


def cosine_sim_vectors(vec1, vec2):
    """
    Compute the similarity between two vectors
    :param vec1: api (Excel)
    :param vec2: api (BDPM)
    :return: similarity measure (between 0 and 1)
    """
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def get_api_similarities():
    """
    Get for each api_excel, its similarity with the corresponding api_bdpm
    :return:  dict of dict
    """
    api_corresp_dict = get_api_correspondance()
    api_sim_dict = defaultdict(dict)
    for api_k, api_values in tqdm(api_corresp_dict.items()):
        for api_v in api_values:
            sentences = [api_k, api_v]
            vectors = get_vectors(sentences)
            api_sim_dict[api_k][api_v] = cosine_sim_vectors(vectors[0], vectors[1])
    return api_sim_dict
