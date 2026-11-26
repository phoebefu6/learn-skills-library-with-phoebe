"""Python reference for the skill-routing bench (assets/skl-live.js).

An independent re-implementation of the same router and scoring, reading the same data file
(assets/skl-sample.js). It must agree with node running the browser engine, by value
(materials/compare-ladder.py). Constructed Pemberton & Thistle example.

    python3 materials/skl_reference.py > py.json
    node materials/skl-node.js > node.json
    python3 materials/compare-ladder.py py.json node.json            # MATCH, exit 0
    python3 materials/compare-ladder.py py.json node.json --plant    # MISMATCH, exit 1 (self-test)
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, "..", "assets", "skl-sample.js")).read()
S = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
R = S["router"]
STOP = set(R["stop"])

RUNGS = [  # id, phase, field, use not-for lines, add twin
    ("vague", "combined", "vague", False, False),
    ("what", "combined", "what", False, False),
    ("notfor", "combined", "what", True, False),
    ("split", "split", "what", True, False),
    ("scorecard", "split", "what", True, False),
    ("stuff", "split", "stuff", True, False),
    ("twin", "split", "what", True, True),
]


def stem(w):
    n = len(w)
    if n > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if n > 5 and w.endswith("ing"):
        return w[:-3]
    if n > 4 and w.endswith("ed"):
        return w[:-2]
    if n > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def tokens(text):
    return [stem(w) for w in re.split(r"[^a-z0-9]+", text.lower()) if w and w not in STOP]


def entry(s, field, use_not):
    pos = s["what"] + " " + s["stuff"] if field == "stuff" else s[field]
    neg = s["notfor"] if use_not else ""
    return {"id": s["id"], "pos": pos, "neg": neg, "shown": pos + " " + neg if neg else pos}


def library(rung):
    _, phase, field, use_not, twin = rung
    lib = []
    for s in S["skills"]:
        p = s.get("phase")
        if (p == "combined" and phase != "combined") or (p == "split" and phase != "split"):
            continue
        lib.append(entry(s, field, use_not))
    if twin:
        k = [e["id"] for e in lib].index(S["twin"]["twin_of"])
        lib.insert(k, entry(S["twin"], field, use_not))  # listed first: ties go to the copy
    return lib


def counter(toks):
    c = {}
    for t in toks:
        c[t] = c.get(t, 0) + 1
    return c


def build_index(lib):
    docs = []
    for e in lib:
        p = tokens(e["pos"])
        n = tokens(re.sub(r"\([^)]*\)", " ", e["neg"]))
        docs.append({"id": e["id"], "tp": counter(p), "tn": counter(n), "dl": len(p) + len(n), "all": set(p + n)})
    N = len(docs)
    df = {}
    for d in docs:
        for t in d["all"]:
            df[t] = df.get(t, 0) + 1
    idf = {t: math.log(1 + (N - c + 0.5) / (c + 0.5)) for t, c in df.items()}
    avdl = sum(d["dl"] for d in docs) / N
    return docs, idf, avdl


def term(tf, dl, avdl, w):
    if not tf:
        return 0.0
    t = tf / ((1 - R["b"]) + R["b"] * dl / avdl)
    return w * t / (R["k1"] + t)


def route(ix, query):
    docs, idf, avdl = ix
    uq = list(dict.fromkeys(tokens(query)))
    best_id, best = None, None
    for d in docs:
        s = 0.0
        for t in uq:
            w = idf.get(t)
            if not w:
                continue
            s += term(d["tp"].get(t, 0), d["dl"], avdl, w)
            s -= R["lambda"] * term(d["tn"].get(t, 0), d["dl"], avdl, w)
        if best is None or s > best:  # strict: ties stay with the first listed
            best_id, best = d["id"], s
    return (best_id if best >= R["tau"] else "none"), best


def expected(target, ids):
    if target == "none" or target in ids:
        return target
    if target in S["combined"]["accepts"]:
        return S["combined"]["id"]
    return target


def tally(rows):
    t = {"total": len(rows), "correct": 0, "misroute": 0, "miss": 0, "falsefire": 0}
    for r in rows:
        t[r["kind"]] += 1
    t["accuracy"] = round(10000 * t["correct"] / t["total"]) / 100 if t["total"] else 0
    return t


def run(rung):
    lib = library(rung)
    ix = build_index(lib)
    ids = [e["id"] for e in lib]
    rows = []
    for r in S["requests"]:
        fired, top = route(ix, r["q"])
        exp = expected(r["target"], ids)
        if exp == "none":
            kind = "correct" if fired == "none" else "falsefire"
        elif fired == exp:
            kind = "correct"
        elif fired == "none":
            kind = "miss"
        else:
            kind = "misroute"
        rows.append({"set": r["set"], "expected": exp, "fired": fired, "kind": kind})
    pairs = {}
    for r in rows:
        if r["kind"] == "misroute":
            k = " + ".join(sorted([r["expected"], r["fired"]]))
            pairs[k] = pairs.get(k, 0) + 1
    worst, wn = "", 0
    for k in sorted(pairs):
        if pairs[k] > wn:
            worst, wn = k, pairs[k]
    return {
        "fired": [r["fired"] for r in rows],
        "skills": len(lib),
        "all": tally(rows),
        "tune": tally([r for r in rows if r["set"] == "t"]),
        "hold": tally([r for r in rows if r["set"] == "h"]),
        "chars": sum(len(e["shown"]) for e in lib),
        "words": sum(len(e["shown"].split()) for e in lib),
        "worstPair": worst,
        "worstPairCount": wn,
    }


def main():
    out = {"params": {"k1": R["k1"], "b": R["b"], "tau": R["tau"], "lambda": R["lambda"]}, "rungs": {}}
    for rg in RUNGS:
        out["rungs"][rg[0]] = run(rg)
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
