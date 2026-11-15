#!/usr/bin/env python3
"""仓库一致性校验。

这个项目由「配置文件 + 生成脚本 + 静态站点 + 手写文档」四部分组成，最容易出问题
的地方不是业务逻辑，而是这四者之间的引用漂移：站点索引指向已删除的报告、文档链接
指向不存在的文件、首页代码和配置不一致、定时任务改了时间却忘了改 workflow。

本脚本只依赖标准库，可以在本地和 CI 中直接运行：

    python scripts/check_consistency.py

检查项：
1. 所有 JSON 文件可解析；
2. docs/reports/daily_reports.json 中每条记录的 rawPath / htmlPath 真实存在；
3. docs/js/reports.js 中静态报告的 rawPath 真实存在；
4. 面向读者的 Markdown 文档里的相对链接存在（跳过代码块和外部链接）；
5. docs/ 下的 HTML 本地资源存在，且不越出发布根目录 docs/（GitHub Pages 会 404）；
6. 配置里的公司股票代码出现在首页（允许 .SS/.SH、港股前导零等写法差异）；
7. 配置里的 cron（含时区）与 .github/workflows/daily-analysis.yml 一致；
8. 最新日报是否过期（仅警告，不影响退出码）。

退出码：有错误返回 1，只有警告返回 0。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 这些前缀代表外部资源或页内锚点，不需要在仓库里存在
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
    "#",
)

# 不参与扫描的目录（生成物、依赖、历史归档）
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "logs", "archive"}

# 面向读者的文档；archive/ 属于历史存档，故意不检查
DOC_MARKDOWN_GLOBS = (
    "README.md",
    "NAVIGATION.md",
    "UPDATE_LOG.md",
    "docs/README.md",
    "guides/*.md",
    "guides/**/*.md",
)

REPORT_INDEX = Path("docs/reports/daily_reports.json")
VALUATION_INDEX = Path("docs/valuation_reports.json")
REPORTS_JS = Path("docs/js/reports.js")
CONFIG_FILE = Path("scripts/daily_analysis_config.json")
WORKFLOW_FILE = Path(".github/workflows/daily-analysis.yml")
DOCS_ROOT = Path("docs")

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)")
JS_RAW_PATH_RE = re.compile(r"rawPath\s*:\s*['\"]([^'\"]+)['\"]")
WORKFLOW_CRON_RE = re.compile(r"-\s*cron:\s*['\"]([^'\"]+)['\"]")


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _iter_files(root: Path, suffixes: set[str]):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def _is_within(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def normalize_target(raw: str | None) -> str | None:
    """把 HTML/Markdown 里的链接值转换成仓库内相对路径，外部链接返回 None。"""
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if value.lower().startswith(EXTERNAL_PREFIXES):
        return None
    value = value.split("#", 1)[0].split("?", 1)[0].strip()
    if not value:
        return None
    return unquote(value)


def markdown_local_links(path: Path) -> list[tuple[int, str]]:
    """返回 Markdown 中 (行号, 原始链接) 列表，忽略围栏代码块。"""
    links: list[tuple[int, str]] = []
    in_fence = False
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in MD_LINK_RE.finditer(line):
            raw = match.group(1)
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            links.append((lineno, raw))
    return links


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.items.append((self.getpos()[0], value))


def check_json_files(root: Path) -> list[str]:
    errors = []
    for path in _iter_files(root, {".json"}):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{_rel(path, root)}: JSON 解析失败：{exc}")
    return errors


def check_report_index(root: Path) -> list[str]:
    index = root / REPORT_INDEX
    if not index.exists():
        return [f"{REPORT_INDEX.as_posix()}: 文件不存在"]

    try:
        payload = json.loads(index.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{REPORT_INDEX.as_posix()}: JSON 解析失败：{exc}"]

    reports = payload.get("reports")
    if not isinstance(reports, list):
        return [f"{REPORT_INDEX.as_posix()}: 缺少 reports 数组"]

    errors = []
    seen: set[str] = set()
    for entry in reports:
        if not isinstance(entry, dict):
            errors.append(f"{REPORT_INDEX.as_posix()}: reports 中存在非对象条目")
            continue
        report_id = entry.get("id", "")
        if not report_id:
            errors.append(f"{REPORT_INDEX.as_posix()}: 存在缺少 id 的条目")
        elif report_id in seen:
            errors.append(f"{REPORT_INDEX.as_posix()}: 重复的报告 id {report_id!r}")
        else:
            seen.add(report_id)

        raw_path = entry.get("rawPath")
        if not raw_path:
            errors.append(f"{REPORT_INDEX.as_posix()}: {report_id or '?'} 缺少 rawPath")
        elif not (root / raw_path).exists():
            errors.append(f"{REPORT_INDEX.as_posix()}: {report_id or '?'} 的 rawPath 不存在 -> {raw_path}")

        html_path = entry.get("htmlPath")
        if html_path and not (root / DOCS_ROOT / html_path).exists():
            errors.append(f"{REPORT_INDEX.as_posix()}: {report_id or '?'} 的 htmlPath 不存在 -> {html_path}")
    return errors


def check_valuation_index(root: Path) -> list[str]:
    """估值页面索引可选；存在时校验归档页面是否落地。"""
    path = root / VALUATION_INDEX
    if not path.exists():
        return []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{VALUATION_INDEX.as_posix()}: JSON 解析失败：{exc}"]

    reports = payload.get("reports") if isinstance(payload, dict) else None
    if not isinstance(reports, list):
        return [f"{VALUATION_INDEX.as_posix()}: 缺少 reports 数组"]

    errors = []
    for entry in reports:
        if not isinstance(entry, dict):
            errors.append(f"{VALUATION_INDEX.as_posix()}: reports 中存在非对象条目")
            continue
        report_id = entry.get("id", "?")
        html_path = entry.get("htmlPath")
        if not html_path:
            errors.append(f"{VALUATION_INDEX.as_posix()}: {report_id} 缺少 htmlPath")
        elif not (root / DOCS_ROOT / html_path).exists():
            errors.append(f"{VALUATION_INDEX.as_posix()}: {report_id} 的 htmlPath 不存在 -> {html_path}")
    return errors


def check_reports_js(root: Path) -> list[str]:
    path = root / REPORTS_JS
    if not path.exists():
        return [f"{REPORTS_JS.as_posix()}: 文件不存在"]

    errors = []
    text = path.read_text(encoding="utf-8")
    for match in JS_RAW_PATH_RE.finditer(text):
        raw_path = match.group(1)
        if not (root / raw_path).exists():
            lineno = text[: match.start()].count("\n") + 1
            errors.append(f"{REPORTS_JS.as_posix()}:{lineno}: rawPath 不存在 -> {raw_path}")
    return errors


def check_markdown_links(root: Path) -> list[str]:
    errors = []
    seen: set[Path] = set()
    for pattern in DOC_MARKDOWN_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            for lineno, raw in markdown_local_links(path):
                target = normalize_target(raw)
                if target is None:
                    continue
                if not (path.parent / target).exists():
                    errors.append(f"{_rel(path, root)}:{lineno}: 链接目标不存在 -> {raw}")
    return errors


def check_html_links(root: Path) -> list[str]:
    docs_root = (root / DOCS_ROOT).resolve()
    if not docs_root.is_dir():
        return [f"{DOCS_ROOT.as_posix()}/: 目录不存在"]

    errors = []
    for path in sorted(docs_root.rglob("*.html")):
        parser = _LinkCollector()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{_rel(path, root)}: 读取失败：{exc}")
            continue
        for lineno, raw in parser.items:
            target = normalize_target(raw)
            if target is None:
                continue
            resolved = (path.parent / target).resolve()
            if not _is_within(resolved, docs_root):
                errors.append(
                    f"{_rel(path, root)}:{lineno}: 链接指向发布根目录之外（GitHub Pages 会 404）-> {raw}"
                )
                continue
            if not resolved.exists():
                errors.append(f"{_rel(path, root)}:{lineno}: 本地资源不存在 -> {raw}")
    return errors


def ticker_aliases(ticker: str) -> set[str]:
    """同一代码的常见等价写法：A 股 .SS/.SH，港股补零。"""
    aliases = {ticker}
    code, _, suffix = ticker.partition(".")
    if suffix == "SS":
        aliases.add(f"{code}.SH")
    elif suffix == "SH":
        aliases.add(f"{code}.SS")
    elif suffix == "HK" and code.isdigit():
        stripped = code.lstrip("0") or "0"
        aliases.add(f"{stripped}.HK")
        aliases.add(f"{stripped.zfill(4)}.HK")
        aliases.add(f"{stripped.zfill(5)}.HK")
    return aliases


def check_ticker_coverage(root: Path) -> list[str]:
    config_path = root / CONFIG_FILE
    index_path = root / DOCS_ROOT / "index.html"
    if not config_path.exists():
        return [f"{CONFIG_FILE.as_posix()}: 文件不存在"]
    if not index_path.exists():
        return [f"{(DOCS_ROOT / 'index.html').as_posix()}: 文件不存在"]

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{CONFIG_FILE.as_posix()}: JSON 解析失败：{exc}"]

    text = index_path.read_text(encoding="utf-8")
    errors = []
    for company in config.get("companies", []):
        ticker = str(company.get("ticker", "")).strip()
        name = company.get("name", company.get("id", "?"))
        if not ticker:
            errors.append(f"{CONFIG_FILE.as_posix()}: 公司 {name} 缺少 ticker")
            continue
        aliases = sorted(ticker_aliases(ticker))
        if not any(alias in text for alias in aliases):
            errors.append(
                f"{(DOCS_ROOT / 'index.html').as_posix()}: 首页找不到 {name} 的代码 "
                f"{ticker}（可接受写法：{', '.join(aliases)}）"
            )
    return errors


def _local_cron_to_utc(fields: list[str], tz_name: str) -> str:
    """把本地时区的 cron 转换成 UTC 的 cron（只处理固定偏移，用于校验一致性）。"""
    if fields[0] == "*" or fields[1] == "*":
        return " ".join(fields)

    minute, hour = int(fields[0]), int(fields[1])
    reference = datetime(2026, 1, 1, hour, minute, tzinfo=ZoneInfo(tz_name))
    offset = reference.utcoffset() or timedelta(0)
    total_minutes = (hour * 60 + minute - int(offset.total_seconds() // 60)) % (24 * 60)
    return f"{total_minutes % 60} {total_minutes // 60} {fields[2]} {fields[3]} {fields[4]}"


def check_schedule_sync(root: Path) -> list[str]:
    config_path = root / CONFIG_FILE
    workflow_path = root / WORKFLOW_FILE
    if not config_path.exists():
        return [f"{CONFIG_FILE.as_posix()}: 文件不存在"]
    if not workflow_path.exists():
        return [f"{WORKFLOW_FILE.as_posix()}: 文件不存在（每日自动化依赖它）"]

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{CONFIG_FILE.as_posix()}: JSON 解析失败：{exc}"]

    schedule = config.get("schedule", {})
    cron = str(schedule.get("cron_expression", "")).strip()
    tz_name = str(schedule.get("timezone", "Asia/Shanghai"))
    fields = cron.split()
    if len(fields) != 5:
        return [f"{CONFIG_FILE.as_posix()}: schedule.cron_expression 非法：{cron!r}"]

    try:
        expected = _local_cron_to_utc(fields, tz_name)
    except Exception as exc:  # 时区名写错时给出可读错误
        return [f"{CONFIG_FILE.as_posix()}: 时区 {tz_name} 无法解析：{exc}"]

    workflow_crons = WORKFLOW_CRON_RE.findall(workflow_path.read_text(encoding="utf-8"))
    if not workflow_crons:
        return [f"{WORKFLOW_FILE.as_posix()}: 未找到 schedule cron"]

    if expected not in workflow_crons:
        return [
            f"调度不同步：配置为 {cron}（{tz_name}），对应 UTC 应为 {expected}，"
            f"而 workflow 中是 {', '.join(workflow_crons)}"
        ]
    return []


def check_freshness(root: Path, max_age_days: int = 7) -> list[str]:
    data_dir = root / "data" / "daily_analysis"
    files = sorted(data_dir.glob("daily_analysis_*.json"))
    if not files:
        return [f"{_rel(data_dir, root)}: 还没有任何日报数据"]

    latest: datetime | None = None
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                continue
            value = payload.get("generated_at", "")
            stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except (ValueError, OSError):
            continue
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        if latest is None or stamp > latest:
            latest = stamp

    if latest is None:
        return [f"{_rel(data_dir, root)}: 无法从日报 JSON 中读取 generated_at"]

    age_days = (datetime.now(timezone.utc) - latest.astimezone(timezone.utc)).days
    if age_days > max_age_days:
        return [
            f"最新日报生成于 {latest.date().isoformat()}，距今 {age_days} 天（阈值 {max_age_days} 天），"
            "请确认定时任务是否仍在运行"
        ]
    return []


def run_all(root: Path, max_age_days: int = 7) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    errors.extend(check_json_files(root))
    errors.extend(check_report_index(root))
    errors.extend(check_valuation_index(root))
    errors.extend(check_reports_js(root))
    errors.extend(check_markdown_links(root))
    errors.extend(check_html_links(root))
    errors.extend(check_ticker_coverage(root))
    errors.extend(check_schedule_sync(root))
    warnings = check_freshness(root, max_age_days)
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="检查仓库文档、站点与配置的一致性")
    parser.add_argument("--root", default=str(PROJECT_ROOT), help="项目根目录（默认：仓库根）")
    parser.add_argument("--max-age-days", type=int, default=7, help="日报允许的最大天数，仅警告（默认 7）")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    errors, warnings = run_all(root, args.max_age_days)

    for item in errors:
        print(f"[错误] {item}")
    for item in warnings:
        print(f"[警告] {item}")

    print(f"\n检查完成：{len(errors)} 个错误，{len(warnings)} 个警告")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
