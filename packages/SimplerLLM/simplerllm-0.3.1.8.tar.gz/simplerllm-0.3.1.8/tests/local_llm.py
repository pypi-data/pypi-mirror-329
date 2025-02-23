from llama_cpp import Llama

## Download the GGUF model
#model_name = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
model_file = "C:\\Users\\hasan\\.cache\\lm-studio\\models\\lmstudio-community\\codegemma-7b-it-GGUF\\codegemma-7b-it-Q3_K_L.gguf" # this is the specific model file we'll use in this example. It's a 4-bit quant, but other levels of quantization are available in the model repo if preferred
#model_path = hf_hub_download(model_name, filename=model_file)

model2= "C:\\Users\\hasan\\.cache\\lm-studio\\models\\TheBloke\\deepseek-coder-6.7B-instruct-GGUF\\deepseek-coder-6.7b-instruct.Q2_K.gguf"

## Instantiate model from downloaded file
llm = Llama(
      model_path=model2,
      chat_format="llama-2"
)


response = llm.create_chat_completion(
     messages=[{
         "role": "user",
         "content": "Hi"
     }]
)


## Unpack and the generated text from the LLM response dictionary and print it
print(response["choices"][0]["message"]["content"])