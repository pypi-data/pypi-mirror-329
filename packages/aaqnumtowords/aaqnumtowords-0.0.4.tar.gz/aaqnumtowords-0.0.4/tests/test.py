from NumberToWords import NumberToWords

try:
    # Convert number to words in Persian
    converter_fa = NumberToWords(language='fa')
    print(converter_fa.number_to_words(123456789123456789123456789))  # Sample number in Persian
    
    # Convert number to words in English
    converter_en = NumberToWords(language='en')
    print(converter_en.number_to_words(123456789123456789123456789))  # Sample number in English
except ValueError as e:
    print(f"Error: {e}")