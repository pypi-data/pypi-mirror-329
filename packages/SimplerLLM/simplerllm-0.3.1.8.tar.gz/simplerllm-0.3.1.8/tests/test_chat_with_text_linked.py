import re

import asyncio
import openai
from typing import List, Dict, Any
import numpy as np
from SimplerLLM.vectors.vector_storage import VectorDatabase, SerializationFormat
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.tools.text_chunker import chunk_by_semantics
from SimplerLLM.language.embeddings import EmbeddingsLLM as EmbeddingLLM, EmbeddingsProvider
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider

class YouTubeChatbot:
    def __init__(self):
        self.vector_db = VectorDatabase("youtube_vector_db", use_semantic_connections=True)
        self.generation_llm = GenerationLLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")
        self.embedding_llm = EmbeddingLLM.create(provider=EmbeddingsProvider.OPENAI, model_name="text-embedding-3-small")
        self.chunk_size = 1000
        self.overlap = 200

    async def process_video(self):
        transcript = load_content("sample.txt").content
        
        if not transcript:
            print(" transcript not available. Please try another video.")
            return
        
        chunks = chunk_by_semantics(text=transcript, llm_embeddings_instance=self.embedding_llm, threshold_percentage=95)
        await self.process_chunks(chunks.chunk_list)
        print(f"Video [video_id] processed and added to the database.")

    async def create_embedding(self, text: str) -> np.ndarray:
        response = await self.embedding_llm.generate_embeddings_async(text)
        # The OpenAI API returns a list of embedding objects
        # We assume there's only one embedding for the input text
        embedding = response[0].embedding
        return np.array(embedding)


    async def process_chunks(self, chunks):
        for i, chunk in enumerate(chunks):
            embedding = await self.create_embedding(chunk.text)
            main_topic = self.extract_main_topic(chunk.text)
            metadata = {

                "topic": main_topic
            }
            
            unique_id = self.vector_db.add_vector(chunk.text, embedding, metadata)
            print(f"Added chunk {i+1}/{len(chunks)} with ID: {unique_id}")





    def extract_main_topic(self, chunk: str) -> str:
        prompt = f"Extract the main topic from this text in 5 words or less:\n\n{chunk[:500]}"
        return self.generation_llm.generate_response(prompt=prompt)



    async def chat(self):
        print("Welcome to the Chatbot!")
        while True:

            await self.process_video()
            
            while True:
                query = input("Ask a question ('q' to quit): ")
                if query.lower() == 'q':
                    return
                
                await self.answer_question(query)

    async def answer_question(self, query: str):
        query_embedding = await self.create_embedding(query)
        relevant_chunks = self.vector_db.semantic_search(query_embedding, top_k=3, depth=2)
        
        print("\nRelevant chunks used to answer the question:")
        for i, chunk in enumerate(relevant_chunks, 1):
            print(f"\nChunk {i}:")
            #print(f"Title: {chunk['metadata']['title']}")
            print(f"Text: {chunk['chunk_text'][:150]}...")  # Display first 150 characters of each chunk
            #print(f"Similarity score: {chunk['similarity']:.4f}")  # Assuming similarity score is available
        
        context = "\n\n".join([f"{chunk['chunk_text']}" for chunk in relevant_chunks])
        
        prompt = f"""
        Based on the following context from a YouTube video, answer the user's question.
        If the answer is not in the context, say "I'm sorry, I don't have enough information to answer that question."

        Context:
        {context}

        User's question: {query}

        Answer:
        """
        
        response = self.generation_llm.generate_response(prompt=prompt)
        
        print("\nAnswer:", response.strip())
        print()

async def main():
    chatbot = YouTubeChatbot()
    await chatbot.chat()

if __name__ == "__main__":
    asyncio.run(main())