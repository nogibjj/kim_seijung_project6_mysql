import os
from main import extract, load, query

# Constants for paths
DATASET_PATH = "../data/titanic.csv"
LOG_PATH = "log.md"


def test_extract():
    """Test the extract function."""
    # Clean up before running the test
    if os.path.exists(DATASET_PATH):
        os.remove(DATASET_PATH)

    # Execute extract function
    dataset_path = extract()

    # Check if the dataset was extracted successfully
    assert dataset_path == DATASET_PATH
    assert os.path.exists(DATASET_PATH)


def test_load():
    """Test the load function."""
    # Make sure dataset is extracted first
    if not os.path.exists(DATASET_PATH):
        extract()

    # Execute load function
    load_status = load(DATASET_PATH)

    # Verify that the data was loaded successfully
    assert "Success" in load_status


def test_query():
    """Test the query function."""
    # Remove existing log.md file before running the test
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    # Execute query function
    query()

    # Check if log.md is generated
    assert os.path.exists(LOG_PATH)
