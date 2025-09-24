import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
import sys

class QuestionGenerator:
    def __init__(self, llm, vector_store=None, faiss_index=None, openai_api_key=None):
        self.llm = llm
        self.vector_store = vector_store if vector_store else [] 
        self.openai_api_key = openai_api_key # List of questions
        # print(self.openai_api_key)
        # sys.exit()  # Debugging line to check if the key is passed correctly
        # Initialize embeddings before calling create_faiss_index
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)  # Initialize OpenAIEmbeddings
        
        # Initialize FAISS index either from input or by creating a new one
        self.faiss_index = faiss_index if faiss_index else self.create_faiss_index()

    def create_faiss_index(self):
        """Create a FAISS index for question embeddings."""
        
        # Sample questions
        sample_questions = [
            "What is a Python decorator?",
            "Explain the difference between a list and a tuple in Python.",
            "What is the difference between a deep copy and a shallow copy?"
        ]
        
        # Create embeddings for these questions using OpenAIEmbeddings
        question_embeddings = np.array([self.embeddings.embed_query(q) for q in sample_questions], dtype=np.float32)
        
        # Create FAISS index (using the L2 distance metric)
        dim = question_embeddings.shape[1]  # The dimensionality of the embeddings
        index = faiss.IndexFlatL2(dim)  # Use L2 distance (Euclidean) for similarity search
        index.add(question_embeddings)  # Add embeddings to the index
        
        # Store questions in the vector store
        self.vector_store = sample_questions
        
        return index

    def load_questions_from_vector_store(self, topic, k=5):
        """Load questions based on similarity using FAISS."""
        
        # Generate the topic embedding using OpenAIEmbeddings
        topic_embedding = np.array([self.embeddings.embed_query(topic)], dtype=np.float32)  # Embedding for the topic
        
        # Perform the similarity search using FAISS
        _, indices = self.faiss_index.search(topic_embedding, k)  # Get top-k indices
        
        # Retrieve the corresponding questions based on the indices
        similar_questions = [self.vector_store[i] for i in indices[0]]
        
        return similar_questions
