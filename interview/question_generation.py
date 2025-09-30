import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
import sys
import warnings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain



warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

class QuestionGenerator:
    def __init__(self, llm, vector_store=None, faiss_index=None, openai_api_key=None):
        self.llm = llm
        self.vector_store = vector_store if vector_store else [] 
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.faiss_index = faiss_index if faiss_index else self.create_faiss_index()

    def create_faiss_index(self):
        """Create a FAISS index for question embeddings."""
        sample_questions = [
            "What is a Python decorator?",
            "Explain the difference between a list and a tuple in Python.",
            "What is the difference between a deep copy and a shallow copy?"
        ]
        question_embeddings = np.array([self.embeddings.embed_query(q) for q in sample_questions], dtype=np.float32)
        dim = question_embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(question_embeddings)
        self.vector_store = sample_questions
        return index

    def load_questions_from_vector_store(self, topic, k=5):
        topic_embedding = np.array([self.embeddings.embed_query(topic)], dtype=np.float32)
        _, indices = self.faiss_index.search(topic_embedding, k)
        similar_questions = [self.vector_store[i] for i in indices[0]]
        return similar_questions
        
    def generate_dynamic_questions(self, topic, questions_list, evaluation_list=None, agent=None, openai_api_key=None):
        """
        Use GPT to generate dynamic interview questions for the given topic.
        :param topic: The topic for the interview (e.g., JavaScript, Python, AI, etc.)
        :param num_questions: The number of questions to generate (default 3, but will always return 1).
        :param evaluation_list: Previous evaluations to provide context (optional).
        :param agent: The agent to use for question generation.
        :return: A list containing a single generated question.
        """
        if agent is None:
            raise ValueError("Agent parameter is required")
        
        # Build history context from evaluation_list
        history_context = ""
        if evaluation_list:
            history_context = f"Previous interview context: {' '.join(evaluation_list)}\n\n"
        
        #print(topic)
        prompt = PromptTemplate(
        input_variables=["topic", "history_context", "questions_list"],
        template="Based on historical evaluation of the candidate {history_context} as a reference to determine next question's difficulty, Generate one interview question on {topic}. " \
        "Only provide one technical questions related to {topic} at a time. No more than one question. Do not repeat questions already asked in {questions_list}.")

        #print(OPENAI_API_KEY)
        llm_chain = LLMChain(
        llm=OpenAI(temperature=0.7, openai_api_key=openai_api_key),
        prompt=prompt)

        result = llm_chain.run({"topic": topic, "history_context": history_context, "questions_list": questions_list})
        questions = result.split("\n")
        #question = questions[0].replace("Question: ", "").strip()

        return [q.strip() for q in questions if q.strip()]  # Clean up any empty entries


        # # Build history context from evaluation_list
        # history_context = ""
        # if evaluation_list:
        #     history_context = f"Previous interview context: {' '.join(evaluation_list)}\n\n"
        
        # # Generate the question using the agent with strict instructions
        # if evaluation_list:
        #     response = agent.invoke({
        #         "input": f"based on {history_context}, Act as a technical interviewer for {topic}. Ask ONLY ONE technical question about {topic}. Return ONLY the question text without any prefixes, greetings, or additional text. Question:"
        #     })
        # else:
        #     response = agent.invoke({
        #         "input": f"Act as a technical interviewer for {topic}. Ask ONLY ONE technical question about {topic}. Return ONLY the question text without any prefixes, greetings, or additional text. Question:"
        #     })
        
        # Extract response text (adjust based on your agent's response format)
        # if "output" in response:
        #     response_text = response["output"]
        # elif "messages" in response and len(response["messages"]) > 0:
        #     response_text = response["messages"][-1].content
        # else:
        #     response_text = str(response)
        
        # # Debugging - print the raw response text for inspection
        # print(f"Raw response text: {response_text}")

        # # Parse and return only the first question if multiple are provided
        # questions = response_text.split("\n")
        # questions = [q.strip() for q in questions if q.strip() and (q.strip()[0].isdigit() or '?' in q)]
        
        # # Return only the first question
        # return questions[:1]
