import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain_openai import OpenAI
import sys

def create_faiss_index(documents, OPENAI_API_KEY):
    """
    Create a FAISS index from a list of documents.
    :param documents: List of document strings (e.g., interview questions).
    :return: FAISS index instance and vector store.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # Pass the API key explicitly
    # Assuming OpenAIEmbeddings will create the embeddings for us
    
    # Generate embeddings for each document (question)
    embeddings_list = [embeddings.embed_query(doc) for doc in documents]  # Embed the questions
    embeddings_array = np.array(embeddings_list, dtype=np.float32)  # Convert to NumPy array for FAISS
    
    # Create a FAISS index (using L2 distance metric)
    dim = embeddings_array.shape[1]  # Dimensionality of the embeddings
    index = faiss.IndexFlatL2(dim)  # Index that uses L2 distance
    index.add(embeddings_array)  # Add embeddings to the FAISS index
    
    # Return the index and the vector store (list of documents)
    return index, documents

def is_technical_topic(topic, OPENAI_API_KEY):
    """
    Check if the topic is technical by querying GPT-3.
    :param topic: The topic for the interview (e.g., JavaScript, Python, AI).
    :param OPENAI_API_KEY: The OpenAI API key.
    :return: True if the topic is technical, False otherwise.
    """
    # Manually handle specific topics like 'carbon dioxide'
    if topic.lower() == "carbon dioxide":
        return True  # Treat 'carbon dioxide' as technical

    prompt = f"Is '{topic}' a technical topic related to IT, programming, or technology? Answer with 'Yes' or 'No'."
    
    llm_chain = LLMChain(
        llm=OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY),
        prompt=PromptTemplate(input_variables=["topic"], template=prompt)
    )
    
    response = llm_chain.run({"topic": topic}).strip().lower()
    if response == "yes":
        return True
    return False


def generate_dynamic_questions(topic, num_questions=3, OPENAI_API_KEY=None):
    """
    Use GPT to generate dynamic interview questions for the given topic.
    :param topic: The topic for the interview (e.g., JavaScript, Python, AI, etc.).s
    :param num_questions: The number of questions to generate.
    :param OPENAI_API_KEY: The OpenAI API key to access the GPT model.
    :return: A list of generated questions.
    """
    prompt = PromptTemplate(
        input_variables=["topic", "num_questions"],
        template="Generate {num_questions} interview questions on {topic}. Only provide technical questions related to {topic}."
    )
    #print(OPENAI_API_KEY)
    llm_chain = LLMChain(
        llm=OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY),
        prompt=prompt
    )

    result = llm_chain.run({"topic": topic, "num_questions": num_questions})
    questions = result.split("\n")
    
    return [q.strip() for q in questions if q.strip()]  # Clean up any empty entries

def load_faiss_vector_store(topic, OPENAI_API_KEY):
    """
    Load or create a FAISS vector store with dynamically generated questions.
    :param topic: The topic for the interview (e.g., JavaScript, Python, AI).
    :param OPENAI_API_KEY: The OpenAI API key to access the GPT model.
    :return: FAISS index and vector store (list of documents).
    """
    # Check if the topic is technical
    if not is_technical_topic(topic, OPENAI_API_KEY):
        raise ValueError(f"The topic '{topic}' is not considered technical or relevant to IT/technology.")
    
    # Dynamically generate questions using GPT
    questions = generate_dynamic_questions(topic, num_questions=3 , OPENAI_API_KEY=OPENAI_API_KEY)
    
    # Create FAISS index and vector store
    faiss_index, vector_store = create_faiss_index(questions, OPENAI_API_KEY)
    
    return vector_store, faiss_index
