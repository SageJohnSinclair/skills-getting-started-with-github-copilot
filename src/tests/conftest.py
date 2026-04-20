"""
Shared test fixtures for the FastAPI application.

Provides test client and fresh activity data isolation for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient instance for making HTTP requests to the app.
    
    Returns:
        TestClient: A test client for the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the in-memory activities database to a fresh state before each test.
    
    This fixture ensures test isolation by resetting shared mutable state
    (the in-memory activities dictionary) before each test runs.
    
    Yields:
        None
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice team strategy and compete in friendly matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "maria@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Develop basketball skills and play pickup games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["tyler@mergington.edu", "nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and creative design",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["lily@mergington.edu", "mason@mergington.edu"]
        },
        "Drama Workshop": {
            "description": "Practice acting, improv, and stage performance",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["emma@mergington.edu", "olivia@mergington.edu"]
        },
        "Science Club": {
            "description": "Run experiments and explore STEM topics",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["sam@mergington.edu", "maya@mergington.edu"]
        },
        "Math Olympiad Training": {
            "description": "Train for math competitions and problem solving",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["lucas@mergington.edu", "zara@mergington.edu"]
        }
    }
    
    # Clear and restore activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (restore to original state)
    activities.clear()
    activities.update(original_activities)
