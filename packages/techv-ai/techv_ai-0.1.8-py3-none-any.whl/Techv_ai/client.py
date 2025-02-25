import os
from openai import OpenAI
from groq import Groq

class techvai_client:
    """
    A flexible client for interacting with different LLM providers such as Groq or DeepSeek.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the client by automatically detecting the provider from the API key.

        Args:
            api_key (str, optional): The API key for the provider. If not provided, it will be fetched from environment variables.
            base_url (str, optional): The base URL for DeepSeek if applicable.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the environment variables.")
        
        self.provider = self.detect_provider()
        self.client = self.initialize_client(base_url)
    
    def detect_provider(self) -> str:
        """
        Detect the provider based on the API key format.

        Returns:
            str: The detected provider name ("groq" or "deepseek").
        """
        if "gsk_" in self.api_key:
            return "groq"
        elif "sk-" in self.api_key:
            return "deepseek"
        else:
            raise ValueError("Unable to determine provider from the API key. Please check the key format.")
    
    def initialize_client(self, base_url: str = None):
        """
        Initialize the client instance based on the detected provider.

        Args:
            base_url (str, optional): The base URL for DeepSeek API.

        Returns:
            The initialized client instance.
        """
        if self.provider == "groq":
            return Groq(api_key=self.api_key)
        elif self.provider == "deepseek":
            return OpenAI(api_key=self.api_key, base_url=base_url or "https://api.deepseek.com")
        else:
            raise ValueError("Invalid provider detected.")
    
    def get_client(self):
        """
        Get the client instance without exposing the provider name.

        Returns:
            The initialized client.
        """
        return self.client
