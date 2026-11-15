"""scripts/check_consistency.py 的单元测试（仅用标准库 unittest）。

运行方式：

    python -m unittest discover -s tests -v
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import check_consistency as cc  # noqa: E402


class TempRepoTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def write_json(self, rel, payload):
        return self.write(rel, json.dumps(payload, ensure_ascii=False))


class MarkdownLinkTests(TempRepoTestCase):
    def test_existing_link_passes(self):
        self.write("README.md", "[报告](reports/a.md)\n")
        self.write("reports/a.md", "# A\n")
        self.assertEqual(cc.check_markdown_links(self.root), [])

    def test_missing_link_reports_line(self):
        self.write("README.md", "# 标题\n\n[报告](reports/missing.md)\n")
        errors = cc.check_markdown_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("README.md:3", errors[0])
        self.assertIn("链接目标不存在", errors[0])

    def test_external_anchor_and_code_fence_ignored(self):
        self.write(
            "README.md",
            "[外链](https://example.com)\n"
            "[锚点](#section)\n"
            "![图](https://example.com/a.png)\n"
            "```\n[示例](not-exist.md)\n```\n",
        )
        self.assertEqual(cc.check_markdown_links(self.root), [])

    def test_guides_are_scanned(self):
        self.write("guides/a.md", "[坏链接](../missing.md)\n")
        errors = cc.check_markdown_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("guides/a.md:1", errors[0])


class HtmlLinkTests(TempRepoTestCase):
    def test_local_asset_missing(self):
        self.write("docs/index.html", '<link rel="stylesheet" href="css/none.css">\n')
        errors = cc.check_html_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("本地资源不存在", errors[0])

    def test_link_outside_docs_root_is_rejected(self):
        self.write("README.md", "# 根目录文件\n")
        self.write("docs/index.html", '<a href="../README.md">文档</a>\n')
        errors = cc.check_html_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("发布根目录之外", errors[0])

    def test_local_asset_present_and_external_ignored(self):
        self.write("docs/css/style.css", "body {}\n")
        self.write(
            "docs/index.html",
            '<link rel="stylesheet" href="css/style.css">\n'
            '<script src="https://cdn.example.com/a.js"></script>\n'
            '<a href="#top">顶部</a>\n',
        )
        self.assertEqual(cc.check_html_links(self.root), [])


class ReportIndexTests(TempRepoTestCase):
    def test_missing_raw_and_html_paths(self):
        self.write_json(
            "docs/reports/daily_reports.json",
            {"reports": [{"id": "d1", "rawPath": "reports/missing.md", "htmlPath": "reports/missing.html"}]},
        )
        errors = cc.check_report_index(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("rawPath" in item for item in errors))
        self.assertTrue(any("htmlPath" in item for item in errors))

    def test_duplicate_id(self):
        self.write("reports/a.md", "x")
        self.write("docs/reports/a.html", "x")
        entry = {"id": "d1", "rawPath": "reports/a.md", "htmlPath": "reports/a.html"}
        self.write_json("docs/reports/daily_reports.json", {"reports": [entry, dict(entry)]})
        errors = cc.check_report_index(self.root)
        self.assertTrue(any("重复的报告 id" in item for item in errors))


class ValuationIndexTests(TempRepoTestCase):
    def test_absent_index_is_allowed(self):
        self.assertEqual(cc.check_valuation_index(self.root), [])

    def test_missing_archive_page_is_reported(self):
        self.write_json(
            "docs/valuation_reports.json",
            {"reports": [{"id": "v1", "date": "2026-11-17", "htmlPath": "valuation/valuation_20261117.html"}]},
        )
        errors = cc.check_valuation_index(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("htmlPath", errors[0])

    def test_existing_archive_page_passes(self):
        self.write("docs/valuation/valuation_20261117.html", "<html></html>")
        self.write_json(
            "docs/valuation_reports.json",
            {"reports": [{"id": "v1", "date": "2026-11-17", "htmlPath": "valuation/valuation_20261117.html"}]},
        )
        self.assertEqual(cc.check_valuation_index(self.root), [])


class ReportsJsTests(TempRepoTestCase):
    def test_missing_raw_path(self):
        self.write("docs/js/reports.js", "const reports = [{ rawPath: 'reports/gone.md' }];\n")
        errors = cc.check_reports_js(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("reports/gone.md", errors[0])

    def test_existing_raw_path(self):
        self.write("reports/a.md", "x")
        self.write("docs/js/reports.js", "const reports = [{ rawPath: 'reports/a.md' }];\n")
        self.assertEqual(cc.check_reports_js(self.root), [])


class TickerCoverageTests(TempRepoTestCase):
    def _prepare(self, ticker, homepage):
        self.write_json(
            "scripts/daily_analysis_config.json",
            {"companies": [{"id": "c", "name": "示例公司", "ticker": ticker}]},
        )
        self.write("docs/index.html", homepage)

    def test_ss_and_sh_are_equivalent(self):
        self._prepare("600703.SS", "<div>600703.SH</div>")
        self.assertEqual(cc.check_ticker_coverage(self.root), [])

    def test_missing_ticker_is_reported(self):
        self._prepare("000001.SZ", "<div>600703.SH</div>")
        errors = cc.check_ticker_coverage(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("000001.SZ", errors[0])

    def test_hk_zero_padding_tolerated(self):
        self._prepare("09660.HK", "<div>9660.HK</div>")
        self.assertEqual(cc.check_ticker_coverage(self.root), [])


class ScheduleSyncTests(TempRepoTestCase):
    def _prepare(self, local_cron, workflow_cron, tz="Asia/Shanghai"):
        self.write_json(
            "scripts/daily_analysis_config.json",
            {"schedule": {"cron_expression": local_cron, "timezone": tz}},
        )
        self.write(
            ".github/workflows/daily-analysis.yml",
            f"on:\n  schedule:\n    - cron: \"{workflow_cron}\"\n",
        )

    def test_matching_utc_cron_passes(self):
        self._prepare("0 9 * * *", "0 1 * * *")
        self.assertEqual(cc.check_schedule_sync(self.root), [])

    def test_drift_is_reported(self):
        self._prepare("0 9 * * *", "0 9 * * *")
        errors = cc.check_schedule_sync(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("调度不同步", errors[0])

    def test_missing_workflow_is_reported(self):
        self.write_json(
            "scripts/daily_analysis_config.json",
            {"schedule": {"cron_expression": "0 9 * * *", "timezone": "Asia/Shanghai"}},
        )
        errors = cc.check_schedule_sync(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("文件不存在", errors[0])


class FreshnessTests(TempRepoTestCase):
    def _write_report(self, generated_at):
        self.write_json(
            "data/daily_analysis/daily_analysis_20260101.json",
            {"generated_at": generated_at},
        )

    def test_stale_report_warns(self):
        old = datetime.now(timezone.utc) - timedelta(days=30)
        self._write_report(old.isoformat())
        warnings = cc.check_freshness(self.root, max_age_days=7)
        self.assertEqual(len(warnings), 1)
        self.assertIn("距今 30 天", warnings[0])

    def test_fresh_report_passes(self):
        now = datetime.now(timezone.utc) - timedelta(hours=1)
        self._write_report(now.isoformat())
        self.assertEqual(cc.check_freshness(self.root, max_age_days=7), [])

    def test_legacy_list_payload_is_ignored(self):
        self.write("data/daily_analysis/daily_analysis_20260312.json", "[]\n")
        warnings = cc.check_freshness(self.root)
        self.assertEqual(len(warnings), 1)
        self.assertIn("无法从日报 JSON 中读取", warnings[0])


class EndToEndTests(TempRepoTestCase):
    def _build_minimal_repo(self):
        self.write("README.md", "[更新日志](UPDATE_LOG.md)\n")
        self.write("UPDATE_LOG.md", "# 日志\n")
        self.write(
            "docs/index.html",
            '<link rel="stylesheet" href="css/style.css">\n'
            "<div>1810.HK</div>\n"
            '<a href="reports_index.html">报告中心</a>\n',
        )
        self.write("docs/css/style.css", "body {}\n")
        self.write("docs/reports_index.html", "<html></html>\n")
        self.write("reports/a.md", "# A\n")
        self.write("docs/reports/a.html", "<html></html>\n")
        self.write_json(
            "docs/reports/daily_reports.json",
            {"reports": [{"id": "a", "rawPath": "reports/a.md", "htmlPath": "reports/a.html"}]},
        )
        self.write("docs/js/reports.js", "const reports = [{ rawPath: 'reports/a.md' }];\n")
        self.write_json(
            "scripts/daily_analysis_config.json",
            {
                "companies": [{"id": "xiaomi", "name": "小米集团", "ticker": "1810.HK"}],
                "schedule": {"cron_expression": "0 9 * * *", "timezone": "Asia/Shanghai"},
            },
        )
        self.write(
            ".github/workflows/daily-analysis.yml",
            'on:\n  schedule:\n    - cron: "0 1 * * *"\n',
        )
        self.write_json(
            "data/daily_analysis/daily_analysis_20260101.json",
            {"generated_at": datetime.now(timezone.utc).isoformat()},
        )

    def test_clean_repo_has_no_errors(self):
        self._build_minimal_repo()
        errors, warnings = cc.run_all(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_broken_link_makes_repo_fail(self):
        self._build_minimal_repo()
        self.write("docs/reports_index.html", '<a href="missing.html">缺失</a>\n')
        errors, _ = cc.run_all(self.root)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
