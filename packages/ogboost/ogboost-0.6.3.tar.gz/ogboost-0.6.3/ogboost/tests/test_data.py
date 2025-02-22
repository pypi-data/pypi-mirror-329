import pandas as pd
from ogboost import load_wine_quality

def test_load_wine_quality():
    red, white = load_wine_quality()
    
    # Assert data is loaded as DataFrames
    assert isinstance(red, pd.DataFrame)
    assert isinstance(white, pd.DataFrame)

    # Assert basic structure of red wine data
    assert "quality" in red.columns
    assert red["quality"].min() == 0
    assert red["quality"].dtype == int

    # Assert basic structure of white wine data
    assert "quality" in white.columns
    assert white["quality"].min() == 0
    assert white["quality"].dtype == int

import os
from unittest.mock import patch
from ogboost.data import _download_wine_quality_datasets

@patch("urllib.request.urlretrieve")
def test_download_wine_quality_datasets(mock_urlretrieve, tmp_path):
    dest = tmp_path / "data"
    os.makedirs(dest, exist_ok=True)

    _download_wine_quality_datasets(dest)

    # Verify the correct calls were made
    assert mock_urlretrieve.call_count == 2
    #assert (dest / "winequality-red.csv").exists()
    #assert (dest / "winequality-white.csv").exists()
