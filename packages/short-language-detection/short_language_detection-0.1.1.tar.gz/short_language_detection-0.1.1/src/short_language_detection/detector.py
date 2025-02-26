""" 
Abstract class for language detection
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractDetector(ABC):
    """Abstract class for language detection"""

    @abstractmethod
    def detect(self, text: str) -> List[Tuple[str, float]]:
        """Detect the language of a text

        Args:
            text (str): The text to detect

        Returns:
            List[Tuple[str, float]]: A list of tuples containing the language and the score
        """
        pass

    @abstractmethod
    def supported_languages(self) -> List[str]:
        """Return the list of supported languages

        Returns:
            List[str]: The list of supported languages
        """
        pass
