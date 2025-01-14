import numpy as np
import pytest


def pytest_addoption(parser):
    parser.addoption("--random-seed", action="store", help="Fix the random seed")


@pytest.fixture()
def random_seed(request) -> int:
    """Provides a test-specific random seed for reproducible "fuzz testing".

    Example use in a test:

        def test_thing(random_seed):

            # Numpy
            rs = np.random.RandomState(seed=random_seed)
            values = rs.randint(...)

            # Pytorch
            torch.manual_seed(random_seed)

            # Tensorflow
            tf.compat.v1.random.set_random_seed(random_seed)

    By default, a new seed is generated on each run of the tests. If a test
    fails, the random seed used will be displayed in the pytest logs.

    The seed can be fixed by providing a CLI option e.g:

        pytest --random-seed 123

    For numpy usage, note the legacy `RandomState` has stricter version-to-version
    compatibility guarantees than new-style `default_rng`:
    https://numpy.org/doc/stable/reference/random/compatibility.html

    """
    manual_seed = request.config.getoption("--random-seed")
    if manual_seed is not None:
        return int(manual_seed)
    else:
        # Otherwise, create a new seed for each test
        rs = np.random.RandomState()
        return rs.randint(0, 1000)


@pytest.fixture(autouse=True)
def global_random_seed():
    """Set the global numpy random seed before each test

    Nb. Tests that use random numbers should instantiate a local
    `np.random.RandomState` rather than use the global numpy random state.
    """
    np.random.seed(0)
