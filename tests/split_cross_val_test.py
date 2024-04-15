import os
from pathlib import Path
import sys

import pandas as pd
import pytest
print(sys.path)
from classifyspectraltype.clean_confidence_intervals import (
    clean_confidence_intervals,
)
from classifyspectraltype.fetch_exoplanet_dataset import fetch_data
from classifyspectraltype.split_cross_val import split_cross_val


@pytest.fixture(scope="session")
def data_dir():
    # this fixture is responsible to download the data and preprocess it then save it
    # under the data folder, finally returning the name of this folder
    columns = [
        "pl_name",
        "st_spectype",
        "sy_umag",
        "sy_gmag",
        "sy_rmag",
        "sy_imag",
        "sy_zmag",
    ]
    exoplanet_data = fetch_data(
        "https://exoplanetarchive.ipac.caltech.edu", "data/raw/test_data.csv", columns
    )
    output_file = Path("data") / "processed" / "planet-systems.csv"
    os.makedirs(output_file.parent, exist_ok=True)
    # Drop the rows with NA values
    exoplanet_data = exoplanet_data.dropna(
        subset=["st_spectype", "sy_umag", "sy_gmag", "sy_rmag", "sy_imag", "sy_zmag"]
    )
    clean_confidence_intervals(exoplanet_data)

    for col in exoplanet_data.columns:
        if col.endswith("str"):
            new_col_name = col[:-3]
            exoplanet_data.rename(columns={col: new_col_name}, inplace=True)
    exoplanet_data = exoplanet_data.copy()
    exoplanet_data["st_spectype"] = exoplanet_data["st_spectype"].transform(
        lambda x: x[0]
    )

    exoplanet_data = exoplanet_data.loc[
        exoplanet_data["st_spectype"].isin(["O", "B", "A", "F", "G", "K", "M"])
    ]
    exoplanet_data["st_spectype"] = exoplanet_data["st_spectype"].astype("category")

    exoplanet_data.to_csv(output_file, index=False)
    return output_file

# Test whether the function returns a dictionary containing the results for logistic regression 
# and random forests models as pd.Series objects, each with the expected number of results.
def test_split_cross_val_results(data_dir):
    results = split_cross_val(data_dir, "st_spectype", split=0.7, folds=5)

    assert (
        "logistic" in results
    ), "Result of logistic regression model should be returned"
    assert (
        "random_forest" in results
    ), "Result of random forests model should be returned"
    assert isinstance(
        results["logistic"], pd.Series
    ), "Item returned should be a pd.Series object"
    assert isinstance(
        results["random_forest"], pd.Series
    ), "Item returned should be a pd.Series object"
    assert (
        len(results["logistic"]) == len(results["random_forest"]) == 4
    ), "There should be 4 results returned"


# Checks that the function returns a dictionary of scores with the appropriate keys, 
# ensuring that fit time, score time, test score, and train score are present for each model.
def test_split_cross_val_scores(data_dir):

    results = split_cross_val(data_dir, "st_spectype", split=0.7, folds=5)

    # Check if the scores are in the expected format
    for model, scores in results.items():
        assert "fit_time" in scores, f"Fit time should be in the {model} model scores."
        assert (
            "score_time" in scores
        ), f"Score time should be in the {model} model scores."
        assert (
            "test_score" in scores
        ), f"Test score should be in the {model} model scores."
        assert (
            "train_score" in scores
        ), f"Train score should be in the {model} model scores."


# Verifies that the function raises appropriate exceptions when provided 
# with invalid parameters. This includes testing for an invalid target column, 
# a non-existing file path, an invalid split ratio, and an invalid number of folds.
def test_invalid_parameters(data_dir):

    # Invalid target column
    with pytest.raises(KeyError):
        split_cross_val(data_dir, "invalid_col", split=0.7, folds=5)

    # Non-existing data
    with pytest.raises(FileNotFoundError):
        split_cross_val(
            "dummy-file-path/data.csv",
            "st_spectype",
            split=0.7,
            folds=5,
        )

    # Invalid split ratio
    with pytest.raises(ValueError):
        split_cross_val(data_dir, "st_spectype", split=1.7, folds=5)

    # Non-existing data
    with pytest.raises(ValueError):
        split_cross_val(data_dir, "st_spectype", split=0.7, folds=-1)
