class AnswerEvaluator:
    def __init__(self, i, topic, clarity, accuracy, depth, agent):
        self.i = i
        self.topic = topic
        self.clarity = clarity
        self.accuracy = accuracy
        self.depth = depth
        self.agent = agent

    def summarize_evaluation(self):
        """Summarize the evaluation using the agent to calculate averages and feedback for a technical interview"""
        
        # Calculate averages for clarity, accuracy, and depth
        average_clarity = self.clarity / (self.i+1)
        average_accuracy = self.accuracy / (self.i+1)
        average_depth = self.depth / (self.i+1)
        
        # Construct the overall feedback for the interview
        overall_feedback = f"""
        Overall, your performance shows an average clarity of {average_clarity:.2f}/10, accuracy of {average_accuracy:.2f}/10, and depth of {average_depth:.2f}/10.
        Based on your performance, I recommend focusing on improving the following areas to do better in future technical interviews:
        """
        
        # Print the overall feedback
        print(overall_feedback)
        # Define the prompt for the LLM to generate a personalized response based on the interview performance
        prompt = f"""
        Based on the following interview performance evaluation, provide detailed feedback for improving interview answers specific to the topic '{self.topic}':
        
        Evaluation:
        Clarity: {average_clarity:.2f}/10
        Accuracy: {average_accuracy:.2f}/10
        Depth: {average_depth:.2f}/10

        The evaluation is based on answers to technical questions in a coding interview related 
        to the topic '{self.topic}'. Offer constructive advice specific to improving clarity, accuracy, 
        and depth for future technical interviews in this topic area. Your feedback should focus on the interviewee's ability 
        to communicate technical knowledge clearly, the accuracy of the information provided, and the depth of understanding 
        displayed in their answers on the topic '{self.topic}'. 
        """

        # Use the agent to call the LLM with the feedback prompt
        evaluation_response = self.agent.invoke({
            "messages": [{"role": "user", "content": prompt}]
        })
        
        # Extract the response from the AI
        ai_message = evaluation_response['messages'][-1].content  # Get the content of the AI's last message

        # Print the personalized feedback from the LLM
        print("\nPersonalized Feedback for Technical Interview:\n")
        print(ai_message)
        
        # Optionally, you can return the AI's response if you want to use it elsewhere
        return ai_message
