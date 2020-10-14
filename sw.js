/* eslint-env worker */

var CACHE_NAME = 'audiomnia-cache-v1'
var staticURLs = [
  '/',
  '/css/audiomnia.css',
  '/js/audiomnia.js',
  '/vendor/ol.css',
  '/vendor/ol.js',
  '/vendor/pako_inflate.min.js',
  '/vendor/querystring.min.js',
  '/data/macaulaylibrary.geojson.gz'
]

const cacheMapTile = async (request) => {
  const cache = await caches.open(CACHE_NAME)
  cache.add(request.url)

  return await fetch(request)
}

const matchMapTile = (url) => url.match(/\/[0-9]+\/[0-9]+\/[0-9]+/)

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(staticURLs)
      })
  )
})

self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        // Cache hit - return response
        if (response) {
          return response
        }

        if (matchMapTile(event.request.url)) {
          return cacheMapTile(event.request)
        }
        return fetch(event.request)
      })
  )
})
