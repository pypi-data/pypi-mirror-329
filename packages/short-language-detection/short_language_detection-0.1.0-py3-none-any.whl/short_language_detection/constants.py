"""
Constants for the package
"""

import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
FASTTEXT_WEIGHTS = ["lid.176.ftz", "discord_langdetect.ftz"]
WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "weights")

top_languages = json.load(
    open(
        os.path.join(
            os.path.join(os.path.dirname(__file__), "data"), "top_languages.json"
        ),
        "r",
    )
)


TOP_LANGUAGES = [
    lang for lang, _ in sorted(top_languages.items(), key=lambda x: x[1], reverse=True)
]
