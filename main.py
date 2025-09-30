#from config.config import LLM_PARAMS
from interview.interview import TechnicalInterview
from langchain_openai import ChatOpenAI  # Change this import
import sys
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from dotenv import load_dotenv


# Directly assign the OpenAI API key
OPENAI_API_KEY = "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"
# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")


def main():
    # ANSI escape code for bold and black text
    cyan = "\033[36m"  # Cyan color
    reset = "\033[0m"  # Reset color
    
    print(f"\n{cyan}Enter the topic for the interview (e.g., JavaScript, Python, etc.): {reset}")

    topic = input()
    #print(OPENAI_API_KEY)
    # Initialize the interview system
    interview = TechnicalInterview(OPENAI_API_KEY)

    # Start the interview process
    interview.start_interview(topic)

if __name__ == "__main__":
    main()