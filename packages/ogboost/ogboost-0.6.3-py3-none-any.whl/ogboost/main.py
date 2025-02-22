"""
Ordinal Gradient Boosting Module
================================

This module implements a gradient boosting framework for ordinal regression tasks.
It provides:

  - A collection of link functions and their derivatives via the `LinkFunctions` class,
    used to map latent scores to probabilities (and vice versa).
  - A utility function `concordance_index` to evaluate ordinal predictions via the concordance index.
  - The `GradientBoostingOrdinal` estimator, a scikit-learn–compatible class that implements
    an iterative coordinate-descent algorithm alternating between updating a latent function
    (using base learners) and refining ordinal thresholds.

Key Features:
  - Supports both holdout- and K-fold cross-validation–based early stopping (via the
    `cv_early_stopping_splits` parameter).
  - Permits heterogeneous base learners, allowing users to supply a single estimator, a list,
    or a generator of different estimators across boosting iterations.
  - Integrates seamlessly with the scikit-learn ecosystem for hyperparameter tuning, model
    evaluation, and pipeline construction.

Example:
  >>> from ogboost import GradientBoostingOrdinal
  >>> model = GradientBoostingOrdinal(cv_early_stopping_splits=5)
  >>> model.fit(X_train, y_train)
  >>> preds = model.predict(X_test)

See Also:
  - sklearn.ensemble.GradientBoostingClassifier
  - statsmodels.miscmodels.ordinal_model.OrderedModel
"""

from itertools import combinations
import warnings
import numpy as np
from scipy.stats import norm
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils.validation import check_is_fitted, validate_data
from sklearn.model_selection import train_test_split, KFold
import matplotlib.pyplot as plt

class LinkFunctions:
    """
    A collection of static methods that implement common link functions for ordinal regression,
    along with their derivatives and inverse functions. Supported link functions include:

    - Probit: Uses the standard normal cumulative distribution function.
    - Logit: Uses the logistic function.
    - Complementary log-log (cloglog): Uses the complementary log-log transformation.

    Each link function is provided with:
    - A forward transformation (e.g., `probit`, `logit`, `cloglog`).
    - A derivative (e.g., `probit_derivative`, `logit_derivative`, `cloglog_derivative`).
    - An inverse function (e.g., `probit_inverse`, `logit_inverse`, `cloglog_inverse`).

    These functions are intended to facilitate the mapping between the continuous latent
    space and the discrete ordinal outcomes.
    """
    @staticmethod
    def probit(x):
        return norm.cdf(x)

    @staticmethod
    def probit_derivative(x):
        return norm.pdf(x)

    @staticmethod
    def probit_inverse(p):
        return norm.ppf(p)

    @staticmethod
    def logit(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def logit_derivative(x):
        sig = 1 / (1 + np.exp(-x))
        return sig * (1 - sig)

    @staticmethod
    def logit_inverse(p):
        return np.log(p / (1 - p))

    @staticmethod
    def cloglog(x):
        return 1 - np.exp(-np.exp(x))

    @staticmethod
    def cloglog_derivative(x):
        return np.exp(x - np.exp(x))

    @staticmethod
    def cloglog_inverse(p):
        return np.log(-np.log(1 - p))


def concordance_index(y_true, y_pred, sample_weight=None):
    """
    Compute the concordance index (C-index) for ordinal predictions, optionally weighted by sample weights.

    Parameters:
    y_true : array-like
        True ordinal labels.
    y_pred : array-like
        Predicted ordinal scores or labels.
    sample_weight : array-like, optional
        Sample weights (must have the same length as y_true). If None, equal weights are assumed.

    Returns:
    float
        The computed concordance index. Returns 0.0 if no permissible pairs are found.

    Raises:
    ValueError:
        If input arrays have mismatched lengths or if sample_weight is invalid (e.g., contains negative values).
    """
    from itertools import combinations
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    if sample_weight is None:
        sample_weight = np.ones_like(y_true, dtype=float)
    else:
        sample_weight = np.asarray(sample_weight)
        if sample_weight.shape[0] != y_true.shape[0]:
            raise ValueError("sample_weight must have the same length as y_true")
        if np.any(sample_weight < 0):
            raise ValueError("sample_weight cannot contain negative values")
        if np.sum(sample_weight) <= 0:
            raise ValueError("sample_weight must have positive sum")
    
    if y_true.shape[0] != y_pred.shape[0]:
        raise ValueError("y_true and y_pred must have the same length")
    
    pairs = list(combinations(range(len(y_true)), 2))
    concordant, permissible = 0.0, 0.0
    
    for i, j in pairs:
        if y_true[i] != y_true[j]:  # skip ties in true labels
            w_ij = sample_weight[i] * sample_weight[j]
            permissible += w_ij
            if (y_true[i] < y_true[j] and y_pred[i] < y_pred[j]) or \
               (y_true[i] > y_true[j] and y_pred[i] > y_pred[j]):
                concordant += w_ij
            elif y_pred[i] == y_pred[j]:
                concordant += 0.5 * w_ij

    return concordant / permissible if permissible > 0 else 0.0


class GradientBoostingOrdinal(ClassifierMixin, BaseEstimator):
    """
    GradientBoostingOrdinal
    -----------------------

    Gradient Boosting for Ordinal Regression.

    This estimator implements a gradient boosting framework tailored for ordinal regression tasks.
    It employs a coordinate-descent algorithm that alternates between:
    - Updating a latent function `g(x)` using regression-based base learners.
    - Refining the threshold vector `θ` to partition the latent space into ordered categories.

    Key Features:
    - **Heterogeneous Base Learners:** The `base_learner` parameter accepts a single estimator,
        a list, or a generator of estimators. This allows different models to be used in successive
        boosting iterations.
    - **CV-Based Early Stopping:** In addition to a conventional holdout-set approach, the parameter
        `cv_early_stopping_splits` enables K-fold cross-validation for a more robust determination of the
        optimal number of boosting iterations.
    - **Customizable Link Functions:** Supports 'probit', 'logit', and 'cloglog' link functions for
        transforming latent scores to class probabilities.
    - **scikit-learn Compatibility:** Inherits from `BaseEstimator` and `ClassifierMixin` for seamless
        integration into scikit-learn pipelines and model selection routines.

    Parameters:
    base_learner : estimator or list/generator of estimators, default=DecisionTreeRegressor(max_depth=3)
        The base learner(s) used to update the latent function. Different learners can be used across iterations.
    n_estimators : int, default=100
        Maximum number of boosting iterations.
    learning_rate : float, default=0.1
        Learning rate for the latent function updates.
    learning_rate_thresh : float, default=0.001
        Learning rate for the threshold updates.
    validation_fraction : float, default=0.1
        Fraction of data to use as a holdout set for early stopping (if CV is not used).
    n_iter_no_change : int or None, default=None
        Number of iterations with no improvement to wait before stopping early.
    tol : float, default=1e-4
        Tolerance for measuring improvement in early stopping.
    validation_stratify : bool, default=True
        Whether to stratify the holdout set by ordinal class.
    n_class : int or None, default=None
        Number of ordinal classes. If None, inferred from the training data.
    link_function : {'probit', 'logit', 'cloglog'}, default='probit'
        Link function used to transform latent scores to probabilities.
    subsample : float, default=1.0
        Fraction of samples used to fit each base learner.
    verbose : int, default=0
        Verbosity level.
    random_state : int, RandomState instance, or None, default=None
        Seed or random state for reproducibility.
    cv_early_stopping_splits : int or None, default=None
        If an integer > 1, uses K-fold cross-validation for early stopping; otherwise, a holdout set is used.

    Attributes:
    classes_ : array-like
        Array of unique ordinal classes.
    n_estimators_ : int
        Actual number of boosting iterations performed.
    _path : dict
        Contains the evolution of the latent function, thresholds, loss values, and other training details.
    _cv_path : dict
        Stores cross-validation loss history and the best iteration when CV early stopping is enabled.

    Methods:
    fit(X, y, sample_weight=None)
        Fit the gradient boosting ordinal regression model.
    predict(X)
        Predict ordinal class labels.
    predict_proba(X)
        Predict class probabilities.
    decision_function(X)
        Compute the latent function values for input samples.
    score(X, y, sample_weight=None, pred_type='latent')
        Compute the concordance index.
    plot_loss(...)
        Plot the evolution of the loss over boosting iterations.
    staged_predict(...), staged_predict_proba(...), staged_decision_function(...)
        Yield predictions at each boosting iteration.

    Example:
    >>> from ogboost import GradientBoostingOrdinal
    >>> model = GradientBoostingOrdinal(cv_early_stopping_splits=5, n_iter_no_change=10)
    >>> model.fit(X_train, y_train)
    >>> preds = model.predict(X_test)
    """

    def __init__(
        self,
        base_learner=DecisionTreeRegressor(max_depth=3, criterion='friedman_mse'),
        n_estimators=100,
        learning_rate=1e-1,
        learning_rate_thresh=1e-3,
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=1e-4,
        validation_stratify=True,
        n_class=None,
        link_function='probit',
        subsample=1.0,
        verbose=0,
        random_state=None,
        cv_early_stopping_splits=None
    ):
        self.base_learner = base_learner
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.learning_rate_thresh = learning_rate_thresh
        self.validation_fraction = validation_fraction
        self.n_iter_no_change = n_iter_no_change
        self.tol = tol
        self.validation_stratify = validation_stratify
        self.n_class = n_class
        self.link_function = link_function
        self.subsample = subsample
        self.verbose = verbose
        self.random_state = random_state
        self.cv_early_stopping_splits = cv_early_stopping_splits

    def _setup_base_learners(self):
        """
        Convert self.base_learner into a 'template' list of length n_estimators.
        
        Each item in this list is a cloned version of the user-supplied base learner(s),
        but we do NOT assign distinct random seeds here. We'll do that per-iteration/fold
        so each sub-model also gets its own reproducible seed.
        
        Returns
        -------
        template_learners : list of length n_estimators
            Each entry is an unfit cloned estimator, one 'template' per iteration.
        """
        import types  # for checking generator types
        
        n = self.n_estimators
        
        # Helper to clone without assigning random_state
        # (distinct seeds will be assigned when we actually use them)
        def clone_without_seed(obj):
            return clone(obj)

        # 1) Single estimator (default or user-supplied)
        #    Check if not a list or generator => treat as single
        if (not hasattr(self.base_learner, '__iter__')) or isinstance(self.base_learner, BaseEstimator):
            return [clone_without_seed(self.base_learner) for _ in range(n)]

        # 2) If it's a list
        if isinstance(self.base_learner, list):
            if len(self.base_learner) < n:
                raise ValueError(
                    "base_learner list has fewer elements than n_estimators."
                )
            # Take exactly n items, clone each
            return [clone_without_seed(bl) for bl in self.base_learner[:n]]

        # 3) If it's a generator or iterator
        if hasattr(self.base_learner, '__next__') or hasattr(self.base_learner, '__iter__'):
            template_learners = []
            for i in range(n):
                try:
                    next_learner = next(self.base_learner)
                except StopIteration:
                    raise ValueError(
                        "Not enough learners yielded from base_learner generator "
                        f"to reach n_estimators={n}."
                    )
                template_learners.append(clone_without_seed(next_learner))
            return template_learners

        # Otherwise, unrecognized type
        raise ValueError(
            "base_learner must be a single estimator, a list of estimators, "
            "or a generator/iterator yielding estimators."
        )

    def _get_random_state(self):
        if self.random_state is None:
            return np.random.mtrand._rand  # Default global RNG
        if isinstance(self.random_state, (int, np.integer)):
            return np.random.RandomState(self.random_state)
        if isinstance(self.random_state, np.random.RandomState):
            return self.random_state
        raise ValueError("random_state must be None, an int, or a RandomState instance.")

    def _has_random_state(self, obj):
        return 'random_state' in obj.get_params()
    
    def fit(self, X, y, sample_weight=None):
        """
        Fit the GradientBoostingOrdinal model to the given training data.

        This method implements a gradient boosting procedure specialized for
        ordinal regression. It builds (and stores) an internal list of base
        learners that iteratively update a latent function g(x) and refine the
        ordinal threshold vector θ.

        Depending on the parameter settings:
        - If `cv_early_stopping_splits > 1`, the model uses K-fold cross-validation
            for early stopping. Training stops when no improvement is observed
            over `n_iter_no_change` iterations in the validation fold.
        - Otherwise, if `n_iter_no_change` is not None, a holdout set (fraction
            of the training data specified by `validation_fraction`) is used for
            early stopping.
        - If neither mechanism is enabled, the model runs for all `n_estimators`
            boosting iterations.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data features.
        y : array-like of shape (n_samples,)
            Ordinal target values. Must be integers in a suitable range
            (0 to n_class-1). If `n_class` is None, the maximum label in `y`
            determines n_class = max(y) + 1.
        sample_weight : array-like of shape (n_samples,), optional
            Sample weights to apply in the loss function. Must have non-negative
            values and a positive sum. If None (default), equal weights are assumed.

        Returns
        -------
        self : GradientBoostingOrdinal
            Fitted estimator.

        Raises
        ------
        ValueError
            - If `y` has invalid ordinal values (e.g., negative or beyond n_class-1).
            - If `sample_weight` is negative, zero-sum, or mismatched in length.
            - If `link_function` is not one of {‘probit’, ‘logit’, ‘cloglog’}.
            - If `subsample` is not in (0, 1].
            - If mismatch occurs between `templates`/`overrides` in heterogeneous 
            learner scenarios.
        
        Notes
        -----
        - After calling `fit`, the model stores the trained base learners and the
        final thresholds in `self._path` and `self._final`.
        - Early stopping details (e.g., holdout or CV) are determined by the
        constructor parameters `n_iter_no_change`, `validation_fraction`, and
        `cv_early_stopping_splits`.
        - When using K-fold CV, the internal `_fit_cv` method is invoked; otherwise,
        the holdout-based approach is used if `n_iter_no_change` is specified.
        """
        # A random state for distinct seeds each iteration
        self._rs_global = self._get_random_state()
        
        # == (New Step) Build the 'template' base learners list ==
        self._template_learners = self._setup_base_learners()

        # == Added or Modified for CV ==
        # If user specified K-fold CV for early stopping, we delegate to _fit_cv:
        if (self.cv_early_stopping_splits is not None 
            and isinstance(self.cv_early_stopping_splits, int) 
            and self.cv_early_stopping_splits > 1):
            return self._fit_cv(X, y, sample_weight)

        # == Otherwise, proceed with the original logic (unchanged except for minimal housekeeping) ==
        #base_learner = clone(self.base_learner)
        #if hasattr(base_learner, 'random_state'):
        #    base_learner.set_params(random_state=self.random_state)

        if sample_weight is None:
            sample_weight = np.ones_like(y, dtype=float)
        else:
            sample_weight = np.asarray(sample_weight)
            if sample_weight.shape[0] != y.shape[0]:
                raise ValueError("sample_weight must have the same length as y")
            if np.any(sample_weight < 0):
                raise ValueError("sample_weight cannot contain negative values")
            if np.sum(sample_weight) <= 0:
                raise ValueError("sample_weight must have positive sum")

        X, y = validate_data(self, X, y)

        if self.link_function not in ['probit', 'logit', 'cloglog']:
            raise ValueError("Invalid link_function. Must be 'probit', 'logit', or 'cloglog'.")

        if not 0 < self.subsample <= 1:
            raise ValueError("subsample must be in the range (0, 1].")

        if self.n_iter_no_change:
            (X, X_holdout, 
             y, y_holdout, 
             sample_weight, sample_weight_holdout) = train_test_split(
                X, y, sample_weight,
                test_size=self.validation_fraction,
                stratify=y if self.validation_stratify else None,
                random_state=self._rs_global
            )

        ylist = self._validate_ordinal(y)
        self.classes_ = np.arange(self._n_class)

        g_init, theta_init = self._initialize(
            y, n_class=self._n_class, laplace_smoothing=True
        )
        loss_init = self._loss_function(y, g_init, theta_init, sample_weight=sample_weight)

        g, theta, loss = g_init, theta_init, loss_init
        loss_all = [loss]
        learner_all = []
        intercept_all = []
        g_all = [g.copy()]
        theta_all = [theta.copy()]

        if self.n_iter_no_change:
            g_init_holdout = self._initialize_g(y_holdout)
            loss_holdout = self._loss_function(
                y_holdout, g_init_holdout, theta_init, sample_weight=sample_weight_holdout
            )
            loss_all_holdout = [loss_holdout]
            g_holdout = g_init_holdout.copy()

        no_change = False
        lr_theta = self.learning_rate_thresh
        lr_theta_all = [lr_theta]

        if self.n_iter_no_change:
            loss_history = np.full(self.n_iter_no_change, np.inf)

        for p in range(self.n_estimators):
            if self.subsample < 1.0:
                n_samples = X.shape[0]
                sample_indices = self._rs_global.choice(
                    np.arange(n_samples),
                    size=int(n_samples * self.subsample),
                    replace=False,
                    p=sample_weight / np.sum(sample_weight) 
                      if sample_weight is not None else None
                )
                X_sub, y_sub = X[sample_indices], y[sample_indices]
                sw_sub = sample_weight[sample_indices]
            else:
                X_sub, y_sub, sw_sub = X, y, sample_weight
                sample_indices = np.arange(X.shape[0])

            # ============ NEW: distinct random state for iteration p
            # clone the p-th template, set random_state if available
            base_learner_this_iter = clone(self._template_learners[p])
            if self._has_random_state(base_learner_this_iter):
                # different seed each iteration
                base_learner_this_iter.set_params(
                    random_state=self._rs_global.randint(0, 2**32 - 1, dtype='uint64')
                )
            # ============ END NEW

            dg = self._derivative_g(y_sub, theta, g[sample_indices], sw_sub)
            weak_learner, intercept = GradientBoostingOrdinal._fit_weak_learner(
                X_sub, -dg, base_learner_this_iter
            )
            h_full = weak_learner.predict(X) + intercept
            g = GradientBoostingOrdinal._update_g(g, h_full, lr=self.learning_rate)

            loss = self._loss_function(y, g, theta, sample_weight=sample_weight)
            loss_all.append(loss)

            dtheta = self._derivative_threshold(X, ylist, theta, g, sample_weight=sample_weight)
            theta, lr_theta = self._update_thresh(
                theta, dtheta, lr_theta, y, g, frac=0.5, sample_weight=sample_weight
            )
            loss = self._loss_function(y, g, theta, sample_weight=sample_weight)
            loss_all.append(loss)

            learner_all.append(weak_learner)
            intercept_all.append(intercept)
            g_all.append(g.copy())
            theta_all.append(theta.copy())
            lr_theta_all.append(lr_theta)

            if self.n_iter_no_change:
                h_holdout = weak_learner.predict(X_holdout) + intercept
                g_holdout = GradientBoostingOrdinal._update_g(
                    g_holdout, h_holdout, lr=self.learning_rate
                )
                loss_holdout = self._loss_function(
                    y_holdout, g_holdout, theta, sample_weight=sample_weight_holdout
                )
                loss_all_holdout.append(loss_holdout)

                # Verbose
                if self.verbose > 0:
                    if self.verbose == 1:
                        if p % max(1, self.n_estimators // 10) == 0:
                            print(f"Iteration {p}/{self.n_estimators}, "
                                  f"Loss: {loss:.4f}, Holdout Loss: {loss_holdout:.4f}")
                    elif self.verbose > 1:
                        print(f"Iteration {p}, Loss: {loss:.4f}, Holdout Loss: {loss_holdout:.4f}")

                # Check for improvement
                if np.any(loss_holdout + self.tol < loss_history):
                    loss_history = np.roll(loss_history, -1)
                    loss_history[-1] = loss_holdout
                else:
                    no_change = True
                    if self.verbose > 0:
                        print(f"Stopping early after {p+1} iterations due to no significant improvement.")
                    break
            else:
                if self.verbose > 0:
                    if self.verbose == 1:
                        if p % max(1, self.n_estimators // 10) == 0:
                            print(f"Iteration {p}/{self.n_estimators}, Loss: {loss:.4f}")
                    elif self.verbose > 1:
                        print(f"Iteration {p}, Loss: {loss:.4f}")

        self.n_estimators_ = p + 1 if no_change else self.n_estimators
        self._init = {'g': g_init, 'theta': theta_init, 'loss': loss_init}
        self._final = {'g': g, 'theta': theta, 'loss': loss_all[-1]}

        loss_all = np.array(loss_all)
        self._path = {
            'g': np.array(g_all),
            'theta': np.array(theta_all),
            'loss': loss_all[::2],  # every other step after g, then after theta
            'loss_diff': self._check_loss_change(loss_all),
            'learner': learner_all,
            'intercept': np.array(intercept_all),
            'learning_rate_thresh': np.array(lr_theta_all)
        }
        if self.n_iter_no_change:
            self._path['loss_holdout'] = np.array(loss_all_holdout)

        return self

    def _fit_cv(self, X, y, sample_weight):
        """
        Internal method to perform K-fold cross-validation at each boosting iteration
        for early stopping.

        Splits the data into K folds, and for each fold, trains on (K-1) folds and
        tracks performance on the held-out fold. This helps determine whether to stop
        early if there is no improvement in validation loss.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Training features.
        y : ndarray of shape (n_samples,)
            Ordinal target labels.
        sample_weight : ndarray of shape (n_samples,), optional
            Sample weights, must be non-negative with positive sum.

        Returns
        -------
        self : GradientBoostingOrdinal
            Fitted estimator with updated internal attributes for cross-validation
            early stopping (e.g., self._cv_path, best iteration, final thresholds, etc.).

        Notes
        -----
        - This method is called automatically from `fit` if `cv_early_stopping_splits > 1`.
        - The final model’s parameters (latent function and thresholds) are updated
        after each boosting iteration based on the full dataset as well.
        """
        # ---------------------------
        # Preliminary validation logic
        # ---------------------------
        K = self.cv_early_stopping_splits
        if K <= 1:
            raise ValueError("cv_early_stopping_splits must be > 1 or None.")

        if sample_weight is None:
            sample_weight = np.ones_like(y, dtype=float)
        else:
            sample_weight = np.asarray(sample_weight)
            if sample_weight.shape[0] != y.shape[0]:
                raise ValueError("sample_weight must have same length as y.")
            if np.any(sample_weight < 0):
                raise ValueError("sample_weight cannot contain negative values.")
            if np.sum(sample_weight) <= 0:
                raise ValueError("sample_weight must have positive sum.")

        X, y = validate_data(self, X, y)
        if self.link_function not in ['probit', 'logit', 'cloglog']:
            raise ValueError("Invalid link_function. Must be 'probit', 'logit', or 'cloglog'.")
        if not 0 < self.subsample <= 1:
            raise ValueError("subsample must be in (0, 1].")

        # Validate ordinal data
        ylist = self._validate_ordinal(y)
        self.classes_ = np.arange(self._n_class)

        g_init_full, theta_init_full = self._initialize(
            y, n_class=self._n_class, laplace_smoothing=True
        )
        loss_init_full = self._loss_function(
            y, g_init_full, theta_init_full, sample_weight=sample_weight
        )

        g_full = g_init_full.copy()
        theta_full = theta_init_full.copy()
        loss_full = loss_init_full

        # Keep track of final model's evolution
        loss_all_full = [loss_full]
        g_all_full = [g_full.copy()]
        theta_all_full = [theta_full.copy()]
        learners_full = []
        intercepts_full = []
        lr_theta = self.learning_rate_thresh
        lr_theta_all = [lr_theta]

        # Store CV details
        self._cv_path = {
            'cv_loss': [],
            'best_iteration': 0
        }

        # -------------------
        # Build K folds
        # -------------------
        from sklearn.model_selection import KFold
        kf = KFold(n_splits=K, shuffle=True, random_state=self._rs_global)

        fold_models = []
        for train_idx, val_idx in kf.split(X, y):
            fm = {}
            fm['train_idx'] = train_idx
            fm['val_idx'] = val_idx
            y_train_fold = y[train_idx]
            fm['g_train'], fm['theta'] = self._initialize(
                y_train_fold, n_class=self._n_class, laplace_smoothing=True
            )
            fm['g_holdout'] = np.zeros(len(val_idx), dtype=float)
            fold_models.append(fm)

        # ------------------------
        # Early stopping variables
        # ------------------------
        no_change = False
        if self.n_iter_no_change:
            loss_history = np.full(self.n_iter_no_change, np.inf)

        # =========================
        # Main boosting iterations
        # =========================
        for iteration in range(self.n_estimators):

            # 1) Update each fold model
            for fm in fold_models:
                train_idx = fm['train_idx']
                val_idx = fm['val_idx']

                # Grab training data
                X_train_fold = X[train_idx]
                y_train_fold = y[train_idx]
                sw_train_fold = sample_weight[train_idx]

                # Possibly subsample from the fold's training
                n_train_local = len(train_idx)
                local_indices = np.arange(n_train_local)

                if self.subsample < 1.0:
                    # Convert sw_train_fold to distribution
                    sw_dist = sw_train_fold / sw_train_fold.sum()
                    chosen_local = self._rs_global.choice(
                        local_indices,
                        size=int(n_train_local * self.subsample),
                        replace=False,
                        p=sw_dist
                    )
                else:
                    chosen_local = local_indices

                # Gather the chosen rows from the fold training
                chosen_global = train_idx[chosen_local]
                X_sub = X[chosen_global]
                y_sub = y[chosen_global]
                sw_sub = sample_weight[chosen_global]

                # Derivative wrt fold's training latent g
                g_sub = fm['g_train'][chosen_local]
                dg = self._derivative_g(
                    y_sub,
                    fm['theta'],
                    g_sub,
                    sample_weight=sw_sub
                )

                # Fit a weak learner on -dg
                fold_learner = clone(self._template_learners[iteration])
                if self._has_random_state(fold_learner):
                    fold_learner.set_params(
                        random_state=self._rs_global.randint(0, 2**32 - 1, dtype='uint64')
                    )
                weak_learner_fold, intercept_fold = self._fit_weak_learner(
                    X_sub, -dg, fold_learner
                )

                # Update entire training latent
                pred_train_fold = weak_learner_fold.predict(X_train_fold) + intercept_fold
                fm['g_train'] = self._update_g(
                    fm['g_train'], 
                    pred_train_fold, 
                    lr=self.learning_rate
                )

                # Also update the fold's holdout latent in an *accumulated* way
                # so it reflects the sum of partial predictions up to iteration t.
                pred_val_fold = weak_learner_fold.predict(X[val_idx]) + intercept_fold
                fm['g_holdout'] = self._update_g(
                    fm['g_holdout'], 
                    pred_val_fold, 
                    lr=self.learning_rate
                )

                # Update thresholds using full training data for this fold
                dtheta_fold = self._derivative_threshold(
                    X_train_fold,
                    [np.where(y_train_fold == m)[0] for m in range(self._n_class)],
                    fm['theta'],
                    fm['g_train'],
                    sample_weight=sw_train_fold
                )
                new_theta_fold, _ = self._update_thresh(
                    fm['theta'],
                    dtheta_fold,
                    self.learning_rate_thresh,
                    y_train_fold,
                    fm['g_train'],
                    frac=0.5,
                    sample_weight=sw_train_fold
                )
                fm['theta'] = new_theta_fold
                fm['base_learner'] = weak_learner_fold
                # Optionally store intercept_fold if you need it later

            # 2) Compute cross-validation loss
            cv_loss_sum = 0.0
            weight_sum = 0.0

            for fm in fold_models:
                val_idx = fm['val_idx']
                sw_val = sample_weight[val_idx]
                y_val = y[val_idx]

                # Now we have an up-to-date "fold holdout latent" in fm['g_holdout'],
                # so partial_loss is straightforward:
                partial_loss = self._loss_function(
                    y_val,
                    fm['g_holdout'],  # the already-accumulated holdout latent
                    fm['theta'],
                    sample_weight=sw_val
                )
                fold_weight = sw_val.sum()
                cv_loss_sum += partial_loss * fold_weight
                weight_sum += fold_weight

            cv_loss = cv_loss_sum / weight_sum
            self._cv_path['cv_loss'].append(cv_loss)

            # 3) Update the full-data model
            if self.subsample < 1.0:
                n_samples_full = X.shape[0]
                sw_dist_full = sample_weight / sample_weight.sum()
                sample_indices = self._rs_global.choice(
                    np.arange(n_samples_full),
                    size=int(n_samples_full * self.subsample),
                    replace=False,
                    p=sw_dist_full
                )
                X_sub, y_sub = X[sample_indices], y[sample_indices]
                sw_sub = sample_weight[sample_indices]
            else:
                sample_indices = np.arange(X.shape[0])
                X_sub, y_sub, sw_sub = X, y, sample_weight

            dg_full = self._derivative_g(y_sub, theta_full, g_full[sample_indices], sw_sub)
            
            base_learner_full = clone(self._template_learners[iteration])
            if self._has_random_state(base_learner_full):
                base_learner_full.set_params(
                    random_state=self._rs_global.randint(0, 2**32 - 1, dtype='uint64')
                )
            
            weak_learner_full, intercept_full = self._fit_weak_learner(
                X_sub, -dg_full, clone(base_learner_full)
            )
            h_full = weak_learner_full.predict(X) + intercept_full
            g_full = self._update_g(g_full, h_full, lr=self.learning_rate)

            # Evaluate loss after updating g (regression function update)
            loss_after_g = self._loss_function(y, g_full, theta_full, sample_weight=sample_weight)
            loss_all_full.append(loss_after_g)

            # Update thresholds on the full-data model
            dtheta_full = self._derivative_threshold(
                X, ylist, theta_full, g_full, sample_weight=sample_weight
            )
            theta_full, lr_theta_new = self._update_thresh(
                theta_full,
                dtheta_full,
                lr_theta,
                y,
                g_full,
                frac=0.5,
                sample_weight=sample_weight
            )
            lr_theta = lr_theta_new

            # Evaluate loss after threshold update
            loss_after_theta = self._loss_function(y, g_full, theta_full, sample_weight=sample_weight)
            loss_all_full.append(loss_after_theta)

            # Compute final-model loss on full data
            #loss_full = self._loss_function(y, g_full, theta_full, sample_weight=sample_weight)
            #loss_all_full.append(loss_full)
            g_all_full.append(g_full.copy())
            theta_all_full.append(theta_full.copy())
            learners_full.append(weak_learner_full)
            intercepts_full.append(intercept_full)
            lr_theta_all.append(lr_theta)

            # 4) Early stopping check
            no_change = False
            if self.n_iter_no_change:
                if self.verbose > 0:
                    if self.verbose == 1:
                        if iteration % max(1, self.n_estimators // 10) == 0:
                            print(f"[CV] Iteration {iteration}/{self.n_estimators}, "
                                f"CV Loss: {cv_loss:.4f}, Full Loss: {loss_full:.4f}")
                    elif self.verbose > 1:
                        print(f"[CV] Iteration {iteration}, "
                            f"CV Loss: {cv_loss:.4f}, Full Loss: {loss_full:.4f}")

                if np.any(cv_loss + self.tol < loss_history):
                    loss_history = np.roll(loss_history, -1)
                    loss_history[-1] = cv_loss
                else:
                    no_change = True
                    if self.verbose > 0:
                        print(f"[CV] Stopping early after {iteration+1} iterations.")
                    self._cv_path['best_iteration'] = iteration + 1
                    break
            else:
                if self.verbose > 0:
                    if self.verbose == 1:
                        if iteration % max(1, self.n_estimators // 10) == 0:
                            print(f"[CV] Iteration {iteration}/{self.n_estimators}, CV Loss: {cv_loss:.4f}")
                    elif self.verbose > 1:
                        print(f"[CV] Iteration {iteration}, CV Loss: {cv_loss:.4f}")

        # Done: finalize iteration count
        final_iteration = (iteration + 1) if no_change else self.n_estimators
        self.n_estimators_ = final_iteration

        # Store states
        self._init = {'g': g_init_full, 'theta': theta_init_full, 'loss': loss_init_full}
        self._final = {'g': g_full, 'theta': theta_full, 'loss': loss_all_full[-1]}

        loss_array_full = np.array(loss_all_full)
        self._path = {
            'g': np.array(g_all_full),
            'theta': np.array(theta_all_full),
            'loss': loss_array_full[::2],
            'loss_diff': self._check_loss_change(loss_array_full),
            'learner': learners_full,
            'intercept': np.array(intercepts_full),
            'learning_rate_thresh': np.array(lr_theta_all)
        }
        self._cv_path['best_iteration'] = final_iteration

        return self

    # Utility method to map 'chosen' indices to the position within 'train_idx'
    @staticmethod
    def _index_in(chosen, train_idx):
        pos_map = {}
        for i, idx in enumerate(train_idx):
            pos_map[idx] = i
        return [pos_map[c] for c in chosen]


    # ================
    # All other methods (unchanged)
    # ================
    def decision_function(self, X):
        check_is_fitted(self)
        X = validate_data(self, X, reset=False)
        per_iter_raw = np.array([
            learner.predict(X) + self._path['intercept'][p]
            for p, learner in enumerate(self._path['learner'])
        ])
        g_init = self._initialize_g(np.zeros(X.shape[0]))
        final_raw = np.sum(per_iter_raw[:self.n_estimators_], axis=0) * self.learning_rate + g_init
        return final_raw

    def staged_decision_function(self, X):
        check_is_fitted(self)
        X = validate_data(self, X, reset=False)
        per_iter_raw = np.array([
            learner.predict(X) + self._path['intercept'][p]
            for p, learner in enumerate(self._path['learner'])
        ])
        g_init = self._initialize_g(np.zeros(X.shape[0]))
        cum_preds = np.cumsum(per_iter_raw, axis=0) * self.learning_rate + g_init
        for i in range(cum_preds.shape[0]):
            yield cum_preds[i, :]

    def predict_proba(self, X):
        check_is_fitted(self)
        latent_values = self.decision_function(X)
        final_theta = self._path['theta'][-1]
        return self._probabilities(latent_values, final_theta, y=None)

    def staged_predict_proba(self, X):
        check_is_fitted(self)
        staged_latent = self.staged_decision_function(X)
        for i, g_iter in enumerate(staged_latent):
            theta_idx = min(i + 1, len(self._path['theta']) - 1)
            yield self._probabilities(g_iter, self._path['theta'][theta_idx], y=None)

    def predict(self, X):
        check_is_fitted(self)
        probs = self.predict_proba(X)
        return self._class_labels(probs)

    def staged_predict(self, X):
        check_is_fitted(self)
        for stage_probs in self.staged_predict_proba(X):
            yield self._class_labels(stage_probs)

    def score(self, X, y, sample_weight=None, pred_type='latent'):
        if pred_type == 'labels':
            y_pred = self.predict(X)
        elif pred_type == 'latent':
            y_pred = self.decision_function(X)
        else:
            raise ValueError("pred_type must be 'labels' or 'latent'")
        return concordance_index(y, y_pred, sample_weight=sample_weight)

    def plot_loss(self, show=True, return_fig=False, **kwargs):
        """
        Plot the training and validation loss over boosting iterations, 
        along with the loss improvement for regression function and threshold updates.

        This method generates two side-by-side plots:
        - The left plot shows the training loss and, if available, the validation loss.
        - The right plot shows the loss improvement at each iteration, 
        separately for updates to the regression function and the threshold vector.

        Parameters
        ----------
        show : bool, default=True
            Whether to immediately display the plot.
            If False, the plot is not shown but can be returned.

        return_fig : bool, default=False
            Whether to return the Matplotlib figure object.
            This can be useful for further customization or saving to a file.

        **kwargs : dict, optional
            Customization options for plot aesthetics. 
            The following keyword arguments are supported:

            - `figsize`: tuple, default=(12, 5)
                Figure size in inches (width, height).
            
            - `training_style`: dict, optional
                Style options for the training loss curve (e.g., `{"color": "blue", "linestyle": "--"}`).
            
            - `validation_style`: dict, optional
                Style options for the validation loss curve (e.g., `{"color": "red", "linestyle": "-."}`).
            
            - `improvement_style`: dict, optional
                Style options for the loss improvement curves for regression function 
                and threshold updates (e.g., `{"color": "green", "linestyle": ":"}`).

            - `title_loss`: str, default="Cross-Entropy Loss"
                Title for the training and validation loss plot.

            - `xlabel_loss`: str, default="Boosting Iteration"
                Label for the x-axis of the training and validation loss plot.

            - `ylabel_loss`: str, default="CE Loss"
                Label for the y-axis of the training and validation loss plot.

            - `title_improvement`: str, default="Cross-Entropy Loss Improvement"
                Title for the loss improvement plot.

            - `xlabel_improvement`: str, default="Boosting Iteration"
                Label for the x-axis of the loss improvement plot.

            - `ylabel_improvement`: str, default="CE Loss Improvement"
                Label for the y-axis of the loss improvement plot.

            - `grid_loss`: bool, default=True
                Whether to show a grid on the training/validation loss plot.

            - `grid_improvement`: bool, default=True
                Whether to show a grid on the loss improvement plot.

        Returns
        -------
        fig : matplotlib.figure.Figure, optional
            The figure object if `return_fig=True`, otherwise None.

        Notes
        -----
        - If validation loss is unavailable (`None`), only the training loss is plotted.
        - If loss improvement data is unavailable, the second plot will indicate that data is missing.
        - The method supports all Matplotlib plot customizations via `kwargs`.

        Example
        -------
        ```python
        model = GradientBoostingOrdinal(n_estimators=100, n_iter_no_change=10)
        model.fit(X_train, y_train)
        
        # Default plot
        model.plot_loss()

        # Customized plot
        model.plot_loss(
            training_style={"color": "blue", "linestyle": "--"},
            validation_style={"color": "red", "linestyle": "-."},
            improvement_style={"color": "green", "linestyle": ":"},
            title_loss="Training and Validation Loss",
            grid_loss=False
        )
        ```
        """
        training_loss = self._path.get('loss')
        
        # Use CV loss if available; otherwise, fall back to holdout loss.
        if hasattr(self, '_cv_path') and 'cv_loss' in self._cv_path:
            validation_loss = self._cv_path['cv_loss']
        else:
            validation_loss = self._path.get('loss_holdout')
        
        loss_diff = self._path.get('loss_diff')
        if loss_diff is not None:
            loss_improvement_g = -np.array(loss_diff[0])
            loss_improvement_theta = -np.array(loss_diff[1])
        else:
            loss_improvement_g = loss_improvement_theta = None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=kwargs.get('figsize', (12, 5)))

        training_style = kwargs.get('training_style', {})
        validation_style = kwargs.get('validation_style', {})
        ax1.plot(training_loss, label="Training Loss", **training_style)
        if validation_loss is not None:
            ax1.plot(validation_loss, label="Validation Loss", **validation_style)
        ax1.set_title(kwargs.get('title_loss', 'Cross-Entropy Loss'))
        ax1.set_xlabel(kwargs.get('xlabel_loss', 'Boosting Iteration'))
        ax1.set_ylabel(kwargs.get('ylabel_loss', 'CE Loss'))
        ax1.legend()
        ax1.grid(kwargs.get('grid_loss', True))

        if loss_improvement_g is not None and loss_improvement_theta is not None:
            improvement_style = kwargs.get('improvement_style', {})
            ax2.plot(loss_improvement_g, label="Regression function", **improvement_style)
            ax2.plot(loss_improvement_theta, label="Threshold vector", **improvement_style)
            ax2.set_title(kwargs.get('title_improvement', 'Cross-Entropy Loss Improvement'))
            ax2.set_xlabel(kwargs.get('xlabel_improvement', 'Boosting Iteration'))
            ax2.set_ylabel(kwargs.get('ylabel_improvement', 'CE Loss Improvement'))
            ax2.legend()
            ax2.grid(kwargs.get('grid_improvement', True))
        else:
            ax2.text(0.5, 0.5, "No loss improvement data available",
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes)
            ax2.set_axis_off()

        if show:
            plt.show()
        else:
            plt.close(fig)
        if return_fig:
            return fig

    # ===========================
    # Internal utility methods
    # ===========================
    @staticmethod
    def _class_labels(probs, axis=1):
        return np.argmax(probs, axis=axis)

    def _probabilities(self, g, theta, y=None):
        """
        Compute the class probabilities given latent scores and thresholds.
        If `y` is not None, also compute the log-likelihood term.

        Parameters
        ----------
        g : array-like of shape (n_samples,)
            The latent function values for each sample.
        theta : array-like of shape (n_classes - 1,)
            The threshold values that partition the latent space.
        y : array-like of shape (n_samples,), optional
            If provided, compute the log-likelihood contribution as well.

        Returns
        -------
        probs : ndarray of shape (n_samples, n_classes)
            The predicted probability for each class (summarizes the intervals between thresholds).
        loglike : float
            Only returned if `y` is provided. The log-likelihood of `y` given the computed probabilities.

        Notes
        -----
        - This method applies the chosen link function to transform the latent scores
        into cumulative probabilities, then derives class-wise probabilities from differences
        of those cumulative values.
        - If `y` is provided, the second return value is `loglike`.
        """
        F = getattr(LinkFunctions, self.link_function)
        probs = np.array([
            np.diff(F(self._pad_thresholds(theta - x))) for x in g
        ])
        if y is None:
            return probs
        loglike = sum([np.log(probs[n, yn]) for n, yn in enumerate(y)])
        return probs, loglike

    @staticmethod
    def _check_loss_change(loss):
        x = np.diff(loss)
        return (x[::2], x[1::2]) # (g, theta)

    def _validate_ordinal(self, arr):
        """
        Validate and analyze an integer array of ordinal labels.

        Checks:
        - That `arr` is a NumPy integer array (no gaps in the range if self.n_class is not specified).
        - That the maximum value does not exceed n_class - 1.
        - Optionally infers n_class if not explicitly specified.

        Parameters
        ----------
        arr : ndarray of shape (n_samples,)
            The array of ordinal labels (must be integers >= 0).

        Returns
        -------
        ylist : list of ndarray
            A list of length n_class, where each entry is an index array for samples
            belonging to the corresponding class. For example, ylist[m] contains the
            indices of samples with label m.

        Raises
        ------
        ValueError
            If the array fails any of the checks (e.g., has gaps, negative values, or
            exceeds n_class - 1).
        """
        if not isinstance(arr, np.ndarray):
            raise ValueError("Input must be a numpy array")
        if arr.dtype.kind not in {'i', 'u'}:
            raise ValueError("Input array must contain integers")

        unique_values = np.unique(arr)
        min_value, max_value = unique_values[0], unique_values[-1]
        if min_value < 0:
            raise ValueError("Minimum of arr cannot be less than 0")

        if not self.n_class:
            check_gap = True
            self._n_class = max_value + 1
        else:
            check_gap = False
            self._n_class = self.n_class

        if max_value >= self._n_class:
            raise ValueError("Maximum of arr cannot be more than n_class-1")

        expected_values = np.arange(self._n_class)
        if check_gap:
            if not np.array_equal(expected_values, unique_values):
                raise ValueError("Unique values in arr have gaps")

        return [np.where(arr == m)[0] for m in expected_values]

    def _initialize(self, y, n_class=None, laplace_smoothing=False):
        return (
            GradientBoostingOrdinal._initialize_g(y),
            self._initialize_thresholds(y, n_class=n_class, laplace_smoothing=laplace_smoothing)
        )

    @staticmethod
    def _initialize_g(y):
        return np.zeros(len(y))

    def _initialize_thresholds(self, y, n_class=None, laplace_smoothing=False):
        if n_class is None:
            n_class = np.max(y) + 1
        else:
            if np.max(y) + 1 > n_class:
                raise ValueError("Class count cannot be smaller than max(y)+1")

        n_samples = len(y)
        P = (
            np.array([np.sum(y == i) + laplace_smoothing for i in range(n_class)]) 
            / (n_samples + laplace_smoothing * n_class)
        )
        cumulative_P = np.cumsum(P[:-1])
        inverse_link_func = getattr(LinkFunctions, f"{self.link_function}_inverse")
        theta = inverse_link_func(cumulative_P)
        return theta

    @staticmethod
    def _pad_thresholds(theta):
        return np.insert(theta, [0, theta.size], [-np.inf, np.inf])

    def _derivative_threshold(self, X, ylist, thresh, g, return_mean=False, sample_weight=None):
        link_func = getattr(LinkFunctions, self.link_function)
        link_derivative = getattr(LinkFunctions, f"{self.link_function}_derivative")
        
        thresh_padded = self._pad_thresholds(thresh)
        M = len(thresh)
        ret = []
        for m in range(M):
            S_m = ylist[m]
            S_mp1 = ylist[m+1]
            z_m = thresh_padded[m+1] - g[S_m]
            z_mp1 = thresh_padded[m+1] - g[S_mp1]
            v1_vec = link_derivative(z_m) / (link_func(z_m) - link_func(thresh_padded[m] - g[S_m]))
            v2_vec = link_derivative(z_mp1) / (link_func(thresh_padded[m+2] - g[S_mp1]) - link_func(z_mp1))
            if sample_weight is not None:
                v1_vec *= sample_weight[S_m]
                v2_vec *= sample_weight[S_mp1]
            v1 = np.sum(v1_vec)
            v2 = np.sum(v2_vec)
            tmp = -v1 + v2
            if return_mean:
                tmp /= X.shape[0]
            ret.append(tmp)
        return np.array(ret)

    def _derivative_g(self, y, thresh, g, sample_weight=None):
        F_prime = getattr(LinkFunctions, f"{self.link_function}_derivative")
        F = getattr(LinkFunctions, self.link_function)
        thresh_padded = self._pad_thresholds(thresh)
        num = F_prime(thresh_padded[y + 1] - g) - F_prime(thresh_padded[y] - g)
        denom = F(thresh_padded[y + 1] - g) - F(thresh_padded[y] - g)
        derivatives = num / denom
        if sample_weight is not None:
            derivatives *= sample_weight
        return derivatives

    @staticmethod
    def _fit_weak_learner(X, pseudo_resids, learner):
        learner.fit(X, pseudo_resids)
        pred = learner.predict(X)
        intercept = -np.mean(pred)
        return (learner, intercept)

    @staticmethod
    def _update_g(g, h, lr=1e-1):
        return g + lr * h

    def _loss_function(self, y, g, theta, sample_weight=None):
        F = getattr(LinkFunctions, self.link_function)
        theta_padded = self._pad_thresholds(theta)
        log_probs = np.log(F(theta_padded[y + 1] - g) - F(theta_padded[y] - g))
        if sample_weight is not None:
            return -np.mean(sample_weight * log_probs)
        return -np.mean(log_probs)

    def _update_thresh(self, thresh, dthresh, lr, y, g, frac=0.5, sample_weight=None):
        """
        Update the threshold vector for ordinal partitioning using a line-search approach.

        Attempts to find a step size that reduces the model loss when applying
        gradient-based updates to the thresholds.

        Parameters
        ----------
        thresh : ndarray of shape (n_classes - 1,)
            Current thresholds.
        dthresh : ndarray of shape (n_classes - 1,)
            Gradient of the loss with respect to the thresholds.
        lr : float
            Current learning rate (step size) for threshold updates.
        y : ndarray of shape (n_samples,)
            True ordinal labels.
        g : ndarray of shape (n_samples,)
            Current latent function values.
        frac : float, default=0.5
            Factor by which to shrink or expand the learning rate (line-search).
        sample_weight : ndarray of shape (n_samples,), optional
            Sample weights.

        Returns
        -------
        new_thresh : ndarray of shape (n_classes - 1,)
            Updated threshold values.
        updated_lr : float
            Possibly adjusted learning rate after the line-search step.

        Notes
        -----
        - `_try_thresh` is used internally to decide whether a proposed threshold
        update lowers the loss. If not, we repeatedly reduce `lr` by `frac`
        until we find an acceptable update.
        - If the update is good, we may increase `lr` by dividing it by `frac`
        to see if further improvement is possible.
        """
        this_accept = self._try_thresh(thresh, thresh - lr * dthresh, y, g, sample_weight)
        if this_accept:
            # keep doubling until reject
            lr_proposed = lr
            while this_accept:
                lr = lr_proposed
                lr_proposed = lr / frac
                this_accept = self._try_thresh(
                    thresh - lr * dthresh,
                    thresh - lr_proposed * dthresh, y, g, sample_weight
                )
        else:
            # keep halving until accept
            while not this_accept:
                lr *= frac
                this_accept = self._try_thresh(thresh, thresh - lr * dthresh, y, g, sample_weight)
        return (thresh - lr * dthresh, lr)

    def _try_thresh(self, thresh_i, thresh_f, y, g, sample_weight=None):
        with warnings.catch_warnings(record=True) as w:
            _ = self._loss_function(y, g, thresh_f, sample_weight=sample_weight)
        if w:
            return False
        return ((self._loss_function(y, g, thresh_f, sample_weight=sample_weight)
                 < self._loss_function(y, g, thresh_i, sample_weight=sample_weight))
                and (np.all(np.diff(thresh_f) > 0)))

