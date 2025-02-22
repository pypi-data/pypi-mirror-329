import numpy as np
from sklearn.base import clone

def generate_heterogeneous_learners(
    templates,          # list of pre-initialized base learner instances (templates)
    overrides,          # list of dicts, one per template mapping parameter names to sampling callables
    total_samples,      # total number of learner instances to generate
    template_probs=None,  # if "round_robin", then round-robin selection is used; otherwise, an array-like probability distribution
    random_state=None   # seed or RandomState for reproducibility
):
    """
    Generate a flat list of heterogeneous base learner instances by applying independent
    hyperparameter sampling to each template.

    Each generated learner is created by cloning a template (using scikit-learn's `clone`)
    and then updating its hyperparameters based on independently sampled values provided
    via the `overrides` dictionaries.

    Parameters
    ----------
    templates : list
        A list of pre-initialized scikit-learn estimator instances that serve as templates.
    overrides : list of dict
        A list of dictionaries (one per template). Each dictionary maps hyperparameter
        names (as strings) to callables that accept a random state (`rng`) and return a sampled value.
        All override values must be callable.
    total_samples : int
        The total number of new base learner instances to generate.
    template_probs : array-like or str or None, optional
        If array-like, a probability distribution over the templates. Must sum to 1 and have the same
        length as `templates`. If the string "round_robin" (case-insensitive) is provided, then round-robin
        selection is used. If None, a uniform random distribution is used.
    random_state : int, np.random.RandomState, or None, optional
        A seed or RandomState instance for reproducibility in sampling hyperparameters.

    Returns
    -------
    list
        A flat list of newly generated base learner instances with updated hyperparameters.

    Raises
    ------
    ValueError
        If an override value is not callable, or if the lengths of `templates` and `overrides`
        do not match, or if `template_probs` is provided with the wrong length.
    """
    # Set up a RandomState instance for reproducibility.
    if random_state is None:
        rng = np.random.RandomState()
    elif isinstance(random_state, (int, np.integer)):
        rng = np.random.RandomState(random_state)
    else:
        rng = random_state

    n_templates = len(templates)
    if len(overrides) != n_templates:
        raise ValueError("Length of overrides must match the number of templates.")
    
    use_round_robin = False
    if template_probs is None:
        # Use uniform random probabilities if none provided.
        template_probs = np.ones(n_templates) / n_templates
    elif isinstance(template_probs, str):
        if template_probs.lower() == "round_robin":
            use_round_robin = True
        else:
            raise ValueError("If template_probs is a string, it must be 'round_robin'.")
    else:
        template_probs = np.asarray(template_probs)
        if template_probs.shape[0] != n_templates:
            raise ValueError("Length of template_probs must match the number of templates.")

    generated_learners = []
    for i in range(total_samples):
        # Choose a template index.
        if use_round_robin:
            chosen_index = i % n_templates
        else:
            chosen_index = rng.choice(n_templates, p=template_probs)
        
        base_template = templates[chosen_index]
        override_dict = overrides[chosen_index]
        
        # Create a new learner instance by cloning the template.
        new_learner = clone(base_template)
        
        # Sample new hyperparameter values using the provided callables.
        sampled_params = {}
        for param, sampler in override_dict.items():
            if not callable(sampler):
                raise ValueError(f"Override for parameter '{param}' must be callable.")
            sampled_params[param] = sampler(rng)
        # Update the learner with the new hyperparameter values.
        new_learner.set_params(**sampled_params)
        
        generated_learners.append(new_learner)
    
    return generated_learners