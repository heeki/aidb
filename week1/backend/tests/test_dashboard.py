import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

import backend.database as db_mod
from backend.db_models import CheckIn, Reminder, Resolution
from backend.main import app


def _mock_categorize(title, description, existing):
    return {"category": "Health", "priority": 1}


def _mock_sentiment(note, resolution_title, resolution_description, past_check_ins):
    return {"sentiment": "positive", "sentiment_score": 0.8, "ai_feedback": "Nice!"}


class TestDashboard(unittest.TestCase):
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

    def test_empty_dashboard(self):
        response = self.client.get("/api/dashboard/summary")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_resolutions"], 0)
        self.assertEqual(data["active_resolutions"], 0)
        self.assertIsNone(data["average_sentiment_score"])

    @patch("backend.routers.check_ins.analyze_sentiment_and_feedback", side_effect=_mock_sentiment)
    @patch("backend.routers.resolutions.categorize_and_prioritize", side_effect=_mock_categorize)
    def test_dashboard_with_data(self, mock_cat, mock_sent):
        self.client.post("/api/resolutions", json={"title": "R1", "description": "d1"})
        resp = self.client.post("/api/resolutions", json={"title": "R2", "description": "d2"})
        rid = resp.json()["id"]
        self.client.post(f"/api/resolutions/{rid}/check-ins", json={"note": "Progress"})

        response = self.client.get("/api/dashboard/summary")
        data = response.json()
        self.assertEqual(data["total_resolutions"], 2)
        self.assertEqual(data["active_resolutions"], 2)
        self.assertEqual(data["total_check_ins"], 1)
        self.assertAlmostEqual(data["average_sentiment_score"], 0.8)
        self.assertEqual(data["sentiment_breakdown"]["positive"], 1)


if __name__ == "__main__":
    unittest.main()
