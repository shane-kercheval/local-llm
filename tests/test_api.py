"""Tests the functionality of the API."""

import json
from fastapi.testclient import TestClient
from source.service.api import CompletionRequest
from source.library.llm import CompletionResponse, prompt_question


def test__completions_endpoint(api_client: TestClient) -> None:  # noqa: D103
    prompt = prompt_question("What is the capital of France?")
    completion_request = CompletionRequest(prompt=prompt)
    token = "token123"
    headers = {"Authorization": f"Bearer {token}"}
    # Send a POST request to the API endpoint with the completion parameters
    response = api_client.post("/completions", headers=headers, json=completion_request.dict())
    assert response.status_code == 200
    # Parse the JSON response data
    response_data = json.loads(response.text)
    # Check that the response data is valid
    assert 'choices' in response_data
    assert len(response_data['choices']) > 0
    assert 'text' in response_data['choices'][0]
    assert 'Paris' in response_data['choices'][0]['text']
    response_object = CompletionResponse.parse_raw(response.text)
    assert 'Paris' in response_object.choices[0].text


def test__401(api_client: TestClient) -> None:  # noqa: D103
    prompt = prompt_question("What is the capital of France?")
    completion_request = CompletionRequest(prompt=prompt)
    token = "invalid"
    headers = {"Authorization": f"Bearer {token}"}
    # Send a POST request to the API endpoint with the completion parameters
    response = api_client.post("/completions", headers=headers, json=completion_request.dict())
    assert response.status_code == 401
    assert response.reason_phrase == 'Unauthorized'
