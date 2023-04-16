# import requests
# import streamlit as st
# from llm import CompletionRequest, CompletionResponse

# # Define the API endpoint URL
# API_URL = "http://localhost:8080/completions"

# # Define the API authentication token
# TOKEN = "your_secret_token"

# # Define the Streamlit app layout
# st.title("Text Completion API")
# prompt = st.text_input("Enter a text prompt:")
# max_tokens = st.slider("Max tokens:", min_value=1, max_value=512, value=16)
# temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, step=0.1, value=0.5)
# top_p = st.slider("Top P:", min_value=0.1, max_value=1.0, step=0.1, value=0.9)

# # Define a function to send the completion request to the API endpoint
# def get_completions(prompt, max_tokens, temperature, top_p):
#     # Define the completion parameters
#     completion_request = CompletionRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

#     # Set the Authorization header with the token
#     headers = {"Authorization": f"Bearer {TOKEN}"}

#     # Send a POST request to the API endpoint with the completion parameters
#     response = requests.post(API_URL, headers=headers, json=completion_request.dict())

#     # Parse the JSON response data
#     completion_response = CompletionResponse.parse_raw(response.text)

#     # Return the completed text
#     return completion_response.choices[0].text

# # Define the Streamlit app behavior
# if st.button("Complete"):
#     completed_text = get_completions(prompt, max_tokens, temperature, top_p)
#     st.write(completed_text)
