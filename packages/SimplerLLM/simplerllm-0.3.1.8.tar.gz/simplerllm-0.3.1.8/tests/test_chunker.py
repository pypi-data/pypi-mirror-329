from SimplerLLM.language.embeddings import EmbeddingsLLM as EmbeddingLLM, EmbeddingsProvider
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from SimplerLLM.tools.youtube import get_youtube_transcript
from SimplerLLM.tools.text_chunker import chunk_by_semantics


#from langchain_experimental.text_splitter import SemanticChunker
#from langchain_openai.embeddings import OpenAIEmbeddings



instance  = GenerationLLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")
embeddings_instance = EmbeddingLLM.create(provider=EmbeddingsProvider.OPENAI,model_name="text-embedding-3-small")

yt_url = "https://www.youtube.com/watch?v=3nnMJ62dJlk&pp=ygUMUkpQIHRlY2huaXFl"

content = get_youtube_transcript(yt_url)

my_chunks = chunk_by_semantics(text=content,llm_embeddings_instance=embeddings_instance,threshold_percentage=95)


print("My Chunker Results:")
print(my_chunks.num_chunks)
print(my_chunks.chunk_list)


#print("------------")
#print("Langchain Results:")
#print(len(langchain_chunks))
#print(langchain_chunks[0])