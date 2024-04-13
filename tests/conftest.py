import pandas as pd
import pytest


@pytest.fixture
def example_data_frame():
    """Provides a DataFrame for tests."""
    return pd.DataFrame(
        {
            "st_spectype": ["G", "K", "M"],
            "sy_umag": [
                "13.0932000&plusmn;0.0039422",
                "15.1234000&plusmn;0.0012345",
                "17.5678000&plusmn;0.0009876",
            ],
            "sy_gmag": [
                "10.0932000&plusmn;0.0039422",
                "12.1234000&plusmn;0.0012345",
                "14.5678000&plusmn;0.0009876",
            ],
            "sy_rmag": [
                "9.0932000&plusmn;0.0039422",
                "11.1234000&plusmn;0.0012345",
                "13.5678000&plusmn;0.0009876",
            ],
            "sy_imag": [
                "8.0932000&plusmn;0.0039422",
                "10.1234000&plusmn;0.0012345",
                "12.5678000&plusmn;0.0009876",
            ],
            "sy_zmag": [
                "7.0932000&plusmn;0.0039422",
                "9.1234000&plusmn;0.0012345",
                "11.5678000&plusmn;0.0009876",
            ],
        }
    )
