import asyncio
from typing import List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from SimplerLLM.tools.youtube import get_youtube_transcript
from SimplerLLM.language.llm_addons import calculate_text_generation_costs
#generation_llm = GenerationLLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-5-sonnet-20240620")
generation_llm = GenerationLLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-haiku-20240307")



cost_per_million_input_tokens = 0.25
cost_per_million_output_tokens = 1.25


def generate_response(query: str, context: str) -> str:
    prompt = f"""
    Given the following youtube Video transcript and user [Query], provide a concise and relevant answer. If the context doesn't contain enough information to answer the query, say so.


    [Query]: {query}

    Answer:
    """

    
    response = generation_llm.generate_response(
        prompt=prompt,
        cached_input= f"<video_transcript>{context}</video_transcript>",
        prompt_caching=True,
        full_response=False,
        system_prompt="Answer in 3-5 sentences max, answer only questions related to the video, if the video doesnt contain the answer, say, I dont know.")
    
    cost = calculate_text_generation_costs(prompt,response,cost_per_million_input_tokens,cost_per_million_output_tokens)
    return response, cost


async def chat_with_video(transcript) -> None:
    print("Chatbot: Hello! I'm ready to answer questions about the sample text. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        response , cost= generate_response(user_input, transcript)

        print(f"Chatbot: {response}")
        print(f"Cost: {cost}")
        



async def main():
    
    youtube_url = "https://youtu.be/M0n4dxhpVm4"
    youtube_transcript = get_youtube_transcript(youtube_url)


    await chat_with_video(youtube_transcript)

    

if __name__ == "__main__":
    asyncio.run(main())