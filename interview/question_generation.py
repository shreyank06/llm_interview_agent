import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
import sys
import warnings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI




warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

class QuestionGenerator:
    def __init__(self, llm, openai_api_key=None):
        self.llm = llm
        self.openai_api_key = openai_api_key
        
    def generate_dynamic_questions(self, topic, questions_list, evaluation_list=None, agent=None, openai_api_key=None):
        """
        Use GPT to generate dynamic interview questions for the given topic.
        :param topic: The topic for the interview (e.g., JavaScript, Python, AI, etc.)
        :param num_questions: The number of questions to generate (default 3, but will always return 1).
        :param evaluation_list: Previous evaluations to provide context (optional).
        :param agent: The agent to use for question generation.
        :return: A list containing a single generated question.
        """
        if agent is None:
            raise ValueError("Agent parameter is required")
        
        # Build history context from evaluation_list
        history_context = ""
        if evaluation_list:
            history_context = f"Previous interview context: {' '.join(evaluation_list)}\n\n"
        
        #print(topic)
        prompt = PromptTemplate(
        input_variables=["topic", "history_context", "questions_list"],
        template="Based on historical evaluation of the candidate {history_context} as a reference to determine next question's difficulty," \
        "Generate one interview question on {topic}. " \
        "Only provide one technical questions related to {topic} at a time. No more than one question. " \
        "Do not repeat questions already asked in {questions_list}.")

        #print(OPENAI_API_KEY)
        llm_chain = LLMChain(
        llm=OpenAI(temperature=0.7, openai_api_key=openai_api_key),
        prompt=prompt)
        
        result = llm_chain.run({"topic": topic, "history_context": history_context, "questions_list": questions_list})
        questions = result.split("\n")
        question = questions[0].replace("Question: ", "").strip()
        print(question)

        return [q.strip() for q in questions if q.strip()]  # Clean up any empty entries

