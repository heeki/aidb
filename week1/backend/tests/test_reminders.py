import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

import backend.database as db_mod
from backend.db_models import CheckIn, Reminder, Resolution
from backend.main import app


def _mock_categorize(title, description, existing):
    return {"category": "Health", "priority": 1}


class TestReminders(unittest.TestCase):
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

    def _create_resolution(self):
        with patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize):
            resp = self.client.post("/api/resolutions", json={"title": "Test", "description": "d"})
        return resp.json()["id"]

    def test_update_reminder(self):
        rid = self._create_resolution()
        response = self.client.put(f"/api/resolutions/{rid}/reminder", json={
            "frequency": "daily", "is_active": True
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["frequency"], "daily")

    def test_update_reminder_invalid_frequency(self):
        rid = self._create_resolution()
        response = self.client.put(f"/api/resolutions/{rid}/reminder", json={
            "frequency": "hourly", "is_active": True
        })
        self.assertEqual(response.status_code, 400)

    def test_get_due_reminders(self):
        rid = self._create_resolution()
        session = db_mod.get_session_factory()()
        reminder = session.query(Reminder).filter(Reminder.resolution_id == rid).first()
        reminder.next_due = "2020-01-01"
        session.commit()
        session.close()

        response = self.client.get("/api/reminders/due")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["resolution_id"], rid)


if __name__ == "__main__":
    unittest.main()
