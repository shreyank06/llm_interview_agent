from config.config import OPENAI_API_KEY, LLM_PARAMS
from interview.interview import TechnicalInterview
from utils.vector_store import load_vector_store
from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import sys

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

def main():
    # Initialize the LLM (Language Model)
    llm = OpenAI(temperature=LLM_PARAMS['temperature'], openai_api_key=OPENAI_API_KEY)
    
    # Load the vector store for questions (or create a new one)
    vector_store = load_vector_store()

    # Initialize the interview system
    interview = TechnicalInterview(llm, vector_store)

    # Start the interview process
    topic = input("Enter the topic for the interview (e.g., JavaScript, Python, etc.): ")
    interview.start_interview(topic)

if __name__ == "__main__":
    main()
