from django.test import TestCase, Client


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_liveness(self):
        response = self.client.get("/healthz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "recommendation-service")
