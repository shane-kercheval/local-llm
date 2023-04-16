from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
from source.library.llm import completion, CompletionResponse


app = FastAPI()
# load the model
print("Loading model...")
llm = Llama(model_path='./models/ggml-alpaca-7b-q4.bin')
# llm = Llama(model_path='./models/ggml-vicuna-13b-1.1-q4_0.bin')
print("Model Loaded")


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 500
    temperature: float = 0.5
    stop: str = None


@app.post("/completions", response_model=CompletionResponse)
def completions(request: CompletionRequest):
    response = completion(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        n=request.n,
        temperature=request.temperature,
        stop=request.stop,
    )
    return response
