import pytest

@pytest.mark.parametrize("input_str, expected", [
    ("The quick brown fox jumps over the lazy dog", "dog lazy the over jumps fox brown quick The"),
    ("Hello, world!", "world! Hello,"),
    ("a", "a"),
    ("Hello @#$ world", "world @#$ Hello"),
])
def test_reverse_api_success(client, input_str, expected):
    response = client.get(f"/reverse?in={input_str}")
    assert response.status_code == 200
    data = response.json
    assert data["result"] == expected

def test_reverse_missing_param(client):
    response = client.get("/reverse")
    assert response.status_code == 400
    data = response.json
    assert "error" in data
    assert data["error"] == "Missing 'in' query parameter"

def test_reverse_empty_input(client):
    response = client.get("/reverse?in=")
    assert response.status_code == 400
    data = response.json
    assert "error" in data
    assert data["error"] == "Input string cannot be empty"

def test_restore_after_reverse(client):
    input_str = "Test case for restore"
    expected_result = "restore for case Test"
    client.get(f"/reverse?in={input_str}")
    response = client.get("/restore")
    assert response.status_code == 200
    data = response.json
    assert data["result"] == expected_result
