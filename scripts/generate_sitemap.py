#!/usr/bin/env python3
"""ルートと blog/ の公開HTMLから sitemap.xml を自動生成する。

除外ルール:
  - EXCLUDE に列挙したファイル（アプリ本体・デモ・旧ローンチページ）
  - <meta name="robots" content="noindex"> を持つページ

lastmod は git の最終コミット日（取れなければ当日）。
ルートで実行する想定: python scripts/generate_sitemap.py
"""
import re
import subprocess
from datetime import date, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://clavis-note.com"

# noindex 検出に加えての保険。検索結果に出したくないページを明示除外。
EXCLUDE = {"app.html", "demo.html", "index-launch-eve.html"}

NOINDEX_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', re.I)

# JST。git が無い環境でのフォールバック用。
JST = timezone(timedelta(hours=9))


def git_lastmod(rel: str) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return date.today().isoformat()


def loc_for(rel: str) -> str:
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel}"


def meta_for(rel: str):
    """(changefreq, priority) を返す。"""
    if rel == "index.html":
        return ("weekly", "1.0")
    if rel == "blog/index.html":
        return ("weekly", "0.8")
    if rel.startswith("blog/"):
        return ("monthly", "0.7")
    if rel in ("privacy.html", "terms.html", "tokushoho.html"):
        return ("yearly", "0.3")
    return ("monthly", "0.6")


def collect():
    candidates = sorted(ROOT.glob("*.html")) + sorted((ROOT / "blog").glob("*.html"))
    pages = []
    for p in candidates:
        rel = p.relative_to(ROOT).as_posix()
        if rel in EXCLUDE:
            continue
        if NOINDEX_RE.search(p.read_text(encoding="utf-8", errors="ignore")):
            continue
        pages.append(rel)
    return pages


def build(rels):
    # priority 降順 → パス昇順で安定的に並べる（順序自体はSEOに影響しないが差分を安定させる）
    rels = sorted(rels, key=lambda r: (-float(meta_for(r)[1]), r))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel in rels:
        cf, prio = meta_for(rel)
        lines += [
            "  <url>",
            f"    <loc>{loc_for(rel)}</loc>",
            f"    <lastmod>{git_lastmod(rel)}</lastmod>",
            f"    <changefreq>{cf}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    xml = build(collect())
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(xml)


if __name__ == "__main__":
    main()
