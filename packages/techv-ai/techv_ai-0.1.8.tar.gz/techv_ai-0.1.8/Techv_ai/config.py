MODELS_CONFIG ={
    "simple": {
        "llama-3.2-1b-preview": { "tokens_per_second": 3100, "input_cost_per_million": 0.04, "output_cost_per_million": 0.04 },
        "llama-3.2-3b-preview": { "tokens_per_second": 1600, "input_cost_per_million": 0.06, "output_cost_per_million": 0.06 },
        "llama-3.1-8b-instant": { "tokens_per_second": 750, "input_cost_per_million": 0.05, "output_cost_per_million": 0.08 },
        "llama3-8b-8192": { "tokens_per_second": 1250, "input_cost_per_million": 0.05, "output_cost_per_million": 0.08 }
    },
    "moderate": {
        "mixtral-8x7b-32768": { "tokens_per_second": 575, "input_cost_per_million": 0.24, "output_cost_per_million": 0.24 },
        "gemma2-9b-it": { "tokens_per_second": 500, "input_cost_per_million": 0.20, "output_cost_per_million": 0.20 }
        
    },
    "complex": {
        "llama-3.3-70b-versatile": { "tokens_per_second": 275, "input_cost_per_million": 0.59, "output_cost_per_million": 0.79 },
        "llama3-70b-8192": { "tokens_per_second": 330, "input_cost_per_million": 0.59, "output_cost_per_million": 0.79 },
        "llama-3.3-70b-specdec": { "tokens_per_second": 1600, "input_cost_per_million": 0.59, "output_cost_per_million": 0.99 }
    }
}