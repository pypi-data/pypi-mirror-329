from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings class for configuring the French public holidays project.

    Attributes:
        HEADERS (list): A list of headers for the data, default is ["date", "description"].
        URL (str): The URL template for fetching public holidays data, default is "https://calendrier.api.gouv.fr/jours-feries/{0}/{1}.json".
    """
    HEADERS: list = ["date", "description"]
    URL: str = "https://calendrier.api.gouv.fr/jours-feries/{0}/{1}.json"