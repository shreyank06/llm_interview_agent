from config.config import LLM_PARAMS
from interview.interview import TechnicalInterview
from utils.vector_store import load_faiss_vector_store
from langchain_openai import ChatOpenAI  # Change this import
import sys
import warnings

# Directly assign the OpenAI API key
OPENAI_API_KEY = "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"
# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")


def main():
    # Initialize the LLM (Language Model) - Use ChatOpenAI instead of OpenAI
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  # or "gpt-4" if you have access
        temperature=LLM_PARAMS['temperature'], 
        openai_api_key=OPENAI_API_KEY
    )
    
    topic = input("Enter the topic for the interview (e.g., JavaScript, Python, etc.): ")

    try:
        # Load the FAISS vector store for questions (or create a new one)
        vector_store, faiss_index = load_faiss_vector_store(topic, OPENAI_API_KEY)
    except ValueError as e:
        # Print the error message without traceback
        print(str(e))
        sys.exit(1)

    # Initialize the interview system
    interview = TechnicalInterview(llm, vector_store, faiss_index, OPENAI_API_KEY)

    # Start the interview process
    interview.start_interview(topic)

if __name__ == "__main__":
    main()