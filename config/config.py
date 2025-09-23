import os

# Example API key configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Assuming you store the API key in environment variables

# LLM configuration
LLM_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 150
}
