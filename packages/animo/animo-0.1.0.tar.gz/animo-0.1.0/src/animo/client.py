from .resources.videos import Videos

class Animo:
    """
    Animo client for interacting with the Animo API.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.animo.video"):
        """
        Initialize the Animo client.

        Args:
            api_key (str): Your API key for authentication
            base_url (str, optional): The base URL for the API. 
                Defaults to "https://api.animo.video"
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
        # Initialize resources
        self.videos = Videos(self) 