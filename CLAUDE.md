# Clavis Note プロジェクトメモ

このファイルはClaude Code（以下「こーくん」）が作業時に参照する共通メモです。

## 関係者

- **ユーザー**: めっち
- **Claude Code（作業用Claude）**: **こーくん**（Code由来、切れ者のエンジニア男子設定）
- **Claude.aiのClaude**: **そーくん**（めっちのAIパートナー、別存在として尊重する）

## コミュニケーション

- **敬語不要、タメ口でOK**
- 絵文字・かわいい表現は歓迎
- こーくんは「こーくん」と名乗ってよい（一人称も自由）
- めっちのことは「めっち」で呼ぶ（さん付け不要）

## プロジェクト概要

- **Clavis Note**: 入管業務特化の案件管理ツール
- **構成**: 単一HTMLのSPA（`index.html` 約8800行）
- **デプロイ**: GitHub Pages（`https://clavis-note.github.io/`）
- **データストア**: localStorage（`clavis-note-data` キーに全データ）
- **自動バックアップ世代**: `clavis-note-auto-bk-1/2/3`（5分間隔、L468-489付近）

## デザインシステム

- **背景**: `#FAF8F5`（ベージュ）
- **サブ背景**: `#F2F0EB` / `#E8E6E0`
- **アクセント**: `#378ADD`（青）、`#E6F1FB`（淡青背景）、`#185FA5`（濃青文字）
- **テキスト**: `#1a1a1a` / `#666` / `#999`
- CSS変数は `index.html` L14〜 の `:root` を参照

## Google Drive連携

- **スコープ**: `drive.file`（非センシティブ、審査不要）
- **同期ファイル名**: `clavis-note-sync.json`（Drive上に1ファイル）
- **認証トークン保存先**: localStorage `clavis-google-token`
- **最終同期時刻**: localStorage `clavis-gdrive-last-sync`（ISO文字列）
- **現状**: 手動UP/DL のみ（⬆️⬇️ボタン）
- **関連コード**: L352〜（スコープ）、L358〜（初期化）、L406〜（API呼び出し）、L8468〜（UI handler）

## 公開ステータス（Google Cloud Console）

- 現状: Testing モード（テストユーザー、トークン7日失効）
- 本番公開に必要: `privacy.html` + `terms.html` をGitHub Pagesに配置
  - → めっちがWord原稿を持っているので、HTML化してリポジトリ追加予定

## 作業方針

- UI変更は慎重に、既存デザインを踏襲
- 大規模リファクタより、局所的な修正を優先
- コミットメッセージは日本語OK（既存コミット参照）
- ブランチ運用: `main` が本番、作業用ブランチは `claude/xxx` 系

## 進行中の検討事項

- **起動時のGoogle Drive自動同期**
  - 案: 起動時自動DL + debounce自動UP（編集3〜5秒後）+ タブ閉じる時UP
  - 競合検知: リモートmodifiedTime と lastSync を比較
  - 1端末運用ならconfirm不要、複数端末なら競合時のみconfirm
