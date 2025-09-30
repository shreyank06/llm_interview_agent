#from config.config import LLM_PARAMS
from interview.interview import TechnicalInterview
from langchain_openai import ChatOpenAI  # Change this import
import sys
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from dotenv import load_dotenv
import os

# Directly assign the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

    # Initialize the interview system
    interview = TechnicalInterview(llm, OPENAI_API_KEY)

    # Start the interview process
    interview.start_interview(topic)

if __name__ == "__main__":
    main()