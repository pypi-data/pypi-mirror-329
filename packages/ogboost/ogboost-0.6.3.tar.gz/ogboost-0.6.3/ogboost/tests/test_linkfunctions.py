import numpy as np
from ogboost import LinkFunctions
import pytest

@pytest.mark.parametrize("func, inv_func, x", [
    (LinkFunctions.probit, LinkFunctions.probit_inverse, np.array([-1, 0, 1])),
    (LinkFunctions.logit, LinkFunctions.logit_inverse, np.array([-1, 0, 1])),
    (LinkFunctions.cloglog, LinkFunctions.cloglog_inverse, np.array([-1, 0, 1]))
])
def test_link_inverse(func, inv_func, x):
    # test that applying a function and then its inverse recovers an approximate value
    y = func(x)
    x_recov = inv_func(y)
    np.testing.assert_allclose(x, x_recov, atol=1e-5)