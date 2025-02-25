
```markdown
# NumberToWords Library Example

This example demonstrates how to use the `numtowords` library to convert numbers to words in both Persian and English languages.
---
## Installation

First, you need to install the `numtowords` library:

```bash
pip install numtowords
```
---

## Usage

Here is an example of using the library to convert numbers to words in both Persian and English.

```python
from numtowords import NumberToWords

try:
    # Convert number to words in Persian
    converter_fa = NumberToWords(language='fa')
    print(converter_fa.number_to_words(123456789123456789123456789))  # Sample number in Persian
    
    # Convert number to words in English
    converter_en = NumberToWords(language='en')
    print(converter_en.number_to_words(123456789123456789123456789))  # Sample number in English
except ValueError as e:
    print(f"Error: {e}")
```

---

### Explanation:

- This code converts a very large number to words in both Persian and English.
- If the input number is too large or invalid, a `ValueError` occurs, and an error message is displayed.

---

### Output:

صد و بیست و سه کوادریلیون چهارصد و پنجاه و شش تریلیون هفتصد و هشتاد و نه بیلیون یکصد و بیست و سه میلیون چهارصد و پنجاه و شش هزار هفتصد و هشتاد و نه
one hundred twenty-three quadrillion four hundred fifty-six trillion seven hundred eighty-nine billion one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine
```

## Notes:

- This code allows you to convert numbers into a readable format in different languages.
- You can change the language of conversion as needed.

