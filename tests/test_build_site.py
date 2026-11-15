"""scripts/build_site.py 的单元测试（仅用标准库 unittest）。"""

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import build_site  # noqa: E402


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write(self, rel, text="# 内容\n"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _minimal_site(self):
        self._write("docs/index.html", "<html></html>\n")
        self._write("docs/css/style.css", "body {}\n")
        self._write("reports/company_analysis/a.md")
        self._write("reports/daily_analysis/b.md")
        self._write("guides/c.md")

    def test_copies_site_and_markdown(self):
        self._minimal_site()
        out = self.root / "dist"

        stats = build_site.build(self.root, out)

        self.assertTrue((out / "index.html").is_file())
        self.assertTrue((out / "css/style.css").is_file())
        self.assertTrue((out / "reports/company_analysis/a.md").is_file())
        self.assertTrue((out / "reports/daily_analysis/b.md").is_file())
        self.assertTrue((out / "guides/c.md").is_file())
        self.assertEqual(stats["reports"], 2)
        self.assertEqual(stats["guides"], 1)
        self.assertGreaterEqual(stats["docs"], 2)

    def test_writes_cloudflare_headers(self):
        self._minimal_site()
        out = self.root / "dist"

        build_site.build(self.root, out)

        headers = (out / "_headers").read_text(encoding="utf-8")
        self.assertIn("X-Content-Type-Options", headers)
        self.assertIn("Cache-Control", headers)

    def test_removes_stale_output(self):
        self._minimal_site()
        out = self.root / "dist"
        out.mkdir()
        stale = out / "old-report.html"
        stale.write_text("stale", encoding="utf-8")

        build_site.build(self.root, out)

        self.assertFalse(stale.exists())
        self.assertTrue((out / "index.html").is_file())

    def test_missing_site_entry_fails(self):
        self._write("reports/a.md")
        with self.assertRaises(SystemExit):
            build_site.build(self.root, self.root / "dist")

    def test_refuses_output_inside_docs(self):
        self._minimal_site()
        with self.assertRaises(SystemExit):
            build_site.build(self.root, self.root / "docs" / "dist")

    def test_refuses_repository_root_as_output(self):
        self._minimal_site()
        with self.assertRaises(SystemExit):
            build_site.build(self.root, self.root)


if __name__ == "__main__":
    unittest.main()
