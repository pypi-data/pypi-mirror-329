import numpy as np
import pytest
from sklearn.tree import DecisionTreeRegressor
from ogboost import generate_heterogeneous_learners

# A simple fixture that returns two templates and their corresponding override dictionaries.
@pytest.fixture
def templates_and_overrides():
    # Create two template learners.
    template1 = DecisionTreeRegressor(max_depth=3)
    template2 = DecisionTreeRegressor(max_depth=4)
    templates = [template1, template2]
    
    # Create override dictionaries.
    # For testing, we use lambdas that return constant values.
    overrides = [
        {"max_depth": lambda rng: 5},  # For template1, always sample max_depth = 5.
        {"max_depth": lambda rng: 7}   # For template2, always sample max_depth = 7.
    ]
    return templates, overrides

def test_length(templates_and_overrides):
    """Test that the number of generated learners matches total_samples."""
    templates, overrides = templates_and_overrides
    total_samples = 10
    learners = generate_heterogeneous_learners(
        templates=templates,
        overrides=overrides,
        total_samples=total_samples,
        template_probs="round_robin",  # using round robin selection here
        random_state=42
    )
    assert len(learners) == total_samples

def test_round_robin_selection(templates_and_overrides):
    """
    Test that when using round robin selection (template_probs="round_robin"),
    the learners are generated in cyclic order.
    """
    templates, overrides = templates_and_overrides
    total_samples = 4
    learners = generate_heterogeneous_learners(
        templates=templates,
        overrides=overrides,
        total_samples=total_samples,
        template_probs="round_robin",
        random_state=42
    )
    # In round robin mode, expected pattern: first learner from template1 (max_depth=5),
    # second from template2 (max_depth=7), then template1 again, etc.
    max_depths = [learner.get_params()["max_depth"] for learner in learners]
    expected = [5, 7, 5, 7]
    assert max_depths == expected

def test_random_selection_fixed_seed(templates_and_overrides):
    """
    Test that using random selection with a fixed random_state produces reproducible results.
    """
    templates, overrides = templates_and_overrides
    total_samples = 10
    # Use random selection with uniform probabilities.
    learners1 = generate_heterogeneous_learners(
        templates=templates,
        overrides=overrides,
        total_samples=total_samples,
        template_probs=[0.5, 0.5],
        random_state=42
    )
    learners2 = generate_heterogeneous_learners(
        templates=templates,
        overrides=overrides,
        total_samples=total_samples,
        template_probs=[0.5, 0.5],
        random_state=42
    )
    # Compare the parameter "max_depth" for corresponding learners.
    for l1, l2 in zip(learners1, learners2):
        assert l1.get_params()["max_depth"] == l2.get_params()["max_depth"]

def test_non_callable_override_error(templates_and_overrides):
    """
    Test that providing a non-callable override value raises a ValueError.
    """
    templates, overrides = templates_and_overrides
    # Make one override non-callable.
    overrides[0]["max_depth"] = 5  # Not callable.
    with pytest.raises(ValueError, match="Override for parameter 'max_depth' must be callable."):
        generate_heterogeneous_learners(
            templates=templates,
            overrides=overrides,
            total_samples=5,
            random_state=42
        )

def test_template_probs_length_error(templates_and_overrides):
    """
    Test that if template_probs is provided with the wrong length, a ValueError is raised.
    """
    templates, overrides = templates_and_overrides
    with pytest.raises(ValueError, match="Length of template_probs must match the number of templates."):
        generate_heterogeneous_learners(
            templates=templates,
            overrides=overrides,
            total_samples=5,
            template_probs=[0.5],  # Incorrect length
            random_state=42
        )
