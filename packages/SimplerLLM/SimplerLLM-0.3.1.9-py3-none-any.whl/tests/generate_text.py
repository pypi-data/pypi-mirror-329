from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm_addons import generate_pydantic_json_model
from SimplerLLM.tools.serp import search_with_duck_duck_go
from SimplerLLM.tools.file_functions import save_text_to_file
from pydantic import BaseModel
from transformers import AutoTokenizer



instance  = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")


# Define a simple Pydantic model
# class Word(BaseModel):
#     word: str
#     count: int

# class Words(BaseModel):
#     words : list[Word]



# search_results = search_with_duck_duck_go(query="ai chatbot on wordpresss",max_results=5)

# for result in search_results:
#     print(result.Domain)
#     print(result.Title)
#     print(result.URL)




#content = load_content("https://youtu.be/l-CjXFmcVzY?si=AnL9CSpAN8E4s4aO")

#youtube_script = content.content



#success = save_text_to_file(youtube_script, "d:\\script.txt")
#print("File saved successfully:", success)


#prompt = "You are a machine learning expert specialized in explaining machine learning concepts in the simplest way, your task is extract the first 15 minutes of the following ML video script and explain it step by step as if I am 10 years old, video script:" + youtube_script

#response = instance.generate_response(prompt=prompt)

#print(response)


#blog = content.content
#print (blog)

#prompt = "extract the top 5 words and their count from the following blog post: " + blog

#response = generate_basic_pydantic_json_model(model_class=Words,prompt=prompt,llm_instance=instance)

#response = instance.generate_response(prompt=f"summarize the following blog post: {blog}")

#print (response)


from SimplerLLM.language.llm import LLM,LLMProvider


youtube_video = load_content("test.pdf")

youtube_script = youtube_video.content

llm_instance  = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-4")


summarize_prompt = f""" 
I will provide you with a [PDF], and you task is to extract the main topics, and turn into a 60 seconds youtube integration.

you should mention titles and text as it is from the PDF, and focus on extracting the main ideas.

PDF Content: {youtube_script}
"""
response = llm_instance.generate_response(prompt=summarize_prompt)

print(response)






# def count_tokens_with_tiktoken(text):
#     # Initialize the tokenizer
#     tokenizer = Tokenizer()

#     # Tokenize the text
#     tokens = tokenizer.tokenize(text)

#     # Return the number of tokens
#     return len(tokens)


# tokens = count_tokens_with_tiktoken( response)
# print(tokens)

