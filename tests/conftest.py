import pytest
from llama_cpp import Llama
from fastapi.testclient import TestClient
from source.service.api import app


@pytest.fixture(scope='session')
def alpaca_model():
    return Llama(model_path='./models/ggml-alpaca-7b-q4.bin', verbose=False)


@pytest.fixture(scope='session')
def vicuna_model():
    return Llama(model_path='./models/ggml-vicuna-13b-1.1-q4_0.bin', verbose=False)


@pytest.fixture(scope='session')
def api_client():
    return TestClient(app)
