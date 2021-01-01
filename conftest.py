import pytest


@pytest.fixture(scope="session")
def tmp_data_directory(tmp_path_factory):
    """Creates temporary directory and returns its path.
    """
    return str(tmp_path_factory.mktemp("getdera"))