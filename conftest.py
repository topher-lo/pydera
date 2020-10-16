import pytest


@pytest.fixture(scope="session")
def tmp_data_directory(tmp_path_factory):
    return str(tmp_path_factory.mktemp("tmp_data"))