from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from interview.question_generation import QuestionGenerator
from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool, AgentType
import sys
import re
from interview.branching_logic import BranchingLogic
from interview.answer_evaluation import AnswerEvaluator

class TechnicalInterview:
    def __init__(self, llm, vector_store=None, faiss_index=None, OPENAI_API_KEY=None):
        self.llm = llm
        self.vector_store = vector_store
        self.faiss_index = faiss_index  # New line to store the FAISS index
        self.OPENAI_API_KEY = OPENAI_API_KEY
        # print(self.OPENAI_API_KEY)
        # sys.exit()
        self.question_generator = QuestionGenerator(llm, vector_store, self.faiss_index, self.OPENAI_API_KEY)

        # Initialize agent without predefined tools for evaluation
        self.agent = create_react_agent(
            model=self.llm,  # Use the GPT-4 model name
            tools=[],  # No predefined tools, agent will handle the evaluation based on prompt
            prompt="You are a helpful assistant conducting a technical interview"
        )
        self.branching_logic = BranchingLogic(self.llm)
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0
        self.performance_evaluator = AnswerEvaluator(0, None, self.clarity, self.accuracy, self.depth, self.agent)


    def start_interview(self, topic):
        print(f"Starting interview on {topic}...\n")
        evaluation_list = []
        
        for i in range(3):  # Ask 3 questions in total
            question = self.ask_question(topic, i)
            print(f"Question: {question}")
            answer = input("Your answer: ")

            # Evaluate the answer based on clarity, accuracy, and depth using intelligent evaluation
            evaluation = self.evaluate_answer_intelligently(answer)
            
            # Print the evaluation feedback
            print(f"\nAI's Evaluation: {evaluation}")
            evaluation_list.append(evaluation)

            # Adjust the topic based on evaluation (dynamic branching)
            topic, self.clarity, self.accuracy, self.depth = self.branching_logic.adjust_topic_based_on_answer(evaluation, self.agent, topic)


        # Summarize the performance after 3 questions
        self.performance_evaluator = AnswerEvaluator(i, topic, self.clarity, self.accuracy, self.depth, self.agent)
        self.performance_evaluator.summarize_evaluation()

    def ask_question(self, topic, question_num):
        # Attempt to retrieve questions from vector store or generate dynamically
        if self.vector_store:
            # Retrieve question(s) from vector store (assuming it's a list)
            question = self.vector_store[question_num]  # Choose the first question from vector store
        else:
            # Generate a dynamic question based on the topic
            question = self.question_generator.generate_dynamic_question(topic)
        return question

    def evaluate_answer_intelligently(self, answer):
        """Evaluate the answer using an intelligent agent (GPT-4 or similar)"""
        
        # Define the dynamic prompt for intelligent evaluation
        prompt = f"Evaluate the following answer based on clarity, accuracy, and depth. Please provide scores for each aspect out of 10:\n\nAnswer: '{answer}'\n\nReturn the evaluation in the format: clarity: X, accuracy: X, depth: X and offer personalized feedback as well"
        
        # Invoke the agent to evaluate the answer
        evaluation = self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        
        # Extract and parse the evaluation response
        ai_message = evaluation['messages'][-1].content  # Get the content of the AI's last message
        return ai_message
        # print(ai_message)
        # sys.exit()  # Debugging line to check the AI's response
        #return self.parse_evaluation(ai_message)

