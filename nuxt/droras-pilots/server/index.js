const express = require('express')
const bodyParser = require('body-parser')
const consola = require('consola')
const {
  Nuxt,
  Builder
} = require('nuxt')
const app = express()

app.use(bodyParser.urlencoded({
  extended: true
}))
app.use(bodyParser.json())

const config = require('../nuxt.config.js')
const ApiRouter = require('./api')

// Import and Set Nuxt.js options
config.dev = process.env.NODE_ENV !== 'production'

async function start () {
  // Init Nuxt.js
  const nuxt = new Nuxt(config)

  const {
    host,
    port
  } = nuxt.options.server

  // Build only in dev mode
  if (config.dev) {
    const builder = new Builder(nuxt)
    await builder.build()
  } else {
    await nuxt.ready()
  }

  // Listen the server
  const server = app.listen(port, host)
  consola.ready({
    message: `Server listening on http://${host}:${port}`,
    badge: true
  })

  const io = require('socket.io').listen(server)
  io.on('connection', (socket) => {
    console.log(`id: ${socket.id} is connected.`)
  })
  app.use('/api', ApiRouter(io))

  // Give nuxt middleware to express
  app.use(nuxt.render)
}
start()
