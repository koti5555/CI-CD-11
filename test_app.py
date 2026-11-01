import unittest

from app import app


class TestPredictionApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import train_model
        train_model.train_model()

    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint_and_request_id(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertTrue(response.headers.get("X-Request-ID"))

    def test_high_performance_prediction(self):
        response = self.client.post("/predict", json={
            "attendance": 90, "internal_marks": 85,
            "assignment_marks": 88, "previous_score": 80,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "PASS")

    def test_low_performance_prediction(self):
        response = self.client.post("/predict", json={
            "attendance": 55, "internal_marks": 30,
            "assignment_marks": 40, "previous_score": 35,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "FAIL")

    def test_missing_field_validation(self):
        response = self.client.post("/predict", json={
            "attendance": 90, "internal_marks": 85,
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.get_json())

    def test_invalid_numeric_validation(self):
        response = self.client.post("/predict", json={
            "attendance": "bad", "internal_marks": 85,
            "assignment_marks": 88, "previous_score": 80,
        })
        self.assertEqual(response.status_code, 400)

    def test_missing_route(self):
        response = self.client.get("/not-a-real-route")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
