from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class QuestionGenerator:
    def __init__(self, llm, vector_store=None):
        self.llm = llm
        self.vector_store = vector_store
        self.question_template = PromptTemplate(input_variables=["topic"], template="Ask a technical question about {topic}.")
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.question_template)

    def generate_dynamic_question(self, topic):
        """Generate a dynamic question using the LLM"""
        return self.llm_chain.run(topic=topic)

    def generate_follow_up_question(self, evaluation):
        """Generate follow-up question based on evaluation"""
        prompt = PromptTemplate(input_variables=["evaluation"], template="Generate a follow-up question based on evaluation: {evaluation}")
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(evaluation=evaluation)
