from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from interview.question_generation import QuestionGenerator
from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool, AgentType
import sys
import re

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
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0  

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
            topic = self.adjust_topic_based_on_answer(evaluation)


        # Summarize the performance after 3 questions
        # print(evaluation_list)
        # sys.exit()
        self.summarize_evaluation(evaluation_list, i)

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

    def parse_evaluation(self, evaluation_response):
        """Parse the agent's response to get clarity, accuracy, and depth scores"""
        evaluation = {}
        print(evaluation_response)  # Debugging line to see the raw response
        #sys.exit()  # Debugging line to stop execution and check the response
        # Example response format: "clarity: 8, accuracy: 7, depth: 6"
        parts = evaluation_response.split(',')
        for part in parts:
            criterion, score = part.split(':')
            evaluation[criterion.strip()] = int(score.strip())
        return evaluation

    # def provide_feedback(self, evaluation):
    #     """Provide feedback based on the evaluation"""
    #     clarity = evaluation.get("clarity", 0)
    #     accuracy = evaluation.get("accuracy", 0)
    #     depth = evaluation.get("depth", 0)

    #     feedback = []
    #     feedback.append(f"Clarity: {clarity}/10")
    #     feedback.append(f"Accuracy: {accuracy}/10")
    #     feedback.append(f"Depth: {depth}/10")

    #     return "\n".join(feedback)

    def adjust_topic_based_on_answer(self, evaluation):
        """Adjust topic based on the evaluation already performed by the agent"""
        
        # Define the prompt to extract clarity, accuracy, and depth from the evaluation
        prompt = f"""
        Given the following evaluation, extract the clarity, accuracy, and depth scores as a dictionary with the keys 'clarity', 'accuracy', and 'depth'. The evaluation is already completed by the agent, so just return the scores.

        Evaluation: {evaluation}

        Return the evaluation in this format:
        {{
            "clarity": X,
            "accuracy": X,
            "depth": X
        }}
        """

        # Invoke the agent to parse the evaluation
        evaluation_result = self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        
        # Extract and parse the evaluation response into a dictionary
        ai_message = evaluation_result['messages'][-1].content  # Get the content of the AI's last message

        # Convert the response into a dictionary
        evaluation_dict = eval(ai_message)  # Make sure this is a valid dictionary
        
        # Extract clarity, accuracy, and depth from the evaluation dictionary
        clarity = evaluation_dict.get("clarity", 0)
        accuracy = evaluation_dict.get("accuracy", 0)
        depth = evaluation_dict.get("depth", 0)

        self.clarity = self.clarity + clarity
        self.accuracy = self.accuracy + accuracy
        self.depth = self.depth + depth 


        # Adjust topic based on the evaluation
        if clarity < 4:
            return "Beginner-level questions (focus on clarity)"
        elif accuracy < 5:
            return "Intermediate-level questions (focus on accuracy)"
        elif depth < 6:
            return "Intermediate-level questions (focus on depth)"
        else:
            return "Advanced-level topics"


    def summarize_evaluation(self, evaluation_list, i):
        """Summarize the evaluation using the agent to calculate averages and feedback"""
        
        average_clarity = self.clarity / (i + 1)
        average_accuracy = self.accuracy / (i + 1)
        average_depth = self.depth / (i + 1)
        overall_feedback = f"Overall, your performance shows an average clarity of {average_clarity:.2f}, accuracy of {average_accuracy:.2f}, and depth of {average_depth:.2f}. Keep practicing to improve these areas!"
        print(overall_feedback)

        # Initialize variables to hold cumulative values for clarity, accuracy, and depth
        # total_clarity = 0
        # total_accuracy = 0
        # total_depth = 0

        # # Parse evaluations and calculate cumulative values
        # for evaluation in evaluation_list:
        #     print(evaluation.split('\n')[0])
        #     scores=evaluation.split('\n')[0]
        #     #sys.exit()
        #     clarity = int(re.search(r'Clarity:\s*(\d+)', scores).group(1))
        #     # print(clarity)
        #     # sys.exit()
        #     accuracy = int(re.search(r'Accuracy:\s*(\d+)', scores).group(1))
        #     depth = int(re.search(r'Depth:\s*(\d+)', scores).group(1))

        #     total_clarity += clarity
        #     total_accuracy += accuracy
        #     total_depth += depth

        # # Calculate averages
        # num_evaluations = len(evaluation_list)
        # average_clarity = total_clarity / num_evaluations
        # average_accuracy = total_accuracy / num_evaluations
        # average_depth = total_depth / num_evaluations

        # # Construct the overall feedback based on the averages
        # overall_feedback = "Your overall feedback here"

        # result = {
        #     "average_clarity": average_clarity,
        #     "average_accuracy": average_accuracy,
        #     "average_depth": average_depth,
        #     "overall_feedback": overall_feedback
        # }

        # print(result)
        sys.exit()  # Debugging line to check the summary result

    def print_evaluation(self, evaluation):
        """Print the evaluation content (clarity, accuracy, depth) in a readable format"""
        clarity = evaluation.get("clarity", 0)
        accuracy = evaluation.get("accuracy", 0)
        depth = evaluation.get("depth", 0)
        
        # Printing the evaluation results in a readable format
        print(f"Clarity: {clarity}/10")
        print(f"Accuracy: {accuracy}/10")
        print(f"Depth: {depth}/10")

