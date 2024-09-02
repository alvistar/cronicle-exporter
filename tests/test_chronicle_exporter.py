import pytest
import requests
from unittest.mock import patch, Mock
from src.cronicle_exporter import get_schedule


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {
        "code": 0,
        "rows": [
            {"id": "1", "title": "Test Event 1"},
            {"id": "2", "title": "Test Event 2"},
        ],
    }
    return mock


def test_get_schedule_success(mock_response):
    with patch("requests.get", return_value=mock_response):
        result = get_schedule("http://test-url", "test-api-key")

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["title"] == "Test Event 1"
    assert result[1]["id"] == "2"
    assert result[1]["title"] == "Test Event 2"


def test_get_schedule_error():
    with patch(
        "requests.get", side_effect=requests.RequestException("Connection error")
    ):
        result = get_schedule("http://test-url", "test-api-key")

    assert result == []


def test_get_schedule_unexpected_response():
    mock_resp = Mock()
    mock_resp.json.return_value = {"code": 1, "error": "Unexpected error"}

    with patch("requests.get", return_value=mock_resp):
        result = get_schedule("http://test-url", "test-api-key")

    assert result == []
