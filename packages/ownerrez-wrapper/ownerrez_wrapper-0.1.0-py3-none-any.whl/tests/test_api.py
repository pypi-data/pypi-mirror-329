"""
Tests for the OwnerRez API wrapper
"""
import pytest
from datetime import datetime
from freezegun import freeze_time
from ownerrez_wrapper.api import API
from ownerrez_wrapper.model import Result, Property, Booking, Guest

@pytest.fixture
def api():
    """Create an API instance for testing"""
    return API(username="test_user", token="test_token")

@pytest.fixture
def mock_property_response():
    return {
        "items": [{
            "id": 1,
            "name": "Test Property",
            "bedrooms": 3,
            "bathrooms": 2,
            "active": True
        }]
    }

@pytest.fixture
def mock_booking_response():
    return {
        "items": [{
            "id": 1,
            "property_id": 1,
            "arrival": "2024-03-01",
            "departure": "2024-03-05",
            "status": "confirmed",
            "guest_id": 1
        }]
    }

@pytest.fixture
def mock_guest_response():
    return {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email_addresses": [{"address": "john@example.com", "is_default": True}]
    }

def test_api_initialization(api):
    """Test API initialization"""
    assert api.username == "test_user"
    assert api.token == "test_token"

def test_getproperties(api, mock_property_response, monkeypatch):
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=mock_property_response)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    
    properties = api.getproperties()
    assert len(properties) == 1
    assert isinstance(properties[0], Property)
    assert properties[0].id == 1
    assert properties[0].name == "Test Property"

def test_getbookings(api, mock_booking_response, monkeypatch):
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=mock_booking_response)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    
    bookings = api.getbookings(property_id=1, since_utc=datetime(2024, 1, 1))
    assert len(bookings) == 1
    assert isinstance(bookings[0], Booking)
    assert bookings[0].id == 1
    assert bookings[0].property_id == 1

def test_getbooking(api, monkeypatch):
    booking_data = {
        "id": 1,
        "property_id": 1,
        "arrival": "2024-03-01",
        "departure": "2024-03-05"
    }
    
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=booking_data)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    
    booking = api.getbooking(booking_id=1)
    assert isinstance(booking, Booking)
    assert booking.id == 1
    assert booking.property_id == 1

def test_getguest(api, mock_guest_response, monkeypatch):
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=mock_guest_response)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    
    guest = api.getguest(guest_id=1)
    assert isinstance(guest, Guest)
    assert guest.id == 1
    assert guest.first_name == "John"
    assert guest.last_name == "Doe"

@freeze_time("2024-03-03")  # A date between arrival and departure
def test_isunitbooked(api, mock_booking_response, monkeypatch):
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=mock_booking_response)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    is_booked = api.isunitbooked(property_id=1)
    assert is_booked is True

@freeze_time("2024-03-06")  # A date after departure
def test_isunitbooked_not_booked(api, mock_booking_response, monkeypatch):
    def mock_get(*args, **kwargs):
        return Result(status=200, message="OK", data=mock_booking_response)
    
    monkeypatch.setattr("ownerrez_wrapper.restAdapter.RestAdapter.get", mock_get)
    is_booked = api.isunitbooked(property_id=1)
    assert is_booked is False
