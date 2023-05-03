"""Tests that we are pulling data from config file correctly."""
from source.config import config


def assert_string_not_empty(value: str) -> None:
    """Helper function to verify str is not empty."""
    assert isinstance(value, str)
    assert value is not None
    assert value.strip() != ''


def test_config_values_are_not_empty() -> None:
    """Tests each function of the config file to ensure expected keys are in yaml."""
    assert_string_not_empty(config.DIR_DATA_PROCESSED)
    assert_string_not_empty(config.DIR_OUTPUT)
    assert_string_not_empty(config.DIR_DATA_RAW)
    assert_string_not_empty(config.DIR_DATA_INTERIM)
    assert_string_not_empty(config.DIR_DATA_EXTERNAL)
    assert_string_not_empty(config.DIR_DATA_PROCESSED)
    assert_string_not_empty(config.DIR_NOTEBOOKS)
