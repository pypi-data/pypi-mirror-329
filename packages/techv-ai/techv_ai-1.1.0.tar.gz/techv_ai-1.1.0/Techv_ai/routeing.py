import os
import json
import time
import re
import numpy as np
from typing import Tuple, Dict
from groq import Groq

# Load model configuration from environment variable

def load_model_config():
    file_path = os.getenv("FILE_PATH")
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading model config: {e}")
        return {}

# Query Complexity Scoring Class

class Query_complexity_score:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
 
    def get_scores(self, question: str) -> Tuple[float, float, float]:
        prompt = f"""
        You are an AI system trained to assess the complexity of a given question.
        Evaluate the following question and distribute a probability score across three categories: Simple, Moderate, and Complex.
        Question: {question}  
        Scoring Guidelines: 
        - Assign values between 0 and 1 to each category.  
        - Ensure the sum of all values is exactly 1.  
        - Respond strictly in the format: Simple: <number>, Moderate: <number>, Complex: <number>.  
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_completion_tokens=50 
            )

            model_response = chat_completion.choices[0].message.content
            scores = re.findall(r"(?:Simple|Moderate|Complex):\s*(\d*\.?\d+)", model_response)
            if len(scores) != 3:
                raise ValueError("Invalid response format from Groq API")
            return tuple(float(score) for score in scores)

        except Exception as e:
            print(f"Error during scoring: {e}")
            return (0.33, 0.33, 0.34)  # Default fallback values

# Query Router Class

class query_router:
    SYSTEM_PROMPT = """
    Ensure the response follows a professional structure:
    - Proper formatting (headings, bullet points)
    - Removal of redundant phrases
    - Ensuring factual correctness
    - Tone must be neutral and professional
    """
    
    def __init__(self, api_key: str, models: Dict[str, Dict[str, Dict[str, float]]]):
        self.models = models
        self.client = Groq(api_key=api_key)
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x)) 
        return exp_x / exp_x.sum()
    
    def generate_answer(self, question: str, model: str, category: str) -> Dict:
        try:
            start_time = time.time()

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                model=model,
                temperature=0.6,
                max_completion_tokens=4096
            )

            end_time = time.time()
            response_time = end_time - start_time 
            response_text = chat_completion.choices[0].message.content
            total_tokens = chat_completion.usage.total_tokens
            model_stats = self.models[category][model]
            estimated_speed = total_tokens / response_time
            estimated_cost = (total_tokens / 1_000_000) * (
                model_stats["input_cost_per_million"] + model_stats["output_cost_per_million"]
            )

            return {
                "model": model,
                "response": response_text,
                "tokens_used": total_tokens,
                "response_time": round(response_time, 3),
                "estimated_speed": round(estimated_speed, 2), 
                "estimated_cost": round(estimated_cost, 3)
            }
        except Exception as e:
            return {"error": f"Error generating response: {e}"}

    def select_best_model(self, complexity_scores: tuple, allowed_categories: list, k=3) -> str:
        simple_score, moderate_score, complex_score = complexity_scores
        if "simple" in allowed_categories and simple_score > max(moderate_score, complex_score):
            category = "simple"
        elif "moderate" in allowed_categories and moderate_score > max(simple_score, complex_score):
            category = "moderate"
        else:
            category = "complex"
        
        models = self.models[category]
        model_names = list(models.keys())
        speeds = np.array([models[m]["tokens_per_second"] for m in model_names])
        costs = np.array([models[m]["input_cost_per_million"] for m in model_names])
        speed_probs = self.softmax(speeds)
        cost_probs = self.softmax(-costs)
        final_probs = 0.3 * speed_probs + 0.7 * cost_probs  
        selected_model = model_names[np.argmax(final_probs)]
        return selected_model

    def routeing(self, question: str, complexity_scorer: 'Query_complexity_score', override: str, purpose: str) -> Dict:
        if override.lower() == "no":
            category = "moderate"
            selected_model = list(self.models[category].keys())[0]  
        else:
            complexity_scores = complexity_scorer.get_scores(question)
            allowed_categories = {
                "learning": ["simple", "moderate"],
                "client": ["moderate", "complex"],
                "research": ["moderate", "complex"],
            }.get(purpose.lower(), ["moderate"])
            
            selected_model = self.select_best_model(complexity_scores, allowed_categories)
            category = next((cat for cat in allowed_categories if selected_model in self.models.get(cat, {})), "moderate")
        
        response_data = self.generate_answer(question, selected_model, category)
        return response_data

# API Integration

def query_router(api_key: str):
    models = load_model_config()
    return query_router(api_key=api_key, models=models)
