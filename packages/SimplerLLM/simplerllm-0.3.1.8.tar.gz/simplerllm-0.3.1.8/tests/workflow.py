
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))





from  test_helpers import get_latest_youtube_comments,post_reply
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider

# Step 1: Get Latest 10 Comments
channel_id = "UC1234567890"
num_comments = 5
latest_comments = get_latest_youtube_comments(channel_id, num_comments)


#Step 2: Define a langueg mondel instance to use
generation_llm = GenerationLLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-haiku-20240307")


# step 3: loop over comments, and generate a generic reply.
for comment in latest_comments:
    reply = generation_llm.generate_response(prompt=f"generate a 5 words reply to the following comment: {comment['comment_text']}")
    post_reply(comment['comment_id'],reply)










