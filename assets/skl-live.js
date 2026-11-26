/* skl-live.js - the skill-routing bench for learn-skills-library-with-phoebe.
   A deterministic lexical router (BM25, Robertson and Zaragoza 2009) reads ONLY the skill descriptions
   and routes 60 constructed requests from the Pemberton & Thistle library. It stands in for the
   language model a real assistant uses to pick a skill: same input (names and descriptions), same
   pressures (vague text, overlap, near-duplicates, length), much simpler reader.
   Mirrors materials/skl_reference.py; the two must agree by value (materials/compare-ladder.py).
   Mount: <div class="skl-bench" data-mode="full|try" data-rung="vague"></div>
   Page API: window.SKL_BENCH.setRung(id), .canon(); engine: window.SKL_ENGINE. */
(function () {
  "use strict";
  var S = window.SKL_SAMPLE;
  if (!S) return;
  var R = S.router;
  var STOP = {};
  R.stop.forEach(function (w) { STOP[w] = 1; });

  var RUNGS = [
    ["vague", "1 · Vague one-liners", "combined", "vague", false, false],
    ["what", "2 · What + when", "combined", "what", false, false],
    ["notfor", "3 · + Do not use for", "combined", "what", true, false],
    ["split", "4 · Split the overlap", "split", "what", true, false],
    ["scorecard", "5 · Scorecard", "split", "what", true, false],
    ["stuff", "Keyword-stuff every description", "split", "stuff", true, false],
    ["twin", "Add a near-duplicate skill", "split", "what", true, true]
  ];

  /* ---------- text ---------- */
  function stem(w) {
    var n = w.length;
    if (n > 4 && w.slice(-3) === "ies") return w.slice(0, -3) + "y";
    if (n > 5 && w.slice(-3) === "ing") return w.slice(0, -3);
    if (n > 4 && w.slice(-2) === "ed") return w.slice(0, -2);
    if (n > 3 && w.slice(-1) === "s" && w.slice(-2) !== "ss") return w.slice(0, -1);
    return w;
  }
  function tokens(text) {
    var raw = text.toLowerCase().split(/[^a-z0-9]+/), out = [];
    for (var i = 0; i < raw.length; i++) {
      var w = raw[i];
      if (!w || STOP[w]) continue;
      out.push(stem(w));
    }
    return out;
  }

  /* ---------- library for a rung ---------- */
  function libraryFor(rungId) {
    var rg = rung(rungId), phase = rg[2], field = rg[3], useNot = rg[4], twin = rg[5];
    var lib = [];
    S.skills.forEach(function (s) {
      if (s.phase === "combined" && phase !== "combined") return;
      if (s.phase === "split" && phase !== "split") return;
      lib.push(entry(s, field, useNot));
    });
    if (twin) {
      /* the copy lands next to its original, listed first: on a tie the first listed wins */
      for (var k = 0; k < lib.length; k++) if (lib[k].id === S.twin.twin_of) { lib.splice(k, 0, entry(S.twin, field, useNot)); break; }
    }
    return lib;
  }
  function entry(s, field, useNot) {
    var pos = field === "stuff" ? s.what + " " + s.stuff : s[field];
    var neg = useNot ? s.notfor : "";
    var shown = neg ? pos + " " + neg : pos;
    return { id: s.id, pos: pos, neg: neg, shown: shown };
  }
  function rung(id) {
    for (var i = 0; i < RUNGS.length; i++) if (RUNGS[i][0] === id) return RUNGS[i];
    throw new Error("unknown rung " + id);
  }

  /* ---------- BM25 index over the descriptions ---------- */
  function counts(list) {
    var c = {};
    for (var i = 0; i < list.length; i++) c[list[i]] = (c[list[i]] || 0) + 1;
    return c;
  }
  function index(lib) {
    var docs = lib.map(function (e) {
      var p = tokens(e.pos), n = tokens(e.neg.replace(/\([^)]*\)/g, " "));
      return { id: e.id, tp: counts(p), tn: counts(n), dl: p.length + n.length, all: counts(p.concat(n)) };
    });
    var N = docs.length, df = {}, total = 0;
    docs.forEach(function (d) {
      total += d.dl;
      for (var t in d.all) df[t] = (df[t] || 0) + 1;
    });
    var idf = {};
    for (var t in df) idf[t] = Math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5));
    return { docs: docs, idf: idf, avdl: total / N, N: N };
  }
  function termScore(tf, dl, avdl, w) {
    if (!tf) return 0;
    var B = (1 - R.b) + R.b * dl / avdl;
    var t = tf / B;
    return w * t / (R.k1 + t);
  }
  function scoreAll(ix, query) {
    var q = tokens(query), seen = {}, out = [];
    var uq = [];
    for (var i = 0; i < q.length; i++) if (!seen[q[i]]) { seen[q[i]] = 1; uq.push(q[i]); }
    ix.docs.forEach(function (d) {
      var s = 0;
      for (var j = 0; j < uq.length; j++) {
        var t = uq[j], w = ix.idf[t];
        if (!w) continue;
        s += termScore(d.tp[t], d.dl, ix.avdl, w);
        s -= R.lambda * termScore(d.tn[t], d.dl, ix.avdl, w);
      }
      out.push({ id: d.id, score: s });
    });
    return out;
  }
  function route(ix, query, fault) {
    var sc = scoreAll(ix, query), best = null;
    for (var i = 0; i < sc.length; i++) {
      if (best === null) { best = sc[i]; continue; }
      var better = fault === "argmin" ? sc[i].score < best.score : sc[i].score > best.score;
      if (better) best = sc[i];
    }
    var fired = best && best.score >= R.tau ? best.id : "none";
    return { fired: fired, top: best ? best.score : 0, scores: sc };
  }

  /* ---------- scoring a rung ---------- */
  function expectedFor(target, lib) {
    if (target === "none") return "none";
    for (var i = 0; i < lib.length; i++) if (lib[i].id === target) return target;
    var c = S.combined;
    if (c.accepts.indexOf(target) >= 0) return c.id;
    return target;
  }
  function run(rungId, fault) {
    var lib = libraryFor(rungId), ix = index(lib);
    var rows = S.requests.map(function (r, i) {
      var res = route(ix, r.q, fault), exp = expectedFor(r.target, lib), kind;
      if (exp === "none") kind = res.fired === "none" ? "correct" : "falsefire";
      else if (res.fired === exp) kind = "correct";
      else if (res.fired === "none") kind = "miss";
      else kind = "misroute";
      return { i: i, q: r.q, set: r.set, target: r.target, expected: exp, fired: res.fired, top: res.top, kind: kind };
    });
    return { rung: rungId, lib: lib, rows: rows };
  }
  function tally(rows) {
    var t = { total: rows.length, correct: 0, misroute: 0, miss: 0, falsefire: 0 };
    rows.forEach(function (r) { t[r.kind] += 1; });
    t.accuracy = t.total ? Math.round(10000 * t.correct / t.total) / 100 : 0;
    return t;
  }
  function score(res) {
    var all = tally(res.rows);
    var tune = tally(res.rows.filter(function (r) { return r.set === "t"; }));
    var hold = tally(res.rows.filter(function (r) { return r.set === "h"; }));
    var chars = 0, words = 0;
    res.lib.forEach(function (e) {
      chars += e.shown.length;
      words += e.shown.split(/\s+/).filter(Boolean).length;
    });
    var pairs = {};
    res.rows.forEach(function (r) {
      if (r.kind !== "misroute") return;
      var k = [r.expected, r.fired].sort().join(" + ");
      pairs[k] = (pairs[k] || 0) + 1;
    });
    var worst = "", wn = 0;
    Object.keys(pairs).sort().forEach(function (k) { if (pairs[k] > wn) { wn = pairs[k]; worst = k; } });
    var per = {};
    res.lib.forEach(function (e) { per[e.id] = { should: 0, reached: 0, lost: 0, wrongIn: 0 }; });
    res.rows.forEach(function (r) {
      if (r.expected !== "none" && per[r.expected]) {
        per[r.expected].should += 1;
        if (r.kind === "correct") per[r.expected].reached += 1; else per[r.expected].lost += 1;
      }
      if (r.fired !== "none" && r.kind !== "correct" && per[r.fired]) per[r.fired].wrongIn += 1;
    });
    return { rung: res.rung, skills: res.lib.length, all: all, tune: tune, hold: hold, chars: chars, words: words, worstPair: worst, worstPairCount: wn, perSkill: per };
  }
  function canon() {
    var out = { params: { k1: R.k1, b: R.b, tau: R.tau, lambda: R.lambda }, rungs: {} };
    RUNGS.forEach(function (rg) {
      var res = run(rg[0]), sc = score(res);
      out.rungs[rg[0]] = { fired: res.rows.map(function (r) { return r.fired; }), skills: sc.skills, all: sc.all, tune: sc.tune, hold: sc.hold, chars: sc.chars, words: sc.words, worstPair: sc.worstPair, worstPairCount: sc.worstPairCount };
    });
    return out;
  }

  /* ---------- self-test: a property that must hold, and must FAIL on a planted fault ----------
     Property A: on every rung, correct + misroute + miss + falsefire = 60.
     Property B: a request that is a skill's own "what" text, verbatim, routes to that skill.
     The planted fault (argmin instead of argmax) keeps A true and must break B. */
  function selfTest(fault) {
    var fails = [];
    RUNGS.forEach(function (rg) {
      var t = tally(run(rg[0], fault).rows);
      if (t.correct + t.misroute + t.miss + t.falsefire !== S.requests.length) fails.push("A " + rg[0]);
    });
    var lib = libraryFor("split"), ix = index(lib);
    lib.forEach(function (e) {
      if (route(ix, e.pos, fault).fired !== e.id) fails.push("B " + e.id);
    });
    return { pass: fails.length === 0, fails: fails };
  }

  var ENGINE = { tokens: tokens, stem: stem, libraryFor: libraryFor, index: index, route: route, run: run, score: score, canon: canon, selfTest: selfTest, RUNGS: RUNGS };
  window.SKL_ENGINE = ENGINE;

  /* ---------- widget ---------- */
  if (typeof document === "undefined" || !document.createElement) return;
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  var KIND_LABEL = { correct: "right skill", misroute: "wrong skill", miss: "no skill fired", falsefire: "fired on a none" };
  var WHY = {
    vague: "One-line descriptions share almost no words with what people type, so most requests score under the firing line and nothing fires.",
    what: "Saying what the skill does and when, in the words people use, lets most requests find their skill. The combined notes-and-interviews skill still pulls in neighbours.",
    notfor: "Each \"Do not use for\" line names the neighbour that owns those requests. The stand-in counts words after it as evidence against; a language model reads the negation itself.",
    split: "notes-and-interviews did two jobs. Split into meeting-minutes and interview-synthesis, each description is shorter and sharper.",
    scorecard: "The same library as rung 4, scored separately on the 40 requests used while writing the descriptions and the 20 held back. The held-out number is the honest one.",
    stuff: "Bolting broad words onto every description makes everything match everything: some misses go away, more requests go to the wrong skill, more requests that should fire nothing fire something, and every description gets longer.",
    twin: "sector-scan is market-scan copied with one phrase changed. The router now has two near-identical candidates and the requests split between them."
  };

  function mountFull(root) {
    var state = { rung: root.getAttribute("data-rung") || "vague" };
    root.innerHTML = "";
    var head = el("div", "skl-head");
    head.appendChild(el("h4", null, "The skill-routing bench · Pemberton & Thistle's library (constructed)"));
    root.appendChild(head);
    root.appendChild(el("p", "skl-rail", "Modelled stand-in: a real assistant picks a skill with a language model reading the names and descriptions. This router is a BM25 keyword scorer reading the same descriptions. It shows the same pressures, not the same numbers. The library and the 60 requests are constructed; the routing is computed live in your browser."));
    var presets = el("div", "skl-presets");
    RUNGS.forEach(function (rg) {
      var b = el("button", "skl-preset" + (rg[0] === "stuff" || rg[0] === "twin" ? " skl-trap" : ""), rg[1]);
      b.type = "button";
      b.setAttribute("data-rung", rg[0]);
      b.addEventListener("click", function () { api.setRung(rg[0]); });
      presets.appendChild(b);
    });
    root.appendChild(presets);
    root.appendChild(el("p", "skl-note", "Rungs 1 to 5 climb the ladder. The two dashed buttons are traps: one is the obvious fix that backfires, one breaks the library on purpose."));
    var headline = el("div", "skl-headline");
    root.appendChild(headline);
    var why = el("p", "skl-why");
    root.appendChild(why);
    var tw = el("div", "skl-tablewrap");
    root.appendChild(tw);
    var foot = el("p", "skl-foot");
    root.appendChild(foot);

    function render() {
      var res = run(state.rung), sc = score(res);
      [].forEach.call(presets.children, function (b) { b.classList.toggle("is-on", b.getAttribute("data-rung") === state.rung); });
      headline.innerHTML = "";
      var big = el("div", "skl-big");
      var showHold = state.rung === "scorecard";
      var acc = showHold ? sc.hold : sc.all;
      big.appendChild(el("b", null, acc.correct + " of " + acc.total));
      big.appendChild(el("span", null, showHold ? "held-out requests reach the right outcome (" + sc.tune.correct + " of " + sc.tune.total + " on the tuning set)" : "requests reach the right outcome (" + sc.skills + " skills in the library)"));
      headline.appendChild(big);
      var two = el("div", "skl-two");
      function stat(txt, bad) { two.appendChild(el("span", "skl-stat" + (bad ? " is-bad" : ""), txt)); }
      stat(sc.all.misroute + " wrong skill", sc.all.misroute > 0);
      stat(sc.all.miss + " no skill fired", sc.all.miss > 0);
      stat(sc.all.falsefire + " fired on a none", sc.all.falsefire > 0);
      stat(sc.chars.toLocaleString("en-GB") + " characters of description loaded up front", false);
      headline.appendChild(two);
      if (sc.worstPair) headline.appendChild(el("p", "skl-pair", "Worst-colliding pair: " + sc.worstPair + " (" + sc.worstPairCount + " misroute" + (sc.worstPairCount === 1 ? "" : "s") + ")"));
      why.textContent = WHY[state.rung];

      tw.innerHTML = "";
      var t = el("table", "clean skl-table");
      var hr = el("tr");
      ["#", "Request (constructed)", "Should reach", "Fired", "Top score", "Outcome"].forEach(function (h) { hr.appendChild(el("th", null, h)); });
      t.appendChild(hr);
      res.rows.forEach(function (r) {
        if (state.rung === "scorecard" && r.set !== "h") return;
        var tr = el("tr", "skl-r-" + r.kind);
        tr.appendChild(el("td", "skl-num", String(r.i + 1)));
        tr.appendChild(el("td", "skl-q", r.q));
        tr.appendChild(el("td", "skl-id", r.expected));
        tr.appendChild(el("td", "skl-id", r.fired));
        tr.appendChild(el("td", "skl-num", r.top.toFixed(2)));
        tr.appendChild(el("td", "skl-kind skl-k-" + r.kind, KIND_LABEL[r.kind]));
        t.appendChild(tr);
      });
      tw.appendChild(t);
      var st = selfTest(null), planted = selfTest("argmin");
      foot.textContent = "Firing line: a skill fires only if its score reaches " + R.tau.toFixed(2) + "; below that, no skill fires. BM25 k1 = " + R.k1 + ", b = " + R.b + ". Engine self-test: " + (st.pass ? "pass" : "FAIL") + "; planted fault detected: " + (planted.pass ? "no" : "yes") + ".";
    }
    var api = {
      setRung: function (id) { rung(id); state.rung = id; render(); },
      canon: canon
    };
    render();
    return api;
  }

  function mountTry(root) {
    var state = { rung: root.getAttribute("data-rung") || "what" };
    root.innerHTML = "";
    root.appendChild(el("h4", "skl-head-t", "Try a request against the library (constructed)"));
    root.appendChild(el("p", "skl-rail", "Modelled stand-in: a BM25 keyword router reading only the descriptions, in place of the language model a real assistant uses. Type the way a colleague would."));
    var sel = el("select", "skl-select");
    RUNGS.forEach(function (rg) {
      if (rg[0] === "scorecard") return;
      var o = el("option", null, rg[1]);
      o.value = rg[0];
      if (rg[0] === state.rung) o.selected = true;
      sel.appendChild(o);
    });
    root.appendChild(sel);
    var inp = el("input", "skl-input");
    inp.type = "text";
    inp.value = root.getAttribute("data-q") || "can you write up the minutes from this morning's call";
    inp.setAttribute("aria-label", "A request to route");
    root.appendChild(inp);
    var out = el("div", "skl-tryout");
    root.appendChild(out);
    function render() {
      var lib = libraryFor(state.rung), ix = index(lib), res = route(ix, inp.value);
      var top = res.scores.slice().sort(function (a, b) { return b.score - a.score; }).slice(0, 3);
      out.innerHTML = "";
      out.appendChild(el("p", "skl-fired", res.fired === "none" ? "No skill fires (top score " + res.top.toFixed(2) + " is under the line of " + R.tau.toFixed(2) + ")." : "Fires: " + res.fired + " (score " + res.top.toFixed(2) + ")"));
      var ul = el("ul", "skl-top3");
      top.forEach(function (s) { ul.appendChild(el("li", null, s.id + " · " + s.score.toFixed(2))); });
      out.appendChild(ul);
    }
    sel.addEventListener("change", function () { state.rung = sel.value; render(); });
    inp.addEventListener("input", render);
    render();
    return { setRung: function (id) { state.rung = id; sel.value = id; render(); }, route: function (q) { inp.value = q; render(); return out.textContent; } };
  }

  function boot() {
    var nodes = document.querySelectorAll(".skl-bench");
    for (var i = 0; i < nodes.length; i++) {
      var mode = nodes[i].getAttribute("data-mode");
      var api = mode === "try" ? mountTry(nodes[i]) : mountFull(nodes[i]);
      if (mode === "try") window.SKL_TRY = api; else window.SKL_BENCH = api;
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
