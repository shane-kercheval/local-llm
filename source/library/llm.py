"""Wrapper around LLM functions and responses."""
# import json
# import copy
from llama_cpp import Llama
from pydantic import BaseModel


class Choice(BaseModel):
    """Represents fields associated with LLM completion response."""

    text: str
    index: int
    logprobs: object
    finish_reason: str


class Usage(BaseModel):
    """Represents fields associated with usage information in response."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    """Represents fields associated with response."""

    id: str  # noqa: A003
    object: str  # noqa: A003
    created: int
    model: str
    usage: Usage
    choices: list[Choice]


def prompt_question(question: str) -> str:
    """Function that wraps a question in a standard LLM prompt."""
    return f"Question:\n{question}\n\nAnswer: "


def completion(
        model: Llama,
        prompt: str,
        temperature: float = 0.5,
        model_max_tokens: int = 512,
        stop: str = None) -> CompletionResponse:
    """
    Args:
        model:
            the llama_cpp.Llama model to pass in
        prompt:
            The prompt to generate text from.
        temperature:
            The temperature to use for sampling.
        model_max_tokens:
            The number of tokens that the `model` can handle.
            The maximum tokens to generate in the completion is model_max_tokens minus the
            number of tokens in the prompt.
        stop:
            A list of strings to stop generation when encountered.
    """
    # .tokenize() approach from take from `lamma.py` line 376
    prompt_tokens = model.tokenize(b" " + prompt.encode("utf-8"))
    output = model.create_completion(
        prompt=prompt,
        max_tokens=model_max_tokens - len(prompt_tokens),
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
