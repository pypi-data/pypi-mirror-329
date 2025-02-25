import pytest


@pytest.fixture(scope="session")
def resource_files():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    return files
