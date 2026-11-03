import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import factory_store as store
from web.app import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = patch.object(store, "DB", Path(self.temp.name) / "factory.db")
        self.env = patch.dict(os.environ, {"FACTORY_ADMIN_TOKEN": "test-access", "FACTORY_AUTOSTART": "0"})
        self.db.start()
        self.env.start()
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)
        self.db.stop()
        self.env.stop()
        self.temp.cleanup()

    def test_authentication_protects_queue_and_static_outputs(self):
        self.assertEqual(self.client.get("/api/factory/state").status_code, 401)
        self.assertEqual(self.client.get("/outputs/factory/test/final.mp4").status_code, 401)
        self.assertEqual(self.client.post("/api/render", json={}).status_code, 401)
        self.assertEqual(self.client.post("/api/factory/session", headers={"Authorization": "Bearer wrong"}).status_code, 401)
        self.assertEqual(self.client.post("/api/factory/session", headers={"Authorization": "Bearer test-access"}).status_code, 200)
        self.assertEqual(self.client.get("/api/factory/state").status_code, 200)

    def test_dashboard_setup_and_external_batch(self):
        self.client.post("/api/factory/session", headers={"Authorization": "Bearer test-access"})
        channel = self.client.post("/api/factory/channels", json={"name": "Story channel"}).json()["id"]
        auto = self.client.post("/api/factory/automations", json={"name": "Canva stories", "channel_id": channel, "recipe": "canva_template", "daily_limit": 30}).json()["id"]
        with patch("engine.factory_runner.start"):
            result = self.client.post("/api/factory/jobs", json={"automation_id": auto, "items": [{"scenes": ["A question", "The answer"], "duration": 20, "rights_confirmed": True}]})
        self.assertEqual(result.status_code, 200)
        job = self.client.get("/api/factory/state").json()["jobs"][0]
        self.assertEqual(job["status"], "waiting_assets")
        self.assertEqual(self.client.post(f"/api/factory/jobs/{job['id']}/approve", json={}).status_code, 409)
        self.assertEqual(self.client.post("/api/factory/channels", headers={"Origin": "https://evil.test"}, json={"name": "bad"}).status_code, 403)

    def test_legacy_output_path_cannot_escape_outputs(self):
        self.client.post("/api/factory/session", headers={"Authorization": "Bearer test-access"})
        self.assertEqual(self.client.post("/api/render", json={"custom_output_name": "../runtime/admin.token"}).status_code, 422)
        self.assertEqual(self.client.post("/api/batch/start").status_code, 409)

if __name__ == "__main__":
    unittest.main()
