# Importing the Chapter 6 dataset into Wikibase

This folder contains a small, teachable dataset that reproduces the example from
**Chapter 6 — "Designing and running collaborative research projects with Wikibase"**:
a mixed-methods study of how Members of Parliament (MPs) communicate across
parliamentary and social-media platforms.

Students import it once, then use it for the interactive part of the session
(browsing the knowledge graph, "What links here", and SPARQL queries).

## What's in the box

| File | What it is |
|---|---|
| `properties.csv` | The 9 properties to create, with datatypes (the ontology's relationships) |
| `items.csv` | All 37 items: 7 classes + 30 individuals (MPs, speeches, posts, interviews, persons, organisations, themes) |
| `statements.csv` | All 77 statements (the links and attributes between items) — the human-readable reference |
| `quickstatements_import.txt` | The bulk-import batch you actually paste into QuickStatements |
| `build_wikibase_data.py` | The generator. Edit it and re-run `python3 build_wikibase_data.py` to regenerate every file from one source |

## The ontology at a glance

Seven classes (`Q1`–`Q7`): **MP**, **Speech**, **Person**, **Social media posting**,
**Interview**, **Organisation**, **Theme**. `MP` is a *subclass of* `Person`.

Nine properties (`P1`–`P9`):

| ID | Label | Datatype | Used for |
|---|---|---|---|
| P1 | instance of | Item | links an individual to its class |
| P2 | subclass of | Item | builds the class hierarchy (MP ⊂ Person) |
| P3 | has | Item | generic link (MP→speech, MP→interview, speech→theme, post→theme…) |
| P4 | has transcript | URL | link to a wiki page holding the full transcript |
| P5 | has media file | Media file | image/video stored on the wiki |
| P6 | has message | String | the text of a short social-media post |
| P7 | publication date | Point in time | when a speech/post/interview happened |
| P8 | has sentiment | Quantity | lexicon-based sentiment score (−10 to +10) |
| P9 | mentions | Item | a person/organisation named in the text |

> **Note on the numbering.** The book uses illustrative IDs that vary between
> figures and SPARQL examples. This dataset uses one **internally consistent**
> scheme so every query below actually runs.

---

## Why order matters (read this first)

Wikibase assigns identifiers **automatically and incrementally**: the first
property you create becomes `P1`, the first item `Q1`, and so on. The
`quickstatements_import.txt` batch refers to fixed IDs (`Q1`…`Q37`, `P1`…`P9`),
so it only produces a correct graph if those IDs come out as expected.

**Therefore each student imports into a _fresh_ Wikibase instance** (the one from
the Chapter 3 / installation-guide setup, before any other items exist), and
**creates the properties in the exact order P1→P9 before running the batch.**

If your instance already contains items or properties, the auto-assigned IDs will
not start at 1 — in that case use the "Plan B" note at the bottom.

---

## Step 1 — Create the 9 properties (in order)

QuickStatements (v1) cannot create *properties* on most installs, so do this part
by hand. For each row in `properties.csv`, in order top to bottom:

1. Go to **Special:NewProperty** (link in the left-hand toolbox, or
   `…/wiki/Special:NewProperty`).
2. Enter the **label** and **description** from `properties.csv`.
3. Set the **Data type** exactly as listed:
   1. *instance of* → **Item**
   2. *subclass of* → **Item**  
   3. *has* → **Item**  
   4. *has transcript* → **URL**
   5. *has media file* → **Media file** (a.k.a. Commons media / local media)
   6. *has message* → **String**
   7. *publication date* → **Point in time**
   8. *has sentiment* → **Quantity**
   9. *mentions* → **Item**  
   
4. Save, and confirm the new ID matches (`instance of` should be **P1**, etc.).

Creating them in this order guarantees `P1`…`P9` line up with the batch file.

## Step 2 — Enable QuickStatements (instructor, once)

QuickStatements talks to your Wikibase over the API. On the standard
`wikibase-docker` / `wbs-deploy` stack it is already available as a separate
container, usually at `http://<your-host>:9191`. If you are using wikibase.cloud 
is instead available here `https://<your-name>.wikibase.cloud/tools/quickstatements`. 

Open it, log in / authorise with a bot or normal account that has edit rights on 
the wiki.


## Step 3 — Run the bulk import

1. Open QuickStatements → **Import commands** (or "New batch").
2. Choose **Version 1** command syntax.
3. Open `quickstatements_import.txt` (available [here](quickstatements_import.txt)), copy **everything below the comment lines**,
   and paste it in.
4. Run the batch and watch it create:
   - **Phase 1** — the 7 class items (`Q1`–`Q7`),
   - **Phase 2** — the 30 individuals (`Q8`–`Q37`) with their `instance of`,
   - **Phase 3** — all 77 statements (links, dates, sentiment, transcripts, media).

When it finishes you have a connected knowledge graph of ~37 items.

**Note:** In my demo on wikibase.cloud, Version 1 didn't work properly - so I 
had to use Version 2 by clicking on **New batch**, copying the command in the text 
field and then clicking **Import V1 commands**.

## Step 4 — Spot-check

Open any MP, e.g. **Margaret Hale (Q8)**. You should see `has` links to two
speeches, a post, and an interview. From a speech, use **"What links here"** to
reverse-navigate back to the MP — exactly the item-to-item exploration described
in the chapter.

---

## SPARQL queries for the interactive part

Open the **Query Service** (`…:8834` or the "SPARQL query service" link or `https://<your-name>.wikibase.cloud/query`). These
are the chapter's queries, adapted to this dataset. If your prefixes differ, hover
the prefix in the editor to confirm it points at your domain.

**1. All MPs and their speeches** (Figure 6.4 example):

```sparql
SELECT ?mp ?mpLabel ?speech ?speechLabel
WHERE {
  ?mp wdt:P1 wd:Q1 .       # ?mp is instance of MP
  ?mp wdt:P3 ?speech .     # ?mp has ?speech
  ?speech wdt:P1 wd:Q2 .   # ?speech is instance of Speech
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

**2. How many posts per theme** (the coding-monitor query from the chapter):

```sparql
SELECT ?theme ?themeLabel (COUNT(?post) AS ?postCount)
WHERE {
  ?post wdt:P1 wd:Q4 .     # ?post is instance of Social media posting
  ?theme wdt:P1 wd:Q7 .    # ?theme is instance of Theme
  ?post wdt:P3 ?theme .    # ?post has ?theme
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?theme ?themeLabel
ORDER BY DESC(?postCount)
```

**3. Average sentiment per MP** (mixing structured + processed data):

```sparql
SELECT ?mpLabel (AVG(?s) AS ?avgSentiment) (COUNT(?doc) AS ?docs)
WHERE {
  ?mp wdt:P1 wd:Q1 .       # ?mp is instance of MP
  ?mp wdt:P3 ?doc .        # ?mp has a document (speech or post)
  ?doc wdt:P8 ?s .         # ?doc has a sentiment score
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?mpLabel
ORDER BY ?avgSentiment
```

**4. Which organisations are mentioned, and where**:

```sparql
SELECT ?orgLabel ?docLabel
WHERE {
  ?doc wdt:P9 ?org .       # ?doc mentions ?org
  ?org wdt:P1 wd:Q6 .      # ?org is instance of Organisation
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?orgLabel
```

**5. Timeline of speeches and posts** (use the "Timeline" / "Scatter" result view):

```sparql
SELECT ?docLabel ?date ?s
WHERE {
  ?doc wdt:P7 ?date .      # ?doc has a publication date
  OPTIONAL { ?doc wdt:P8 ?s . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?date
```

**6. Find orphans** (items with no `instance of`, from Chapter 4) — should return
nothing after a clean import:

```sparql
SELECT ?item ?itemLabel
WHERE {
  ?item rdfs:label ?itemLabel .
  MINUS { ?item wdt:P1 ?class }
  FILTER(LANG(?itemLabel) = "en")
}
```