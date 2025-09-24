from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from interview.question_generation import QuestionGenerator
from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool, AgentType
import sys

class TechnicalInterview:
    def __init__(self, llm, vector_store=None, faiss_index=None, OPENAI_API_KEY=None):
        self.llm = llm
        self.vector_store = vector_store
        self.faiss_index = faiss_index  # New line to store the FAISS index
        self.OPENAI_API_KEY = OPENAI_API_KEY
        # print(self.OPENAI_API_KEY)
        # sys.exit()
        self.question_generator = QuestionGenerator(llm, vector_store, self.faiss_index, self.OPENAI_API_KEY)
        
        # Define evaluation tools using LangGraph
        self.tools = [
            Tool(
                name="clarity_tool",
                func=self.evaluate_clarity,
                description="Evaluate the clarity of the answer"
            ),
            Tool(
                name="accuracy_tool",
                func=self.evaluate_accuracy,
                description="Evaluate the accuracy of the answer"
            ),
            Tool(
                name="depth_tool",
                func=self.evaluate_depth,
                description="Evaluate the depth of the answer"
            )
        ]
        
        self.agent = create_react_agent(
            model=self.llm,  # Use the GPT-4 model name
            tools=self.tools,
            prompt="You are a helpful assistant conducting a technical interview"
        )

    def start_interview(self, topic):
        print(f"Starting interview on {topic}...\n")
        
        for i in range(3):  # Ask 3 questions in total
            question = self.ask_question(topic)
            print(f"Question {i+1}: {question}")
            answer = input("Your answer: ")

            # Use LangGraph's agent to evaluate the answer
            evaluation = self.agent.invoke(
                {"messages": [{"role": "user", "content": answer}]}
            )
            
            # Extract and print the AI's content from the evaluation
            ai_message = evaluation['messages'][-1].content  # Get the content of the AI's last message
            print(f"\nAI's Response: {ai_message}")

            # Provide feedback based on evaluation
            feedback = self.provide_feedback(evaluation)
            print("Feedback for your answer:")
            print(feedback)

            # Adjust the topic based on evaluation (dynamic branching)
            topic = self.adjust_topic_based_on_answer(evaluation)

        # Summarize the performance after 3 questions
        self.summarize_performance()


    def ask_question(self, topic):
        # Attempt to retrieve questions from vector store or generate dynamically
        if self.vector_store:
            # Retrieve question(s) from vector store (assuming it's a list)
            question = self.vector_store[0]  # Choose the first question from vector store
        else:
            # Generate a dynamic question based on the topic
            question = self.question_generator.generate_dynamic_question(topic)
        return question

    def provide_feedback(self, evaluation):
        """Provide feedback based on the evaluation"""
        # Provide clear feedback based on evaluation (clarity, accuracy, depth)
        feedback = []
        clarity = evaluation.get("clarity", 0)
        accuracy = evaluation.get("accuracy", 0)
        depth = evaluation.get("depth", 0)

        feedback.append(f"Clarity: {clarity}/10")
        feedback.append(f"Accuracy: {accuracy}/10")
        feedback.append(f"Depth: {depth}/10")

        return "\n".join(feedback)

    def adjust_topic_based_on_answer(self, evaluation):
        """Adjust topic based on the evaluation"""
        # Adjust topic dynamically based on the clarity, accuracy, and depth scores
        clarity = evaluation.get("clarity", 0)
        accuracy = evaluation.get("accuracy", 0)
        depth = evaluation.get("depth", 0)

        if clarity < 4:
            return "Beginner-level questions (focus on clarity)"
        elif accuracy < 5:
            return "Intermediate-level questions (focus on accuracy)"
        elif depth < 6:
            return "Intermediate-level questions (focus on depth)"
        else:
            return "Advanced-level topics"

    def summarize_performance(self):
        """Summarize overall performance after the interview"""
        print("\nInterview performance summary:")
        # Here, you can add logic to summarize the total scores or performance over the 3 questions
        print("Performance summary will be based on the feedback scores.")

    def print_evaluation(self, evaluation):
        """Print the evaluation content (clarity, accuracy, depth) in a readable format"""
        clarity = evaluation.get("clarity", 0)
        accuracy = evaluation.get("accuracy", 0)
        depth = evaluation.get("depth", 0)
        
        # Printing the evaluation results in a readable format
        print(f"Clarity: {clarity}/10")
        print(f"Accuracy: {accuracy}/10")
        print(f"Depth: {depth}/10")

    # Example of evaluation functions that will be used by LangGraph tools
    def evaluate_clarity(self, answer):
        """Evaluate the clarity of the answer"""
        return len(answer.split())  # Simple clarity check: word count

    def evaluate_accuracy(self, answer):
        """Evaluate the accuracy of the answer"""
        return 8 if "correct" in answer else 4  # Basic accuracy check for demo purposes

    def evaluate_depth(self, answer):
        """Evaluate the depth of the answer"""
        return 6 if len(answer.split()) > 5 else 3  # Basic depth check for demo purposes
