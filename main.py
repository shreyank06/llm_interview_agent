#from config.config import LLM_PARAMS
from interview.interview import TechnicalInterview
from utils.vector_store import load_faiss_vector_store
from langchain_openai import ChatOpenAI  # Change this import
import sys
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)


# Directly assign the OpenAI API key
OPENAI_API_KEY = "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"
# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")


def main():
    # ANSI escape code for bold and black text
    cyan = "\033[36m"  # Cyan color
    reset = "\033[0m"  # Reset color


    # Initialize the LLM (Language Model) - Use ChatOpenAI instead of OpenAI
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  # or "gpt-4" if you have access
        temperature=0.7, 
        openai_api_key=OPENAI_API_KEY
    )
    
    print(f"\n{cyan}Enter the topic for the interview (e.g., JavaScript, Python, etc.): {reset}")


    topic = input()

    try:
        # Load the FAISS vector store for questions (or create a new one)
        vector_store, faiss_index = load_faiss_vector_store(topic, OPENAI_API_KEY)
    except ValueError as e:
        # Print the error message without traceback
        print(str(e))
        sys.exit(1)

    #print(vector_store, faiss_index)
    #sys.exit(0)

    # Initialize the interview system
    interview = TechnicalInterview(llm, vector_store, faiss_index, OPENAI_API_KEY)

    # Start the interview process
    interview.start_interview(topic)

if __name__ == "__main__":
    main()