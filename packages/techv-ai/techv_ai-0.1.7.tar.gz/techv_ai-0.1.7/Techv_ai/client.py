import os 
from groq import Groq
from Techv_ai.routeing import query_router, query_complexity_score, load_model_config

class techvai_client:
    """
    A flexible client for interacting with different LLM providers such as Groq or DeepSeek.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the client with automatic provider detection.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the environment variables.")

        self.client = None
        self.models = load_model_config()  # Load models from config file
        self.query_router = query_router(api_key=self.api_key, models=self.models)
        self.complexity_scorer = query_complexity_score(api_key=self.api_key)

        if "gsk_" in self.api_key:
            self.client = Groq(api_key=self.api_key)
        elif "sk-" in self.api_key:
            self.client = Groq(api_key=self.api_key, base_url=base_url or "https://api.deepseek.com")

        if not self.client:
            raise ValueError("Unable to determine provider from the API key. Please check the key format.")

    def route_query(self, question: str, override: str = "no", purpose: str = "default"):
        """
        Routes queries based on complexity scoring and override settings.

        Args:
            question (str): User's query.
            override (str): "yes" to enable complexity-based routing, "no" to use the default model.
            purpose (str): Purpose category for routing, e.g., "learning", "client", "research".

        Returns:
            Dict: Response from the selected model.
        """
        if override.lower() == "yes":
            return self.query_router.routeing(question, self.complexity_scorer, override, purpose)
        else:
            # Default to a predefined model category (e.g., "moderate")
            category = "moderate"
            default_model = list(self.models.get(category, {}).keys())[0]  # Select first available model
            return self.query_router.generate_answer(question, default_model, category)
