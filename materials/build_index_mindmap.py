"""Write window.MINDMAP_DATA into index.html with json.dumps (never string interpolation)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "index.html")
F = ["01-when-work-deserves-a-skill.html", "02-a-description-it-can-find.html", "03-one-job-clear-inputs.html",
     "04-the-skill-routing-bench.html", "05-testing-a-skill-like-code.html", "06-upkeep-overlap-drift-cost.html"]
S = [
    ("When work\ndeserves a skill", "#34D399", ["The three-times rule", "Skill, template, automation", "Progressive disclosure"]),
    ("A description\nit can find", "#34D399", ["What + when", "Trigger phrases", "Do not use for"]),
    ("One job, clear\ninputs, a check", "#FBBF24", ["Inputs and steps", "A built-in self-check", "References on demand"]),
    ("The routing\nbench", "#FB923C", ["Misroutes and misses", "Keyword stuffing", "Near-duplicate twins"]),
    ("Testing a skill\nlike code", "#FB923C", ["Should and should not fire", "Held-out requests", "Regression after edits"]),
    ("Upkeep", "#F87171", ["Overlap and drift", "Context cost", "Retire with a pointer"]),
]
data = {"title": "Your Own\nSkills Library", "centerColor": "#3F4800", "sessions": [
    {"label": l, "href": "courses/" + f, "color": c, "concepts": [{"label": x, "href": "courses/" + f} for x in cs]}
    for f, (l, c, cs) in zip(F, S)]}
html = open(P).read()
block = "<script>\nwindow.MINDMAP_DATA = " + json.dumps(data, indent=1) + ";\n</script>"
html, n = re.subn(r"<script>\nwindow\.MINDMAP_DATA = .*?;\n</script>", lambda m: block, html, flags=re.S)
assert n == 1
open(P, "w").write(html)
print("ok")
