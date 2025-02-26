#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import httpx

try:
    from .config_manager import ConfigurationManager
    from .exceptions import YearInTheFutureException, YearInThePastException
    from .output import Output
    from .settings import Settings
except ImportError:
    from config_manager import ConfigurationManager
    from exceptions import YearInTheFutureException, YearInThePastException
    from output import Output
    from settings import Settings

class FrenchPublicHolidays:
    """
    FrenchPublicHolidays is a class that manages the retrieval and storage of French public holidays.

    Attributes:
        _settings (Settings): An instance of the Settings class containing configuration settings.
        _config (ConfigurationManager): An instance of the ConfigurationManager class for managing configuration.
        kwargs (dict): Additional keyword arguments.
        zone (str): The zone for which to retrieve public holidays.
        args (dict): A dictionary containing parsed command-line arguments and configuration data.
        french_public_holidays (list): A list to store the retrieved French public holidays.

    Methods:
        get_args():
            Returns a dictionary containing the configuration data.
        get_french_public_holidays():
            Returns a list of dictionaries containing public holiday data for each year in the specified range.
        get_public_holidays(url, years):
            Returns the HTTP response object containing the public holidays data.
        save_french_public_holidays(french_public_holidays):
            Returns None.
        set_zone(url, zone):
            Returns the formatted URL with the zone inserted.
    """

    def __init__(self, settings: Settings = Settings(), **kwargs):
        self._settings = settings
        self._config = ConfigurationManager(kwargs)
        self.args = self._get_args().get("french_public_holidays")
        self.french_public_holidays: list = []
        self.url = self._settings.URL.format(self.args.get("zone"), "{0}")

    def _get_args(self):
        """
        Parses command-line arguments and loads configuration settings.
        This method adds arguments for output file, duration, and zone to the argument parser,
        parses the arguments, loads the configuration file, and sets configuration values
        for the 'french_public_holidays' section.

        Returns:
            dict: A dictionary containing the configuration data.
        """
        self._config.add_argument("--duration", "-d", help="Duration in years")
        self._config.add_argument("--output", "-o", help="Output file")
        self._config.add_argument("--year", "-y", help="Starting year")
        self._config.add_argument("--zone", "-z", help="Zone", choices=["alsace-moselle", "guadeloupe", "guyane", "la-reunion", "martinique", "mayotte", "metropole", "nouvelle-caledonie", "polynesie-francaise", "saint-barthelemy", "saint-martin", "saint-pierre-et-miquelon", "wallis-et-futuna"])
        args = self._config.parser.parse_args()

        self._config.load_config_file(args.config)
        self._config.set_config(section="french_public_holidays", key="duration", env_key="FRENCH_PUBLIC_HOLIDAYS_DURATION", default=1)
        self._config.set_config(section="french_public_holidays", key="output", env_key="FRENCH_PUBLIC_HOLIDAYS_OUTPUT", default="french_public_holidays.csv")
        self._config.set_config(section="french_public_holidays", key="year", env_key="FRENCH_PUBLIC_HOLIDAYS_YEAR", default=datetime.date.today().year)
        self._config.set_config(section="french_public_holidays", key="zone", env_key="FRENCH_PUBLIC_HOLIDAYS_ZONE", default="metropole")
        self.validate(self._config.config_data.get("french_public_holidays"))

        return self._config.config_data

    def get_french_public_holidays(self):
        """
        Retrieves French public holidays for a specified range of years.

        This method fetches public holidays for a given zone and duration starting from a specified year.
        The holidays are retrieved from an external API and stored in a list.

        Returns:
            list: A list of dictionaries containing public holiday data for each year in the specified range.
        """

        self.french_public_holidays: list = []
        for year in range(int(self.args.get("year")), int(self.args.get("year")) + int(self.args.get("duration"))):
            self.french_public_holidays.append(self.get_public_holidays(year).json())
        return self.french_public_holidays

    def get_public_holidays(self, years):
        """
        Fetches public holidays for the specified years from the given URL.

        Args:
            years (int): The year for which to fetch the public holidays.

        Returns:
            Response: The HTTP response object containing the public holidays data.
        """
        return httpx.get(self.url.format(years))

    def get_public_holiday(self, date):
        """
        Fetches the description of public holidays for the specified years from the given URL.

        Args:
            url (str): The URL to fetch the public holidays from. The URL should contain a placeholder for the year.
            years (int): The year for which to fetch the public holidays.

        Returns:
            str: The description of the public holiday.
        """
        day = datetime.datetime.strptime(date, "%Y-%m-%d")
        year = day.year
        public_holidays = self.get_public_holidays(year).json()
        return public_holidays.get(day.strftime("%Y-%m-%d"))

    def is_public_holiday(self, date):
        """
        Checks if the specified date is a public holiday.

        Args:
            date (datetime.date): The date to check.

        Returns:
            bool: True if the date is a public holiday, False otherwise.
        """
        return self.get_public_holiday(date) is not None

    def save_french_public_holidays(self, french_public_holidays):
        """
        Saves the provided list of French public holidays to the specified output.

        Args:
            french_public_holidays (list): A list of dictionaries, each representing a French public holiday.

        Returns:
            None
        """
        output = Output(self._settings.HEADERS, self.args.get("output"))
        output.save(french_public_holidays)

    def validate(self, args):
        """
        Validates the given arguments to ensure that the year is within a valid range.

        Args:
            args (dict): A dictionary containing the year and duration as keys.

        Raises:
            YearInThePastException: If the year is more than 20 years in the past.
            YearInTheFutureException: If the year is more than 5 years in the future.
        """
        if datetime.date.today().year - int(args.get("year")) > 20:
            raise YearInThePastException("The year cannot exceed 20 years in the past.")
        elif datetime.date.today().year + 5 < int(args.get("year")) + int(args.get("duration")):
            raise YearInTheFutureException("The year cannot exceed 5 years in the future.")

    def get_duration(self):
        return self.args.get("duration")

    def get_output(self):
        return self.args.get("output")

    def get_year(self):
        return self.args.get("year")

    def get_zone(self):
        return self.args.get("zone")

    def set_duration(self, duration):
        self.args["duration"] = duration

    def set_output(self, output):
        self.args["output"] = output

    def set_year(self, year):
        self.args["year"] = year

    def set_zone(self, zone):
        self.args["zone"] = zone
        self.url = self._settings.URL.format(zone, "{0}")