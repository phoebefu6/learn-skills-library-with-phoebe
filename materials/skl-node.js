// Runs assets/skl-live.js headlessly in node and prints the canon JSON (the same file the browser runs).
// Usage: node materials/skl-node.js > node.json     node materials/skl-node.js --rows <rung>
var fs = require("fs"), path = require("path");
global.window = {};
global.document = undefined;
eval(fs.readFileSync(path.join(__dirname, "..", "assets", "skl-sample.js"), "utf8"));
eval(fs.readFileSync(path.join(__dirname, "..", "assets", "skl-live.js"), "utf8"));
var E = window.SKL_ENGINE;
if (process.argv[2] === "--rows") {
  var res = E.run(process.argv[3]);
  res.rows.forEach(function (r) { console.log((r.i + 1) + "\t" + r.kind + "\t" + r.expected + "\t" + r.fired + "\t" + r.top.toFixed(2) + "\t" + r.q); });
} else if (process.argv[2] === "--q") {
  // node materials/skl-node.js --q <rung> "request text"   -> fired skill and top three scores
  var ix = E.index(E.libraryFor(process.argv[3])), res = E.route(ix, process.argv[4]);
  var top = res.scores.sort(function (a, b) { return b.score - a.score; }).slice(0, 3);
  console.log("fires: " + res.fired + " | " + top.map(function (t) { return t.id + " " + t.score.toFixed(2); }).join("; "));
} else if (process.argv[2] === "--selftest") {
  console.log(JSON.stringify({ clean: E.selfTest(null), planted: E.selfTest("argmin") }));
} else {
  process.stdout.write(JSON.stringify(E.canon(), null, 1));
}
