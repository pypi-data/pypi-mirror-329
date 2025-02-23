import asyncio
from typing import List, Dict, Any
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
from SimplerLLM.tools.youtube import get_youtube_transcript
from SimplerLLM.vectors.vector_storage import VectorDatabase, SerializationFormat
from SimplerLLM.language.embeddings import EmbeddingsLLM as EmbeddingLLM, EmbeddingsProvider
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from SimplerLLM.tools.text_chunker import chunk_by_semantics

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the embedding and generation models
embedding_llm = EmbeddingLLM.create(provider=EmbeddingsProvider.OPENAI, model_name="text-embedding-3-small")
generation_llm = GenerationLLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")




def create_embedding(text: str) -> np.ndarray:
    response = embedding_llm.generate_embeddings(text)
    # The OpenAI API returns a list of embedding objects
    # We assume there's only one embedding for the input text
    embedding = response[0].embedding
    return np.array(embedding)

async def add_text_to_database(db: VectorDatabase, text: str) -> None:
    chunks = chunk_by_semantics(text,embedding_llm)
    for i, chunk in enumerate(chunks.chunk_list):
        if chunk.text.strip():  # This checks if the chunk is not empty or just whitespace
            embedding = create_embedding(chunk.text)
            db.add_vector(chunk.text, embedding, {"index": i})
    await db.save_to_disk(SerializationFormat.BINARY)

def generate_response(query: str, context: List[str]) -> str:
    prompt = f"""
    Given the following context and query, provide a concise and relevant answer. If the context doesn't contain enough information to answer the query, say so.

    Context:
    {' '.join(context)}

    Query: {query}

    Answer:
    """
    return generation_llm.generate_response(prompt=prompt)

async def chat_with_database(db: VectorDatabase) -> None:
    print("Chatbot: Hello! I'm ready to answer questions about the sample text. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        query_embedding = create_embedding(user_input)

        results = db.semantic_search(query_embedding,  depth=3)
        
        if results:
            context = [result['text'] for result in results]
            response = generate_response(user_input, context)
            print(f"Chatbot: {response}")
        else:
            print("Chatbot: I'm sorry, I couldn't find any relevant information to answer your question.")

async def main():
    
    youtube_url = "https://www.youtube.com/watch?v=RWzHE28YgBk"
    youtube_transcript = get_youtube_transcript(youtube_url)
    
    db = VectorDatabase("yt_2_db", use_semantic_connections=True)
    #await db.load_from_disk("yt_2_db.svdb")
    await add_text_to_database(db, youtube_transcript)
    await chat_with_database(db)

if __name__ == "__main__":
    asyncio.run(main())