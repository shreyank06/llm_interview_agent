from colorama import Fore, Style, init
import sys
# Initialize colorama for terminal color support
init(autoreset=True)
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain


class AnswerEvaluator:
    def __init__(self, interview_count, topic, clarity, accuracy, depth, agent, openai_api_key):
        """
        Initialize the AnswerEvaluator with the necessary parameters.
        
        :param interview_count: The number of interviews conducted so far (used to calculate averages)
        :param topic: The topic of the technical interview
        :param clarity: The clarity score of the answers
        :param accuracy: The accuracy score of the answers
        :param depth: The depth score of the answers
        :param agent: The agent responsible for generating the feedback
        """
        self.interview_count = interview_count
        self.topic = topic
        self.clarity = clarity
        self.accuracy = accuracy
        self.depth = depth
        self.agent = agent
        self.openai_api_key = openai_api_key

    def summarize_evaluation(self):
        """
        Summarize the evaluation of the interview performance and provide feedback.
        This includes calculating averages for clarity, accuracy, and depth.
        """
        # Calculate the total number of interviews + 1 to avoid division by zero
        total_interviews = self.interview_count + 1
        
        # Calculate averages for clarity, accuracy, and depth
        average_clarity = self.clarity / total_interviews
        average_accuracy = self.accuracy / total_interviews
        average_depth = self.depth / total_interviews
        
        # Construct the overall feedback message with enhanced visibility
        overall_feedback = f"""
        {Fore.YELLOW}{Style.BRIGHT}Overall Evaluation{Style.RESET_ALL}:
        {Fore.CYAN}Clarity: {Style.BRIGHT}{average_clarity:.2f}/10{Style.RESET_ALL}
        {Fore.GREEN}Accuracy: {Style.BRIGHT}{average_accuracy:.2f}/10{Style.RESET_ALL}
        {Fore.MAGENTA}Depth: {Style.BRIGHT}{average_depth:.2f}/10{Style.RESET_ALL}
        
        {Fore.RED}{Style.BRIGHT}Recommendations for Improvement{Style.RESET_ALL}:
        Based on your performance, I recommend focusing on improving the following areas to 
        do better in future technical interviews:
        """

        # Print the overall feedback with enhanced visibility
        print(overall_feedback)
        
        # Define the prompt for the LLM to generate personalized feedback
        prompt = PromptTemplate(
            input_variables=["topic", "average_clarity", "average_accuracy", "average_depth"],
            template="Based on the following interview performance evaluation, provide detailed feedback for improving interview answers specific to the topic '{topic}':\n\n"
                    "Evaluation:\n"
                    "Clarity: {average_clarity:.2f}/10\n"
                    "Accuracy: {average_accuracy:.2f}/10\n"
                    "Depth: {average_depth:.2f}/10\n\n"
                    "The evaluation is based on answers to technical questions in a coding interview related to the topic '{topic}'.\n"
                    "Offer constructive advice specific to improving clarity, accuracy, and depth for future technical interviews in this "
                    "topic area. Your feedback should focus on the interviewee's ability to communicate technical knowledge clearly, "
                    "the accuracy of the information provided, and the depth of understanding displayed in their answers on the topic '{topic}'.\n\n"
                    "Please provide structured feedback with the following sections:\n"
                    "- `clarity_feedback`: Clear, simple advice to improve clarity in responses.\n"
                    "- `accuracy_feedback`: Suggestions for improving accuracy in answers.\n"
                    "- `depth_feedback`: Advice on improving depth in the answers.\n\n"
                    "Make sure the output includes placeholders for these sections like `[clarity_feedback]`, `[accuracy_feedback]`, `[depth_feedback]` that we can later format with colors."
        )

        #print(OPENAI_API_KEY)
        llm_chain = LLMChain(
        llm=OpenAI(temperature=0.7, openai_api_key=self.openai_api_key),
        prompt=prompt)

        feedback_result = llm_chain.run({
        "topic": self.topic,
        "average_clarity": average_clarity,  # Your clarity score variable
        "average_accuracy": average_accuracy,  # Your accuracy score variable  
        "average_depth": average_depth  # Your depth score variable
    })

        #print(feedback_result)
        feedback_result_colored = self.apply_color_to_feedback(feedback_result)
        return feedback_result_colored
        sys.exit()
        
    def apply_color_to_feedback(self, feedback):
        """
        Apply color formatting to the AI feedback using colorama.
        This method looks for placeholders like `[clarity_feedback]` and replaces them
        with colored text.

        :param feedback: The raw feedback message from the agent with placeholders.
        :return: The feedback message with applied color formatting.
        """
        # Replace placeholders with the appropriate color formatting
        feedback = feedback.replace("[clarity_feedback]", f"{Fore.CYAN}{Style.BRIGHT}Clarity Feedback:{Style.RESET_ALL}")
        feedback = feedback.replace("[accuracy_feedback]", f"{Fore.GREEN}{Style.BRIGHT}Accuracy Feedback:{Style.RESET_ALL}")
        feedback = feedback.replace("[depth_feedback]", f"{Fore.MAGENTA}{Style.BRIGHT}Depth Feedback:{Style.RESET_ALL}")
        
        print(feedback)
        return feedback
