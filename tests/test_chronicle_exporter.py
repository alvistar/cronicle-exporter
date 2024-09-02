import pytest
import requests
from unittest.mock import patch, Mock
from cronicle_exporter.api_client import ApiClient


@pytest.fixture
def api_client():
    return ApiClient("http://test-url", "test-api-key")


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


def test_get_schedule_success(api_client, mock_response):
    with patch("requests.get", return_value=mock_response):
        result = api_client.get_schedule()

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["title"] == "Test Event 1"
    assert result[1]["id"] == "2"
    assert result[1]["title"] == "Test Event 2"


def test_get_schedule_error(api_client):
    with patch(
        "requests.get", side_effect=requests.RequestException("Connection error")
    ):
        result = api_client.get_schedule()

    assert result == []


def test_get_schedule_unexpected_response(api_client):
    mock_resp = Mock()
    mock_resp.json.return_value = {"code": 1, "error": "Unexpected error"}

    with patch("requests.get", return_value=mock_resp):
        result = api_client.get_schedule()

    assert result == []


def test_get_last_event_success(api_client):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "code": 0,
        "rows": [{"id": "1", "title": "Last Event", "status": "success"}],
    }

    with patch("requests.get", return_value=mock_resp):
        result = api_client.get_last_event("1")

    assert result["id"] == "1"
    assert result["title"] == "Last Event"
    assert result["status"] == "success"


def test_get_last_event_error(api_client):
    with patch(
        "requests.get", side_effect=requests.RequestException("Connection error")
    ):
        result = api_client.get_last_event("1")

    assert result == {}


def test_get_last_event_no_events(api_client):
    mock_resp = Mock()
    mock_resp.json.return_value = {"code": 0, "rows": []}

    with patch("requests.get", return_value=mock_resp):
        result = api_client.get_last_event("1")

    assert result == {}
