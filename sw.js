// Clavis Note Service Worker
// 静的資産のキャッシュ + アップデート検知用。Drive同期等の動的処理には介入しない。

// CACHE_VERSION はデプロイ毎に手動で上げるか、ビルド時置換するのが理想だが、
// 現状は本ファイルのcommit hash相当の文字列を直書き。新版時はここを書き換える。
const CACHE_VERSION = 'v2-2026-05-02-auth-fix';
const CACHE_NAME = 'clavis-note-' + CACHE_VERSION;

// 起動に必要な最小資産（pre-cache）。CDN資産は runtime cache に任せる
// (addAll はひとつでも失敗すると全ロールバックなので最小限に絞る)
const PRE_CACHE = ['/app.html'];

// 以下のオリジン/パスは SW でキャッシュしない（API・認証など動的なもの）
const NO_CACHE_HOSTS = [
  'api.anthropic.com',         // Claude API（ポイポイ式・Docs解析）
  'oauth2.googleapis.com',     // Google OAuth トークン
];
const NO_CACHE_PATH_KEYWORDS = [
  '/drive/v3/files',           // Google Drive API（同期データ取得）
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRE_CACHE))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function shouldBypass(req) {
  if (req.method !== 'GET') return true;
  const url = new URL(req.url);
  if (NO_CACHE_HOSTS.includes(url.hostname)) return true;
  if (NO_CACHE_PATH_KEYWORDS.some((kw) => url.pathname.includes(kw))) return true;
  if (url.protocol === 'chrome-extension:') return true;
  return false;
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (shouldBypass(req)) return;

  // Cache First with network fallback、レスポンス取得時は cache 更新
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetchAndUpdate = fetch(req).then((resp) => {
        // 200 と opaque (no-cors) のみキャッシュ
        if (resp && (resp.status === 200 || resp.type === 'opaque')) {
          const respClone = resp.clone();
          caches.open(CACHE_NAME).then((c) => c.put(req, respClone)).catch(() => {});
        }
        return resp;
      }).catch(() => cached);
      return cached || fetchAndUpdate;
    })
  );
});

// page から SKIP_WAITING を受け取ったら即 activate
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
