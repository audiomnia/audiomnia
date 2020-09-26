const fs = require('fs')

const IPFS = require('ipfs')
const jsonlines = require('jsonlines')
const OrbitDB = require('orbit-db')

const finalize = async (orbitdb) => {
  await orbitdb.disconnect()
  await orbitdb._ipfs.stop()
}

const parseJsonLines = (orbitdb) => {
  return new Promise((resolve, reject) => {
    let itemCount = 0
    const parser = jsonlines.parse()

    orbitdb.docs('audiomnia', { indexBy: 'url' }).then(db => {
      const stream = fs.createReadStream('scrapers/data/macaulaylibrary.jl', {encoding: 'utf8'});
      stream.pipe(parser)

      parser.on('data', async (item) => {
        itemCount++

        await db.put(item)
        itemCount--
        process.stdout.write(`Added: ${item.url}, ${itemCount} left\r`)

        if(itemCount === 0) {
          resolve(orbitdb)
        }
      })
    })
  })
}

IPFS.create()
  .then(OrbitDB.createInstance)
  .then(parseJsonLines)
  .then(finalize)
