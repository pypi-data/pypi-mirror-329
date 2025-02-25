import os
from typing import List, Dict
from openai import OpenAI
from groq import Groq



class techvai_chat:
    """
    A chat interface for interacting with LLM providers via the client.
    """

    def __init__(self, client):
        """
        Initialize the chat interface.

        Args:
            client: A generic LLM API client instance.
        """
        if not hasattr(client, "chat"): 
            raise ValueError("Invalid client instance. Ensure it supports chat functionality.")
        self.client = client

    def chat(self, 
             messages: List[Dict[str, str]], 
             model: str, 
             temperature: float = 0.6, 
             max_tokens: int = 4096, 
             top_p: float = 0.9, 
             stream: bool = False):
        """
        Send a chat request to the LLM provider.

        Args:
            messages (list): List of message dictionaries in the format [{"role": "user", "content": "Hello"}].
            model (str): The model to use.
            temperature (float): Sampling temperature (default: 0.6).
            max_tokens (int): Maximum number of tokens to generate (default: 1024).
            top_p (float): Top-p sampling parameter (default: 0.9).
            stream (bool): Whether to stream the response (default: False).

        Returns:
            The response from the LLM provider.
        """
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
        )
