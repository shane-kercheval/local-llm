"""Creates an API for interacting with the LLM."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel
from llama_cpp import Llama
from source.library.llm import completion, CompletionResponse
import source.config.config as config

app = FastAPI()

# Define a security scheme that uses a bearer token
http_bearer = HTTPBearer()
N_CONTEXT = 2048

# load the model
print("Loading model...")
model = Llama(
    model_path=config.LLM_VICUNA_13B,
    n_ctx=N_CONTEXT,
)
# model = Llama(model_path='./models/ggml-vicuna-13b-1.1-q4_0.bin')
print("Model Loaded")


class CompletionRequest(BaseModel):
    """Wraps data needed in the completion request."""

    prompt: str
    temperature: float = 0.5
    stop: list[str] = None


def token_required(func: callable) -> callable:
    """Implements logic for checking credentials/token. Dummy Token is currently used."""
    def token_wrapper(
            request: CompletionRequest,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> object:
        try:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )
            if credentials.credentials != 'token123':
                raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        return func(request)

    return token_wrapper


@app.post("/completions", response_model=CompletionResponse)
@token_required
def completions(request: CompletionRequest) -> CompletionResponse:
    """Makes a `completion` request on the LLM."""
    return completion(
        model=model,
        prompt=request.prompt,
        temperature=request.temperature,
        stop=request.stop,
        model_max_tokens=N_CONTEXT,
    )
