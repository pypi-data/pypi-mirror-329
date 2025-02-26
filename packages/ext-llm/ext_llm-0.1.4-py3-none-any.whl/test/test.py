import ext_llm

config : str = open("ext_llm_config.yaml").read()

print(ext_llm.ExtLlmContext(config).get_configs()["models"])