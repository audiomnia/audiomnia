#!/usr/bin/env node

var liveServer = require('live-server')

const LOGLEVEL_ERROR = 0
// const LOGLEVEL_SOME = 1
// const LOGLEVEL_LOTS = 2

var params = {
  port: 8080,
  root: './',
  open: false, // open browser?
  ignore: 'scrapers', // comma-separated string
  logLevel: LOGLEVEL_ERROR

  // Mount a directory to a route.
  // mount: [['/components', './node_modules']],
  // file: "./404.html", // File for 404
}
liveServer.start(params)

process.stdout.write('Audiomnia is running at http://localhost:8080')
