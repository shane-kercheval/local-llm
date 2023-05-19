"""Tests that our local models are working."""

from llama_cpp import Llama
from source.library.llm import completion, prompt_question


def test__completion(llm_model: Llama) -> None:  # noqa: D103
    # getting this for alpaca model; author for vicuna updated to latest version but couldn't find
    # latest version of alpaca; re-add at later time
    # >>> error loading model: this format is no longer supported
    # (see https://github.com/ggerganov/llama.cpp/pull/1305)
    # llama_init_from_file: failed to load model

    # GGLM format changed and orginal alpaca model is no longer
    # response = completion(
    #     model=alpaca_model,
    #     prompt=prompt_question('What is the capital of France?'),
    #     temperature=0.2,
    #     stop=None,
    # )
    # assert response.object == 'text_completion'
    # assert 'Paris' in response.choices[0].text

    response = completion(
        model=llm_model,
        prompt=prompt_question('What is the capital of France?'),
        temperature=0.2,
        stop=None,
    )
    assert response.object == 'text_completion'
    assert 'Paris' in response.choices[0].text
