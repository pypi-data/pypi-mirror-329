""" 
The output formater of the language detection.
"""

from typing import List, Tuple

from .constants import TOP_LANGUAGES


class Output:
    """
    The output of the language detection.
    """

    def __init__(
        self,
        predictions: List[Tuple[str, float]],
        reliability_threshold: float,
        filter_threshold: float,
    ):
        """Initialize the output of the language detection.

        Args:
            predictions (List[Tuple[str, float]]): The list of languages and their scores.
            reliability_threshold (float): the threshold to consider a language as reliable.
            filter_threshold (float): the threshold to filter the languages.
        """
        self._reliability_threshold = reliability_threshold
        self._filter_threshold = filter_threshold

        predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
        predictions = self._score_threshold(predictions, self._filter_threshold)

        self._predictions = self._sort_by_language_popularity(predictions)

    def _score_threshold(
        self, scores: List[Tuple[str, float]], threshold: float = 0.0
    ) -> List[Tuple[str, float]]:
        """Removes the languages with a score below the threshold.

        Args:
            scores (List[Tuple[str, float]]): The list of languages and their scores.

        Returns:
            List[Tuple[str, float]]: The list of languages and their scores above the threshold.
        """
        return [(lang, score) for lang, score in scores if score >= threshold]

    def _sort_by_language_popularity(
        self, scores: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        """Sorts the languages by popularity.

        Args:
            scores (List[Tuple[str, float]]): The list of languages and their scores.

        Returns:
            List[Tuple[str, float]]: The list of languages and their scores sorted by popularity.
        """
        # sort equal scores by the top languages
        # [('fr', 1.0), ('ro', 0.5), ('en', 0.5), ('ca', 0.25), ('es', 0.25)]
        # becomes
        # [('fr', 1.0), ('en', 0.5), ('ro', 0.5), ('es', 0.25), ('ca', 0.25)]

        result = sorted(
            scores,
            key=lambda x: (
                x[1],
                (
                    -TOP_LANGUAGES.index(x[0])
                    if x[0] in TOP_LANGUAGES
                    else -len(TOP_LANGUAGES)
                ),
            ),
            reverse=True,
        )

        return result

    @property
    def predictions(self) -> List[dict[str, float, bool]]:
        """Return the predictions.

        Returns:
            List[Dict[str, float, bool]]: The list of languages and their scores.
        """
        results = []

        for i, (lang, score) in enumerate(self._predictions):
            results.append(
                {
                    "language": lang,
                    "score": round(score, 2),
                    "prefered": i == 0 and score >= self._reliability_threshold,
                    "reliable": score >= self._reliability_threshold,
                }
            )

        return tuple(results)

    def __iter__(self):
        return iter(self.predictions)

    def __getitem__(self, i):
        return self.predictions[i]

    def __str__(self):
        return str(self.predictions)

    def __repr__(self):
        return f"Output(predictions={self.predictions}, reliability_threshold={self._reliability_threshold}, filter_threshold={self._filter_threshold})"
