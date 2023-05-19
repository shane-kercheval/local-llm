"""Provides convenience functions for configuration settings."""

from helpsk.utility import open_yaml


def read_file(file_name: str) -> str:
    """Helper to clean up code."""
    with open(file_name) as handle:
        return handle.read().strip()


CONFIG = open_yaml('source/config/config.yaml')

DIR_OUTPUT = CONFIG['output']['directory']
DIR_DATA_RAW = CONFIG['data']['raw_directory']
DIR_DATA_INTERIM = CONFIG['data']['interim_directory']
DIR_DATA_EXTERNAL = CONFIG['data']['external_directory']
DIR_DATA_PROCESSED = CONFIG['data']['processed_directory']
DIR_NOTEBOOKS = CONFIG['notebooks']['directory']

LLM_ALPACA_7B = CONFIG['llms']['ggml-alpaca-7b']
LLM_VICUNA_13B = CONFIG['llms']['ggml-vicuna-13b']
