import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

import backend.database as db_mod
from backend.db_models import CheckIn, Reminder, Resolution
from backend.main import app


def _mock_categorize(title, description, existing):
    return {"category": "Health", "priority": 1}


def _mock_sentiment(note, resolution_title, resolution_description, past_check_ins):
    return {"sentiment": "positive", "sentiment_score": 0.9, "ai_feedback": "Great progress!"}


class TestCheckIns(unittest.TestCase):
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
            resp = self.client.post("/api/resolutions", json={"title": "Run", "description": "Run daily"})
        return resp.json()["id"]

    @patch("backend.routers.check_ins.analyze_sentiment_and_feedback", side_effect=_mock_sentiment)
    def test_create_check_in(self, mock_ai):
        rid = self._create_resolution()
        response = self.client.post(f"/api/resolutions/{rid}/check-ins", json={"note": "Ran 5km today"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["sentiment"], "positive")
        self.assertEqual(data["ai_feedback"], "Great progress!")
        self.assertAlmostEqual(data["sentiment_score"], 0.9)

    @patch("backend.routers.check_ins.analyze_sentiment_and_feedback", side_effect=_mock_sentiment)
    def test_list_check_ins(self, mock_ai):
        rid = self._create_resolution()
        self.client.post(f"/api/resolutions/{rid}/check-ins", json={"note": "Day 1"})
        self.client.post(f"/api/resolutions/{rid}/check-ins", json={"note": "Day 2"})
        response = self.client.get(f"/api/resolutions/{rid}/check-ins")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_check_in_resolution_not_found(self):
        response = self.client.post("/api/resolutions/999/check-ins", json={"note": "test"})
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
