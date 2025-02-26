""" 
Language detector based on dictionaries
"""

import os

from .constants import DATA_PATH
from .detector import AbstractDetector


class DictDetector(AbstractDetector):
    """
    A language detector based on dictionaries
    """

    def __init__(self) -> None:
        """
        Load the language dictionaries and the top languages
        """

        self._language = {}

        for f in os.listdir(os.path.join(DATA_PATH, "dictionaries")):
            file = open(
                os.path.join(DATA_PATH, "dictionaries", f), "r", encoding="utf-8"
            )
            self._language[f.split(".")[0]] = set(
                file.read().split("\n")
            )  # using set for faster lookup

    def detect(self, text):
        # split the string into words, can't use nltk because at this point we don't have know the language
        text = text.lower().split()

        scores = {}

        # calculate the score for each language
        # the score is the number of common words between the text and the language dictionary
        for lang in self._language.keys():
            common_words = 0
            for v in text:
                if v in self._language[lang]:
                    common_words += 1
            scores[lang] = common_words

        # remove languages with score 0
        result = [
            (lang, scores[lang] / len(text)) for lang in scores if scores[lang] != 0
        ]

        # sort the result by score
        result = sorted(result, key=lambda x: x[1], reverse=True)

        return result

    @property
    def supported_languages(self):
        return list(self._language.keys())
