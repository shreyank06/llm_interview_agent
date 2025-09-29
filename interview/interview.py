from interview.question_generation import QuestionGenerator
from langgraph.prebuilt import create_react_agent
from interview.branching_logic import BranchingLogic
from interview.answer_evaluation import AnswerEvaluator
from colorama import Fore, Style, init
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import sys

class TechnicalInterview:
    def __init__(self, llm, vector_store=None, faiss_index=None, OPENAI_API_KEY=None):
        self.llm = llm
        self.vector_store = vector_store
        self.faiss_index = faiss_index  # New line to store the FAISS index
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.question_generator = QuestionGenerator(llm, vector_store, self.faiss_index, self.OPENAI_API_KEY)

        # Initialize agent without predefined tools for evaluation
        self.agent = create_react_agent(
            model=self.llm,
            tools=[],
            prompt="You are a helpful assistant conducting a technical interview"
        )
        self.branching_logic = BranchingLogic(self.llm, self.OPENAI_API_KEY)
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0
        self.performance_evaluator = AnswerEvaluator(0, None, self.clarity, self.accuracy, self.depth, self.agent, self.OPENAI_API_KEY)

    def start_interview(self, topic):
        # Starting the interview with clear formatting
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Starting interview on '{topic}'...{Style.RESET_ALL}\n")
        
        evaluation_list = []
        question_list = []

        for i in range(5):  # Ask 3 questions in total
            print(f"\n{Fore.CYAN}{Style.BRIGHT}--- Question {i + 1} ---{Style.RESET_ALL}")
            
            question = self.ask_question(topic, i, evaluation_list, question_list)
            topic = None
            question_list.append(question)
            print(f"{Fore.GREEN}{Style.BRIGHT}Question:{Style.RESET_ALL} {Fore.WHITE}{question[0]}{Style.RESET_ALL}")
            
            answer = input(f"{Fore.MAGENTA}{Style.BRIGHT}Your answer: {Style.RESET_ALL}")
            
            # Evaluate the answer based on clarity, accuracy, and depth
            evaluation = self.evaluate_answer_intelligently(question, answer)
            
            # Display evaluation feedback clearly after the answer
            #print(f"\n{Fore.YELLOW}{Style.BRIGHT}AI's Evaluation: {Style.RESET_ALL}\n{Fore.WHITE}{evaluation}{Style.RESET_ALL}")
            evaluation_list.append(evaluation)

            # Adjust the topic based on evaluation (dynamic branching)
            topic, self.clarity, self.accuracy, self.depth = self.branching_logic.adjust_topic_based_on_answer(evaluation, self.agent, topic)
            # Optionally show the adjusted topic for next question
            #print(f"{Fore.CYAN}{Style.BRIGHT}Topic for next question: {topic}{Style.RESET_ALL}\n")

        # Summarize the performance after 3 questions
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Interview Complete ---{Style.RESET_ALL}\n")
        
        # Use performance evaluator to summarize and color the evaluation
        self.performance_evaluator = AnswerEvaluator(i, topic, self.clarity, self.accuracy, self.depth, self.agent, self.OPENAI_API_KEY)
        self.performance_evaluator.summarize_evaluation()

    def ask_question(self, topic, question_num, evaluation_list, question_list=None):
        # Attempt to retrieve questions from vector store or generate dynamically
        # if self.vector_store:
        #     # Retrieve question(s) from vector store (assuming it's a list)
        #     question = self.vector_store[question_num]  # Choose the first question from vector store
        # else:
        #     # Generate a dynamic question based on the topic
        question = self.question_generator.generate_dynamic_questions(topic, question_list, evaluation_list, self.agent, self.OPENAI_API_KEY)
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
       # evaluation = eval(evaluation)
        # print(evaluation)
        # sys.exit()

        #evaluation = self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        #ai_message = evaluation['messages'][-1].content  # Get the content of the AI's last message
        return evaluation   
