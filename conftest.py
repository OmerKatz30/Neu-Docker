import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client
