import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.boxplot_table_function import make_boxplot_and_table


@pytest.fixture
def data():
    # Create a Dataframe with our requires st_spectype column and our other columns
    data = {
        "st_spectype": ["A", "A", "B", "C", "A", "C"],
        "column_star": [2, 5, 6, 8, 1, 3],
        "column_moon": [4, 9, 10, 22, 5, 14],
        "column_sun": [13, 5, 2, 3, 12, 10],
        "column_pluto": [4, 7, 1, 10, 8, 9],
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="session")
def csv_dir():
    csv_dir = "results/tables"

    # Create directories if they don't exist
    os.makedirs(csv_dir, exist_ok=True)

    yield csv_dir


@pytest.fixture(scope="session")
def bp_dir():
    bp_dir = "results/figures"

    # Create directories if they don't exist
    os.makedirs(bp_dir, exist_ok=True)

    yield bp_dir


def test_csv_saves_to_dir(data, csv_dir, bp_dir):
    # Test 1: Ensures csv is saved to the given directory
    column_star = "column_star"

    make_boxplot_and_table(data, column_star, csv_dir, bp_dir)
    assert os.path.exists(
        f"{csv_dir}/{column_star}.csv"
    ), "Csv file was not saved properly!"


if False:

    def test_csv_matches(data, csv_dir, bp_dir):
        # Test 2: Makes sure csv matches the expected test data given
        column_moon = "column_moon"
        make_boxplot_and_table(data, column_moon, csv_dir, bp_dir)

        dir_csv_data = pd.read_csv(f"{csv_dir}/{column_moon}.csv")
        csv_data = data[["st_spectype", column_moon]].groupby("st_spectype").describe()
        assert dir_csv_data.equals(csv_data), ".csv files do not match eachother!"


def test_bp_saves_to_dir(data, csv_dir, bp_dir):
    # Test 3: Ensures boxplot is saved to the given directory
    column_sun = "column_sun"
    make_boxplot_and_table(data, column_sun, csv_dir, bp_dir)
    assert os.path.exists(
        f"{bp_dir}/{column_sun}.png"
    ), "Boxplot file was not saved properly"


if False:

    def test_bp_matches(data, csv_dir, bp_dir):
        # Test 4: Ensures boxplot matches the expected test data given
        column_moon = "column_moon"
        make_boxplot_and_table(data, column_moon, csv_dir, bp_dir)
        dir_bp_read = plt.imread(f"{bp_dir}/{column_moon}.png")
        test_bp_data = (
            data[["st_spectype", {column_moon}]]
            .groupby("st_spectype")
            .describe()
            .boxplot()
        )
        test_bp_fig = test_bp_data.figure.savefig("function_boxplot.png")
        test_bp_read = plt.imread
        assert dir_bp_read == test_bp_read, "Boxplot figures do not match eachother!"


def test_invalid_path(data):
    # Test 5: Checks if an invalid path is given
    column_moon = "column_moon"
    with pytest.raises(OSError) as e:
        make_boxplot_and_table(
            data, column_moon, "/path/doesntwork", "/path/doesntwork"
        )
    assert (
        str(e.value)
        == "Cannot save file into a non-existent directory: '/path/doesntwork'"
    )
