"""Defines test fixtures."""

import pytest
from llama_cpp import Llama
from fastapi.testclient import TestClient
from library.dataset_types import CsvDataLoader, DatasetsBase, PickledDataLoader
from source.service.api import app
import source.config.config as config


# @pytest.fixture(scope='session')
# def alpaca_model() -> Llama:
#     """Returns an alpaca LLM."""
#     return Llama(model_path='./models/ggml-alpaca-7b-q4.bin', verbose=False)


@pytest.fixture(scope='session')
def llm_model() -> Llama:
    """Returns an vicuna LLM."""
    return Llama(model_path=config.LLM_VICUNA_13B, verbose=False)


@pytest.fixture(scope='session')
def api_client() -> TestClient:
    """Returns an TestClient so that we can unit test our API."""
    return TestClient(app)


class TestDatasets(DatasetsBase):
    """Mock datasets to test functionality of Datasets classes."""

    def __init__(self, cache) -> None:  # noqa: ANN001
        self.dataset_1 = PickledDataLoader(
            description="Dataset description",
            dependencies=['SNOWFLAKE.SCHEMA.TABLE'],
            directory='.',
            cache=cache,
        )
        self.other_dataset_2 = PickledDataLoader(
            description="Other dataset description",
            dependencies=['dataset_1'],
            directory='.',
            cache=cache,
        )
        self.dataset_3_csv = CsvDataLoader(
            description="Other dataset description",
            dependencies=['other_dataset_2'],
            directory='.',
            cache=cache,
        )
        super().__init__()


@pytest.fixture()
def datasets_fake_cache() -> TestDatasets:
    """Returns fake dataset with cache turned on."""
    return TestDatasets(cache=True)


@pytest.fixture()
def datasets_fake_no_cache() -> TestDatasets:
    """Returns fake dataset with cache turned off."""
    return TestDatasets(cache=False)
