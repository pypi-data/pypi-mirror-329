""" 
LinguaDetector class
"""

from lingua import Language, LanguageDetectorBuilder

from .detector import AbstractDetector


class LinguaDetector(AbstractDetector):
    """A language detector based on Lingua"""

    def __init__(
        self,
    ) -> None:
        """Load the Lingua model"""
        self._model = (
            LanguageDetectorBuilder.from_all_spoken_languages()
            .with_preloaded_language_models()
            .with_low_accuracy_mode()
            .build()
        )

    def detect(self, text):
        lingua_detection = self._model.compute_language_confidence_values(text)

        result = []
        for lingua_output in lingua_detection:
            result.append(
                (
                    lingua_output.language.iso_code_639_1.name.lower(),
                    round(lingua_output.value, 2),
                )
            )

        return result

    @property
    def supported_languages(self):
        return [lang.iso_code_639_1.name.lower() for lang in Language.all()]
