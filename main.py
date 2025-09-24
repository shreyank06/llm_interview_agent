from config.config import LLM_PARAMS
from interview.interview import TechnicalInterview
from utils.vector_store import load_faiss_vector_store  # Assuming you create this function
from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import sys
import warnings

# Directly assign the OpenAI API key
OPENAI_API_KEY = "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"

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")


def main():
    # Initialize the LLM (Language Model)
    llm = OpenAI(temperature=LLM_PARAMS['temperature'], openai_api_key=OPENAI_API_KEY)
    
    topic = input("Enter the topic for the interview (e.g., JavaScript, Python, etc.): ")

    try:
        # Load the FAISS vector store for questions (or create a new one)
        vector_store, faiss_index = load_faiss_vector_store(topic, OPENAI_API_KEY)  # Adjust this function to load FAISS index
    except ValueError as e:
        # Print the error message without traceback
        print(str(e))
        sys.exit(1)  # Exit the program or handle the error as required

    # Initialize the interview system
    interview = TechnicalInterview(llm, vector_store, faiss_index, OPENAI_API_KEY)

    # Start the interview process
    interview.start_interview(topic)

if __name__ == "__main__":
    main()
