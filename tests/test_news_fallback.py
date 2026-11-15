"""新闻兜底源（Google News RSS）的单元测试。

只测试解析、时间窗过滤与回退选择逻辑，不访问网络。
"""

import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import daily_company_analysis as analysis  # noqa: E402

TZ = ZoneInfo("Asia/Shanghai")

SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>小米集团回购股份</title>
      <link>https://example.com/a</link>
      <pubDate>Fri, 13 Nov 2026 12:50:03 GMT</pubDate>
      <source url="https://example.com">21财经</source>
    </item>
    <item>
      <title>很久以前的新闻</title>
      <link>https://example.com/old</link>
      <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
      <source>旧来源</source>
    </item>
    <item>
      <title></title>
      <link>https://example.com/empty</link>
      <pubDate>Fri, 13 Nov 2026 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def build_config():
    return {
        "schedule": {"timezone": "Asia/Shanghai"},
        "news": {
            "provider": "yfinance",
            "fallback_providers": ["google-news-rss"],
            "industry_queries": ["港股"],
            "rss": {"timeout": 5},
        },
    }


class FakeRssProvider(analysis.GoogleNewsRssProvider):
    def __init__(self, config, payload=SAMPLE_RSS):
        super().__init__(config, "Asia/Shanghai")
        self.payload = payload
        self.queries = []

    def _fetch_xml(self, query):
        self.queries.append(query)
        return self.payload.encode("utf-8")


class DummyProvider(analysis.NewsProvider):
    def __init__(self, name, items=None, error=None):
        self.name = name
        self.items = items or []
        self.error = error

    def _result(self):
        return {
            "provider": self.name,
            "source": self.name,
            "items": list(self.items),
            "error": self.error,
        }

    def fetch_company_news(self, company, start, end, limit):
        return self._result()

    def fetch_industry_news(self, tickers, start, end, limit):
        return self._result()


class RssParsingTests(unittest.TestCase):
    def test_parse_items_skips_empty_titles(self):
        items = analysis.parse_rss_items(SAMPLE_RSS, "Asia/Shanghai")
        self.assertEqual([item["title"] for item in items], ["小米集团回购股份", "很久以前的新闻"])
        self.assertEqual(items[0]["publisher"], "21财经")

    def test_parse_datetime_converts_to_local_timezone(self):
        parsed = analysis.parse_rss_datetime("Fri, 13 Nov 2026 12:50:03 GMT", "Asia/Shanghai")
        self.assertEqual(parsed.hour, 20)
        self.assertEqual(parsed.day, 13)

    def test_invalid_datetime_returns_none(self):
        self.assertIsNone(analysis.parse_rss_datetime("not a date", "Asia/Shanghai"))
        self.assertIsNone(analysis.parse_rss_datetime("", "Asia/Shanghai"))


class RssProviderTests(unittest.TestCase):
    def setUp(self):
        self.config = build_config()
        self.provider = FakeRssProvider(self.config)
        self.end = datetime(2026, 11, 15, 23, 0, tzinfo=TZ)
        self.start = datetime(2026, 11, 13, 0, 0, tzinfo=TZ)

    def test_company_news_filters_window(self):
        result = self.provider.fetch_company_news(
            {"name": "小米集团", "ticker": "1810.HK"}, self.start, self.end, 5
        )
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["title"], "小米集团回购股份")
        self.assertIn("小米集团", self.provider.queries[0])
        self.assertIsNone(result["error"])

    def test_company_query_can_be_overridden(self):
        self.provider.fetch_company_news(
            {"name": "小米集团", "ticker": "1810.HK", "news_query": "小米 财报"},
            self.start,
            self.end,
            5,
        )
        self.assertEqual(self.provider.queries[0], "小米 财报")

    def test_industry_news_uses_configured_queries_and_dedupes(self):
        result = self.provider.fetch_industry_news([], self.start, self.end, 5)
        self.assertEqual(self.provider.queries, ["港股"])
        self.assertEqual(len(result["items"]), 1)

    def test_fetch_error_is_reported(self):
        class BrokenProvider(FakeRssProvider):
            def _fetch_xml(self, query):
                raise OSError("network down")

        provider = BrokenProvider(self.config)
        result = provider.fetch_company_news({"name": "美团", "ticker": "3690.HK"}, self.start, self.end, 5)
        self.assertEqual(result["items"], [])
        self.assertIn("network down", result["error"])


class FallbackProviderTests(unittest.TestCase):
    def setUp(self):
        self.end = datetime(2026, 11, 15, 23, 0, tzinfo=TZ)
        self.start = self.end - timedelta(days=2)
        self.item = {"title": "回退新闻", "published_at": "2026-11-13T20:50:00+08:00"}

    def test_primary_result_wins(self):
        primary = DummyProvider("primary", items=[{"title": "主源"}])
        fallback = DummyProvider("fallback", items=[self.item])
        provider = analysis.FallbackNewsProvider(primary, [fallback])

        result = provider.fetch_company_news({}, self.start, self.end, 5)

        self.assertEqual(result["items"][0]["title"], "主源")
        self.assertEqual(result["source"], "primary")

    def test_empty_primary_falls_back(self):
        primary = DummyProvider("yfinance")
        fallback = DummyProvider("google-news-rss", items=[self.item])
        provider = analysis.FallbackNewsProvider(primary, [fallback])

        result = provider.fetch_company_news({}, self.start, self.end, 5)

        self.assertEqual(result["items"][0]["title"], "回退新闻")
        self.assertIn("已回退", result["source"])
        self.assertIsNone(result["error"])

    def test_all_sources_empty_sets_error(self):
        provider = analysis.FallbackNewsProvider(
            DummyProvider("yfinance"),
            [DummyProvider("google-news-rss")],
        )

        result = provider.fetch_company_news({}, self.start, self.end, 5)

        self.assertEqual(result["items"], [])
        self.assertIn("均无结果", result["error"])

    def test_fallback_errors_are_collected(self):
        provider = analysis.FallbackNewsProvider(
            DummyProvider("yfinance", error="缺少依赖"),
            [DummyProvider("google-news-rss", error="超时")],
        )

        result = provider.fetch_company_news({}, self.start, self.end, 5)

        self.assertIn("缺少依赖", result["error"])
        self.assertIn("超时", result["error"])


class BuildProviderTests(unittest.TestCase):
    def test_builds_fallback_chain_from_config(self):
        provider = analysis.build_news_provider(build_config())
        self.assertIsInstance(provider, analysis.FallbackNewsProvider)
        self.assertEqual(provider.name, "yfinance")
        self.assertEqual([item.name for item in provider.fallbacks], ["google-news-rss"])

    def test_without_fallback_returns_primary(self):
        config = build_config()
        config["news"]["fallback_providers"] = []
        provider = analysis.build_news_provider(config)
        self.assertIsInstance(provider, analysis.YFinanceNewsProvider)


if __name__ == "__main__":
    unittest.main()
