import concurrent.futures
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import factory_store as store, factory_runner as runner

class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.patch = patch.object(store, "DB", Path(self.temp.name) / "factory.db")
        self.patch.start()
        store.init()
        self.channel = store.channel({"name": "Hindi stories"})
        self.auto = store.automation({"name": "Stories", "channel_id": self.channel, "recipe": "storytelling", "daily_limit": 2})

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def item(self, text="First scene"):
        return {"scenes": [text, "A useful ending"], "duration": 20, "rights_confirmed": True}

    def test_duplicate_copy_is_blocked_across_recipes(self):
        other = store.automation({"name": "Tips", "channel_id": self.channel, "recipe": "listicle"})
        self.assertEqual(len(store.submit(self.auto, [self.item()])["added"]), 1)
        self.assertEqual(store.submit(other, [self.item()])["duplicates"], 1)

    def test_concurrent_submissions_do_not_lose_jobs(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda i: store.submit(self.auto, [self.item(f"Scene {i}")]), range(40)))
        self.assertEqual(sum(len(r["added"]) for r in results), 40)
        self.assertEqual(len(store.list_rows("jobs")), 40)

    def test_daily_quota_and_claim_are_transactional(self):
        store.submit(self.auto, [self.item(f"Story {i}") for i in range(5)])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            claimed = [j for j in pool.map(lambda _: store.claim(), range(4)) if j]
        self.assertEqual(len(claimed), 2)
        self.assertEqual(len({j["id"] for j in claimed}), 2)

    def test_batch_is_atomic_on_invalid_script(self):
        with self.assertRaises(ValueError):
            store.submit(self.auto, [self.item(), {"scenes": ["only one"], "rights_confirmed": True}])
        self.assertEqual(store.list_rows("jobs"), [])

    def test_native_and_external_have_distinct_states(self):
        external = store.automation({"name": "Canva", "channel_id": self.channel, "recipe": "canva_template"})
        native = store.submit(self.auto, [self.item()])["added"][0]
        imported = store.submit(external, [self.item("Different script")])["added"][0]
        self.assertEqual(store.get_job(native)["status"], "pending")
        self.assertEqual(store.get_job(imported)["status"], "waiting_assets")

    def test_voice_or_output_failure_is_not_success(self):
        store.submit(self.auto, [self.item()])
        with patch.object(runner, "render", side_effect=RuntimeError("render failed")):
            runner.run_once()
        self.assertEqual(store.list_rows("jobs")[0]["status"], "failed")

    def test_approval_requires_qa_and_unchanged_file(self):
        job_id = store.submit(self.auto, [self.item()])["added"][0]
        with self.assertRaises(ValueError):
            runner.approve(job_id)
        with tempfile.NamedTemporaryFile(dir=store.BASE, delete=False) as file:
            file.write(b"reviewed video")
            path = Path(file.name)
        try:
            store.update(job_id, status="awaiting_approval", output=path.name, qa={"passed": True, "sha256": runner.digest(path)})
            path.write_bytes(b"changed video")
            with self.assertRaises(ValueError):
                runner.approve(job_id)
            store.update(job_id, qa={"passed": True, "sha256": runner.digest(path)})
            runner.approve(job_id)
            self.assertEqual(store.get_job(job_id)["status"], "approved")
        finally:
            path.unlink()

    def test_publish_timeout_never_retries_blindly(self):
        job_id = store.submit(self.auto, [self.item()])["added"][0]
        with tempfile.NamedTemporaryFile(dir=store.BASE, delete=False) as file:
            file.write(b"video")
            path = Path(file.name)
        try:
            store.update(job_id, status="approved", output=path.name, approved_hash=runner.digest(path), drive_id="drive-id")
            job = store.get_job(job_id)
            job["payload"]["destination"] = "channel-account"
            with patch.dict(os.environ, {"FACTORY_PUBLISH_WEBHOOK": "https://example.test/publish", "FACTORY_PUBLISH_SECRET": "test"}), patch("requests.post", side_effect=TimeoutError):
                runner.deliver(job)
            self.assertEqual(store.get_job(job_id)["status"], "publish_unknown")
            with self.assertRaises(ValueError):
                runner.deliver(job)
        finally:
            path.unlink()

    def test_photo_assets_cannot_escape_public_folder(self):
        photo = store.automation({"name": "Photos", "channel_id": self.channel, "recipe": "photo_story"})
        data = self.item()
        data["assets"] = ["../../secret.png", "image.jpg"]
        with self.assertRaises(ValueError):
            store.submit(photo, [data])

    def test_quiz_long_format_is_rejected(self):
        with self.assertRaises(ValueError):
            store.automation({"name": "Wrong", "channel_id": self.channel, "recipe": "quiz", "format": "long"})

    def test_pause_persists_and_does_not_claim_jobs(self):
        store.submit(self.auto, [self.item()])
        store.enabled(False)
        self.assertIsNone(store.claim())
        self.assertFalse(store.enabled())
        store.enabled(True)
        self.assertIsNotNone(store.claim())

    def test_edit_changes_future_jobs_without_retargeting_old_jobs(self):
        old_id = store.submit(self.auto, [self.item()])["added"][0]
        old_payload = store.get_job(old_id)["payload"]
        store.channel({"name": "New name", "destination": "new-account"}, self.channel)
        new_id = store.submit(self.auto, [self.item("A different story")])["added"][0]
        self.assertEqual(store.get_job(new_id)["payload"]["destination"], "new-account")
        self.assertEqual(store.get_job(old_id)["payload"], old_payload)

if __name__ == "__main__":
    unittest.main()
