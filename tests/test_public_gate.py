import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_public_site import validate

SOURCE = Path(__file__).resolve().parents[1]


class PublicReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ("index.html", "news.html", "methodology.html",
                     "data/evidence.json", "assets/app.js"):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, dest)

    def test_current_status_only_site_passes(self):
        self.assertEqual(validate(self.root), [])

    def test_old_rate_ratio_blocks_pages(self):
        p = self.root / "index.html"
        p.write_text(p.read_text() + "<p>RR 1.26 / control mean 5.56</p>")
        self.assertTrue(validate(self.root))

    def test_empty_payload_fails_closed(self):
        (self.root / "data/evidence.json").write_text("{}")
        self.assertTrue(validate(self.root))

    def test_hidden_results_are_rejected(self):
        p = self.root / "data/evidence.json"
        data = json.loads(p.read_text())
        data["historical_results"] = [{"event_count": 7}]
        p.write_text(json.dumps(data))
        self.assertTrue(validate(self.root))

    def test_exploratory_signal_is_rejected(self):
        p = self.root / "data/evidence.json"
        data = json.loads(p.read_text())
        data["exploratory_signal"] = {"rate_ratio": 1.7}
        p.write_text(json.dumps(data))
        self.assertTrue(validate(self.root))


if __name__ == "__main__":
    unittest.main()
