import os
import sys
from pathlib import Path

import pandas as pd
import pytest
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scripts.read_data import fetch_data


@pytest.fixture
def base_url():
    return "https://exoplanetarchive.ipac.caltech.edu"


@pytest.fixture
def columns():
    return ["pl_name", "st_spectype"]


@pytest.fixture
def output_path():
    return "data/raw/test_data.csv"


def test_fetch_data_downloads_data(base_url, output_path, columns):
    df = fetch_data(base_url, output_path, columns)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert os.path.exists(output_path)


def test_fetch_data_raises_exception_for_invalid_url(base_url, output_path, columns):
    base_url = "invalid_url"
    with pytest.raises(requests.exceptions.RequestException):
        fetch_data(base_url, output_path, columns)


def test_fetch_data_saves_data_to_specified_output_path(base_url, output_path, columns):
    output_path = "data/raw/custom_test_data.csv"
    fetch_data(base_url, output_path, columns)
    assert os.path.exists(output_path)


def test_fetch_data_default_output_path(base_url, columns):
    fetch_data(base_url, None, columns)
    default_output_path = Path("data/raw/planet-systems.csv")
    assert os.path.exists(default_output_path)


def test_fetch_data_response_is_dataframe(base_url, output_path, columns):
    df = fetch_data(base_url, output_path, columns)
    assert isinstance(df, pd.DataFrame)


def test_fetch_data_downloads_data_from_default_url(output_path, columns):
    fetch_data(None, output_path, columns)
    assert os.path.exists(output_path)


def test_fetch_data_returns_df_with_columns_that_are_given(output_path, columns):
    df = fetch_data(None, output_path, columns)
    assert list(df.columns) == columns
