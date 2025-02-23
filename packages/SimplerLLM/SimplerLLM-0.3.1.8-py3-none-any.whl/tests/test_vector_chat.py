import numpy as np
from SimplerLLM.vectors.vector_storage import VectorDatabase, SerializationFormat
import asyncio
from typing import List, Dict, Any
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(text: str) -> np.ndarray:
    return model.encode([text])[0]

def split_text_into_chunks(text: str, chunk_size: int = 3) -> List[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence.split()) > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence.split())
        else:
            current_chunk.append(sentence)
            current_length += len(sentence.split())
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

async def initialize_database(db_folder: str) -> VectorDatabase:
    db = VectorDatabase(db_folder, use_semantic_connections=True)
    await db.load_from_disk("sample_text", SerializationFormat.JSON)
    return db

async def add_text_to_database(db: VectorDatabase, text: str) -> None:
    chunks = split_text_into_chunks(text)
    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)
        db.add_vector(chunk, embedding, {"index": i})
    await db.save_to_disk("sample_text", SerializationFormat.JSON)

async def chat_with_database(db: VectorDatabase) -> None:
    print("Chatbot: Hello! I'm ready to answer questions about the sample text. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        query_embedding = create_embedding(user_input)
        results = db.semantic_search(query_embedding, top_k=3, depth=1)
        
        if results:
            response = "Here's what I found:\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result['chunk_text']}\n"
            print(f"Chatbot: {response}")
        else:
            print("Chatbot: I'm sorry, I couldn't find any relevant information.")

async def main():
    db_folder = "vector_db"
    sample_text = """
    The Python programming language, created by Guido van Rossum in the late 1980s, has become one of the most popular languages in the world. It is known for its simplicity and readability, making it an excellent choice for beginners and experts alike. Python is versatile and can be used for web development, data analysis, artificial intelligence, and more.

    One of Python's key features is its extensive standard library, which provides a wide range of modules and functions for various tasks. This "batteries included" philosophy means that developers can often find the tools they need without having to rely on external libraries.

    Python's popularity in data science and machine learning has grown significantly in recent years. Libraries such as NumPy, Pandas, and Scikit-learn have made it easier for researchers and data scientists to work with large datasets and implement complex algorithms.

    The language's support for object-oriented, functional, and procedural programming paradigms makes it flexible and suitable for a variety of programming styles. This flexibility, combined with its clean syntax, has contributed to Python's widespread adoption in both industry and academia.
    """
    
    db = await initialize_database(db_folder)
    await add_text_to_database(db, sample_text)
    await chat_with_database(db)

if __name__ == "__main__":
    asyncio.run(main())