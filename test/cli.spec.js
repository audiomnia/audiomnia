var { spawn } = require('child_process')
const assert = require('assert')

describe('CLI', function () {
  let audiomnia

  before(() => {
    audiomnia = spawn('./cli.js')
  })

  it('starts a thing', (done) => {
    const expected = 'Audiomnia is running at http://localhost:8080'

    audiomnia.stdout.on('data', function (msg) {
      const actual = msg.toString()
      assert.strictEqual(actual, expected)
      done()
    })
  })

  after(() => {
    audiomnia.kill()
  })
})
