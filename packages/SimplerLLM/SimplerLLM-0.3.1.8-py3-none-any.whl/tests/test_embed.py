from SimplerLLM.language.embeddings import EmbeddingsLLM, EmbeddingsProvider

embeddings_instance = EmbeddingsLLM.create(provider=EmbeddingsProvider.OPENAI,model_name="text-embedding-3-small")

test_input = [
    "apple",
    "banana"
]

# Generate embeddings

generated_embeddings = embeddings_instance.generate_embeddings(test_input,full_response=False)

print(generated_embeddings[0].embedding)