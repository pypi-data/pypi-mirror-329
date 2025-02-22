import numpy as np
from ogboost import load_wine_quality
from ogboost import GradientBoostingOrdinal
import pytest

def test_model_initialization():
    model = GradientBoostingOrdinal(n_estimators=10, link_function='logit')
    assert model.n_estimators == 10
    assert model.link_function == 'logit'

@pytest.fixture
def wine_data():
    X, y, _, _ = load_wine_quality(return_X_y=True)
    return X, y

def test_fit(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10)
    model.fit(X, y)
    assert model.classes_.size == y.unique().size
    assert hasattr(model, "_path")

def test_predict_methods(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10)
    model.fit(X, y)

    preds = model.predict(X)
    assert preds.shape[0] == X.shape[0]

    probs = model.predict_proba(X)
    assert probs.shape == (X.shape[0], model.classes_.size)
    assert np.allclose(probs.sum(axis=1), 1)

def test_end_to_end(wine_data):
    X, y = wine_data

    model = GradientBoostingOrdinal(n_estimators=10)
    model.fit(X, y)

    preds = model.predict(X)
    assert preds.shape[0] == X.shape[0]