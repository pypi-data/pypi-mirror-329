import numpy as np
import pytest
from ogboost import concordance_index

def test_concordance_index_basic():
    # Simple case: two pairs with clear ordering.
    y_true = np.array([0, 1, 2])
    y_pred = np.array([0.1, 1.1, 2.1])
    cindex = concordance_index(y_true, y_pred)
    assert 0.99 < cindex <= 1.0

def test_concordance_index_with_ties():
    # With ties in predictions
    y_true = np.array([0, 1, 2, 2])
    y_pred = np.array([0.2, 0.5, 0.5, 0.5])
    cindex = concordance_index(y_true, y_pred)
    # Expected behavior: ties contribute 0.5 weight.
    assert 0.5 < cindex < 1.0

def test_concordance_index_errors():
    with pytest.raises(ValueError):
        # mismatched lengths should raise an error
        concordance_index(np.array([0,1]), np.array([0.1]))
