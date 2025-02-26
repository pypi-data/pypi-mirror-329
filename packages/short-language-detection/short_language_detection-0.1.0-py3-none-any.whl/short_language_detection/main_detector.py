""" 
Main class to detect the language of a text.
"""

import re
import unicodedata

import emoji

from .constants import FASTTEXT_WEIGHTS
from .dict_detector import DictDetector
from .fasttext_detector import FastTextDetector
from .lingua_detector import LinguaDetector
from .output_formater import Output


class Detector:
    """Main class to detect the language of a text."""

    def __init__(
        self,
        reliability_threshold: float = 0.35,
        filter_threshold: float = 0.1,
        equal_traitements: bool = False,
    ):
        """Initializes the Detector object.

        Args:
            reliability_threshold (float, optional): The threshold above which the language is considered reliable. Defaults to 0.5.
            filter_threshold (float, optional): The threshold below which the language is filtered out. Defaults to 0.35.
            equal_traitements (bool, optional): If True, all detectors are considered equally important. Defaults to False (more focus on english and popular languages).
        """

        self._reliability_threshold = reliability_threshold
        self._filter_threshold = filter_threshold
        self._equal_traitements = equal_traitements

        self._detectors = []
        self._detectors.append(DictDetector())
        self._detectors.append(LinguaDetector())

        for i, weight in enumerate(FASTTEXT_WEIGHTS):
            # The first detector has a weight of 1, the others have a weight of 0.5
            importance = 1 if i == 0 else 0.5

            self._detectors.append(
                FastTextDetector(weight, weighted_reliability=importance)
            )

        # Count the number of detectors for each language
        self._detectors_for_each_language = {}
        for detector in self._detectors:
            for lang in detector.supported_languages:
                if lang not in self._detectors_for_each_language:
                    self._detectors_for_each_language[lang] = 0

                self._detectors_for_each_language[lang] += 1

    def _clean_text(self, text: str) -> str:
        """Cleans the text by removing special characters, emojis, and numbers.

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        text = re.sub(
            r"[!\"#$%&\'()*+,\-.\/:;<=>?@\[\\\]^_`{|}~ ]{2,}",
            lambda match: match.group()[0] + (" " if " " in match.group() else ""),
            text,
        )
        text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
        text = re.sub(r"\d+|\^", "", text)

        s = "@#$<>[]*_-~&%+/§{}=\|:▬"
        for char in text:
            if char in s:
                text = text.replace(char, "", 1)

        text = emoji.replace_emoji(text, replace="").strip()

        return unicodedata.normalize("NFKC", text.replace("\n", ""))[:200]

    def detect(self, text: str) -> Output:
        """Detects the language of a text.

        Args:
            text (str): The text to detect.

        Returns:
            Output: The detected languages and their scores.
        """

        text = self._clean_text(text)
        if text == "":
            return []

        predictions = [detector.detect(text) for detector in self._detectors]

        # If the language is detected with a score of 1 from the dictionary detector, return it
        if len(predictions[0]) != 0:
            if predictions[0][0][1] == 1:
                return Output(
                    predictions[0], self._reliability_threshold, self._filter_threshold
                )

        scores = {}
        for prediction in predictions:
            for lang, score in prediction:
                if lang not in scores:
                    scores[lang] = 0
                scores[lang] += score

        # Normalize the scores by the number of detectors for each language
        if self._equal_traitements:
            for lang in scores:
                scores[lang] /= max(1, self._detectors_for_each_language[lang] - 3)

        # convert the scores to list
        scores = list(scores.items())

        return Output(scores, self._reliability_threshold, self._filter_threshold)

    @property
    def supported_languages(self):
        return tuple(self._detectors_for_each_language.keys())
