# French Public Holidays

A Python library for handling French public holidays.

## Installation

```bash
pip install french-public-holidays
```

## Usage

```python
from french_public_holidays import FrenchPublicHolidays

fph = FrenchPublicHolidays()

# Check if a date is a French public holiday
is_holiday = fph.is_holiday('2023-07-14')
print(is_holiday)  # True (Bastille Day)

# Get the name of the holiday
holiday_name = fph.get_holiday_name('2023-07-14')
print(holiday_name)  # 'Fête nationale'

# Get all holidays for a specific year
holidays_2023 = fph.get_holidays(2023)
print(holidays_2023)
```

### CLI

The library also comes with a CLI tool that can be used for extract public holidays in export file.

```bash
python -m french_public_holidays -c .\config.yaml
```

or

```bash
french-public-holidays --config .\config.yaml
```


## Features

- Accurately calculates French public holidays including moveable ones (Easter Monday, Ascension Day, etc.)
- Handles regional specifics (Alsace-Moselle, DOM-TOM)
- Works with date strings

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions or need support, please open an issue on the GitHub repository.