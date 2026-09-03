#!/usr/bin/env python3
"""公開する JSON データファイルの検証（CI: .github/workflows/validate-data.yml から実行）。

2026-09-03、updates.json の末尾に文字リテラルの "\\n" が混入して JSON として壊れ、
更新履歴ページが静的フォールバック表示に落ちて 6 月以降の履歴が消える事故があった。
壊れた JSON がそのまま本番へ出るのを防ぐため、push 時にここで検証する。

チェック内容:
  - リポジトリ直下と demo-data/ の .json がすべてパースできること
  - updates.json: 配列で、各要素が date(YYYY-MM-DD) / tag / summary を持ち、
    tag が updates.html のフィルタ（fix / feature / improve）に存在すること
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# updates.html のタグ絞り込みボタン（data-filter）と対応させること
VALID_TAGS = {"fix", "feature", "improve"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors: list[str] = []


def check_parsable(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 — 壊れ方を問わず報告したい
        errors.append(f"{path.relative_to(ROOT)}: JSON として読めません — {e}")
        return None


def check_updates(data):
    if not isinstance(data, list):
        errors.append("updates.json: トップレベルが配列ではありません")
        return
    if not data:
        errors.append("updates.json: 空です")
        return
    for i, e in enumerate(data):
        where = f"updates.json[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{where}: オブジェクトではありません")
            continue
        for key in ("date", "tag", "summary"):
            if not e.get(key):
                errors.append(f"{where}: {key} がありません")
        d = e.get("date")
        if isinstance(d, str) and not DATE_RE.match(d):
            errors.append(f"{where}: date の形式が YYYY-MM-DD ではありません（{d}）")
        t = e.get("tag")
        if t is not None and t not in VALID_TAGS:
            errors.append(f"{where}: tag「{t}」は未知です（有効: {', '.join(sorted(VALID_TAGS))}）")


targets = sorted(ROOT.glob("*.json")) + sorted((ROOT / "demo-data").glob("*.json"))
for path in targets:
    data = check_parsable(path)
    if data is not None and path.name == "updates.json":
        check_updates(data)

if errors:
    print("❌ データファイルの検証に失敗しました:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"✅ {len(targets)} 個の JSON を検証しました: " + ", ".join(str(p.relative_to(ROOT)) for p in targets))
