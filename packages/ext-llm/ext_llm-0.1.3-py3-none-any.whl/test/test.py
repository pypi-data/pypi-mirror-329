from ext_llm import LLMXClient

client = LLMXClient()

print(client.generate_text("system_prompt", "prompt", 10, 0.5))