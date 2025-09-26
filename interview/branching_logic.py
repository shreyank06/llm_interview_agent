class BranchingLogic:
    def __init__(self, llm):
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0  
        self.llm = llm


    def adjust_topic_based_on_answer(self, evaluation, agent, topic):
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
        evaluation_result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        
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
            return f"Beginner-level questions on: {topic} (focus on clarity)", self.clarity, self.accuracy, self.depth
        elif accuracy < 5:
            return f"Intermediate-level questions on: {topic} (focus on accuracy)", self.clarity, self.accuracy, self.depth
        elif depth < 6:
            return f"Intermediate-level questions on: {topic} (focus on depth)", self.clarity, self.accuracy, self.depth
        else:
            return f"Advanced-level topics on: {topic}", self.clarity, self.accuracy, self.depth
