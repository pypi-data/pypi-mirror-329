class Llm:

    def __init__(self):
        pass

    def generate_text(self, system_prompt : str, prompt : str, max_tokens: int, temperature: float) -> str :
        raise NotImplementedError("This method should be implemented by subclasses.")

class AwsLlm(Llm):

    def __init__(self):
        super().__init__()

    def generate_text(self, system_prompt : str, prompt : str, max_tokens: int, temperature: float) -> str :
        return "Hello AwsLlm"

class GroqLlm(Llm):

    def __init__(self):
        super().__init__()

    def generate_text(self, system_prompt : str, prompt : str, max_tokens: int, temperature: float) -> str :
        return "Hello GroqLlm"