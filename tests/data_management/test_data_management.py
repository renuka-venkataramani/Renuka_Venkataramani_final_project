import pytest
from final_project.config import TEST_DIR
from final_project.utilities import read_yaml


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")


def test_load_data(file_path):
    with pytest.raises(ValueError):
        file_path = "Examplefile/path/sample.pkl"
        assert load_data(file_path), "The covariance matrix should be positive definite"
