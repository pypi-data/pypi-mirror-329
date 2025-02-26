# Short Language Detection

This project is designed to detect the language of short text snippets. It uses machine learning models to accurately identify the language of a given input.

## Features

- Detects language from short text inputs
- Supports multiple languages
- High accuracy and performance

## Installation

To install the necessary dependencies, run:

```bash
pip install short-language-detection
```

## Usage

To use the language detection model, run the following command:

```python
import short_language_detection as sld

# Create a detector
predictor = sld.Detector()

# Detect the language of a text
print(predictor.detect("hello the world"))
# ({'language': 'en', 'score': 1.0, 'prefered': True, 'reliable': True}, {'language': 'sk', 'score': 0.33, 'prefered': False, 'reliable': False})
```

## Contributing

We welcome contributions! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact us at [jourdelune863@gmail.com](mailto:jourdelune863@gmail.com).
