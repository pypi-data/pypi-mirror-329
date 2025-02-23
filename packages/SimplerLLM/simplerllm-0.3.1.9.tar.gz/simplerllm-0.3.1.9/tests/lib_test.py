
from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.language.llm_addons import generate_pydantic_json_model
from SimplerLLM.tools.text_chunker import chunk_by_semantics,chunk_by_max_chunk_size,chunk_by_sentences,chunk_by_paragraphs
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.embeddings import LLM as LLMEmbedding,EmbeddingsProvider


from typing import List
from pydantic import BaseModel



openai_instance  = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")
gemini_instance  = LLM.create(provider=LLMProvider.GEMINI,model_name="gemini-pro")
anthropic_instance  = LLM.create(provider=LLMProvider.ANTHROPIC,model_name="claude-3-opus-20240229")



#Test basic generation

# print("Testing Basic Generation with available models")
# openai_basic_response = openai_instance.generate_response(prompt="Generate a 3 word sentence.")
# print(f"Generated: {openai_basic_response}")
# print("OpenAI Basic Generation Test Done!")

# gemini_basic_response = gemini_instance.generate_response(prompt="Generate a 3 word sentence.")
# print(f"Generated: {gemini_basic_response}")
# print("Gemini Basic Generation Test Done!")


# anthropic_basic_response = anthropic_instance.generate_response(prompt="Generate a 3 word sentence.")
# print(f"Generated: {anthropic_basic_response}")
# print("Anthropic Basic Generation Test Done!")
# print("Test Done Successfully!")



#Test system prompt generation
system_prompt = "Generate only in french"

# openai_basic_response = openai_instance.generate_response(prompt="Generate a 3 word sentence.",system_prompt=system_prompt)
# print(f"Generated: {openai_basic_response}")
# print("OpenAI Test Done!")

# gemini_basic_response = gemini_instance.generate_response(prompt="Generate a 3 word sentence.",system_prompt=system_prompt)
# print(f"Generated: {gemini_basic_response}")
# print("Gemini Test Done!")


# anthropic_basic_response = anthropic_instance.generate_response(prompt="Generate a 3 word sentence.",system_prompt=system_prompt)
# print(f"Generated: {anthropic_basic_response}")
# print("Anthropic Test Done!")





#Test with messages
# messages = [{"role": "user", "content": "what is the capital of frace?"},
#             {"role": "system", "content": "generate only in arabic"}]

#openai_basic_response = openai_instance.generate_response(messages=messages)
#print(f"Generated: {openai_basic_response}")
#print("OpenAI Test Done!")

gemini_messages = [{"role": "user", "parts": [{"text": "what is the capital of france?"}]},
                   {"role": "user", "parts": [{"text": "what is the capital of pakistan?"}]}]
# gemini_basic_response = gemini_instance.generate_response(messages=gemini_messages,system_prompt=system_prompt)
# print(f"Generated: {gemini_basic_response}")
# print("Gemini Test Done!")

# anthropic_messages = [{"role": "user", "content": "what is the capital of frace?"}]
            

# anthropic_basic_response = anthropic_instance.generate_response(messages=anthropic_messages, system_prompt="generate in french, and in 2-3 words max")
# print(f"Generated: {anthropic_basic_response}")
#print("Anthropic Test Done!")





#test pydnatic generation

print("Testing pydnatic Generation")

generate_blog_titles_prompt = """I want you to act as a professional blog titles generator. 
Think of titles that are seo optimized and attention-grabbing at the same time,
and will encourage people to click and read the blog post.
They should also be creative and clever.
Try to come up with titles that are unexpected and surprising.
Do not use titles that are too generic,or titles that have been used too many times before. I want to generate 10 titles maximum.
My blog post is is about {topic}
                                                                                   
"""


class BlogTitles(BaseModel):
    titles: List[str]

pydantic_prompt = generate_blog_titles_prompt.format(topic="AI Chatbots")

response = generate_pydantic_json_model(model_class=BlogTitles,prompt=pydantic_prompt,llm_instance=anthropic_instance)

print (response.titles)



#test chunking
embeddings_instance = LLMEmbedding.create(provider=EmbeddingsProvider.OPENAI,model_name="text-embedding-3-small")

#content = load_content("https://youtu.be/l-CjXFmcVzY?si=AnL9CSpAN8E4s4aO")
content = load_content("https://learnwithhasan.com/free-ai-chatbot-on-wordpress")

text = content.content

#text_chunks = chunk_by_semantics(text=text, llm_embeddings_instance=embeddings_instance)
#text_chunks = chunk_by_max_chunk_size(text=text, max_chunk_size=300,preserve_sentence_structure=True)
#text_chunks = chunk_by_sentences(text=text)
text_chunks = chunk_by_paragraphs(text=text)
print(text_chunks.num_chunks)
print(text_chunks.chunk_list[0])