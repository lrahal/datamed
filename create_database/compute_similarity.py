from collections import Counter
from math import sqrt
from typing import Tuple


class WordsSimilarity:

    def __init__(self, word_tuple: Tuple):
        self.word1 = word_tuple[0]
        self.word2 = word_tuple[1]

        # Count the number of characters in each word
        self.char_counter_1 = Counter(self.word1)
        self.char_counter_2 = Counter(self.word2)
        # Get the set of characters
        self.char_set_1 = set(self.char_counter_1)
        self.char_set_2 = set(self.char_counter_2)
        # Compute vectors lengths
        self.char_len_1 = sqrt(sum(c * c for c in self.char_counter_1.values()))
        self.char_len_2 = sqrt(sum(c * c for c in self.char_counter_2.values()))

    def cosine_similarity(self, ndigits: int) -> float:
        # Get the common characters between the two character sets
        common_characters = self.char_set_1.intersection(self.char_set_2)
        # Sum of the product of each intersection character
        product_summation = sum(self.char_counter_1[character] * self.char_counter_2[character]
                                for character in common_characters)
        # Compute product of vectors lengths
        length = self.char_len_1 * self.char_len_2
        # Compute cosine similarity and rounds the value to ndigits decimal places
        if length == 0:
            # Set value to 0 if word is empty
            return 0
        else:
            return round(product_summation / length, ndigits)


def get_similarity(api_tuple: Tuple, ndigits: int) -> float:
    """
    Compute cosine similarity between a tuple of api
    """
    ws = WordsSimilarity(api_tuple)
    return ws.cosine_similarity(ndigits)
