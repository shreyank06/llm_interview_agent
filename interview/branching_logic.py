import sys
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain

class BranchingLogic:
    def __init__(self):
        #self.openai_api_key = openai_api_key
        self.clarity = 0
        self.accuracy = 0
        self.depth = 0  
        #self.llm = llm


    def adjust_topic_based_on_answer(self, evaluation, openai_api_key):
        """Adjust topic based on the evaluation already performed by the agent"""
        
        # Define the prompt to extract clarity, accuracy, and depth from the evaluation
        
        prompt = PromptTemplate(
            input_variables=["evaluation"],
            template="Given the following evaluation, extract the clarity, accuracy, and depth scores as a dictionary with the keys 'clarity', 'accuracy', and 'depth'. The evaluation is already completed by the agent, so just return the scores.\n\n"
                     "Evaluation: {evaluation}\n\n"
                     "Return the evaluation in this format:\n"
                     "{{\n"
                     "    'clarity': X,\n"
                     "    'accuracy': X,\n"
                     "    'depth': X\n"
                     "}}"
        )   
        llm_chain = LLMChain(
            llm=OpenAI(temperature=0.7, openai_api_key=openai_api_key),
            prompt=prompt
        )

        result = llm_chain.run({"evaluation": evaluation})

        # Convert the response into a dictionary
        evaluation_dict = eval(result)  # Make sure this is a valid dictionary
        # print(evaluation_dict)
        # sys.exit()

        
        # Extract clarity, accuracy, and depth from the evaluation dictionary
        clarity = evaluation_dict.get("clarity", 0)
        accuracy = evaluation_dict.get("accuracy", 0)
        depth = evaluation_dict.get("depth", 0)

        self.clarity = self.clarity + clarity
        self.accuracy = self.accuracy + accuracy
        self.depth = self.depth + depth 

        #print(topic)
        #sys.exit()
        # Adjust topic based on the evaluation
        if clarity < 4:
            return f"Beginner-level questions (focus on clarity)", self.clarity, self.accuracy, self.depth
        elif accuracy < 5:
            return f"Intermediate-level questions (focus on accuracy)", self.clarity, self.accuracy, self.depth
        elif depth < 6:
            return f"Intermediate-level questions (focus on depth)", self.clarity, self.accuracy, self.depth
        else:
            return f"Advanced-level topics on ", self.clarity, self.accuracy, self.depth
