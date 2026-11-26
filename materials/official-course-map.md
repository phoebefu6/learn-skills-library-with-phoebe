# Official course map - learn-skills-library-with-phoebe ("Your Own Skills Library")

Internal build document. Never link it from an audience page. Written 2026-11-25/26, before any page.

**Re-verify the docs before delivery.** Every vendor fact below was read at source on 2026-11-25. Skills
features change monthly (Claude Code's listing budget and Codex's locations both changed in 2026); re-read
the A-tier pages before teaching from this map.

Evidence tiers: **A** = read at source (official docs, the spec, the paper itself). **R** = reported
(secondary or not read in full); say "reported" on the page. **C** = constructed for teaching (Pemberton &
Thistle, the bench library, its requests and every bench number).

## The question across the course

For each request you send, does it reach the right skill, and what does keeping that true cost?

## Session plan (single track, 6 x 45 min, files courses/01..06)

| # | File | Title (h1 accent in brackets) | Difficulty | Covers |
|---|---|---|---|---|
| 1 | 01-when-work-deserves-a-skill.html | When repeated work deserves a [skill] | green | three-times rule and cost side; skill vs template vs automation vs just asking; anatomy (folder, name, description, instructions, scripts, references); progressive disclosure |
| 2 | 02-a-description-it-can-find.html | A description the assistant [can find] | green | description = router's only evidence; what + when; trigger phrases people really type; "do not use for"; naming schemes; third person vs imperative (contested) |
| 3 | 03-one-job-clear-inputs.html | One job, clear inputs, a [built-in check] | yellow | body structure: purpose, inputs to ask for, steps, output format, self-check; references/scripts one level deep; under 500 lines; degrees of freedom |
| 4 | 04-the-skill-routing-bench.html | The skill-routing [bench] | orange | the bench: ladder, anti-lever, break button, scorecard |
| 5 | 05-testing-a-skill-like-code.html | Testing a skill [like code] | orange | trigger tests (should / should not fire), near-misses, train/validation split, runs per query and trigger rate, golden-output assertions, with vs without baseline, regression after an edit, testing against the passing state |
| 6 | 06-upkeep-overlap-drift-cost.html | Upkeep: overlap, drift, [token cost], retirement | red | overlap audit, description drift, context cost of a growing library, merge, retire with a pointer, an owner per skill; capstone: quarterly library review scored on the bench |

## Running case (C, every time labelled "Constructed Pemberton & Thistle example")

Pemberton & Thistle: an invented four-person research consultancy writing client briefs, market scans and
workshop packs. Running artifact = their skills library:
s1 repeated-work inventory and first three skills -> s2 descriptions rewritten -> s3 one well-structured
skill (main file + reference) -> s4 routing scorecard -> s5 a 12-case trigger test set -> s6 upkeep log and
quarterly review. Invented client names used in requests: Halden Water, Norbury Council, Fenwick, Corvel
Analytics, Brightlane, Ostrander Group; new associate Priya. Never Phoebe's own skills, estate, employers
or clients.

## Verified facts (A unless marked)

### The shared pattern (Agent Skills open format)
- agentskills.io/specification (A): a skill is a directory with, at minimum, a `SKILL.md`; optional
  `scripts/`, `references/`, `assets/`. Frontmatter required: `name` (1-64 chars; lowercase a-z, 0-9 and
  hyphens; not starting or ending with a hyphen; no consecutive hyphens; must match the parent directory
  name) and `description` (1-1024 chars, non-empty, "Describes what the skill does and when to use it").
  Optional: `license`, `compatibility` (max 500 chars), `metadata`, `allowed-tools` (experimental).
- Spec, progressive disclosure (A): metadata ~100 tokens loaded at startup for all skills; instructions
  "< 5000 tokens recommended" loaded when activated; resources as needed. "Keep your main SKILL.md under 500
  lines." Keep file references one level deep from SKILL.md.
- agentskills.io/home (A): format "originally developed by Anthropic, released as an open standard, and has
  been adopted by a growing number of agent products". Three stages: discovery, activation, execution.
- Anthropic engineering post "Equipping agents for the real world with Agent Skills", 16 Oct 2025 (A):
  skills are "organized folders of instructions, scripts, and resources that agents can discover and load
  dynamically"; at startup the agent "pre-loads the name and description of every installed skill into its
  system prompt"; progressive disclosure is "the core design principle"; advice: start with evaluation,
  structure for scale, think from Claude's perspective, iterate with Claude. Dated update: published as an
  open standard.

### Anthropic (Claude) implementation
- platform.claude.com Agent Skills overview (A): Level 1 metadata always loaded, ~100 tokens per skill;
  Level 2 SKILL.md body when triggered, under 5k tokens; Level 3 resources as needed, scripts run and only
  output enters context. "The description is what Claude matches your request against when determining
  whether to trigger the Skill." name: max 64 chars, lowercase/numbers/hyphens, no XML tags, reserved words
  `anthropic`, `claude`. description: max 1,024 chars, no XML tags. Custom skills do not sync across
  surfaces (claude.ai, API, Claude Code are separate). Security: use skills only from trusted sources;
  audit every bundled file; a malicious skill can direct tool use or code that does not match its stated
  purpose.
- Skill authoring best practices (A): "The context window is a public good." "Always write in third
  person" (good: "Processes Excel files and generates reports"). Description used "to choose the right
  Skill from potentially 100+ available Skills". Naming: gerund form suggested (`processing-pdfs`);
  avoid vague names (`helper`, `utils`, `tools`). Keep SKILL.md body under 500 lines; references one level
  deep; table of contents for reference files over 100 lines. Degrees of freedom (high / medium / low).
  Build evaluations first: "Build three scenarios"; checklist says "At least three evaluations created";
  test with Haiku, Sonnet and Opus. Feedback loops: run validator, fix, repeat. Avoid time-sensitive
  info; consistent terminology. "There is not currently a built-in way to run these evaluations" (on that
  page; Claude Code docs now describe plugin evals and skill-creator, below).
- Claude Code skills docs, code.claude.com/docs/en/skills (A): locations enterprise > personal > project
  (same name: enterprise overrides personal, personal overrides project); in a session only descriptions
  load, full content when invoked; invoke directly with `/skill-name`; `disable-model-invocation: true`
  (only you can invoke) and `user-invocable: false`; combined description + when_to_use text truncated at
  1,536 characters in the listing; listing budget scales at 1% of the model's context window, and when it
  overflows descriptions are dropped starting with the least-invoked skills; troubleshooting "not
  triggering": check the description includes keywords users would naturally say; "triggers too often":
  make the description more specific, or `disable-model-invocation: true`. skill-creator plugin does
  should-trigger / should-not-trigger description tuning, blind A/B between versions, benchmark with vs
  without skill.

### OpenAI (Codex / ChatGPT) implementation
- learn.chatgpt.com/docs/build-skills (developers.openai.com/codex/skills redirects there) (A): a skill is
  a directory with a required SKILL.md (`name`, `description`), optional `scripts/`, `references/`,
  `assets/`, `agents/openai.yaml`. Codex starts with each skill's name, description and file path; full
  SKILL.md only when selected. Initial list uses "at most 2% of the model's context window", or 8,000
  characters when the window is unknown; with many skills it shortens descriptions first and may omit
  some with a warning; `skills.max_context_tokens` up to 10,000 tokens. Explicit invocation: `$` or
  `/skills` in CLI/IDE, `@` in ChatGPT; implicit when the task matches the description;
  `allow_implicit_invocation` (default true). Locations: `$CWD/.agents/skills`, parent, repo root,
  `$HOME/.agents/skills`, `/etc/codex/skills`, system (skill-creator, skill-installer). Same-name skills
  are not merged; both can appear. Advice: concise descriptions with clear scope and boundaries; put the
  main use case and trigger words first so matching survives shortening; one job per skill; test prompts
  against the description. Disable with `[[skills.config]]` ... `enabled = false`.
- R: an earlier Codex create-skill page showed `~/.codex/skills`; the docs disagreed with each other in
  search snippets. Teach the current page's locations; say locations differ by version.
- AGENTS.md (agents.md) (A): open plain-Markdown "README for agents", no required fields; stewarded by
  the Agentic AI Foundation under the Linux Foundation; nearest file in the directory tree takes
  precedence; explicit user prompts override. It is ALWAYS-loaded project instruction, not an on-demand
  skill: link learn-codex s3 once in session 3.

### GitHub Copilot implementation
- docs.github.com "About agent skills" (A): "folders of instructions, scripts, and resources that Copilot
  can load when relevant"; follows the open Agent Skills spec; project skills in `.github/skills`,
  `.claude/skills` or `.agents/skills`; personal in `~/.copilot/skills` or `~/.agents/skills`; surfaces
  include Copilot CLI, cloud agent, code review, and agent mode in VS Code, Visual Studio, JetBrains
  (version dependent). The page does not describe the selection mechanism: say so.

### Testing descriptions and outputs (agentskills.io)
- "Optimizing skill descriptions" (A): description "carries the entire burden of triggering"; agents
  often do not consult a skill for simple one-step requests even when it matches. Principles: imperative
  phrasing ("Use this skill when..."), user intent not implementation, "Err on the side of being pushy",
  concise, 1024-char limit. Trigger eval set: about 20 queries, 8-10 should trigger, 8-10 should not;
  most valuable negatives are near-misses. Run each query multiple times (3 to start), trigger rate,
  threshold 0.5. Train ~60% / validation ~40%, fixed split, choose best iteration by validation pass rate;
  avoid adding keywords from failed queries (overfitting); five iterations usually enough; when
  false-triggering, "Add specificity about what the skill does not do".
- "Evaluating skill output quality" (A): test case = prompt + expected output + optional files in
  `evals/evals.json`; start with 2-3 cases; run with skill and without (or previous version as baseline);
  assertions added after the first run; good assertions are verifiable; grading needs concrete evidence;
  benchmark delta = what the skill costs (time, tokens) vs what it buys (pass rate); remove assertions
  that always pass in both configurations.

### Retrieval basics for the stand-in router
- Robertson and Zaragoza (2009), "The Probabilistic Relevance Framework: BM25 and Beyond", Foundations
  and Trends in Information Retrieval 3(4): 333-389 (A, read at source): BM25 saturating tf with soft
  length normalisation B = (1 - b) + b dl/avdl, 0 <= b <= 1; "A common combination would be b = 0.5 and
  k1 = 2. (However, many experiments suggest a somewhat lower value of k1 and a somewhat higher value of
  b.)" We use k1 = 1.2, b = 0.75 (in that direction), with the always-positive idf ln(1 + (N - n + .5)/(n + .5)).

### Contested (teach the disagreement, never resolve)
1. **How many skills before routing degrades.** Vendors design for large libraries: Anthropic's best
   practices speak of choosing "from potentially 100+ available Skills"; both Claude Code (1% of context)
   and Codex (2%, 8,000 chars) cap the listing and start shortening or dropping descriptions as the
   library grows. Against: Gan and Sun, "RAG-MCP" (arXiv 2505.03275, May 2025, A for the abstract):
   with a large MCP tool catalogue in the prompt, tool selection accuracy was 13.62%; retrieving a subset
   first raised it to 43.13% and cut prompt tokens by over 50%. That is MCP tools on a stress benchmark,
   not skills; a third-party summary's per-count curve (85% at 5 tools to 45% at 20) is R, do not quote as
   fact. No published threshold for skills: never print one.
2. **Model routing vs explicit invocation.** Implicit routing is the default in Claude Code and Codex;
   both offer opt-outs (`disable-model-invocation`, `allow_implicit_invocation: false`) and explicit
   calls (`/name`, `$name`). Anthropic's docs put side-effect workflows (deploy) on explicit invocation.
   No source measures which is better overall.
3. **Third person vs imperative descriptions.** Anthropic: "Always write in third person". agentskills.io:
   "Use imperative phrasing" ("Use this skill when..."). Both agree on what + when. Teach both.
4. **"Pushy" vs "do not use for".** agentskills.io says err on the side of pushy; it also says, for
   false-triggers, add what the skill does not do. Anthropic says make it more specific. The bench shows
   both pressures; it cannot say which a real model rewards more.

## Seams (link with absolute https, never reteach)

| Sibling | Link | Used in |
|---|---|---|
| learn-claude-skills (one vendor's catalogue) | https://phoebefu6.github.io/learn-claude-skills-with-phoebe/ | s1 |
| learn-claude s3 "From SOP to skill" | https://phoebefu6.github.io/learn-claude-with-phoebe/courses/03-sop-to-skill.html | s1, s3 |
| learn-codex s3 "AGENTS.md and skills" | https://phoebefu6.github.io/learn-codex-with-phoebe/courses/03-agents-and-skills.html | s3 (once) |
| learn-prompt-engineering | https://phoebefu6.github.io/learn-prompt-engineering-with-phoebe/ | s3 |
| learn-ai-evals | https://phoebefu6.github.io/learn-ai-evals-with-phoebe/ | s5 |
| learn-ai-productivity | https://phoebefu6.github.io/learn-ai-productivity-with-phoebe/ | s1 |
| learn-automation | https://phoebefu6.github.io/learn-automation-with-phoebe/ | s1 |

## Bench canon (C, constructed library; computed by assets/skl-live.js; python == node by value)

Router: BM25 (k1 1.2, b 0.75) over each description; words after "Do not use for" count as evidence
against (weight 1.0) with parenthesised hand-off names ignored; a skill fires only if its score reaches
the firing line 1.2; ties go to the skill listed first. 60 requests: 52 aimed at a skill, 8 "none";
40 tuning, 20 held out. Modelled stand-in: a real assistant routes with a language model.

| Rung | Skills | Right | Wrong skill | No skill fired | Fired on a none | Chars | Worst pair |
|---|---|---|---|---|---|---|---|
| 1 Vague one-liners | 18 | 14 | 3 | 42 | 1 | 247 | survey-analysis + survey-design (3) |
| 2 What + when | 18 | 52 | 1 | 1 | 6 | 3,605 | house-style + invoice-chaser (1) |
| 3 + Do not use for | 18 | 54 | 1 | 2 | 3 | 5,186 | exec-summary + invoice-chaser (1) |
| 4 Split the overlap | 19 | 55 | 1 | 1 | 3 | 5,391 | exec-summary + invoice-chaser (1) |
| 5 Scorecard (rung 4 library) | 19 | held out 18 of 20; tuning 37 of 40 | | | | 5,391 | |
| Trap: keyword-stuff | 19 | 53 | 2 | 0 | 5 | 6,900 | exec-summary + invoice-chaser (1) |
| Break: near-duplicate | 20 | 53 | 3 | 1 | 3 | 5,685 | market-scan + sector-scan (2) |

Word counts: 33, 591, 822, 855, 855, 1,060, 907. Accuracy %: 23.33, 86.67, 90.00, 91.67, 91.67 (held out
90.00), 88.33, 88.33.

Named rows the pages may quote (numbers as the widget prints them, two decimals):
- Vague: "Surveys." is the only description containing "survey", so all three survey-analysis requests
  (#22-24) go to survey-design (score 1.39 each).
- What + when, false fires: #54 "book a meeting room" -> notes-and-interviews 1.24; #56 "translate this
  email into French" -> invoice-chaser 1.24; #57 survey tool -> survey-analysis 1.31; #58 "remind me how
  VLOOKUP works" -> proposal-writer 1.31 ("works" stems to "work", and the proposal description says "new
  work"); #59 birthday message -> proposal-writer 1.33; #60 thank-you email after the offsite ->
  workshop-pack 1.95. Misroute #42 "fix the spelling and tone" -> invoice-chaser 1.24 ("tone"). Miss #15
  "who agreed to do what on yesterday's call?" 0.66.
- + Do not use for: false fires fall 6 -> 3 (#54, #56, #57, #58 stop firing; #53 "what's the time in Singapore" starts firing newsletter at 1.23, because the newsletter description says "when it is time to write" and every score moved when the descriptions grew); new misroute #38 "the board wants the short version of our
  final report" -> invoice-chaser 1.23 ("final", from "final notice"); #42 becomes a miss (0.98).
- Split: #15 now reaches meeting-minutes; right 54 -> 55.
- Stuff: misses 1 -> 0 (#42 reaches house-style at 1.77) but #12 "half-day workshop" -> onboarding-guide
  2.37; false fires 3 -> 5 (#55 news article -> newsletter 1.47, #57 survey tool -> survey-design 2.16);
  characters 5,391 -> 6,900.
- Twin: sector-scan (market-scan copied, one sentence edited, listed first) takes #5 (4.37) and #6 (1.61);
  misroutes 1 -> 3.
- Self-test: property A (counts sum to 60 on every rung) and B (each skill's own what-text routes to
  itself) pass; planted fault (argmin) breaks B on all 19 skills. compare-ladder.py --plant (0.1% on one
  accuracy) reports MISMATCH, exit 1.

## Not covered (honest list)
- Vendor-specific install, upload or sync steps (claude.ai zip upload, Skills API endpoints, plugins,
  marketplaces, `gh skill`): one line each at most, link the vendor docs.
- MCP servers and tool definitions, hooks, subagents: different mechanisms; named once in s1 only.
- How any vendor's model actually ranks skills internally: not published; never claimed.
- Measured routing accuracy of any real assistant: we did not measure one; the bench is a stand-in.
- Security review of third-party skills: one card in s6 from the Anthropic security section, not a
  security course.
- Prompt technique in general (learn-prompt-engineering) and eval methods in general (learn-ai-evals).

## Citation appendix (exact forms for pages)
1. Agent Skills specification, agentskills.io/specification (read 2026-11-25).
2. Agent Skills overview, agentskills.io/home; "Optimizing skill descriptions" and "Evaluating skill output
   quality", agentskills.io/skill-creation (read 2026-11-25).
3. Anthropic, "Equipping agents for the real world with Agent Skills", engineering blog, 16 Oct 2025.
4. Anthropic, "Agent Skills" overview and "Skill authoring best practices", platform.claude.com docs (read
   2026-11-25).
5. Anthropic, "Extend Claude with skills", Claude Code docs, code.claude.com/docs/en/skills (read
   2026-11-25).
6. OpenAI, "Build skills" (Codex and ChatGPT), learn.chatgpt.com/docs/build-skills (read 2026-11-25).
7. AGENTS.md, agents.md (read 2026-11-25).
8. GitHub, "About agent skills", docs.github.com Copilot docs (read 2026-11-25).
9. S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond", Foundations and
   Trends in Information Retrieval 3(4): 333-389, 2009.
10. T. Gan and Q. Sun, "RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented
    Generation", arXiv 2505.03275, May 2025 (abstract read at source).

## Added at verify (2026-11-26, from page-agent reports; all read at source 2026-11-25)
- Anthropic best practices (A): BigQuery example (only the needed reference file loads, others cost zero
  tokens); "Solve, don't defer"; no "voodoo constants" (Ousterhout's law); forward slashes in paths;
  descriptive file names; plan-validate-execute pattern for batch or destructive work. Used in s3.
- agentskills.io "Evaluating skill output quality" (A): "Explain the why" (reasoning-based instructions
  over rigid ALWAYS/NEVER); "Keep the skill lean". Used in s3 and s5.
- Anthropic best practices (A): "Helps with documents" is the vague-description example. Used in s2, s4.
- Build history (C): while the bench was tuned, an early survey-design "Do not use for" line contained the
  word "survey" and penalised its own skill; the shipped lines avoid each skill's own words. Used in s2.
- s5 build-along: 12 new meeting-minutes trigger cases on rung split, 9 of 12 pass (fails #3 1.18, #4
  1.09, #9 false fire 2.27); every score reproduced with materials/skl-node.js --q on 2026-11-26.
- s6: on the twin rung request 6 ties exactly (1.609317 each) and the copy wins by list order.
