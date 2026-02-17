import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

import backend.database as db_mod
from backend.db_models import CheckIn, Reminder, Resolution
from backend.main import app


def _mock_categorize(title, description, existing):
    return {"category": "Learning", "priority": 2}


class TestResolutions(unittest.TestCase):
    def setUp(self):
        db_mod.init_db()
        self.client = TestClient(app)

    def tearDown(self):
        session = db_mod.get_session_factory()()
        session.query(CheckIn).delete()
        session.query(Reminder).delete()
        session.query(Resolution).delete()
        session.commit()
        session.close()

    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_create_resolution(self, mock_ai):
        response = self.client.post("/api/resolutions", json={
            "title": "Test Resolution",
            "description": "A test goal",
            "target_date": "2026-12-31",
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Test Resolution")
        self.assertEqual(data["category"], "Learning")
        self.assertEqual(data["priority"], 2)
        self.assertEqual(data["status"], "active")

    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_list_resolutions(self, mock_ai):
        self.client.post("/api/resolutions", json={"title": "Res 1", "description": "d1"})
        self.client.post("/api/resolutions", json={"title": "Res 2", "description": "d2"})
        response = self.client.get("/api/resolutions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_get_resolution_detail(self, mock_ai):
        create = self.client.post("/api/resolutions", json={"title": "Detail", "description": "d"})
        rid = create.json()["id"]
        response = self.client.get(f"/api/resolutions/{rid}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Detail")
        self.assertIn("check_ins", data)
        self.assertIn("reminder", data)

    def test_get_resolution_not_found(self):
        response = self.client.get("/api/resolutions/999")
        self.assertEqual(response.status_code, 404)

    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_update_resolution(self, mock_ai):
        create = self.client.post("/api/resolutions", json={"title": "Old", "description": "d"})
        rid = create.json()["id"]
        response = self.client.put(f"/api/resolutions/{rid}", json={"title": "New Title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "New Title")

    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_delete_resolution(self, mock_ai):
        create = self.client.post("/api/resolutions", json={"title": "Del", "description": "d"})
        rid = create.json()["id"]
        response = self.client.delete(f"/api/resolutions/{rid}")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"/api/resolutions/{rid}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
