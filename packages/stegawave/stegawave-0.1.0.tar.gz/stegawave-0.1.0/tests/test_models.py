import pytest
from datetime import datetime
from stegawave.models import Event, DecodingResult

def test_event_model():
    event_data = {
        "eventID": "test-123",
        "eventName": "Test Event",
        "active": True,
        "startTime": "2024-02-20T00:00:00Z",
        "endTime": "2024-02-21T00:00:00Z",
        "ipWhitelist": ["127.0.0.1"],
        "testOutput": None,
        "sessionInitPrefix": None,
        "hlsPlaybackPrefix": None,
        "running": True
    }
    event = Event.model_validate(event_data)
    assert event.eventID == "test-123"
    assert event.eventName == "Test Event"
    assert event.active is True

def test_decoding_result_model():
    result_data = {
        "eventID": "test-123",
        "results": ["result1", "result2"]
    }
    result = DecodingResult.model_validate(result_data)
    assert result.eventID == "test-123"
    assert len(result.results) == 2



def test_event_model_missing_optional():
    """Test that Event model handles missing optional fields."""
    minimal_event_data = {
        "eventID": "test-123",
        "eventName": "Test Event",
        "active": True,
        "startTime": "2024-02-20T00:00:00Z",
        "endTime": "2024-02-21T00:00:00Z",
        "ipWhitelist": [],
        "running": True
    }
    event = Event.model_validate(minimal_event_data)
    assert event.testOutput is None
    assert event.sessionInitPrefix is None
    assert event.hlsPlaybackPrefix is None

def test_event_model_invalid_date():
    """Test that Event model validates dates properly."""
    invalid_event_data = {
        "eventID": "test-123",
        "eventName": "Test Event",
        "active": True,
        "startTime": "invalid-date",
        "endTime": "2024-02-21T00:00:00Z",
        "ipWhitelist": [],
        "running": True
    }
    with pytest.raises(ValueError):
        Event.model_validate(invalid_event_data)