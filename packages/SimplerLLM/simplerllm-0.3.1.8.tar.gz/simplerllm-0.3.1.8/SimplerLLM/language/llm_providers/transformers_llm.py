from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class TransformersModule:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.generator = None

    def download_model(self, model_name, download_path):
        """
        Downloads the model and tokenizer and saves them to the specified path.
        """
        try:
            # The 'cache_dir' parameter directs where to download and save the models
            model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=download_path)
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=download_path)
            model.save_pretrained(download_path)
            tokenizer.save_pretrained(download_path)
            print(f"Model and tokenizer for {model_name} downloaded and saved to {download_path}.")
        except Exception as e:
            print(f"An error occurred during model download: {e}")

    def load_model(self, model_name, load_path):
        """
        Load a model and its tokenizer from the specified path.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(load_path)
            self.model = AutoModelForCausalLM.from_pretrained(load_path)
            self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
            print(f"Model {model_name} loaded successfully from {load_path}.")
        except Exception as e:
            print(f"An error occurred while loading the model from {load_path}: {e}")

    def generate_text(self, prompt, max_length=50, temperature=1.0, top_p=0.9, num_return_sequences=1):
        """
        Generate text using the loaded model.
        """
        if not self.generator:
            print("No model is loaded. Please load a model first.")
            return None

        try:
            generated = self.generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences
            )
            return generated
        except Exception as e:
            print(f"An error occurred during text generation: {e}")
            return None