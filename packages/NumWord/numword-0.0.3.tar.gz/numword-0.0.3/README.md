# NumWord

![Manual Test](https://github.com/HarshitDalal/numword/actions/workflows/manual_test.yml/badge.svg)
![Daily Test](https://github.com/HarshitDalal/numword/actions/workflows/daily_test.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/NumWord)
![PyPI Downloads](https://img.shields.io/pypi/dm/NumWord)
![License MIT](https://img.shields.io/github/license/HarshitDalal/numword)
![codecov](https://codecov.io/gh/HarshitDalal/NumWord/graph/badge.svg?token=3DAOLLEYO3)

NumWord is a Python package that converts numbers written in words to their numerical representation.

## Features

- Convert single digits, two digits, large numbers, decimal numbers, and mixed numbers from words to numbers.
- Convert numbers to words.
- Supports English language.
- Supports Hindi language.
- Supports convert number into humanize number e.g.
    - 1500000 -> 1.5M
    - 1.5M -> 10L / 10 लाख

## Installation

To install the package, use pip:

```bash
pip install -r requirements.txt
```

## Usage

Here is an example of how to use the NumWord package:

### Convert number word into number

```python
from NumWord import WordToNumber

word_to_num_converter = WordToNumber()

# Convert words to numbers in English
result = word_to_num_converter.convert("one hundred twenty three point four five six")
print(result)  # Output: 123.456

# Convert words to numbers in Hindi
result = word_to_num_converter.convert("एक सौ तेईस दशमलव चार पांच छह", lang='hi')
print(result)  # Output: 123.456
``` 

### Convert number into number word

```python
from NumWord import NumberToWord

num_to_word_converter = NumberToWord()

# Convert numbers to words in English
result = num_to_word_converter.convert(123.456)
print(result)  # Output: one hundred twenty-three point four five six

# Convert numbers to words in Hindi
result = num_to_word_converter.convert(123.456, lang='hi')
print(result)  # Output: एक सौ तेईस दशमलव चार पांच छह
```

### Convert number into Humanize Number or convert one number system to another humanize number system

```python
from NumWord import HumanizeNumber

humanize_number = HumanizeNumber()

result = humanize_number.convert(1500000, lang='en')
print(result)  # Output: 1.5M

result = humanize_number.convert("1.5M", lang="en", to_lang="hi")
print(result)  # Output: 15 लाख

result = humanize_number.convert("1.5M", lang="en", to_lang="en-hi")
print(result)  # Output: 15L
```

## Running Tests

To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the MIT License file for details.

