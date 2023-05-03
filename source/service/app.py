"""Creates a streamlit app that allows takes a prompt and returns a completion request."""

import logging
import logging.config
import requests
import streamlit as st
from source.library.llm import CompletionResponse, prompt_question
from source.service.api import CompletionRequest


logging.config.fileConfig(
    "source/config/logging.conf",
    disable_existing_loggers=False,
)

TOKEN = 'token123'  # matches the dummy token used in api.py


# Define the Streamlit app layout
st.title("Text Completion API")
prompt = st.text_area(
    "Enter a text prompt:",
    value=prompt_question("What is the capital of France?"),
    height=200,
)
temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, step=0.1, value=0.5)
# max_tokens = st.slider("Max tokens:", min_value=1, max_value=512, value=16)
# top_p = st.slider("Top P:", min_value=0.1, max_value=1.0, step=0.1, value=0.9)


# Define a function to send the completion request to the API endpoint
def get_completions(prompt: str, temperature: float) -> CompletionResponse:
    """Calls the `completions` endpoint, wrapping the request/response."""
    completion_request = CompletionRequest(
        prompt=prompt,
        temperature=temperature,
    )
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.post(
        'http://api:8080/completions',
        headers=headers,
        json=completion_request.dict(),
    )
    logging.info(response.text)
    return CompletionResponse.parse_raw(response.text)


# Define the Streamlit app behavior
if st.button("Complete"):
    completion_response = get_completions(prompt, temperature)
    st.write(completion_response.choices[0].text.strip())
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Response:")
    st.write(completion_response)
