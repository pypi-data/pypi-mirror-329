
from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.generic_loader import load_content


youtube_url = "https://www.youtube.com/watch?v=JN3KPFbWCy8"

youtube_content = load_content(youtube_url).content

llm=LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")

response = llm.generate_response(prompt=f"Extract 3 Key points from the following [PODCAST]
                                  that can act as a good idea for a viral tweet.
                                    From each key point, generate a viral tweet of less
                                  than 280 characters. Return only the tweets in a JSON array.
                                 [PODCAST]: {youtube_content}")


print(response)





#Author: Hasan Aboul Hasan

#import SimplerLLM

generate_blog_titles_prompt = """
I want you to act as a professional blog titles generator. 
Think of titles that are seo optimized and attention-grabbing at the same time,
and will encourage people to click and read the blog post.
They should also be creative and clever.
My blog post is is about {topic}                                                                    
"""







from pydantic import BaseModel

from SimplerLLM.language.llm_addons import generate_pydantic_json_model


    

    
#Define your pydantic model
class PydanticModel(BaseModel):
    ideas: list[str]

#Create an LLM Instance


#Generate your Pydantic - JSON Response
JSON_Response =  generate_pydantic_json_model(model_class=PydanticModel,
                                            prompt="your prompt goes here",
                                            llm_instance=llm,
                                            max_retries=1)
#access as simple as this
print(JSON_Response.ideas)


video_url = "https://youtu.be/AOYUEqlWOGU"

#load the video content
video = load_content(video_url)

#get the video script
video_script = video.content

#Create the Prompt
prompt = f""" 
Generate a Consise summary in bullet
points format for the following 
video script: {video_script}
"""

#generate the summary
res = llm.generate_response(prompt=prompt)

#print the results
print(res)

