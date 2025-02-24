# currency_to_words/__init__.py

def convert_currency_to_words(amount):
    """Convert a numeric amount to words (Indian numbering system)"""
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_two_digits(n):
        """Convert a number less than 100 to words"""
        if n == 0:
            return ""
        elif n < 20:
            return units[n]
        else:
            return tens[n // 10] + ('' if n % 10 == 0 else ' ' + units[n % 10])

    def convert_three_digits(n):
        """Convert a number less than 1000 to words"""
        if n == 0:
            return ""
        elif n < 100:
            return convert_two_digits(n)
        else:
            return units[n // 100] + " Hundred" + ('' if n % 100 == 0 else ' ' + convert_two_digits(n % 100))

    def num_to_words(n):
        """Convert a number to words for Indian currency system"""
        if n == 0:
            return "Zero"

        crore = n // 10000000
        n %= 10000000

        lakh = n // 100000
        n %= 100000

        thousand = n // 1000
        n %= 1000

        hundred = n

        words = []
        if crore > 0:
            words.append(convert_two_digits(crore) + " Crore")
        if lakh > 0:
            words.append(convert_two_digits(lakh) + " Lakh")
        if thousand > 0:
            words.append(convert_two_digits(thousand) + " Thousand")
        if hundred > 0:
            words.append(convert_three_digits(hundred))

        return ' '.join(words).strip()

    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    rupees_in_words = num_to_words(rupees)

    if paise > 0:
        paise_in_words = num_to_words(paise)
        return f"{rupees_in_words} Rupees and {paise_in_words} Paise"
    else:
        return f"{rupees_in_words} Rupees"
