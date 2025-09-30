from interview.question_generation import QuestionGenerator
from interview.branching_logic import BranchingLogic
from interview.answer_evaluation import AnswerEvaluator
from colorama import Fore, Style, init
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import sys

class TechnicalInterview:
    def __init__(self, OPENAI_API_KEY=None):
       # self.llm = llm
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.question_generator = QuestionGenerator(self.OPENAI_API_KEY)
        #print(self.OPENAI_API_KEY)

        # # Initialize agent without predefined tools for evaluation
        # self.agent = create_react_agent(
        #     model=self.llm,
        #     tools=[],
        #     prompt="You are a helpful assistant conducting a technical interview"
        #)
        self.branching_logic = BranchingLogic()
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0
        self.performance_evaluator = AnswerEvaluator(0, None, self.clarity, self.accuracy, self.depth, self.OPENAI_API_KEY)

    def start_interview(self, topic):
        # Starting the interview with clear formatting
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Starting interview on '{topic}'...{Style.RESET_ALL}\n")
        
        evaluation_list = []
        question_list = []

        for i in range(5):  # Ask 3 questions in total
            print(f"\n{Fore.CYAN}{Style.BRIGHT}--- Question {i + 1} ---{Style.RESET_ALL}")
            
            question = self.ask_question(topic, i, evaluation_list, question_list)
            #print(question)
            cleaned_question = self.remove_text_from_question(question[0])
            #print(cleaned_question)
            topic = None
            #print(question)
            question_list.append(question)
            print(f"{Fore.GREEN}{Style.BRIGHT}Question:{Style.RESET_ALL} {Fore.WHITE}{cleaned_question}{Style.RESET_ALL}")
            
            answer = input(f"{Fore.MAGENTA}{Style.BRIGHT}Your answer: {Style.RESET_ALL}")
            
            # Evaluate the answer based on clarity, accuracy, and depth
            evaluation = self.evaluate_answer_intelligently(question, answer)
            
            # Display evaluation feedback clearly after the answer
            #print(f"\n{Fore.YELLOW}{Style.BRIGHT}AI's Evaluation: {Style.RESET_ALL}\n{Fore.WHITE}{evaluation}{Style.RESET_ALL}")
            evaluation_list.append(evaluation)

            # Adjust the topic based on evaluation (dynamic branching)
            topic, self.clarity, self.accuracy, self.depth = self.branching_logic.adjust_topic_based_on_answer(evaluation, self.OPENAI_API_KEY)
            # Optionally show the adjusted topic for next question
            #print(f"{Fore.CYAN}{Style.BRIGHT}Topic for next question: {topic}{Style.RESET_ALL}\n")

        # Summarize the performance after 3 questions
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Interview Complete ---{Style.RESET_ALL}\n")
        
        # Use performance evaluator to summarize and color the evaluation
        self.performance_evaluator = AnswerEvaluator(i, topic, self.clarity, self.accuracy, self.depth, self.OPENAI_API_KEY)
        self.performance_evaluator.summarize_evaluation()

    def ask_question(self, topic, question_num, evaluation_list, question_list=None):
        """Ask a question using the QuestionGenerator"""
        question = self.question_generator.generate_dynamic_questions(topic, question_list, evaluation_list, self.OPENAI_API_KEY)
        #print(question)
        return question

    def evaluate_answer_intelligently(self,question, answer):
        """Evaluate the answer using an intelligent agent (GPT-4 or similar)"""
        #prompt = f"Evaluate the following answer based on clarity, accuracy, and depth. Please provide scores for each aspect out of 10:\n\nAnswer: '{answer}'\n\nReturn the evaluation in the format: clarity: X, accuracy: X, depth: X and offer personalized feedback as well"
                
        prompt = PromptTemplate(
            input_variables=["question", "answer"],
            template="You are a technical interviewer evaluating a candidate's response. The question asked was: '{question}'. The candidate's answer was: '{answer}'. Evaluate the answer based on clarity, accuracy, and depth. Please provide scores for each aspect out of 10. The score should reflect the answer's quality **relative to the question**. A simple 'no' or 'yes' should score low on depth and accuracy if it's not a complete answer. Return the evaluation in the format: clarity: X, accuracy: X, depth: X. Also, offer personalized feedback for improvement."
        )
        llm_chain = LLMChain(
            llm=OpenAI(temperature=0.7, openai_api_key=self.OPENAI_API_KEY),
            prompt=prompt
        )   
        evaluation = llm_chain.run({"question":question, "answer": answer})

        return evaluation   
    
    def remove_text_from_question(self, question):
        """Remove 'Question: ' prefix from the question string"""
        prompt = PromptTemplate(
            input_variables=["question"],
            template="Remove all the prefix from the following question if it exists or any other text apart from the question. Return only the cleaned question.\n\nQuestion: {question}"
        )
        llm_chain = LLMChain(
            llm=OpenAI(temperature=0.7, openai_api_key=self.OPENAI_API_KEY),
            prompt=prompt
        )   
        cleaned_question = llm_chain.run({"question": question})
        return cleaned_question.strip()
