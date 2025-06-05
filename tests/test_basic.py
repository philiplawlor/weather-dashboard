import os
import pytest
from app import create_app
from app.models import db, WeatherData

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        
        # Add test data
        test_data = WeatherData(
            location="Test City, Test",
            temperature=25.5,
            humidity=60,
            description="Sunny",
            icon="01d"
        )
        db.session.add(test_data)
        db.session.commit()
    
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Weather Dashboard' in response.data

def test_weather_api(client):
    """Test the weather API endpoint."""
    response = client.get('/api/weather/history')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['data']) > 0
    assert data['data'][0]['location'] == 'Test City, Test'
