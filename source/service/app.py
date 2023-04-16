import logging
import logging.config
import requests
import streamlit as st
from source.library.llm import CompletionResponse, prompt_question
from source.service.api import CompletionRequest


logging.config.fileConfig(
    "source/config/logging.conf",
    disable_existing_loggers=False
)

API_URL = 'http://api:8080/completions'
#API_URL = 'http://0.0.0.0:8080/completions'
TOKEN = 'token123'


# Define the Streamlit app layout
st.title("Text Completion API")
prompt = prompt_question(st.text_input(
    "Enter a text prompt:",
    value="Q: What is the capital of France? A:"
))
temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, step=0.1, value=0.5)
# max_tokens = st.slider("Max tokens:", min_value=1, max_value=512, value=16)
# top_p = st.slider("Top P:", min_value=0.1, max_value=1.0, step=0.1, value=0.9)


# Define a function to send the completion request to the API endpoint
def get_completions(prompt, temperature) -> CompletionResponse:
    # Define the completion parameters
    completion_request = CompletionRequest(
        prompt=prompt,
        temperature=temperature,
    )
    # Set the Authorization header with the token
    headers = {'Authorization': f'Bearer {TOKEN}'}
    # Send a POST request to the API endpoint with the completion parameters
    response = requests.post(API_URL, headers=headers, json=completion_request.dict())
    logging.info(response.text)
    # Parse the JSON response data
    completion_response = CompletionResponse.parse_raw(response.text)
    # Return the completed text
    return completion_response


    # data = {"prompt": prompt}
    # headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    # response = requests.post(API_URL, headers=headers, json=data)
    # logging.info("-------------------------")
    # logging.info(response)
    # logging.info("-------------------------")


# Define the Streamlit app behavior
if st.button("Complete"):
    completion_response = get_completions(prompt, temperature)
    st.write(completion_response.choices[0].text.strip())
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Response:")
    st.write(completion_response)