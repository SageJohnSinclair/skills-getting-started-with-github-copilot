"""
API endpoint tests for the Mergington High School extracurricular activities system.

Tests follow the AAA (Arrange-Act-Assert) pattern for clarity:
- Arrange: Set up test data and preconditions
- Act: Perform the HTTP request
- Assert: Verify the response status code, headers, and payload
"""

from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests for the root endpoint (GET /)."""
    
    def test_root_redirects_to_static_index(self, client: TestClient):
        """
        Test that the root endpoint redirects to the static index.html page.
        
        AAA Pattern:
        - Arrange: TestClient ready
        - Act: Send GET request to root
        - Assert: Verify 307 redirect status and Location header
        """
        # Arrange
        # (client fixture already provides a ready TestClient)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["Location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for the get activities endpoint (GET /activities)."""
    
    def test_get_all_activities_returns_complete_list(self, client: TestClient):
        """
        Test that GET /activities returns all available activities with correct structure.
        
        AAA Pattern:
        - Arrange: Fresh activities data loaded by fixture
        - Act: Send GET request to /activities
        - Assert: Verify 200 status and response contains expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class", 
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Studio",
            "Drama Workshop",
            "Science Club",
            "Math Olympiad Training"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in data
            activity = data[activity_name]
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)


class TestSignupEndpoint:
    """Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""
    
    def test_signup_success_adds_participant(self, client: TestClient):
        """
        Test that a student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Activity exists with available space, new email provided
        - Act: Send POST request with activity name and email
        - Assert: Verify 200 status, success message, and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newemail@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Get updated activity data
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_already_registered_returns_409(self, client: TestClient):
        """
        Test that attempting to sign up an already-registered student returns 409 Conflict.
        
        AAA Pattern:
        - Arrange: Retrieve an existing participant email
        - Act: Send POST request with already-registered email
        - Assert: Verify 409 status with conflict error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in fixture
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 409
        assert response.json()["detail"] == "Student already signed up for this activity"
    
    def test_signup_activity_full_returns_400(self, client: TestClient):
        """
        Test that attempting to sign up when activity is full returns 400 Bad Request.
        
        AAA Pattern:
        - Arrange: Find or create a full activity (max_participants reached)
        - Act: Send POST request with new email to full activity
        - Assert: Verify 400 status with capacity error message
        """
        # Arrange
        activity_name = "Art Studio"  # max_participants: 14
        # Art Studio has only 2 participants: lily@mergington.edu, mason@mergington.edu
        # We'll fill it up to capacity
        for i in range(12):  # Add 12 more to reach 14 (2 existing + 12 new = 14)
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": f"student{i}@mergington.edu"}
            )
        
        # Act - try to add one more when full
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "onemore@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    
    def test_signup_activity_not_found_returns_404(self, client: TestClient):
        """
        Test that attempting to sign up for a non-existent activity returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Prepare a non-existent activity name
        - Act: Send POST request with invalid activity name
        - Assert: Verify 404 status with not found error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterEndpoint:
    """Tests for the unregister endpoint (DELETE /activities/{activity_name}/signup)."""
    
    def test_unregister_success_removes_participant(self, client: TestClient):
        """
        Test that a student can successfully unregister from an activity.
        
        AAA Pattern:
        - Arrange: Retrieve an existing participant
        - Act: Send DELETE request with activity name and participant email
        - Assert: Verify 200 status, success message, and participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Get updated activity data
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_student_not_registered_returns_404(self, client: TestClient):
        """
        Test that attempting to unregister a non-registered student returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Prepare an email not registered for the activity
        - Act: Send DELETE request with non-registered email
        - Assert: Verify 404 status with not found error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student not signed up for this activity"
    
    def test_unregister_activity_not_found_returns_404(self, client: TestClient):
        """
        Test that attempting to unregister from a non-existent activity returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Prepare a non-existent activity name
        - Act: Send DELETE request with invalid activity name
        - Assert: Verify 404 status with activity not found error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
