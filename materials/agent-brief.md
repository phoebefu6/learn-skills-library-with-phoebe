# Agent brief - shared by every fan-out page of learn-skills-library-with-phoebe

Filled from `~/.claude/skills/course-builder/references/agent-brief.template.md` on 2026-11-26.
Internal build document: never link it from an audience page.

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file, return its path and one
line of coverage. No HTML in your reply.

## Read first, in this order

1. The template page. Copy its structure, classes, SVG grammar and quiz markup EXACTLY, including
   how many options each question has (FOUR options, "A · ...", "B · ...", "C · ...", "D · ..."):
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/courses/01-when-work-deserves-a-skill.html`
   For rhythm and the bench, also read the bench page
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/courses/04-the-skill-routing-bench.html`
2. The source map: every verified fact, its evidence tier (A read at source, R reported, C constructed),
   per-session coverage, the seams, the contested questions and the bench canon. Use ONLY its facts and
   numbers; never invent a statistic; if a fact is missing, teach the uncertainty.
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/materials/official-course-map.md`
3. The stylesheet `:root` block for the palette tokens (first 30 lines):
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/assets/style.css`
4. If your page quotes or uses Pemberton & Thistle's skill descriptions or requests, read them in
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/materials/build_skl_sample.py`
   (fields vague, what, notfor, stuff; REQUESTS with target and tuning/held-out set). Quote them
   verbatim; never invent a description the bench does not have. If your page mounts the try widget, any
   score you quote must be one you computed with
   `node /Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/materials/skl-node.js --rows <rung>`
   (rungs: vague, what, notfor, split, stuff, twin), or for any single request
   `node /Users/phoebe.fu/Documents/claude_work/github_repo/learn-skills-library-with-phoebe/materials/skl-node.js --q <rung> "request text"`
   (prints the skill that fires and the top three scores), or that the course map's canon lists. Do not edit
   anything in assets/ or materials/.

## Page skeleton (keep every component)

toolbar (crumb EXACTLY "learn-skills-library-with-phoebe / Session N of 6" with the repo name linked to
../index.html, #toggle-all, #zoom-toggle) · masthead (eyebrow
"Learn Your Own Skills Library with Phoebe · Session N of 6", h1 with one `<span class="accent">`, .sub,
.chip-row with the level chip given in your outline, the audience chip "Builders and knowledge workers
with too many saved prompts", one more audience chip of your choice, `.chip.time` "45 min", .agenda a1-a4
with flex weights 1/4/5/1) · main.wrap · section#intro (Part 0 "Where we start": kicker, .lede, .legend
pills exactly as in the template, .callout.win "★ What you walk out with tonight.") · 3 Parts, each
`section.section#part-N` with section-kicker (klabel "Part N · covers ...", h2, `.tag.concept "N min
live"`), a `.lede`, ONE figure, `details.card` accordions (summary: `.mode.live` or `.mode.self`, title,
`.mini`, `.caret ▶`), and a `.callout.example` with `span.ex-pill` "Real world" in every Part ·
section#demo-1 Build-along (klabel "Build-along", h2, `.tag.demo "★ 22 min · everyone builds"`, .lede,
ONE figure, `.steps > .step`, each step a `<p>` with any code box BELOW it as `.prompt-box.good` carrying
a `span.label` "★ Step N · ...") then a `.callout.tip` · section#exercise Homework (klabel "Homework", h2
"Before session N+1" (session 6: "After the last session"), `.tag.exercise "30 min"`, ol of 4 items) ·
section#quiz (klabel "Check yourself", h2 "Three questions", the passport line, 3 x `.quiz-q
data-answer="0-based"` with `p.qtext`, four `button.qopt`, `p.qwhy`; vary the correct letter across the
three; one `p.quiz-score` after the last) · section#official, klabel "Sources covered", h2 EXACTLY "What
this session teaches, and where it came from", `.covered > .covered-row` (pill solid ✓ / light ◐ + name +
note), then the `.mono` line EXACTLY "Every fact on this page, and its verification tier, is recorded in
the course's source map." · section.cheat#cheatsheet (h3 "Session N cheat sheet <span>· pin this</span>",
.grid-2 of six .cheat-item with b + span) · `.callout.next` with `.nx-pill` "Next session" (session 6:
`.nx-pill` "Where next" pointing at the sibling courses) · footer.pagefoot · scripts (see below).

Head: copy the template's social meta block with this page's own title/description/url
(`https://phoebefu6.github.io/learn-skills-library-with-phoebe/courses/<file>`, og-image
`.../assets/og-cover.png`); `<title>Session N · <short title> - learn skills library with phoebe</title>`;
`<link rel="stylesheet" href="../assets/style.css?v=1">`. Nothing else external.

Scripts at the end of body: `<script src="../assets/app.js?v=1"></script>`. ONLY a page that mounts the
bench widget also loads, BEFORE app.js, `<script src="../assets/skl-sample.js?v=1"></script>` and
`<script src="../assets/skl-live.js?v=2"></script>`. The try widget markup is
`<div class="skl-bench" data-mode="try" data-rung="what" data-q="a request"></div>`; the full bench is
`<div class="skl-bench" data-mode="full" data-rung="split"></div>`. One widget of each mode per page at most.

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm practitioner
voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines is guidance about
depth, never a target: never collapse whitespace, dissolve a list into a paragraph, or drop a component.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". State the
  professional norm directly with its reason. The two exact estate phrases above are the only
  self-references; "session 5" cross-references are fine.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map or is labelled constructed. For constructed data print "your
  numbers will differ", never invented outputs as if run.
- Contested or missing evidence: teach the disagreement; never resolve what the evidence has not. The
  map lists four contested questions; never print a threshold for how many skills is too many.
- Citations in the exact form of the map's appendix; anything marked R is "reported".
- NEVER "lottery" or "lotteries"; say the mechanism ("decided by list order", "a random draw").
- Default to the English word. No Chinese terms are needed on these pages.
- NO CROSS MARKS anywhere: never ✗ ✘ ✕ ❌ × (not even as a multiplication sign: write "x" or "times").
  Label states in words ("fires", "should not fire", "pass", "fail"). Ticks ✓ appear only in the covered
  rows as in the template.
- Light surfaces only. Never a dark background on anything you add.
- Vendor-neutral: teach the shared pattern, then name where Anthropic, OpenAI (Codex) and GitHub
  Copilot implement it, only with facts the map lists. No product endorsements, no "best tool".
- Titles, widget ids and class names must not collide with siblings. Do not reuse these titles: "Build
  your own skill", "From SOP to skill", "AGENTS.md and skills: your taste, encoded", "Routing decisions
  expire", "Three routing questions". Class prefix `skl-` belongs to the bench engine; your figures use the
  `sNx` prefix below.
- Course-specific: every Part that mentions Pemberton & Thistle labels it "Constructed Pemberton & Thistle
  example" (or "constructed" in the same sentence) at least once. Its clients (Halden Water, Norbury
  Council, Fenwick, Corvel Analytics, Brightlane, Ostrander Group) and associate Priya are invented. Never
  Phoebe's employers, clients, projects or her own skills. Do not use the names Ines, Marlow, Juniper,
  Halyard, Wrenfold, Kittiwake, Wrenfield.
- The bench router is a MODELLED STAND-IN (BM25 keyword scorer) for the language model a real assistant
  uses; say so wherever you show a routing score. Claim only directions from it, never "your assistant
  will score X".
- Seams: link, never reteach (absolute URLs in the map). Prompt technique = learn-prompt-engineering.
  General LLM evaluation = learn-ai-evals. One product's AGENTS.md = learn-codex s3 (link once, s3 only).
  SOP to one skill in Claude = learn-claude s3.

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): #5E6B00 (primary, library olive) · #3F4800 (deep) ·
#677500 (mid) · #D5DC9E (soft) · #F4F6E2 (tint) · #22260F (ink) · #555A40 (muted) · #CDD1B4 (faint) ·
#E6E9D5 (hairline) · #E4B437 (gold: a FILL only, never text; text on it is #22260F) · #7A5800 (gold ink,
text) · #FBF3DA (gold tint) · #FEFEF9 (paper) · `#FFFFFF` · universal reds `#991B1B` `#FEF2F2` `#FCA5A5`
only for a wrong outcome (misroute, miss, false fire, a failing test).

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" xmlns="http://www.w3.org/2000/svg" role="img"
  aria-label="the data, not the shape">` > `<defs>` + `<style>` + content, then
  `<figcaption>🔍 Click to zoom - takeaway</figcaption>`. Grow H, never W.
- Prefix unique per figure, used for every class and id: `s{session}{letter}`, e.g. s2a, s2b, s2c, s2d
  for session 2's four figures (filter `s2aSk`, hatch `s2aHc`, arrow `s2aAr`, classes `.s2aH` ...).
- `<defs>` holds three things with the figure prefix P: a wobble filter `id="PSk"`
  (`feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="<int>"` +
  `feDisplacementMap scale="2.4" xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%"
  width="106%" height="106%"`), a hachure pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one
  #5E6B00 line, opacity .5), an open arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none, #22260F
  stroke 1.6). Omit the hatch or arrow only if unused. ALL shapes sit inside ONE `<g filter="url(#PSk)"
  fill="none" stroke="#22260F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`; rects
  carry a tiny rotation (-4 to 4 degrees for hand-placed items, under 1 for panels). Fills: white,
  #F4F6E2, the hachure for "the pile" or "the data", and #E4B437 ONLY for the one thing the figure is
  about (text on it is #22260F; if a text class is muted, override with style="fill:#22260F"). One doodle
  anchor per figure, simple strokes, never a mascot. Text classes: `.PH` 800 12px #22260F heading · `.PL`
  600 11-12px #22260F label · `.PS` 400 11px #555A40 · `.PA` 700 11px #5E6B00 axis caption · `.PV` 800
  12-16px #3F4800 value · `.PW` 800 12px #FFFFFF on a #5E6B00 or #3F4800 fill only · `.PR` 800 11px
  #991B1B for a wrong outcome · `.PC` code `font: 700 11px ui-monospace, Menlo, monospace` #22260F · `.PN`
  400 12px #555A40 note. Hand-placed items must not overlap as painted rects (the gate flags a pile).
- ALL `<text>` outside the filtered group, sans stack, never below 10.5px.
- Fit: max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px; full-width note under 110 chars;
  40px between neighbouring point labels; bottom note 22px below the last row, H clears it by 8px. No
  line, arrow or curve may cross a label (the scanner flags line-through-text and text-out-of-box); keep
  every label inside its box with 10px padding; keep arrows in the gaps BETWEEN labels. When in doubt,
  shorten.
- Floor: one figure per Part plus one in the build-along (four figures). Draw the MECHANISM (which words
  a description and a request share, where the body and references load, which test case reads which
  output, which two skills claim the same request), never a metaphor, never decoration. Numbers in figures
  come from the map's canon or are labelled constructed.

## Voice and honesty

Every Part gets a real-world story from the map (vendor docs, the spec, the evaluation guides, BM25,
RAG-MCP as contested). Constructed: Pemberton & Thistle, its library, its requests, its test sets, its
upkeep log, and any minutes or counts you invent for it ("your numbers will differ"). Never claim a
measured accuracy for any real assistant.

## Cross-links (absolute URLs)

- learn-claude-skills: https://phoebefu6.github.io/learn-claude-skills-with-phoebe/
- learn-claude s3: https://phoebefu6.github.io/learn-claude-with-phoebe/courses/03-sop-to-skill.html
- learn-codex s3: https://phoebefu6.github.io/learn-codex-with-phoebe/courses/03-agents-and-skills.html
- learn-prompt-engineering: https://phoebefu6.github.io/learn-prompt-engineering-with-phoebe/
- learn-ai-evals: https://phoebefu6.github.io/learn-ai-evals-with-phoebe/
- learn-ai-productivity: https://phoebefu6.github.io/learn-ai-productivity-with-phoebe/
- learn-automation: https://phoebefu6.github.io/learn-automation-with-phoebe/
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chain and session titles

Footer left: "Session N of 6 · learn-skills-library-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>"
Footer right: "<a href="PREV">← Prev: <title></a> &nbsp;·&nbsp; <a href="NEXT">Next: <title> →</a>" (last page:
"← Prev" and `<a href="../index.html">Course home</a>`).

Session titles (exact, sentence case, one accent span in h1) and files:
1. When repeated work deserves a skill · 01-when-work-deserves-a-skill.html
2. A description the assistant can find · 02-a-description-it-can-find.html
3. One job, clear inputs, a built-in check · 03-one-job-clear-inputs.html
4. The skill-routing bench · 04-the-skill-routing-bench.html
5. Testing a skill like code · 05-testing-a-skill-like-code.html
6. Upkeep: overlap, drift, token cost, retirement · 06-upkeep-overlap-drift-cost.html
