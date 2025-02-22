import numpy as np
import pytest
from ogboost import GradientBoostingOrdinal, concordance_index
from sklearn.exceptions import NotFittedError
import matplotlib.figure as mpl_fig
from test_gradient_boosting_ordinal import wine_data

# --- Score Method Tests ---
def test_score_method_labels_and_latent(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10, n_iter_no_change=5, random_state=42)
    model.fit(X, y)
    
    score_latent = model.score(X, y, pred_type='latent')
    score_labels = model.score(X, y, pred_type='labels')
    
    # Both scores should be floats and likely differ.
    assert isinstance(score_latent, float)
    assert isinstance(score_labels, float)
    assert score_latent != score_labels

def test_score_invalid_pred_type(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10, random_state=42)
    model.fit(X, y)
    with pytest.raises(ValueError, match="pred_type must be 'labels' or 'latent'"):
        model.score(X, y, pred_type='invalid')

# --- Staged Prediction Tests ---
def test_staged_methods(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Test that staged_decision_function yields correct shapes.
    staged_scores = list(model.staged_decision_function(X))
    for stage in staged_scores:
        assert stage.shape == (X.shape[0],)
    
    # Test staged_predict_proba yields arrays with proper shape.
    staged_probas = list(model.staged_predict_proba(X))
    for probas in staged_probas:
        assert probas.shape == (X.shape[0], model.classes_.size)
    
    # Test staged_predict yields correct labels.
    staged_preds = list(model.staged_predict(X))
    for preds in staged_preds:
        assert preds.shape == (X.shape[0],)

# --- CV Early Stopping Tests ---
def test_cv_early_stopping(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=20, n_iter_no_change=3, cv_early_stopping_splits=3, random_state=42)
    model.fit(X, y)
    # Check that _cv_path is populated
    assert hasattr(model, "_cv_path")
    assert "cv_loss" in model._cv_path
    # Also ensure that best_iteration is <= n_estimators
    assert model._cv_path['best_iteration'] <= model.n_estimators_

# --- Error Handling Tests ---
def test_invalid_link_function(wine_data):
    X, y = wine_data
    with pytest.raises(ValueError, match="Invalid link_function"):
        model = GradientBoostingOrdinal(link_function="invalid")
        model.fit(X, y)

def test_negative_sample_weight(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10, random_state=42)
    negative_weights = -np.ones(y.shape[0])
    with pytest.raises(ValueError, match="sample_weight cannot contain negative values"):
        model.fit(X, y, sample_weight=negative_weights)

# --- Reproducibility Test ---
def test_reproducibility(wine_data):
    X, y = wine_data
    model1 = GradientBoostingOrdinal(n_estimators=10, random_state=123)
    model1.fit(X, y)
    preds1 = model1.predict(X)
    
    model2 = GradientBoostingOrdinal(n_estimators=10, random_state=123)
    model2.fit(X, y)
    preds2 = model2.predict(X)
    
    np.testing.assert_allclose(preds1, preds2)

# --- Plot Loss Test ---
def test_plot_loss_returns_figure(wine_data):
    X, y = wine_data
    model = GradientBoostingOrdinal(n_estimators=10, random_state=42)
    model.fit(X, y)
    fig = model.plot_loss(return_fig=True, show=False)
    assert isinstance(fig, mpl_fig.Figure)
