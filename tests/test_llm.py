"""Tests that our local models are working."""

from llama_cpp import Llama
from source.library.llm import completion, prompt_question


def test__completion(alpaca_model: Llama, vicuna_model: Llama) -> None:  # noqa: D103
    response = completion(
        model=alpaca_model,
        prompt=prompt_question('What is the capital of France?'),
        temperature=0.2,
        stop=None,
    )
    assert response.object == 'text_completion'
    assert 'Paris' in response.choices[0].text

    response = completion(
        model=vicuna_model,
        prompt=prompt_question('What is the capital of France?'),
        temperature=0.2,
        stop=None,
    )
    assert response.object == 'text_completion'
    assert 'Paris' in response.choices[0].text
