# import json
import copy
from llama_cpp import Llama

# load the model
print("Loading model...")
# MODEL = './models/ggml-vicuna-13b-1.1-q4_0.bin'
MODEL = './models/ggml-alpaca-7b-q4.bin'

llm = Llama(model_path=MODEL)
print("Model Loaded")
question = """

"""
stream = llm(
    f"Write a short haiku about how large language models are not GAI",
    # "Question: What is the capital of France? Answer:",
    max_tokens=400,
    temperature=0.0,
    # stop=["\n"],
    stop=["Q:", "Question:"],
    # echo=True,
    stream=True
)
# print(json.dumps(output, indent=4))

for output in stream:
    fragment = copy.deepcopy(output)
    print(fragment['choices'][0]['text'], end="", flush=True)
