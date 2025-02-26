try:
    from .french_public_holidays import FrenchPublicHolidays
except ImportError:
    from french_public_holidays import FrenchPublicHolidays

def main():
    fph = FrenchPublicHolidays()
    french_public_holidays = fph.get_french_public_holidays()
    fph.save_french_public_holidays(french_public_holidays)

main()