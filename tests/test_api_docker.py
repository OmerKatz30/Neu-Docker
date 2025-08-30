import pytest
import requests

API_BASE_URL = "http://localhost:5000"

@pytest.mark.parametrize("input_str, expected", [
    ("The quick brown fox jumps over the lazy dog", "dog lazy the over jumps fox brown quick The"),
    ("Hello, world!", "world! Hello,"),
    ("a", "a"),
    ("Hello @#$ world", "world @#$ Hello"),
])
def test_reverse_api_success(app_container, input_str, expected):
    response = requests.get(f"{API_BASE_URL}/reverse", params={'in': input_str}, timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == expected

def test_reverse_missing_param(app_container):
    response = requests.get(f"{API_BASE_URL}/reverse", timeout=5)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Missing 'in' query parameter"

def test_reverse_empty_input(app_container):
    response = requests.get(f"{API_BASE_URL}/reverse", params={'in': ""}, timeout=5)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Input string cannot be empty"

def test_restore_after_reverse(app_container):
    input_str = "Test case for restore"
    expected_result = "restore for case Test"
    response = requests.get(f"{API_BASE_URL}/reverse", params={'in': input_str}, timeout=5)
    assert response.status_code == 200
    response = requests.get(f"{API_BASE_URL}/restore", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == expected_result