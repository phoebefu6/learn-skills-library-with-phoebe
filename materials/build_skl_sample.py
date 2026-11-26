"""Build assets/skl-sample.js: the constructed Pemberton & Thistle skills library and request set.

Constructed Pemberton & Thistle example. Every description and every request below is invented for
teaching; no real firm, person or client is described. Run from the repo root:

    python3 materials/build_skl_sample.py

The output is serialised with json.dumps (never string interpolation), so quoting cannot break it.

Each skill carries four description variants:
  vague   - the one-liner a busy person writes on day one
  what    - says what the skill does AND when to use it, with the phrases people really type
  notfor  - a "Do not use for" line naming the neighbour that owns those requests (added on rung 3)
  stuff   - neighbours' trigger words bolted on to "make it trigger more" (the anti-lever)

The library changes shape on two rungs:
  rung 1-3: one combined skill, notes-and-interviews, does two jobs (meeting minutes AND interview
            synthesis); requests for either job count as correct when they reach it.
  rung 4+ : the combined skill is split into meeting-minutes and interview-synthesis.
  break   : a near-duplicate of market-scan (sector-scan) is added, copied with a small edit.

Requests: 60, each labelled with the job it should reach, or "none". 40 are the tuning set (used
while the descriptions were written) and 20 are held out (only scored on the scorecard rung).
"""
import json, os

SKILLS = [
    {
        "id": "client-brief",
        "vague": "Helps with briefs.",
        "what": "Drafts a two-page client project brief from intake notes: objectives, scope, deliverables, timeline and open questions. Use when a new engagement starts and someone asks for a project brief, a scoping brief or a brief for the client.",
        "notfor": "Do not use for pricing, fees or tenders (proposal-writer) or for condensing a finished report (exec-summary).",
        "stuff": "Also use for proposals, pitches, fees, summaries, reports, meeting notes and any client document.",
    },
    {
        "id": "market-scan",
        "vague": "Research helper.",
        "what": "Runs a desk research scan of a market or sector: market size, main players, growth trends and sources. Use when asked for a market scan, market sizing, a sector overview or the landscape of an industry.",
        "notfor": "Do not use for one named company (competitor-profile) or for academic papers (lit-review).",
        "stuff": "Also use for companies, competitors, profiles, pricing, papers and academic research.",
    },
    {
        "id": "competitor-profile",
        "vague": "Company research.",
        "what": "Writes a one-page profile of one named competitor or company: offer, pricing, positioning, recent news, strengths and weaknesses. Use when someone names a company and asks for a profile, a teardown or what a competitor is doing.",
        "notfor": "Do not use for a whole sector or industry landscape (market-scan).",
        "stuff": "Also use for markets, sectors, industries, landscapes, sizing and research.",
    },
    {
        "id": "workshop-pack",
        "vague": "Workshop stuff.",
        "what": "Builds a workshop pack: agenda, timed exercises, facilitator notes, materials list and a slide outline. Use when preparing to run a workshop, offsite or training session for a client team.",
        "notfor": "Do not use for minutes or actions after the event (meeting-minutes) or for tidying finished decks (slide-polish).",
        "stuff": "Also use for meetings, minutes, notes, decks, slides, team sessions, onboarding and new starters.",
    },
    {
        "id": "notes-and-interviews",
        "vague": "Notes and interviews.",
        "what": "Turns meeting recordings into minutes with decisions and actions, and synthesises stakeholder interview transcripts into themes, quotes and findings. Use for meeting notes, minutes, action items, interview transcripts or a synthesis of interviews.",
        "notfor": "Do not use for questionnaire responses or cross-tabs (survey-analysis) or for preparing exercises (workshop-pack).",
        "stuff": "Also use for surveys, responses, workshops, calls, conversations and summaries.",
        "phase": "combined",
    },
    {
        "id": "meeting-minutes",
        "vague": "Meeting notes.",
        "what": "Turns a meeting recording or rough notes into minutes: attendees, decisions, action items with owners and dates. Use when someone shares a call recording or meeting notes and asks for minutes or actions.",
        "notfor": "Do not use for research transcripts, themes or quotes (interview-synthesis).",
        "stuff": "Also use for interviews, workshops, transcripts, themes, quotes and conversations.",
        "phase": "split",
    },
    {
        "id": "interview-synthesis",
        "vague": "Interview analysis.",
        "what": "Synthesises stakeholder or customer interview transcripts into themes, supporting quotes and findings. Use when there are several research interviews to code, compare or synthesise.",
        "notfor": "Do not use for decisions and action items (meeting-minutes) or questionnaire responses (survey-analysis).",
        "stuff": "Also use for meetings, calls, actions, survey responses, findings and notes.",
        "phase": "split",
    },
    {
        "id": "survey-design",
        "vague": "Surveys.",
        "what": "Drafts a survey questionnaire: question wording, answer scales, routing logic and a pilot checklist. Use when someone needs to write, design or review the questions for a survey before it goes out.",
        "notfor": "Do not use for responses that came back, cross-tabs or charts (survey-analysis), or for comparing tools or software.",
        "stuff": "Also use for survey results, responses, cross-tabs, charts, tools and forms.",
    },
    {
        "id": "survey-analysis",
        "vague": "Data analysis.",
        "what": "Analyses survey results from a CSV or spreadsheet export: response counts, cross-tabs, charts and a findings summary. Use when survey responses are back and need analysing or charting.",
        "notfor": "Do not use for drafting questions or answer scales (survey-design) or for interview transcripts (interview-synthesis).",
        "stuff": "Also use for survey questions, questionnaires, scales, interviews, transcripts and spreadsheets.",
    },
    {
        "id": "proposal-writer",
        "vague": "Sales documents.",
        "what": "Writes a proposal or statement of work for a prospective client: approach, team, timeline, fees and terms. Use when pitching for new work, answering a tender or pricing an engagement.",
        "notfor": "Do not use for scoping a job already won (client-brief).",
        "stuff": "Also use for briefs, scoping, kickoff notes, statements, letters and emails.",
    },
    {
        "id": "invoice-chaser",
        "vague": "Finance emails.",
        "what": "Drafts polite payment reminder emails for overdue invoices, escalating in tone from first nudge to final notice. Use when an invoice is late or a client has not paid.",
        "notfor": "Do not use for hours worked (timesheet-summary), translation or social messages.",
        "stuff": "Also use for timesheets, hours, emails, replies, letters and translation.",
    },
    {
        "id": "slide-polish",
        "vague": "Slides.",
        "what": "Tidies an existing slide deck: one message per title, consistent fonts and charts, house template, speaker notes. Use when a deck is drafted and needs polishing before it goes to a client.",
        "notfor": "Do not use for building a session from scratch (workshop-pack) or for prose copy-editing (house-style).",
        "stuff": "Also use for documents, reports, spelling, copy-editing, workshops and templates.",
    },
    {
        "id": "citation-check",
        "vague": "Checks things.",
        "what": "Checks every number and claim in a draft report against its cited source and flags anything unsourced, stale or misquoted. Use before a report goes out, when someone asks to fact-check, verify sources or check citations.",
        "notfor": "Do not use for spelling, grammar or tone (house-style).",
        "stuff": "Also use for spelling, proofreading, copy-editing, numbers and data.",
    },
    {
        "id": "exec-summary",
        "vague": "Summaries.",
        "what": "Writes a one-page executive summary of a long finished report: the answer first, three findings, the recommendation. Use when a report is done and the client needs a summary for senior readers.",
        "notfor": "Do not use for minutes of a meeting (meeting-minutes), a project brief at kickoff (client-brief) or news articles.",
        "stuff": "Also use for briefs, minutes, articles, news, overviews, notes and kickoff.",
    },
    {
        "id": "house-style",
        "vague": "Writing help.",
        "what": "Copy-edits text into Pemberton & Thistle house style: British spelling, plain words, short sentences, numbered headings, no jargon. Use when someone asks to proofread, copy-edit or put a draft into house style.",
        "notfor": "Do not use for checking facts, figures or sources (citation-check) or for slide layout (slide-polish).",
        "stuff": "Also use for tone, spelling, emails, slides, decks, facts and citations.",
    },
    {
        "id": "newsletter",
        "vague": "Newsletter.",
        "what": "Drafts the monthly client newsletter: three short items from recent work, one chart, upcoming events and a sign-off. Use when it is time to write or plan the monthly newsletter.",
        "notfor": "Do not use for one-off client emails (invoice-chaser).",
        "stuff": "Also use for posts, updates, articles, news, messages and emails.",
    },
    {
        "id": "timesheet-summary",
        "vague": "Time tracking.",
        "what": "Totals weekly timesheets into hours per client and per project, flagging budgets over 80 percent used. Use when someone shares a timesheet export or asks how many hours went to a client.",
        "notfor": "Do not use for chasing unpaid invoices (invoice-chaser).",
        "stuff": "Also use for invoices, overdue payments, budgets and spreadsheets.",
    },
    {
        "id": "lit-review",
        "vague": "Reading.",
        "what": "Writes a literature review of academic papers on a topic: search terms, a table of studies, what they agree on and where they disagree. Use when asked for a literature review, academic evidence or what the research papers say.",
        "notfor": "Do not use for a commercial market or sector scan (market-scan).",
        "stuff": "Also use for markets, sectors, industries, evidence and reading.",
    },
    {
        "id": "data-cleaning",
        "vague": "Spreadsheet help.",
        "what": "Cleans a messy spreadsheet or CSV: fixes dates and duplicates, splits columns, standardises names and logs every change. Use when a data file is messy, has duplicates or will not sort or filter properly.",
        "notfor": "Do not use for analysing survey results (survey-analysis).",
        "stuff": "Also use for survey data, responses, cross-tabs, charts, lookups and formulas.",
    },
    {
        "id": "onboarding-guide",
        "vague": "New starters.",
        "what": "Builds a first-week onboarding plan for a new associate: accounts to set up, people to meet, reading list and a first small project. Use when someone new is joining the team.",
        "notfor": "Do not use for client training sessions or workshops (workshop-pack) or messages to colleagues.",
        "stuff": "Also use for workshops, offsites, training, exercises, team plans, people and schedules.",
    },
]

# The near-duplicate for the break button: market-scan copied, one phrase edited.
TWIN = {
    "id": "sector-scan",
    "twin_of": "market-scan",
    "vague": "Research helper.",
    "what": "Runs a desk research scan of a market or sector: market size, main players, growth trends and sources. Use when asked how big a sector is, for a sector scan, a market map or the landscape of an industry.",
    "notfor": "Do not use for one named company (competitor-profile) or for academic papers (lit-review).",
    "stuff": "Also use for companies, competitors, profiles, pricing, papers and academic research.",
}

# (text, target job, set). target "none" = no skill should fire. set "t" = tuning, "h" = held out.
REQUESTS = [
    # client-brief
    ("We just won the Halden Water job, can you draft the project brief from my intake notes?", "client-brief", "t"),
    ("turn these kickoff notes into a scoping brief for the client", "client-brief", "t"),
    ("New engagement starting Monday - need a brief with objectives, scope and timeline", "client-brief", "h"),
    # market-scan
    ("Can you do a market scan of plant-based dairy in the UK?", "market-scan", "t"),
    ("how big is the market for heat pumps in Ireland and who are the main players", "market-scan", "t"),
    ("give me the landscape of the cybersecurity training industry", "market-scan", "h"),
    # competitor-profile
    ("What is Corvel Analytics doing these days? Profile them for me", "competitor-profile", "t"),
    ("one-pager teardown of Brightlane's pricing and positioning please", "competitor-profile", "t"),
    ("Can you profile Ostrander Group, the competitor that keeps beating us on bids?", "competitor-profile", "h"),
    # workshop-pack
    ("Prepare the pack for next week's strategy offsite: agenda, exercises and facilitator notes", "workshop-pack", "t"),
    ("I'm running a training session for the client's ops team, need exercises and timings", "workshop-pack", "t"),
    ("build me a half-day workshop on prioritisation for 12 people", "workshop-pack", "h"),
    # meeting-minutes (combined skill accepts these on rungs 1-3)
    ("here's the recording from this morning's call, can you write the minutes and actions", "meeting-minutes", "t"),
    ("write up the notes from Tuesday's client workshop: decisions and actions", "meeting-minutes", "t"),
    ("who agreed to do what on yesterday's call? notes attached", "meeting-minutes", "h"),
    # interview-synthesis
    ("I have nine stakeholder interview transcripts, pull out the themes and best quotes", "interview-synthesis", "t"),
    ("synthesise the customer interviews we ran last week into findings", "interview-synthesis", "t"),
    ("compare what the five store managers said in their interviews", "interview-synthesis", "h"),
    # survey-design
    ("Help me write the questions for a member survey about the new pricing", "survey-design", "t"),
    ("review my questionnaire draft, are the answer scales ok?", "survey-design", "t"),
    ("we need to design a short survey for the client's staff before the workshop", "survey-design", "h"),
    # survey-analysis
    ("The survey responses are back (CSV attached), can you do cross-tabs and charts", "survey-analysis", "t"),
    ("the member survey closed with 340 responses, what are the findings?", "survey-analysis", "t"),
    ("chart the survey results by region and give me the headline findings", "survey-analysis", "h"),
    # proposal-writer
    ("We're pitching to Norbury Council, draft the proposal with fees", "proposal-writer", "t"),
    ("help me answer this tender, need approach, team and pricing", "proposal-writer", "t"),
    ("write a statement of work for the six-week discovery phase", "proposal-writer", "h"),
    # invoice-chaser
    ("Fenwick still hasn't paid invoice 2207, it's 45 days late, draft a reminder", "invoice-chaser", "t"),
    ("quick sector overview of UK craft brewing, who is growing?", "market-scan", "t"),
    ("the client hasn't paid us, can you nudge them politely", "invoice-chaser", "h"),
    # slide-polish
    ("This deck goes to the client tomorrow, can you polish it and fix the titles", "slide-polish", "t"),
    ("make my slides consistent with the house template and add speaker notes", "slide-polish", "t"),
    ("tidy up this 30 slide deck before the board sees it", "slide-polish", "h"),
    # citation-check
    ("fact-check the numbers in this report before it goes out", "citation-check", "t"),
    ("check this report before it goes to the client", "citation-check", "t"),
    ("are all these claims actually backed by the sources we cite?", "citation-check", "h"),
    # exec-summary
    ("The final report is 60 pages, write the executive summary for the board", "exec-summary", "t"),
    ("the board wants the short version of our final report", "exec-summary", "t"),
    ("boil the final report down to the answer and three findings for the CEO", "exec-summary", "h"),
    # house-style
    ("proofread this and put it into house style please", "house-style", "t"),
    ("copy-edit my draft: British spelling, shorter sentences", "house-style", "t"),
    ("can you fix the spelling and tone of this paragraph", "house-style", "h"),
    # newsletter
    ("It's time for the monthly newsletter, draft three items from recent work", "newsletter", "t"),
    ("plan this month's client newsletter", "newsletter", "h"),
    # timesheet-summary
    ("how many hours did we spend on the Halden account last month? timesheet export attached", "timesheet-summary", "t"),
    ("summarise this week's timesheets by client and flag budgets over 80 percent", "timesheet-summary", "t"),
    # lit-review
    ("what do the academic papers say about four-day weeks and productivity?", "lit-review", "t"),
    ("I need a literature review on nudges in pension saving", "lit-review", "h"),
    # data-cleaning
    ("this spreadsheet is a mess, dates in three formats and duplicates everywhere", "data-cleaning", "t"),
    ("clean up the contacts CSV so it sorts properly", "data-cleaning", "h"),
    # onboarding-guide
    ("Priya joins the team on Monday as an associate, plan her first week", "onboarding-guide", "t"),
    ("onboarding plan for our new researcher please", "onboarding-guide", "h"),
    # none: nothing in the library should fire
    ("what's the time in Singapore right now?", "none", "t"),
    ("book a meeting room for Thursday at 2", "none", "t"),
    ("summarise this news article for me, just for my own interest", "none", "t"),
    ("translate this email into French", "none", "t"),
    ("which is the better survey tool, Typeform or Google Forms?", "none", "t"),
    ("remind me how VLOOKUP works", "none", "h"),
    ("write a birthday message for a colleague on the team", "none", "h"),
    ("draft a thank-you email to the team after the offsite", "none", "t"),
]

# Router constants, read by BOTH the browser engine and the Python reference. BM25 k1 and b: the review
# (Robertson and Zaragoza 2009, section 3.4) notes experiments favour k1 below 2 and b above 0.5; 1.2 and
# 0.75 are a widely used setting in that range. tau is the firing line; lambda weights "Do not use for".
ROUTER = {
    "k1": 1.2,
    "b": 0.75,
    "tau": 1.2,
    "lambda": 1.0,
    "stop": sorted(set("""a an and are as at be been being but by can could do does did for from get give got
        has have had how i i'm im in into is it it's its just let me my need of on one or our out please so
        than that the their them then there these they this those to up us was we were what when where which
        who will with would you your yes no not any all also should may might must use used using skill
        about after before over some""".split())),
}

# Which skill ids exist on which rung (the split happens on rung 4).
def library(phase):
    out = []
    for s in SKILLS:
        p = s.get("phase")
        if p == "combined" and phase != "combined":
            continue
        if p == "split" and phase != "split":
            continue
        out.append(s["id"])
    return out

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "..", "assets", "skl-sample.js")
    data = {
        "about": "Constructed Pemberton & Thistle example: an invented four-person research consultancy, its skills library and 60 requests labelled with the job each should reach. Built by materials/build_skl_sample.py.",
        "skills": SKILLS,
        "twin": TWIN,
        "requests": [{"q": q, "target": t, "set": st} for (q, t, st) in REQUESTS],
        "router": ROUTER,
        "combined": {"id": "notes-and-interviews", "accepts": ["meeting-minutes", "interview-synthesis"]},
    }
    js = "/* skl-sample.js - generated by materials/build_skl_sample.py with json.dumps. Constructed data. */\nwindow.SKL_SAMPLE = " + json.dumps(data, ensure_ascii=True, indent=0) + ";\n"
    with open(out_path, "w") as f:
        f.write(js)
    n_t = sum(1 for r in REQUESTS if r[2] == "t")
    print("wrote", os.path.normpath(out_path), len(js), "bytes;", len(SKILLS), "skill records;", len(REQUESTS), "requests (", n_t, "tuning,", len(REQUESTS) - n_t, "held out )")

if __name__ == "__main__":
    main()
