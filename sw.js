/* Little Grand Prix service worker: keeps the whole app on the device so it opens without wifi.
   Strategy: answer from the saved copy straight away, then quietly fetch a fresh copy in the
   background when online. A new version of the app therefore shows up the next time it is opened.
   Bump VERSION whenever a file in ASSETS is added, renamed or removed. */
const VERSION = 'lgp-v1';
const ASSETS = [
  './',
  'index.html',
  'manifest.webmanifest',
  'icons/icon.svg',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/apple-touch-icon.png',
  'icons/favicon-32.png',
  'fonts/fredoka.woff2',
  'fonts/nunito.woff2',
  'fonts/andika-regular.woff2',
  'fonts/andika-bold.woff2',
  'fonts/racing-sans-one.woff2',
  'fonts/noto-sans-sc.woff2'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(VERSION)
      .then(cache => cache.addAll(ASSETS.map(a => new Request(a, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Every page visit (with or without index.html or a ?query) uses the one saved copy of the app.
  const home = new URL('./', self.registration.scope).href;
  const key = req.mode === 'navigate' ? home : req;

  event.respondWith(caches.open(VERSION).then(async cache => {
    const saved = await cache.match(key, { ignoreSearch: true });
    const fresh = fetch(req).then(res => {
      if (res.ok && res.type === 'basic') cache.put(key, res.clone());
      return res;
    });
    if (saved) {
      event.waitUntil(fresh.catch(() => {}));
      return saved;
    }
    try {
      return await fresh;
    } catch (err) {
      if (req.mode === 'navigate') {
        const fallback = await cache.match(home);
        if (fallback) return fallback;
      }
      throw err;
    }
  }));
});
