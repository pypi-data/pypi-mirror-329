from SimplerLLM.language.llm_addons import generate_pydantic_json_model,generate_json_example_from_pydantic
from pydantic import BaseModel
from typing import List, Optional
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)


# Email Subject Line Analyzer
class EffectivenessScore(BaseModel):
    Score: int
    Explanation: str

class ScannabilityScore(BaseModel):
    Score: int
    Explanation: str

class SentimentAnalysis(BaseModel):
    Tone: str
    Explanation: str

class SpamTriggers(BaseModel):
    Triggers: List[str]
    Explanation: str

class AllCapsWords(BaseModel):
    Words: List[str]
    Impact: str

class Emojis(BaseModel):
    Recommendation: str
    Explanation: str

class EmailSubjectLineAnalysis(BaseModel):
    Effectiveness_Score: EffectivenessScore
    Scannability_Score: ScannabilityScore
    Sentiment_Analysis: SentimentAnalysis
    Spam_Triggers: SpamTriggers
    All_Caps_Words: AllCapsWords
    Emojis: Emojis
    Alternative_Subject_Lines: List[str]


subject_line_analyzer_prompt = """As a professional email subject line copywriter, your task is to analyze and provide feedback on the given subject lines. You should evaluate each input subject line based on factors such as effectiveness, scannability, sentiment, spammy triggers, usage of all caps words, and emojis. After analyzing each aspect, provide a detailed report explaining what's wrong with the subject line and how it can be improved. Finally, offer a list of alternative subject lines that are more effective.

Input Subject Line: {subject}

For your analysis response, please follow this structure:


1. Effectiveness Score (50-100): Provide an overall score for the effectiveness of the input subject line.
   - Briefly explain your Effectiveness score here.

2. Scannability Score (1-10): Rate how easy it is for users to quickly understand the main message of the subject line.
   - Briefly explain your Scannability score here.

3. Sentiment Analysis: Determine if the tone in the subject line is positive or negative.
   - Briefly explain your Sentiment analysis here.

4. Spam Triggers: Identify any phrases or elements that might trigger spam filters and briefly discuss them.

5. All Caps Words: Note any words written in all capital letters and briefly discuss their impact on readers' perception of the email.

6. Emojis: Assess whether adding an emoji would enhance or detract from the effectiveness of the subject line and briefly explain why and suggest the best emoji to add.

7. Alternative Subject Lines:
Provide a list of 3-5 improved alternatives based on your analysis.

"""


class SubTopics(BaseModel):
    sub_topics: List[str]

sub_topics_prompt = """as an expert in keyword and topic research specialized in {topic}, 
    generate 5 sub topics to write about in the form of SEARCHABLE keywords
    for the the following parent topic: {topic}"""


llm=LLM.create(provider=LLMProvider.LWH,
               model_name="gpt-4")

generated_prompt = sub_topics_prompt.format(topic="marketing")

ai_response =  generate_pydantic_json_model(model_class=SubTopics, prompt=generated_prompt, llm_instance=llm,max_retries=1)
        

#json_example = generate_json_example_from_pydantic(EmailSubjectLineAnalysis)
print(ai_response)