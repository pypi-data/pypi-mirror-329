
from pydantic import BaseModel
from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.language.llm_addons import generate_pydantic_json_model_async
from typing import List

from SimplerLLM.tools.web_crawler import crawl_website
from SimplerLLM.prompts.messages_template import MessagesTemplate


openai_instance  = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")
anthropic_instance  = LLM.create(provider=LLMProvider.ANTHROPIC,model_name="claude-3-opus-20240229")
gemini_instance  = LLM.create(provider=LLMProvider.GEMINI,model_name="gemini-pro")

# Create a new message template
template = MessagesTemplate()

# Add messages to the template
#template.add_message("system", "Answer Only in French")


# Add user and assistant messages to the template
template.add_user_message("generate one word")
# template.add_assistant_message("I'm good, thank you! How can I assist you today?")
# template.add_assistant_message("I'm good, thank you! How can I assist you today?")

# Get the messages
#template.add_user_message("generate one word")
#messages = template.get_messages()

#res1 = anthropic_instance.generate_response(prompt="generate one sentence")
#response = anthropic_instance.generate_response(messages=messages, system_prompt="you know only arabic, generate everything in ARABIC")
#response = gemini_instance.generate_response(prompt="generate one word", system_prompt="you know only arabic, generate everything in ARABIC")


#print(res1)


#from SimplerLLM.language.llm_providers.transformers_llm import TransformersModule


# tm = TransformersModule()
#download_path = '/'
# model_name = 'gpt2'

# tm.download_model(model_name, download_path)


import os

# List all files in the download directory
# files_in_directory = os.listdir(download_path)
# print("Files in directory:", files_in_directory)





class BlogTitles(BaseModel):
    titles: List[str]


generate_blog_titles_prompt = """I want you to act as a professional blog titles generator. 
Think of titles that are seo optimized and attention-grabbing at the same time,
and will encourage people to click and read the blog post.
They should also be creative and clever.
Try to come up with titles that are unexpected and surprising.
Do not use titles that are too generic,or titles that have been used too many times before. I want to generate 10 titles maximum.
My blog post is is about {topic}
                                                                                   
"""

# prompt = generate_blog_titles_prompt.format(topic="AI Chatbots")

# response = generate_pydantic_json_model_async(model_class=BlogTitles,prompt=prompt,llm_instance=instance)

# print (response.titles)


import asyncio

# async def main():
#     prompt = generate_blog_titles_prompt.format(topic="AI Chatbots")
#     response = await generate_pydantic_json_model_async(model_class=BlogTitles, prompt=prompt, llm_instance=instance)
#     print(response.titles)

# Assuming this is inside an async function or a coroutine
#await main()
#asyncio.run(main())


# Example usage:
# Crawling example.com up to depth 2, filtering by '/blog' slug
# result = crawl_website("http://learnwithhasan.com", 1)



# for link, (links_beneath, num_links_beneath, unique_links) in result.items():
#     print(f"Link: {link}")
#     print(f"Number of links beneath it: {num_links_beneath}")
#     print(f"Links beneath it: {links_beneath}")
#     print(f"Unique links beneath it: {unique_links}")
#     print()



generation_llm = LLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-5-sonnet-20241022")

def generate_blog_post(topic, advanced_section, notes, length, tone, audience, focus_keyword):
    prompt = f"""Your task is to write an SEO-optimized blog post based on a given topic, advanced section, and notes.

Your goal is to create an engaging, informative, and well-structured article that is ready for publication and optimized for search engines.

Follow these instructions carefully:

1. Begin by reading the following topic, notes, and focus keyword:

<topic>
{topic}
</topic>

<advanced section>
{advanced_section}
</advanced section>

<notes>
{notes}
</notes>

<focus_keyword>
{focus_keyword}
</focus_keyword>

<parameters>
Length: {length} words
Tone: {tone}
Target Audience: {audience}
</parameters>

1. Structure your blog post according to the following outline, incorporating SEO best practices:
a. SEO-optimized title (include focus keyword near the beginning)
b. Meta description (155-160 characters, including focus keyword)
c. Hook (1-2 sentences)
d. Core Idea and Benefits
e. Implementation Steps
f. Advanced Section
g. Conclusion
h. FAQs to rank as search snippets (incorporate focus keyword naturally)

2. SEO Optimization Guidelines:
    a. Include the focus keyword in:
        - First paragraph (within first 100-150 words)
        - At least one H2 heading
        - Meta description
        - Title
        - URL slug suggestion
        - Image alt text suggestions
    b. Use LSI (Latent Semantic Indexing) keywords and related terms naturally throughout the content
    c. Maintain a keyword density of 1-2% for the focus keyword
    d. Create short, SEO-friendly URLs
    e. Optimize heading structure (H1, H2, H3) with keywords where natural

3. Throughout the blog post:
    a. Suggest diagrams or images to add where they would enhance understanding. Format these as: <image_suggestion>Description of the image|SEO-optimized alt text</image_suggestion>
    b. Propose relevant interlinks to other content within the blog. Format these as: <interlink>Anchor text|Target page</interlink>
    c. Recommend external links to authoritative sources that support your points. Format these as: <external_link>Anchor text|URL</external_link>

4. Writing style and vocabulary:
    a. Adjust your writing style to match the specified tone and target audience
    b. Use vocabulary appropriate for the target audience
    c. Keep sentences and paragraphs clear and concise
    d. Use active voice and conversational tone where appropriate
    e. Explain any technical terms or jargon that cannot be avoided

5. Code snippets and formatting:
   a. When including code snippets, wrap them in appropriate markdown code blocks. Specify the language for syntax highlighting.
   b. Use appropriate HTML tags for headings (h1, h2, h3) and paragraphs (p)
   c. For emphasis, use <strong> for bold and <em> for italics
   d. For lists, use <ul> and <li> tags for unordered lists, and <ol> and <li> for ordered lists

6. Present your final blog post within <blog_post> tags, preceded by the SEO metadata in their own tags:

<seo_metadata>
Title: [SEO-optimized title]
Meta Description: [155-160 character description]
Suggested URL Slug: [SEO-friendly URL]
Focus Keyword: [primary keyword]
Secondary Keywords: [list of LSI keywords used]
</seo_metadata>

<blog_post>
[Your content here]
</blog_post>"""
    
    return generation_llm.generate_response(prompt=prompt, max_tokens=8096)


initial_response = generate_blog_post("How To Generate Linkedin Posts With AI",
                                       "monetize the tools",
                                         "a sample post about the topic",
                                           "200",
                                             "Pro",
                                               "beginners",
                                                 "Generate Linkedin Posts")


#test_prompt = "generate one sentence"
#generation_llm.generate_response(prompt=test_prompt, max_tokens=8096)
#res1 = generation_llm.generate_response(prompt=test_prompt, max_tokens=8096)
print(initial_response)