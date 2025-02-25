import pytest
import responses
from datetime import datetime, timezone
from stegawave.client import StegawaveClient
from stegawave.models import Event
from stegawave.exceptions import StegawaveError


BASE_URL = "https://api.stegawave.com/v1"

@pytest.fixture
def client():
    return StegawaveClient(api_key="test-key")

@responses.activate
def test_list_events(client, mock_events_response):
    # Setup mock response
    responses.add(
        responses.GET,
        f"{BASE_URL}/events",
        json=mock_events_response,
        status=200
    )

    # Test without active parameter
    events = client.list_events()
    assert len(events) == 2
    assert isinstance(events[0], Event)
    assert events[0].eventID == "test-123"
    assert events[1].eventID == "test-456"

    # Test with active=True
    responses.add(
        responses.GET,
        f"{BASE_URL}/events",
        json={"events": [mock_events_response["events"][0]]},
        status=200
    )
    active_events = client.list_events(active=True)
    assert len(active_events) == 1

@responses.activate
def test_create_event(client, mock_event_data):
    # Setup mock response
    responses.add(
        responses.POST,
        f"{BASE_URL}/create-event",
        json=mock_event_data,
        status=200
    )

    start_time = datetime.now(timezone.utc)
    end_time = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    event = client.create_event(
        name="Test Event",
        start_time=start_time,
        end_time=end_time,
        ip_whitelist=["127.0.0.1"]
    )

    assert isinstance(event, Event)
    assert event.eventID == "test-123"
    assert event.eventName == "Test Event"

@responses.activate
def test_api_error(client):
    # Setup mock error response
    error_message = "Invalid API key"
    responses.add(
        responses.GET,
        f"{BASE_URL}/events",
        json={"error": error_message},
        status=401,
        headers={"Content-Type": "application/json"}
    )

    with pytest.raises(StegawaveError) as exc_info:
        client.list_events()
    assert "401" in str(exc_info.value)  # Check for status code instead

@responses.activate
def test_decode_file(client, mock_event_data):
    # Mock responses for multipart upload process
    initiate_response = {
        "uploadId": "upload-123",
        "key": "file-key-123"
    }
    responses.add(
        responses.POST,
        f"{BASE_URL}/upload/initiate",
        json=initiate_response,
        status=200
    )

    # Mock presigned URL response
    presigned_url_response = {
        "presignedUrl": "https://example.com/upload"
    }
    responses.add(
        responses.POST,
        f"{BASE_URL}/upload/presigned-url",
        json=presigned_url_response,
        status=200
    )

    # Mock the actual upload
    responses.add(
        responses.PUT,
        "https://example.com/upload",
        status=200,
        headers={"ETag": "\"test-etag\""}
    )

    # Mock complete upload response
    complete_response = {
        "status": "success",
        "uploadId": "upload-123"
    }
    responses.add(
        responses.POST,
        f"{BASE_URL}/upload/complete",
        json=complete_response,
        status=200
    )

    # Create a temporary file for testing
    import tempfile
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(b"test content")
        tmp_file.flush()
        
        result = client.decode_file("test-123", tmp_file.name)
        assert result["status"] == "success"
        assert result["uploadId"] == "upload-123"

@responses.activate
def test_network_error(client):
    responses.add(
        responses.GET,
        f"{BASE_URL}/events",
        status=500,  # Use HTTP 500 instead of Exception
        json={"error": "Network error"}
    )

    with pytest.raises(StegawaveError) as exc_info:
        client.list_events()
    assert "500" in str(exc_info.value)