"""
tests/test_activities_api.py
Uses AAA (Arrange, Act, Assert) Pattern with pytest
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Arrange: Setup test client"""
    return TestClient(app)

@pytest.fixture
def sample_activity():
    """Arrange: Sample test data"""
    return {
        "name": "Chess Club",
        "max_participants": 12,
        "current_participants": 2
    }

# GET /activities tests
class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        """Arrange (implicit via fixture), Act, Assert"""
        # Act
        response = client.get("/activities")
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 9
        assert "Chess Club" in response.json()

    def test_activity_has_required_fields(self, client):
        # Act
        response = client.get("/activities")
        # Assert
        activity = response.json()["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

# POST signup tests
class TestSignupForActivity:
    def test_signup_new_student(self, client):
        # Arrange
        email = "new-student@mergington.edu"
        activity_name = "Chess Club"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Fake Club"
        email = "student@mergington.edu"
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404

# DELETE participant tests
class TestRemoveParticipant:
    def test_remove_existing_participant(self, client):
        # Arrange: First add a participant
        email = "new-student@mergington.edu"
        activity_name = "Chess Club"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Act: Remove the participant
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_remove_nonexistent_participant_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        # Assert
        assert response.status_code == 404