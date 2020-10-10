var { spawn } = require('child_process')
const assert = require('assert')
const puppeteer = require('puppeteer')

describe('Rendering and layout', function () {
  let audiomnia, browser, page

  before(async () => {
    audiomnia = spawn('./cli.js')
    browser = await puppeteer.launch()
    page = await browser.newPage()

    // Assert 200 response on page load
    const response = await page.goto('http://localhost:8080')
    assert.strictEqual(response.status(), 200)
  })

  it('renders the full size map', async () => {
    const mapElement = await page.$('#map')
    const mapBoundingBox = await mapElement.boundingBox()

    assert.strictEqual(page.viewport().width, mapBoundingBox.width)
    assert.strictEqual(page.viewport().height, mapBoundingBox.height)
  })

  it('results list starts off invisible and minimized', async () => {
    const result = await page.$eval('#results', elem => {
      return [parseInt(elem.style.opacity, 10), elem.offsetHeight]
    })

    assert.strictEqual(result[0], 0)
    assert.strictEqual(result[1], 0)
  })

  after(async () => {
    await browser.close();
    audiomnia.kill()
  })
})
