const assign = require('lodash/assign');
const fs = require('fs');
const path = require('path');

const { Fleet, Planet } = require('./dataTypes');

const MAP_DIR = path.join(__dirname, 'maps');
const AI_DIR = path.join(__dirname, 'ai');

function loadMap(mapPath) {
  let planets = [];
  let fleets = [];
  let contents = fs.readFileSync(mapPath, 'utf8');
  let lines = contents.split('\n');
  for (let line of lines) {
    if (line.indexOf('#') >= 0) {
      line = line.slice(0, line.indexOf('#'));
    }
    let tokens = line.split(/\s/);
    if (tokens.length === 0) {
      continue;
    } else if (tokens[0] === 'P') {
      let x = parseFloat(tokens[1]);
      let y = parseFloat(tokens[2]);
      let owner = parseInt(tokens[3]);
      let ships = parseInt(tokens[4]);
      let growth = parseInt(tokens[5]);
      planets.push(new Planet(planets.length, x, y, owner, ships, growth));
    } else if (tokens[0] === 'F') {
      let owner = parseInt(tokens[1]);
      let ships = parseInt(tokens[2]);
      let source = parseInt(tokens[3]);
      let destination = parseInt(tokens[4]);
      let totalTurns = parseInt(tokens[5]);
      let remainingTurns = parseInt(tokens[6]);
      fleets.push(new Fleet(
        owner, ships, source, destination, totalTurns, remainingTurns));
    }
  }
  return [planets, fleets];
}

function loadAllMaps() {
  let maps = {};
  let mapFiles = fs.readdirSync(MAP_DIR);
  for (let mapFile of mapFiles) {
    let mapPath = path.join(MAP_DIR, mapFile);
    let mapName = path.parse(mapPath).name;
    maps[mapName] = loadMap(mapPath);
  }
  return maps;
}

function loadAllAIs() {
  let ais = {};
  let aiFiles = fs.readdirSync(AI_DIR);
  for (let aiFile of aiFiles) {
    let aiPath = path.join(AI_DIR, aiFile);
    let attrs = path.parse(aiPath);
    if (attrs.ext === '.js') {
      assign(ais, require(aiPath));
    }
  }
  return ais;
}

module.exports = { loadAllAIs, loadAllMaps };
