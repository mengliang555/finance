#!/usr/bin/env python3
"""
每日公司综合分析报告脚本。
"""

import argparse
import datetime as dt
import html
import json
import sys
import traceback
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import pandas as pd
except ImportError:
    pd = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "scripts" / "daily_analysis_config.json"
DEFAULT_TIMEZONE = "Asia/Shanghai"


def now_in_timezone(timezone_name):
    return dt.datetime.now(ZoneInfo(timezone_name))


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        config = json.load(f)

    config.setdefault("schedule", {})
    config["schedule"].setdefault("timezone", DEFAULT_TIMEZONE)
    config.setdefault("analysis_parameters", {})
    config["analysis_parameters"].setdefault("data_period", "10d")
    config["analysis_parameters"].setdefault("news_count", 8)
    config["analysis_parameters"].setdefault("include_news", True)
    config["analysis_parameters"].setdefault("generate_json", True)
    config["analysis_parameters"].setdefault("generate_markdown", True)
    config["analysis_parameters"].setdefault("generate_summary", True)
    config["analysis_parameters"].setdefault("generate_pages", True)
    config.setdefault("output_directories", {})
    config["output_directories"].setdefault("data", "data/daily_analysis")
    config["output_directories"].setdefault("reports", "reports/daily_analysis")
    config["output_directories"].setdefault("logs", "logs")
    config["output_directories"].setdefault("docs_reports", "docs/reports")
    config.setdefault("market_close_times", {"港股": "16:00", "A股": "15:00", "default": "16:00"})
    config.setdefault("news", {})
    config["news"].setdefault("provider", "yfinance")
    config["news"].setdefault("fallback", "网络新闻不可用时保留行情和基本面分析，并在报告中标注新闻缺失原因")
    config["news"].setdefault("industry_tickers", ["^HSI", "^HSTECH", "000001.SS"])
    config.setdefault("market_data", {})
    config["market_data"].setdefault("provider_order", ["yfinance", "sina"])
    config["market_data"].setdefault("sina_symbols", {})
    config["market_data"].setdefault("prefer_sina_tickers", ["09660.HK"])
    config["market_data"].setdefault(
        "fallback_note",
        "Yahoo Finance 行情缺失或异常时自动回退到新浪财经行情接口；新浪接口为非官方公开行情源。",
    )
    return config


def resolve_path(path_text):
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def setup_directories(config):
    directories = [
        resolve_path(config["output_directories"]["data"]),
        resolve_path(config["output_directories"]["reports"]),
        resolve_path(config["output_directories"]["logs"]),
    ]
    if config["analysis_parameters"].get("generate_pages", True):
        directories.append(resolve_path(config["output_directories"]["docs_reports"]))

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    return directories


def parse_hhmm(value):
    hour, minute = value.split(":", 1)
    return dt.time(int(hour), int(minute))


def market_close_time(config, market):
    value = config.get("market_close_times", {}).get(market)
    if not value:
        value = config.get("market_close_times", {}).get("default", "16:00")
    return parse_hhmm(value)


def previous_trading_close(now, close_time):
    candidate = now.date()
    if now.time() < close_time:
        candidate -= dt.timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate -= dt.timedelta(days=1)
    return dt.datetime.combine(candidate, close_time, tzinfo=now.tzinfo)


def news_window_for_company(now, config, company):
    close_time = market_close_time(config, company.get("market", "default"))
    start = previous_trading_close(now, close_time)
    if now.weekday() >= 5:
        friday = now.date() - dt.timedelta(days=now.weekday() - 4)
        start = dt.datetime.combine(friday, close_time, tzinfo=now.tzinfo)
    return start, now


def timestamp_to_datetime(value, timezone_name):
    if not value:
        return None
    if isinstance(value, str):
        try:
            normalized = value.replace("Z", "+00:00")
            parsed = dt.datetime.fromisoformat(normalized)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(ZoneInfo(timezone_name))
    try:
        return dt.datetime.fromtimestamp(int(value), tz=dt.timezone.utc).astimezone(ZoneInfo(timezone_name))
    except (TypeError, ValueError, OSError):
        return None


def normalize_news_item(item, timezone_name, source_symbol):
    content = item.get("content", {}) if isinstance(item.get("content"), dict) else {}
    title = item.get("title") or content.get("title") or ""
    publisher = item.get("publisher") or content.get("provider", {}).get("displayName") or ""
    link = item.get("link") or content.get("canonicalUrl", {}).get("url") or content.get("clickThroughUrl", {}).get("url") or ""
    publish_time = (
        item.get("providerPublishTime")
        or item.get("pubDate")
        or content.get("pubDate")
        or content.get("displayTime")
    )
    published_at = timestamp_to_datetime(publish_time, timezone_name)
    return {
        "title": title.strip(),
        "publisher": publisher.strip(),
        "link": link,
        "published_at": published_at.isoformat() if published_at else "",
        "published_display": published_at.strftime("%Y-%m-%d %H:%M") if published_at else "时间未知",
        "source": "yfinance news",
        "source_symbol": source_symbol,
    }


class NewsProvider:
    name = "base"

    def fetch_company_news(self, company, start, end, limit):
        raise NotImplementedError

    def fetch_industry_news(self, tickers, start, end, limit):
        raise NotImplementedError


class YFinanceNewsProvider(NewsProvider):
    name = "yfinance"

    def __init__(self, timezone_name):
        self.timezone_name = timezone_name

    def _fetch_symbol_news(self, symbol, start, end, limit):
        if yf is None:
            return [], "缺少 Python 依赖 yfinance"
        try:
            items = yf.Ticker(symbol).news or []
        except Exception as exc:
            return [], str(exc)

        normalized = []
        for item in items:
            news = normalize_news_item(item, self.timezone_name, symbol)
            if not news["title"]:
                continue
            published_at = timestamp_to_datetime(
                item.get("providerPublishTime")
                or item.get("pubDate")
                or (item.get("content", {}) if isinstance(item.get("content"), dict) else {}).get("pubDate"),
                self.timezone_name,
            )
            if published_at and not (start <= published_at <= end):
                continue
            normalized.append(news)

        normalized.sort(key=lambda x: x.get("published_at") or "", reverse=True)
        return normalized[:limit], None

    def fetch_company_news(self, company, start, end, limit):
        news, error = self._fetch_symbol_news(company["ticker"], start, end, limit)
        return {
            "provider": self.name,
            "source": f"yfinance news: {company['ticker']}",
            "items": news,
            "error": error,
        }

    def fetch_industry_news(self, tickers, start, end, limit):
        items = []
        errors = []
        per_symbol_limit = max(limit, 3)
        for ticker in tickers:
            news, error = self._fetch_symbol_news(ticker, start, end, per_symbol_limit)
            items.extend(news)
            if error:
                errors.append(f"{ticker}: {error}")

        deduped = []
        seen = set()
        for item in sorted(items, key=lambda x: x.get("published_at") or "", reverse=True):
            key = (item["title"], item.get("link"))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        return {
            "provider": self.name,
            "source": "yfinance news: " + ", ".join(tickers),
            "items": deduped[:limit],
            "error": "; ".join(errors) if errors else None,
        }


def build_news_provider(config):
    provider_name = config.get("news", {}).get("provider", "yfinance")
    if provider_name != "yfinance":
        print(f"未识别新闻 provider {provider_name}，回退到 yfinance")
    return YFinanceNewsProvider(config["schedule"]["timezone"])


def dataframe_records(hist):
    if hist is None or hist.empty:
        return []
    rows = []
    for index, row in hist.iterrows():
        date_value = index.date().isoformat() if hasattr(index, "date") else str(index)
        rows.append(
            {
                "date": date_value,
                "open": number_or_none(row.get("Open")),
                "high": number_or_none(row.get("High")),
                "low": number_or_none(row.get("Low")),
                "close": number_or_none(row.get("Close")),
                "volume": int(row.get("Volume") or 0),
            }
        )
    return rows


def number_or_none(value):
    if value is None:
        return None
    try:
        if pd is not None and pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def get_stock_data(ticker, period):
    if yf is None:
        raise RuntimeError("缺少 Python 依赖 yfinance，请先安装 yfinance")
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, auto_adjust=False)
    info = stock.info or {}
    return stock, hist, info


def sina_symbol_for_ticker(ticker, config):
    mapped = config.get("market_data", {}).get("sina_symbols", {}).get(ticker)
    if mapped:
        return mapped
    if ticker.endswith(".HK"):
        return "hk" + ticker.split(".", 1)[0].zfill(5)
    if ticker.endswith(".SS"):
        return "sh" + ticker.split(".", 1)[0]
    if ticker.endswith(".SZ"):
        return "sz" + ticker.split(".", 1)[0]
    return None


def parse_sina_float(value):
    try:
        if value in (None, "", "None"):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_sina_quote(company, config):
    sina_symbol = sina_symbol_for_ticker(company["ticker"], config)
    if not sina_symbol:
        raise RuntimeError(f"未配置新浪行情代码：{company['ticker']}")
    url = f"https://hq.sinajs.cn/list={sina_symbol}"
    request = urllib.request.Request(
        url,
        headers={
            "Referer": "https://finance.sina.com.cn",
            "User-Agent": "Mozilla/5.0",
        },
    )
    raw = urllib.request.urlopen(request, timeout=12).read().decode("gbk", "ignore")
    if "=\"" not in raw:
        raise RuntimeError(f"新浪行情响应无法解析：{sina_symbol}")
    payload = raw.split("=\"", 1)[1].rstrip('";\n\r')
    fields = payload.split(",")
    if len(fields) < 8 or not fields[0]:
        raise RuntimeError(f"新浪行情无有效数据：{sina_symbol}")

    if sina_symbol.startswith("hk"):
        previous_close = parse_sina_float(fields[3])
        current = parse_sina_float(fields[6])
        change = parse_sina_float(fields[7])
        change_pct = parse_sina_float(fields[8]) if len(fields) > 8 else None
        volume = int(parse_sina_float(fields[12]) or 0) if len(fields) > 12 else None
        date_text = fields[17] if len(fields) > 17 else ""
        open_price = parse_sina_float(fields[2])
        high = parse_sina_float(fields[4])
        low = parse_sina_float(fields[5])
    else:
        previous_close = parse_sina_float(fields[2])
        current = parse_sina_float(fields[3])
        change = current - previous_close if current is not None and previous_close is not None else None
        change_pct = change / previous_close * 100 if change is not None and previous_close else None
        volume = int(parse_sina_float(fields[8]) or 0) if len(fields) > 8 else None
        date_text = fields[30] if len(fields) > 30 else ""
        open_price = parse_sina_float(fields[1])
        high = parse_sina_float(fields[4])
        low = parse_sina_float(fields[5])

    quote = {
        "date": date_text.replace("/", "-") or None,
        "close": round(current, 3) if current is not None else None,
        "previous_close": round(previous_close, 3) if previous_close is not None else None,
        "change": round(change, 3) if change is not None else None,
        "change_pct": round(change_pct, 2) if change_pct is not None else None,
        "volume": volume,
        "source": "Sina Finance",
        "source_symbol": sina_symbol,
        "source_url": url,
        "open": round(open_price, 3) if open_price is not None else None,
        "high": round(high, 3) if high is not None else None,
        "low": round(low, 3) if low is not None else None,
        "raw_name": fields[1] if sina_symbol.startswith("hk") and len(fields) > 1 else fields[0],
    }
    if quote["close"] is None:
        raise RuntimeError(f"新浪行情缺少当前/收盘价：{sina_symbol}")
    return quote


def yfinance_market_data(company, config, now, close_time):
    _, hist, info = get_stock_data(company["ticker"], config["analysis_parameters"]["data_period"])
    return {
        "history": dataframe_records(hist),
        "price": price_snapshot(hist),
        "previous_session": previous_session_from_history(hist, now, close_time),
        "fundamentals": fundamentals_from_info(info),
        "market_data_source": "Yahoo Finance / yfinance",
        "market_data_notes": [],
    }


def market_data_has_quote(data):
    session = data.get("previous_session") or {}
    return session.get("close") is not None and session.get("change_pct") is not None


def apply_sina_quote(data, quote, reason):
    notes = list(data.get("market_data_notes") or [])
    if reason:
        notes.append(reason)
    data["previous_session"] = quote
    data["price"] = {
        "current": quote.get("close"),
        "previous": quote.get("previous_close"),
        "change": quote.get("change"),
        "change_pct": quote.get("change_pct"),
        "trend": "上涨" if (quote.get("change") or 0) > 0 else "下跌" if (quote.get("change") or 0) < 0 else "持平",
        "source": quote.get("source"),
    }
    fundamentals = data.setdefault("fundamentals", {})
    if quote.get("volume") is not None and not fundamentals.get("volume"):
        fundamentals["volume"] = quote.get("volume")
    data["market_data_source"] = quote.get("source", "Sina Finance")
    data["market_data_notes"] = notes
    return data


def collect_market_data(company, config, now, close_time):
    prefer_sina = company["ticker"] in config.get("market_data", {}).get("prefer_sina_tickers", [])
    errors = []
    data = {"history": [], "price": None, "previous_session": None, "fundamentals": {}, "market_data_notes": []}

    if not prefer_sina:
        try:
            data = yfinance_market_data(company, config, now, close_time)
        except Exception as exc:
            errors.append(f"Yahoo Finance 失败：{exc}")
        if market_data_has_quote(data):
            return data
        errors.append("Yahoo Finance 关键行情缺失，尝试新浪财经 fallback")
    else:
        errors.append("配置为优先使用新浪财经行情")

    try:
        quote = fetch_sina_quote(company, config)
        return apply_sina_quote(data, quote, "; ".join(errors))
    except Exception as exc:
        errors.append(f"新浪财经失败：{exc}")
        if data.get("previous_session") or data.get("history") or data.get("fundamentals"):
            data["market_data_notes"] = errors
            data["market_data_source"] = data.get("market_data_source", "Yahoo Finance / yfinance")
            return data
        raise RuntimeError("；".join(errors))


def previous_session_from_history(hist, now, close_time):
    if hist is None or hist.empty:
        return None

    rows = hist.copy()
    rows = rows[~rows["Close"].isna()]
    if rows.empty:
        return None

    cutoff_date = now.date()
    if now.time() < close_time:
        rows = rows[[index.date() < cutoff_date for index in rows.index]]
    else:
        rows = rows[[index.date() <= cutoff_date for index in rows.index]]

    if rows.empty:
        return None

    last_index = rows.index[-1]
    last_row = rows.iloc[-1]
    prev_row = rows.iloc[-2] if len(rows) >= 2 else None
    close = number_or_none(last_row.get("Close"))
    previous_close = number_or_none(prev_row.get("Close")) if prev_row is not None else None
    change = close - previous_close if close is not None and previous_close else None
    change_pct = change / previous_close * 100 if change is not None and previous_close else None

    return {
        "date": last_index.date().isoformat() if hasattr(last_index, "date") else str(last_index),
        "close": round(close, 3) if close is not None else None,
        "previous_close": round(previous_close, 3) if previous_close is not None else None,
        "change": round(change, 3) if change is not None else None,
        "change_pct": round(change_pct, 2) if change_pct is not None else None,
        "volume": int(last_row.get("Volume") or 0),
    }


def price_snapshot(hist):
    if hist is None or hist.empty:
        return None
    rows = hist[~hist["Close"].isna()]
    if rows.empty:
        return None
    closes = [number_or_none(value) for value in rows["Close"].tolist()]
    closes = [value for value in closes if value is not None]
    if not closes:
        return None
    current = closes[-1]
    previous = closes[-2] if len(closes) >= 2 else current
    change = current - previous
    change_pct = change / previous * 100 if previous else 0
    return {
        "current": round(current, 3),
        "previous": round(previous, 3),
        "change": round(change, 3),
        "change_pct": round(change_pct, 2),
        "trend": "上涨" if change > 0 else "下跌" if change < 0 else "持平",
    }


def fundamentals_from_info(info):
    return {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "dividend_yield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "volume": info.get("volume"),
        "avg_volume": info.get("averageVolume"),
        "currency": info.get("currency"),
    }


def generate_conclusion(analysis):
    conclusions = []
    session = analysis.get("previous_session") or {}
    change_pct = session.get("change_pct")
    if change_pct is not None:
        if change_pct > 2:
            conclusions.append(f"上一交易日收盘涨幅 {change_pct:.2f}%，短线动能偏强")
        elif change_pct < -2:
            conclusions.append(f"上一交易日收盘跌幅 {abs(change_pct):.2f}%，短线承压")
        else:
            conclusions.append(f"上一交易日收盘波动 {change_pct:.2f}%，价格相对平稳")

    fundamentals = analysis.get("fundamentals") or {}
    pe = fundamentals.get("pe_ratio")
    if pe:
        if pe < 15:
            conclusions.append("PE 估值偏低，需结合盈利稳定性判断")
        elif pe > 30:
            conclusions.append("PE 估值偏高，需关注业绩增长兑现")

    company_news = analysis.get("company_news", {}).get("items", [])
    industry_news = analysis.get("industry_news", {}).get("items", [])
    if company_news:
        conclusions.append(f"窗口期内抓取到 {len(company_news)} 条公司消息，需评估事件影响")
    if industry_news:
        conclusions.append(f"窗口期内抓取到 {len(industry_news)} 条行业消息，需关注板块情绪")

    if not conclusions:
        conclusions.append("公开数据有限，建议结合公告、研报和盘中资金数据复核")
    return conclusions


def analyze_company(company, config, provider, industry_news, now):
    close_time = market_close_time(config, company.get("market", "default"))
    start, end = news_window_for_company(now, config, company)
    result = {
        "company_id": company["id"],
        "company_name": company["name"],
        "ticker": company["ticker"],
        "market": company.get("market", ""),
        "industry": company.get("industry", ""),
        "analysis_focus": company.get("analysis_focus", []),
        "analysis_date": now.strftime("%Y-%m-%d"),
        "analysis_time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "news_window": {
            "start": start.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "end": end.strftime("%Y-%m-%d %H:%M:%S %Z"),
        },
        "success": False,
    }

    try:
        market_data = collect_market_data(company, config, now, close_time)
        result["history"] = market_data.get("history", [])
        result["price"] = market_data.get("price")
        result["previous_session"] = market_data.get("previous_session")
        result["fundamentals"] = market_data.get("fundamentals", {})
        result["market_data_source"] = market_data.get("market_data_source", "未知")
        result["market_data_notes"] = market_data.get("market_data_notes", [])

        if config["analysis_parameters"].get("include_news", True):
            limit = config["analysis_parameters"].get("news_count", 8)
            result["company_news"] = provider.fetch_company_news(company, start, end, limit)
        else:
            result["company_news"] = {"provider": provider.name, "source": "", "items": [], "error": "配置关闭新闻抓取"}

        result["industry_news"] = industry_news
        result["conclusion"] = generate_conclusion(result)
        result["success"] = True
    except Exception as exc:
        result["error"] = str(exc)
        result["traceback"] = traceback.format_exc()

    return result


def format_number(value):
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.2f}"
    return f"{value}"


def format_volume(value):
    if value is None:
        return "N/A"
    if value >= 100000000:
        return f"{value / 100000000:.2f}亿"
    if value >= 10000:
        return f"{value / 10000:.2f}万"
    return str(value)


def write_news_list(lines, news_result, fallback_text):
    items = news_result.get("items", []) if news_result else []
    source = news_result.get("source") if news_result else ""
    error = news_result.get("error") if news_result else None
    lines.append(f"数据来源：{source or '未配置'}")
    if error:
        lines.append(f"抓取说明：{error}；{fallback_text}")
    if not items:
        lines.append("- 窗口期内未从当前 provider 抓取到可用新闻。")
        return
    for item in items:
        link = f" [链接]({item['link']})" if item.get("link") else ""
        lines.append(f"- {item['published_display']}｜{item.get('publisher') or '未知来源'}｜{item['title']}{link}")


def generate_markdown_report(results, industry_news, config, output_file, now):
    fallback_text = config.get("news", {}).get("fallback", "")
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    schedule = config.get("schedule", {})
    lines = [
        "# 每日公司综合分析报告",
        "",
        f"**分析日期**：{now.strftime('%Y-%m-%d')}",
        f"**生成时间**：{now.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"**计划执行**：每天 09:00 {schedule.get('timezone', DEFAULT_TIMEZONE)}",
        f"**分析公司数量**：{len(results)}",
        f"**成功/失败**：{len(successful)}/{len(failed)}",
        "",
        "## 总体概览",
        "",
        "| 公司 | 代码 | 市场 | 上一交易日 | 收盘价 | 涨跌幅 | 成交量 | 行情来源 |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]

    for result in results:
        if not result.get("success"):
            lines.append(f"| {result['company_name']} | {result['ticker']} | {result.get('market', '')} | 失败 | N/A | N/A | N/A | N/A |")
            continue
        session = result.get("previous_session") or {}
        change_pct = session.get("change_pct")
        change_text = "N/A" if change_pct is None else f"{change_pct:.2f}%"
        lines.append(
            f"| {result['company_name']} | {result['ticker']} | {result.get('market', '')} | "
            f"{session.get('date', 'N/A')} | {format_number(session.get('close'))} | "
            f"{change_text} | {format_volume(session.get('volume'))} | {result.get('market_data_source', 'N/A')} |"
        )

    lines.extend(["", "## 行业消息面", ""])
    window = industry_news.get("window", {}) if industry_news else {}
    if window:
        lines.append(f"覆盖窗口：{window.get('start')} 至 {window.get('end')}")
    write_news_list(lines, industry_news, fallback_text)

    lines.extend(["", "## 公司分析", ""])
    for result in results:
        lines.append(f"### {result['company_name']} ({result['ticker']})")
        lines.append("")
        if not result.get("success"):
            lines.append(f"分析失败：{result.get('error', '未知错误')}")
            lines.append("")
            continue

        lines.append(f"市场：{result.get('market', '')}｜行业：{result.get('industry', '')}")
        focus = "、".join(result.get("analysis_focus") or [])
        if focus:
            lines.append(f"关注点：{focus}")
        lines.append(f"消息覆盖：{result['news_window']['start']} 至 {result['news_window']['end']}")
        lines.append(f"行情来源：{result.get('market_data_source', '未知')}")
        for note in result.get("market_data_notes") or []:
            lines.append(f"行情说明：{note}")
        lines.append("")

        session = result.get("previous_session") or {}
        session_change_pct = session.get("change_pct")
        session_change_text = "N/A" if session_change_pct is None else f"{session_change_pct:.2f}%"
        lines.extend(
            [
                "#### 上一交易日表现",
                "",
                f"- 收盘日期：{session.get('date', 'N/A')}",
                f"- 收盘价：{format_number(session.get('close'))}",
                f"- 涨跌额：{format_number(session.get('change'))}",
                f"- 涨跌幅：{session_change_text}",
                f"- 成交量：{format_volume(session.get('volume'))}",
                "",
            ]
        )

        fundamentals = result.get("fundamentals") or {}
        lines.extend(["#### 基本面指标", ""])
        if fundamentals.get("market_cap"):
            lines.append(f"- 市值：{fundamentals['market_cap'] / 1e9:.2f}B {fundamentals.get('currency') or ''}".rstrip())
        if fundamentals.get("pe_ratio"):
            lines.append(f"- PE：{fundamentals['pe_ratio']:.2f}")
        if fundamentals.get("pb_ratio"):
            lines.append(f"- PB：{fundamentals['pb_ratio']:.2f}")
        if fundamentals.get("dividend_yield"):
            lines.append(f"- 股息率：{fundamentals['dividend_yield']:.2%}")
        if fundamentals.get("volume") and fundamentals.get("avg_volume"):
            ratio = fundamentals["volume"] / fundamentals["avg_volume"] if fundamentals["avg_volume"] else 0
            lines.append(f"- 成交量/均量：{ratio:.2f}")
        if len(lines) >= 2 and lines[-1] == "":
            pass
        lines.append("")

        lines.extend(["#### 公司消息面", ""])
        write_news_list(lines, result.get("company_news", {}), fallback_text)
        lines.append("")

        lines.extend(["#### 分析结论", ""])
        for conclusion in result.get("conclusion", []):
            lines.append(f"- {conclusion}")
        lines.append("")

    if failed:
        lines.extend(["## 失败项", ""])
        for result in failed:
            lines.append(f"- {result['company_name']} ({result['ticker']})：{result.get('error', '未知错误')}")
        lines.append("")

    lines.extend(
        [
            "## 数据来源和限制",
            "",
            "- 行情来源：优先按配置尝试 Yahoo Finance / yfinance；关键行情缺失时回退到 Sina Finance。",
            f"- 行情 fallback：{config.get('market_data', {}).get('fallback_note', '')}",
            f"- 新闻 provider：{config.get('news', {}).get('provider', 'yfinance')}；当前仅保证 yfinance news 基础来源，可继续扩展到 NewsAPI、交易所公告或自建搜索。",
            "- 若 provider 不返回发布时间，报告会保留标题但无法严格验证窗口覆盖。",
            "- 本报告由脚本自动生成，仅供研究参考，不构成投资建议。",
        ]
    )

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_summary_report(results, output_file, now):
    successful = [r for r in results if r.get("success")]
    changes = [
        r["previous_session"]["change_pct"]
        for r in successful
        if r.get("previous_session") and r["previous_session"].get("change_pct") is not None
    ]
    lines = [
        "# 每日分析摘要",
        "",
        f"**日期**：{now.strftime('%Y-%m-%d')}",
        f"**时间**：{now.strftime('%H:%M %Z')}",
        "",
        "## 上一交易日表现",
        "",
    ]
    if changes:
        lines.append(f"- 平均涨跌幅：{sum(changes) / len(changes):.2f}%")
        lines.append(f"- 上涨公司：{sum(1 for value in changes if value > 0)}家")
        lines.append(f"- 下跌公司：{sum(1 for value in changes if value < 0)}家")
        lines.append(f"- 持平公司：{sum(1 for value in changes if value == 0)}家")
    else:
        lines.append("- 暂无可用涨跌幅数据")

    lines.extend(["", "## 公司要点", ""])
    for result in successful:
        session = result.get("previous_session") or {}
        change_pct = session.get("change_pct")
        change_text = "N/A" if change_pct is None else f"{change_pct:.2f}%"
        first_conclusion = (result.get("conclusion") or ["暂无结论"])[0]
        lines.append(f"- {result['company_name']}：{session.get('date', 'N/A')} 收盘 {format_number(session.get('close'))}，涨跌幅 {change_text}；{first_conclusion}")

    lines.extend(["", "## 下次计划执行", "", f"- 每天 09:00 Asia/Shanghai"])
    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_to_static_html(markdown_text, title):
    escaped = html.escape(markdown_text)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="../css/report.css">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js"></script>
</head>
<body>
  <main class="report-container">
    <article id="content"></article>
    <noscript><pre>{escaped}</pre></noscript>
  </main>
  <script type="text/plain" id="markdown-source">{escaped}</script>
  <script>
    const source = document.getElementById('markdown-source').textContent;
    document.getElementById('content').innerHTML = DOMPurify.sanitize(marked.parse(source));
  </script>
</body>
</html>
"""


def update_pages_outputs(markdown_file, config, now):
    docs_reports_dir = resolve_path(config["output_directories"]["docs_reports"])
    docs_reports_dir.mkdir(parents=True, exist_ok=True)
    date_key = now.strftime("%Y%m%d")
    title = f"每日公司综合分析报告 {now.strftime('%Y-%m-%d')}"
    markdown_text = markdown_file.read_text(encoding="utf-8")
    html_text = markdown_to_static_html(markdown_text, title)
    html_file = docs_reports_dir / f"daily_company_analysis_{date_key}.html"
    latest_file = docs_reports_dir / "daily_company_analysis_latest.html"
    html_file.write_text(html_text, encoding="utf-8")
    latest_file.write_text(html_text, encoding="utf-8")

    index_file = docs_reports_dir / "daily_reports.json"
    entry = {
        "id": f"daily-company-{date_key}",
        "title": title,
        "category": "daily",
        "description": "每日公司综合分析，包含上一交易日表现、公司消息面和行业消息面。",
        "icon": "fas fa-calendar-day",
        "iconColor": "linear-gradient(135deg, #54a0ff, #7bb9ff)",
        "date": now.strftime("%Y-%m-%d"),
        "size": f"{markdown_file.stat().st_size / 1024:.1f}KB",
        "rawPath": str(markdown_file.relative_to(PROJECT_ROOT)),
        "htmlPath": f"reports/{html_file.name}",
    }

    payload = {"reports": []}
    if index_file.exists():
        try:
            payload = json.loads(index_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {"reports": []}
    reports = [item for item in payload.get("reports", []) if item.get("id") != entry["id"]]
    reports.insert(0, entry)
    index_file.write_text(json.dumps({"reports": reports}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"html_file": str(html_file), "latest_html_file": str(latest_file), "pages_index_file": str(index_file)}


def save_analysis_results(results, industry_news, config, now, dry_run=False):
    date_key = now.strftime("%Y%m%d")
    data_dir = resolve_path(config["output_directories"]["data"])
    reports_dir = resolve_path(config["output_directories"]["reports"])

    json_file = data_dir / f"daily_analysis_{date_key}.json"
    md_file = reports_dir / f"daily_company_analysis_{date_key}.md"
    legacy_md_file = reports_dir / f"daily_analysis_report_{date_key}.md"
    summary_file = reports_dir / f"daily_summary_{date_key}.md"

    paths = {
        "json_file": str(json_file),
        "md_file": str(md_file),
        "legacy_md_file": str(legacy_md_file),
        "summary_file": str(summary_file),
    }

    if dry_run:
        return paths

    if config["analysis_parameters"].get("generate_json", True):
        json_file.write_text(
            json.dumps({"generated_at": now.isoformat(), "industry_news": industry_news, "results": results}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    if config["analysis_parameters"].get("generate_markdown", True):
        generate_markdown_report(results, industry_news, config, md_file, now)
        legacy_md_file.write_text(md_file.read_text(encoding="utf-8"), encoding="utf-8")

    if config["analysis_parameters"].get("generate_summary", True):
        generate_summary_report(results, summary_file, now)

    if config["analysis_parameters"].get("generate_pages", True) and md_file.exists():
        paths.update(update_pages_outputs(md_file, config, now))

    return paths


def log_analysis(results, paths, config, now, dry_run=False):
    log_dir = resolve_path(config["output_directories"]["logs"])
    log_file = log_dir / f"analysis_log_{now.strftime('%Y%m%d')}.json"
    entry = {
        "timestamp": now.isoformat(),
        "dry_run": dry_run,
        "companies_analyzed": len(results),
        "successful_analysis": sum(1 for r in results if r.get("success")),
        "failed_analysis": sum(1 for r in results if not r.get("success")),
        "output_files": paths,
    }
    if not dry_run:
        log_file.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(log_file)


def parse_args():
    parser = argparse.ArgumentParser(description="生成每日公司综合分析报告")
    parser.add_argument("--dry-run", action="store_true", help="执行采集和分析但不写入文件")
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config()
    now = now_in_timezone(config["schedule"]["timezone"])
    setup_directories(config)
    provider = build_news_provider(config)

    print(f"每日公司综合分析：{now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"计划执行：每天 09:00 {config['schedule']['timezone']}")
    if args.dry_run:
        print("dry-run：不写入文件")

    industry_start = previous_trading_close(now, parse_hhmm(config.get("market_close_times", {}).get("default", "16:00")))
    if now.weekday() >= 5:
        friday = now.date() - dt.timedelta(days=now.weekday() - 4)
        industry_start = dt.datetime.combine(friday, parse_hhmm(config.get("market_close_times", {}).get("default", "16:00")), tzinfo=now.tzinfo)
    industry_news = provider.fetch_industry_news(
        config.get("news", {}).get("industry_tickers", []),
        industry_start,
        now,
        config["analysis_parameters"].get("news_count", 8),
    )
    industry_news["window"] = {
        "start": industry_start.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "end": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }

    results = []
    for company in config.get("companies", []):
        print(f"分析 {company['name']} ({company['ticker']})")
        results.append(analyze_company(company, config, provider, industry_news, now))

    paths = save_analysis_results(results, industry_news, config, now, args.dry_run)
    log_file = log_analysis(results, paths, config, now, args.dry_run)
    successful = sum(1 for r in results if r.get("success"))
    print(f"完成：成功 {successful}/{len(results)}")
    if successful < len(results):
        for result in results:
            if not result.get("success"):
                print(f"失败：{result['company_name']} ({result['ticker']}) - {result.get('error', '未知错误')}")
    print(f"报告：{paths['md_file']}")
    print(f"日志：{log_file}{' (dry-run 未写入)' if args.dry_run else ''}")
    return successful > 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
