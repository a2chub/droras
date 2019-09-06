const fs = require('fs')
const path = require('path')
const express = require('express')
const router = express.Router()

let heatData = JSON.parse(fs.readFileSync(path.resolve(__dirname, 'get_race_data'), 'utf8'))
let currentHeat = 1

router.get('/heat-data', (req, res) => {
  res.json(heatData)
})

router.post('/upload-heat-data', (req, res) => {
  heatData = req.body
  res.json({
    response: 'success'
  })
})

router.get('/current-heat', (req, res) => {
  res.json({
    id: currentHeat
  })
})

router.get('/set-current-heat', (req, res) => {
  currentHeat = req.query.id
  res.json({
    response: 'success'
  })
})

module.exports = router
