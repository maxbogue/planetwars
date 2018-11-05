function gameID () {
  let digits = 'abcdef1234567890';
  let id = randomChoice(digits) + randomChoice(digits) + randomChoice(digits) + randomChoice(digits) + randomChoice(digits);
  return id;
}
function max(ls, key) {
  let pairs = ls.map((v) => [key ? key(v) : v, v]);
  let maxPair = null;
  for (let pair of pairs) {
    if (!maxPair || pair[0] > maxPair[0]) {
      maxPair = pair;
    }
  }
  return maxPair[1];
}

function min(ls, key) {
  let pairs = ls.map((v) => [key ? key(v) : v, v]);
  let minPair = null;
  for (let pair of pairs) {
    if (!minPair || pair[0] < minPair[0]) {
      minPair = pair;
    }
  }
  return minPair[1];
}

function randomChoice(ls) {
  return ls[Math.floor(Math.random() * ls.length)];
}

module.exports = { gameID, max, min, randomChoice };
