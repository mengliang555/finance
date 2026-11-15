#!/usr/bin/env python3
"""组装 Cloudflare 部署用的站点目录。

仓库里有两类文件需要出现在站点上：

1. ``docs/`` —— 页面、样式、脚本、报告中心索引（站点的发布根目录）；
2. ``reports/`` 与 ``guides/`` 下的 Markdown —— 报告中心的正文，平时是按
   ``rawPath`` 从 GitHub raw 拉取的。

Cloudflare 只上传构建产物目录，访问不到 ``docs/`` 之外的仓库文件，所以这里把
两类内容合并到一个自包含目录（默认 ``dist/``）：

    dist/
    ├── index.html ...        # 原样复制 docs/
    ├── reports/*.md          # 报告正文（与原路径一致）
    ├── guides/*.md           # 指南正文
    └── _headers              # Cloudflare 响应头

这样报告中心可以优先同源加载 Markdown，GitHub 只作为源码仓库，不再是运行时依赖。

用法：
    python scripts/build_site.py
    python scripts/build_site.py --out dist
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 站点的发布根目录（GitHub Pages 的 /docs 源）
SITE_DIR = "docs"

# 需要随站点一起发布的 Markdown 目录
MARKDOWN_DIRS = ("reports", "guides")

HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN

/*.md
  Cache-Control: public, max-age=300
"""


def _validate_paths(root: Path, out_dir: Path) -> Path:
    site = root / SITE_DIR
    if not (site / "index.html").is_file():
        raise SystemExit(f"未找到站点入口：{site / 'index.html'}")

    resolved_out = out_dir.resolve()
    resolved_site = site.resolve()
    if resolved_out == root.resolve():
        raise SystemExit("输出目录不能是仓库根目录")
    if resolved_out == resolved_site or resolved_site in resolved_out.parents:
        raise SystemExit("输出目录不能是 docs/ 或位于 docs/ 之内")
    return site


def build(root: Path = PROJECT_ROOT, out_dir: Path | None = None) -> dict[str, int]:
    """把站点与 Markdown 组装到 out_dir，返回各部分文件数量。"""
    out_dir = out_dir or (root / "dist")
    site = _validate_paths(root, out_dir)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(site, out_dir)

    stats = {
        "docs": sum(1 for path in out_dir.rglob("*") if path.is_file()),
        "reports": 0,
        "guides": 0,
    }

    for name in MARKDOWN_DIRS:
        source = root / name
        if not source.is_dir():
            continue
        for path in source.rglob("*.md"):
            rel_path = path.relative_to(root)
            destination = out_dir / rel_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            stats[name] += 1

    (out_dir / "_headers").write_text(HEADERS, encoding="utf-8")
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="组装 Cloudflare 部署用的站点目录")
    parser.add_argument("--out", default="dist", help="输出目录（默认 dist）")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    stats = build(PROJECT_ROOT, out_dir)
    print(f"站点构建完成：{out_dir}")
    print(f"- 页面与静态资源：{stats['docs']} 个")
    print(f"- 报告 Markdown：{stats['reports']} 个")
    print(f"- 指南 Markdown：{stats['guides']} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
