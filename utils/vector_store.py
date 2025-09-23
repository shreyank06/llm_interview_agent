# utils/vector_store.py
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document  # Import Document

def create_vector_store(documents):
    """
    Create a vector store (Chroma) from a list of documents.
    :param documents: List of document strings (e.g., interview questions).
    :return: Chroma vector store instance.
    """
    embeddings = OpenAIEmbeddings()  # Ensure this uses the correct package

    # Wrap the documents in the Document class
    wrapped_documents = [Document(page_content=doc) for doc in documents]
    
    # Create the Chroma vector store from the wrapped documents
    return Chroma.from_documents(wrapped_documents, embeddings)

def load_vector_store():
    """
    Load or create a vector store.
    :return: Chroma vector store instance.
    """
    # Sample documents (could be interview questions or other content)
    sample_questions = [
        "What is a Python decorator?",
        "Explain the difference between a list and a tuple in Python.",
        "What is the difference between a deep copy and a shallow copy?"
    ]
    
    return create_vector_store(sample_questions)
