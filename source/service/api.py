from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel
from llama_cpp import Llama
from source.library.llm import completion, CompletionResponse


app = FastAPI()

# Define a security scheme that uses a bearer token
http_bearer = HTTPBearer()

# load the model
print("Loading model...")
model = Llama(model_path='./models/ggml-alpaca-7b-q4.bin')
# model = Llama(model_path='./models/ggml-vicuna-13b-1.1-q4_0.bin')
print("Model Loaded")


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 500
    temperature: float = 0.5
    stop: list[str] = None


def token_required(func):
    def token_wrapper(
            request: CompletionRequest,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
        try:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme"
                )
            if credentials.credentials != 'token123':
                raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        return func(request)

    return token_wrapper


@app.post("/completions", response_model=CompletionResponse)
@token_required
def completions(request: CompletionRequest):
    prompt_tokens = model.tokenize(
        b" " + request.prompt.encode("utf-8")
    )
    response = completion(
        model=model,
        prompt=request.prompt,
        max_tokens=512 - len(prompt_tokens),
        temperature=request.temperature,
        stop=request.stop,
    )
    return response
