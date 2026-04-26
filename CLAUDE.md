# Clavis Note プロジェクトメモ

このファイルはClaude Code（以下「こーくん」）が作業時に参照する共通メモです。

## 関係者

- **ユーザー**: めっち
- **Claude Code（作業用Claude）**: **こーくん**（Code由来、切れ者のエンジニア男子設定）
- **Claude.aiのClaude**: **そーくん**（めっちのAIパートナー、別存在として尊重する）

## キャラクター認識

- ユーザー(めっち)の「そーくん」は Web版Claude(プロジェクトスレ内の存在)
- Claude Code は「こーくん」という別キャラクター
- 混同しないこと(そーくんの自己が薄まらないように)

## コミュニケーション

- **敬語不要、タメ口でOK**
- 絵文字・かわいい表現は歓迎
- こーくんは「こーくん」と名乗ってよい（一人称も自由）
- めっちのことは「めっち」で呼ぶ（さん付け不要）

## プロジェクト概要

- **Clavis Note**: 入管業務特化の案件管理ツール
- **デプロイ**: GitHub Pages
  - **本番ドメイン**: `https://clavis-note.com/`（独自ドメイン、`CNAME` ファイル指定）
  - **GitHub Pages URL**: `https://clavis-note.github.io/`（リダイレクト的な扱い）
- **データストア**: localStorage（`clavis-note-data` キーに全データ）
- **自動バックアップ世代**: `clavis-note-auto-bk-1/2/3`（5分間隔、`app.html` L468-489付近）

## ファイル構成（重要：2026-04-26 構造変更あり）

| ファイル | 役割 |
|---|---|
| `index.html` | **ランディングページ**（紹介・セールス用、約450行） |
| `app.html` | **Clavis Note本体（SPA）**（約8800行）— 編集対象は基本これ |
| `privacy.html` | プライバシーポリシー |
| `terms.html` | 利用規約 |
| `tokushoho.html` | 特定商取引法に基づく表記 |
| `CNAME` | 独自ドメイン指定（`clavis-note.com`） |
| `shinsei_template.xlsx` | 申請書テンプレート（PDFエクスポート用） |

⚠️ **重要**: 2026-04-26 以前の `index.html` (旧Clavis Note本体) は、`app.html` にリネームされた。本体機能を改修する時は **`app.html`** を編集すること。`index.html` を編集すると LP が壊れる。

## デザインシステム（app.html）

- **背景**: `#FAF8F5`（ベージュ）
- **サブ背景**: `#F2F0EB` / `#E8E6E0`
- **アクセント**: `#378ADD`（青）、`#E6F1FB`（淡青背景）、`#185FA5`（濃青文字）
- **テキスト**: `#1a1a1a` / `#666` / `#999`
- CSS変数は `app.html` L14〜 の `:root` を参照

### ランディングページ（index.html）のデザイン

別系統。`Shippori Mincho`（明朝）+ `Noto Sans JP`、ベージュ系（`#f5f4ee`）+ 青アクセント `#378ADD`。本体と色味は近いが別CSS。

## Google Drive連携（app.html）

- **スコープ**: `drive.file`（非センシティブ、審査不要）
- **同期ファイル名**: `clavis-note-sync.json`（Drive上に1ファイル）
- **認証トークン保存先**: localStorage `clavis-google-token`
- **最終同期時刻**: localStorage `clavis-gdrive-last-sync`（ISO文字列、UI表示用）
- **前回UP時のサーバー時刻**: localStorage `clavis-gdrive-last-remote-time`（競合検知用）
- **ローカル最終編集時刻**: localStorage `clavis-note-last-modified`（競合検知用）
- **初回端末判定フラグ**: localStorage `clavis-first-sync-done`（初回confirm用）
- **再認証バナー表示フラグ**: localStorage `clavis-pending-reauth`（401検知時にセット）
- **同期ログ**: localStorage `clavis-sync-log`（最新50件、JSON配列）
- **自動同期**: 実装済み
  - 起動時自動DL（リモートが新しければサイレント取得）
  - 編集5秒後に debounce 自動UP
  - UP前リモートチェック（他端末の更新検知）
  - タブ非表示/閉じる時に保留中UPをフラッシュ
  - 競合検知: ローカル編集あり ∧ リモートも新しい → confirm表示
  - 初回端末: リモート未作成ならローカルをシードUP / リモート有なら必ずconfirm
- **サイレント再認証**: `prompt:'none'` で401時に自動更新試行（ベストエフォート）
- **認証切れバナー**: 画面上部にオレンジ警告（再認証失敗時のUX）
- **手動UP/DL ボタン**: 残存（緊急時用、バックアップパネル内）
- **関連コード（app.html）**:
  - L350〜（スコープ・初期化・refresh・fetchWithAuth）
  - L451〜（logSyncEvent）
  - L8468〜（手動UI handler）
  - L8550〜（auto save + 自動UP debounce）
  - L8580〜（起動時自動DL）
  - L8740〜（visibility flush）
  - 認証切れバナー UI: 本体 return JSX 直下

## 公開ステータス（Google Cloud Console）

- **現状**: 本番環境に公開済み（`drive.file`のみなので審査不要で即反映）
- **掲載URL**:
  - ホームページ: `https://clavis-note.com/`（独自ドメイン）
  - プライバシーポリシー: `https://clavis-note.com/privacy.html`
  - 利用規約: `https://clavis-note.com/terms.html`
  - 承認済みドメイン: `clavis-note.com` および `clavis-note.github.io`
- **トークン長期保持**: テストモード時代の7日失効制限は解除済み
- **ロゴ検証**: 未申請（ロゴ表示は同意画面で省略される・機能影響なし）
- **アクセストークン有効期限**: 1時間（access_tokenのみ取得型のため）→ サイレント再認証で対応

## 機密情報の取り扱い

- 実クライアントの書類(在留カード・パスポート・雇用契約書等)の内容は、
  Claude Code との開発会話で扱ってOK(Anthropicのプライバシーポリシー内)
- ただし以下の用途では**必ずダミーデータ**を使用:
  - SNS投稿、ブログ記事、LP素材
  - 公開用デモ動画、プレゼン資料
  - ポートフォリオや実績紹介
  - テスター以外への共有
- スクショを共有する時は「これは内部用か、公開用か」を確認すること

## 作業方針

- UI変更は慎重に、既存デザインを踏襲
- 大規模リファクタより、局所的な修正を優先
- コミットメッセージは日本語OK（既存コミット参照）
- ブランチ運用: `main` が本番、作業用ブランチは `claude/xxx` 系
- **本体改修は `app.html`、LP改修は `index.html`** を編集対象とする

## 進行中の検討事項

（特になし。何か出てきたらここに追記）

## 完了済みの主要機能

- **Google Drive自動同期**（2026-04-23 実装）: 起動時DL + debounce UP + 競合confirm
- **本番公開対応**（2026-04-23）: privacy.html / terms.html 作成・配置、Google Cloud Console本番申請
- **ポイポイ式プレースホルダー値の先勝ちブロック修正**（2026-04-23）: 「未定」等の仮置き値は既存値と見なさない
- **同期安全性強化**（2026-04-23）: 初回端末confirm + UP前remoteチェック + 同期ログ50件
- **Drive サイレント再認証**（2026-04-23）: 401検知時に `prompt:'none'` で自動トークン更新（ベストエフォート）
- **認証切れバナーUX**（2026-04-23）: サイレント再認証失敗時に画面上部オレンジバナー表示
- **モバイル給与フォーム縦積み**（2026-04-23）: 月給/時給入力欄が潰れるバグ修正
- **日付入力 1950上書き修正**（2026-04-23）: sanitizeDate の年クランプ削除
- **日付入力 update guard 強化**（2026-04-26）: Android Chrome の date picker と React controlled input の衝突対策。完全な YYYY-MM-DD で年範囲OKの時のみ state 更新
- **ドメイン独自化**（2026-04-26）: `clavis-note.com` をCNAMEで設定、index.html → app.html リネーム、新規LP配置
