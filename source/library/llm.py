# import json
# import copy
from llama_cpp import Llama
from typing import List
from pydantic import BaseModel


class Choice(BaseModel):
    text: str
    index: int
    logprobs: object
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]


def prompt_question(text: str) -> str:
    return f"Question:\n{text}\n\nAnswer: "


def completion(
        model: Llama,
        prompt: str,
        temperature: float = 0.5,
        stop: str = None) -> CompletionResponse:

    # .tokenize() approach from take from `lamma.py` line 376
    prompt_tokens = model.tokenize(b" " + prompt.encode("utf-8"))
    output = model.create_completion(
        prompt=prompt,
        max_tokens=512 - len(prompt_tokens),
        temperature=temperature,
        stop=stop or [],
        # echo=True,
        # stream=True
    )
    # print(json.dumps(output, indent=4))
    # for output in stream:
    #     fragment = copy.deepcopy(output)
    #     print(fragment['choices'][0]['text'], end="", flush=True)
    return CompletionResponse(**output)
