class NumberToWords:
    def __init__(self, language='fa'):
        self.language = language

        self.ones_fa = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
        self.tens_fa = ["", "ده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
        self.hundreds_fa = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
        self.thousands_fa = ["", "هزار", "میلیون", "میلیارد", "تریلیون", "کوآدریلیون", "کوینتیلیون", "سکستیلیون", "سپتیلیون", "اکتیلیون", "نونیلیون", "دهیلیون"]
        
        self.ones_en = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        self.tens_en = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.hundreds_en = ["", "one hundred", "two hundred", "three hundred", "four hundred", "five hundred", "six hundred", "seven hundred", "eight hundred", "nine hundred"]
        self.thousands_en = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion"]

    def number_to_words(self, num):
        if num < 0 or num > 10**36:
            raise ValueError("The number is too large. The valid range is from 0 to 10^36.")

        if self.language == 'fa':
            ones = self.ones_fa
            tens = self.tens_fa
            hundreds = self.hundreds_fa
            thousands = self.thousands_fa
        elif self.language == 'en':
            ones = self.ones_en
            tens = self.tens_en
            hundreds = self.hundreds_en
            thousands = self.thousands_en
        else:
            raise ValueError("Language must be either 'fa' for Persian or 'en' for English.")

        def convert_hundreds(n):
            if n == 0:
                return ""
            elif n < 10:
                return ones[n]
            elif n < 100:
                return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")
            else:
                return hundreds[n // 100] + (" " + convert_hundreds(n % 100) if n % 100 != 0 else "")

        def convert_group(n, idx):
            if n == 0:
                return ""
            return convert_hundreds(n) + " " + thousands[idx] if idx > 0 else convert_hundreds(n)

        if num == 0:
            return "zero" if self.language == 'en' else "صفر"
        
        result = ""
        idx = 0
        while num > 0:
            result = convert_group(num % 1000, idx) + (" " + result if result else "")
            num //= 1000
            idx += 1
            if idx >= len(thousands):
                thousands.append(f"10^{3*idx}")
        
        return result.strip()

