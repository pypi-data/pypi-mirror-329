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

        self.client = None  # Generic client instance

        # Detect provider automatically but do not expose it
        if "gsk_" in self.api_key:  # Example pattern for Groq API keys
            self.client = Groq(api_key=self.api_key)

        elif "sk-" in self.api_key:  # Example pattern for DeepSeek API keys
            self.client = OpenAI(api_key=self.api_key, base_url=base_url or "https://api.deepseek.com")

        if not self.client:
            raise ValueError("Unable to determine provider from the API key. Please check the key format.")

    def get_client(self):
        """
        Get the client instance without exposing the provider name.

        Returns:
            The initialized client.
        """
        return self.client
