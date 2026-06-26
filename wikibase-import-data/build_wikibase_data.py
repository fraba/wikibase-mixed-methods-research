#!/usr/bin/env python3
"""
Build the teaching dataset for the Chapter 6 example
(MP political communication, mixed-methods research with Wikibase).

Single source of truth -> outputs:
  - properties.csv
  - items.csv
  - statements.csv
  - quickstatements_import.txt
This script also runs an internal integrity check.
"""
import csv, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# PROPERTIES  (create these FIRST, in this exact order, on a fresh instance)
# pid is the identifier you WILL get on a fresh Wikibase if created in order.
# ---------------------------------------------------------------------------
PROPERTIES = [
    # pid, label, datatype, description
    ("P1", "instance of", "wikibase-item", "that class of which this item is a particular example and member"),
    ("P2", "subclass of",  "wikibase-item", "this class is a subset (subclass) of that class"),
    ("P3", "has",          "wikibase-item", "generic link from one individual to another (e.g. an MP has a speech)"),
    ("P4", "has transcript","url",          "URL of the MediaWiki page holding the full transcript text"),
    ("P5", "has media file","commonsMedia", "media file (image or video) stored on the wiki and linked to the item"),
    ("P6", "has message",  "string",        "verbatim text of a short social media message"),
    ("P7", "publication date","time",        "date (and time) the item was published or recorded"),
    ("P8", "has sentiment","quantity",      "overall sentiment score from a lexicon-based analysis (-10 to +10)"),
    ("P9", "mentions",     "wikibase-item", "an entity (person or organisation) named in the text of the item"),
]

# ---------------------------------------------------------------------------
# CLASS ITEMS (Q1-Q7) -- 7 classes, mirroring Figure 6.2
# ---------------------------------------------------------------------------
CLASSES = [
    ("Q1", "MP",                    "Member of Parliament"),
    ("Q2", "Speech",                "a speech delivered in a parliamentary debate"),
    ("Q3", "Person",                "a human being"),
    ("Q4", "Social media posting",  "a message published by an MP on a social media platform"),
    ("Q5", "Interview",             "a research interview conducted with an MP"),
    ("Q6", "Organisation",          "a named organisation"),
    ("Q7", "Theme",                 "a theme used to code documents during thematic analysis"),
]

# ---------------------------------------------------------------------------
# INDIVIDUALS (Q8 onward). (qid, label, description, class_qid)
# ---------------------------------------------------------------------------
INDIVIDUALS = [
    # --- MPs (instance of Q1) ---
    ("Q8",  "Margaret Hale",   "Member of Parliament", "Q1"),
    ("Q9",  "David Okonkwo",   "Member of Parliament", "Q1"),
    ("Q10", "Priya Raman",     "Member of Parliament", "Q1"),
    ("Q11", "Tomas Herrera",   "Member of Parliament", "Q1"),
    ("Q12", "Eleanor Whitfield","Member of Parliament","Q1"),
    # --- Speeches (instance of Q2) ---
    ("Q13", "Speech on rural development (Hale)",     "parliamentary speech", "Q2"),
    ("Q14", "Speech on healthcare funding (Okonkwo)", "parliamentary speech", "Q2"),
    ("Q15", "Speech on climate policy (Raman)",       "parliamentary speech", "Q2"),
    ("Q16", "Speech on education reform (Hale)",      "parliamentary speech", "Q2"),
    ("Q17", "Speech on national security (Herrera)",  "parliamentary speech", "Q2"),
    ("Q18", "Speech on housing affordability (Whitfield)","parliamentary speech","Q2"),
    # --- Social media postings (instance of Q4) ---
    ("Q19", "Post by Hale on rural development",       "social media posting", "Q4"),
    ("Q20", "Post by Raman on climate policy",         "social media posting", "Q4"),
    ("Q21", "Post by Okonkwo on healthcare",           "social media posting", "Q4"),
    ("Q22", "Post by Whitfield on housing",            "social media posting", "Q4"),
    ("Q23", "Post by Herrera on national security",    "social media posting", "Q4"),
    # --- Interviews (instance of Q5) ---
    ("Q24", "Interview with Hale",  "research interview", "Q5"),
    ("Q25", "Interview with Raman", "research interview", "Q5"),
    # --- Persons: interviewers (instance of Q3) ---
    ("Q26", "Sarah Lindqvist", "researcher / interviewer", "Q3"),
    ("Q27", "James Pham",      "researcher / interviewer", "Q3"),
    # --- Organisations (instance of Q6) ---
    ("Q28", "National Farmers Federation", "industry organisation", "Q6"),
    ("Q29", "Department of Health",        "government department", "Q6"),
    ("Q30", "Climate Action Coalition",    "advocacy organisation", "Q6"),
    ("Q31", "Housing Australia",           "government agency",     "Q6"),
    # --- Themes (instance of Q7) ---
    ("Q32", "Rural development",   "coding theme", "Q7"),
    ("Q33", "Healthcare",          "coding theme", "Q7"),
    ("Q34", "Climate policy",      "coding theme", "Q7"),
    ("Q35", "Housing affordability","coding theme","Q7"),
    ("Q36", "National security",   "coding theme", "Q7"),
    ("Q37", "Education",           "coding theme", "Q7"),
]

# ---------------------------------------------------------------------------
# STATEMENTS: (subject_qid, pid, value)
# value is a QID for item-valued props, or a literal (string/url/time/quantity)
# Time literals use QuickStatements format: +YYYY-MM-DDT00:00:00Z/11
# ---------------------------------------------------------------------------
WIKI = "https://students.wikibase.example/wiki/"  # placeholder transcript base URL

STATEMENTS = [
    # subclass: MP is a subclass of Person
    ("Q1", "P2", "Q3"),

    # === MP -> Speech (P3 has) ===
    ("Q8",  "P3", "Q13"),
    ("Q8",  "P3", "Q16"),
    ("Q9",  "P3", "Q14"),
    ("Q10", "P3", "Q15"),
    ("Q11", "P3", "Q17"),
    ("Q12", "P3", "Q18"),

    # === MP -> Social media posting (P3 has) ===
    ("Q8",  "P3", "Q19"),
    ("Q10", "P3", "Q20"),
    ("Q9",  "P3", "Q21"),
    ("Q12", "P3", "Q22"),
    ("Q11", "P3", "Q23"),

    # === MP -> Interview (P3 has) ===
    ("Q8",  "P3", "Q24"),
    ("Q10", "P3", "Q25"),

    # === Interviewer (Person) -> Interview (P3 has) ===
    ("Q26", "P3", "Q24"),
    ("Q27", "P3", "Q25"),

    # === Speech -> Theme (P3 has) ===
    ("Q13", "P3", "Q32"),
    ("Q14", "P3", "Q33"),
    ("Q15", "P3", "Q34"),
    ("Q16", "P3", "Q37"),
    ("Q17", "P3", "Q36"),
    ("Q18", "P3", "Q35"),

    # === Posting -> Theme (P3 has) ===
    ("Q19", "P3", "Q32"),
    ("Q20", "P3", "Q34"),
    ("Q21", "P3", "Q33"),
    ("Q22", "P3", "Q35"),
    ("Q23", "P3", "Q36"),

    # === Posting -> mentions Organisation (P9) ===
    ("Q19", "P9", "Q28"),
    ("Q20", "P9", "Q30"),
    ("Q21", "P9", "Q29"),
    ("Q22", "P9", "Q31"),
    ("Q23", "P9", "Q30"),  # also mentions Climate Action Coalition (cross-theme link)

    # === Speech -> mentions Organisation (P9) ===
    ("Q13", "P9", "Q28"),
    ("Q14", "P9", "Q29"),
    ("Q15", "P9", "Q30"),
    ("Q18", "P9", "Q31"),

    # === Transcript URLs (P4) on speeches and interviews ===
    ("Q13", "P4", f'"{WIKI}Transcript:Speech_rural_development_Hale"'),
    ("Q14", "P4", f'"{WIKI}Transcript:Speech_healthcare_Okonkwo"'),
    ("Q15", "P4", f'"{WIKI}Transcript:Speech_climate_Raman"'),
    ("Q16", "P4", f'"{WIKI}Transcript:Speech_education_Hale"'),
    ("Q17", "P4", f'"{WIKI}Transcript:Speech_security_Herrera"'),
    ("Q18", "P4", f'"{WIKI}Transcript:Speech_housing_Whitfield"'),
    ("Q24", "P4", f'"{WIKI}Transcript:Interview_Hale"'),
    ("Q25", "P4", f'"{WIKI}Transcript:Interview_Raman"'),

    # === Media files (P5) -- placeholder file names on the wiki ===
    ("Q19", "P5", '"Post_Hale_rural.jpg"'),
    ("Q20", "P5", '"Post_Raman_climate.jpg"'),
    ("Q24", "P5", '"Interview_Hale.webm"'),
    ("Q25", "P5", '"Interview_Raman.webm"'),

    # === Post messages (P6 string) ===
    ("Q19", "P6", '"Backing our farmers with a fair go on rural infrastructure. #ruraldevelopment"'),
    ("Q20", "P6", '"We cannot wait any longer to act on climate. The science is clear. #climatepolicy"'),
    ("Q21", "P6", '"More funding for hospitals means shorter waiting lists for families. #healthcare"'),
    ("Q22", "P6", '"Every family deserves an affordable home. Time to fix the housing crisis. #housing"'),
    ("Q23", "P6", '"Keeping our nation safe is my first responsibility. #nationalsecurity"'),

    # === Publication dates (P7 time) ===
    ("Q13", "P7", "+2025-03-04T00:00:00Z/11"),
    ("Q14", "P7", "+2025-03-11T00:00:00Z/11"),
    ("Q15", "P7", "+2025-03-18T00:00:00Z/11"),
    ("Q16", "P7", "+2025-04-01T00:00:00Z/11"),
    ("Q17", "P7", "+2025-04-08T00:00:00Z/11"),
    ("Q18", "P7", "+2025-04-15T00:00:00Z/11"),
    ("Q19", "P7", "+2025-03-05T00:00:00Z/11"),
    ("Q20", "P7", "+2025-03-19T00:00:00Z/11"),
    ("Q21", "P7", "+2025-03-12T00:00:00Z/11"),
    ("Q22", "P7", "+2025-04-16T00:00:00Z/11"),
    ("Q23", "P7", "+2025-04-09T00:00:00Z/11"),
    ("Q24", "P7", "+2025-05-06T00:00:00Z/11"),
    ("Q25", "P7", "+2025-05-13T00:00:00Z/11"),

    # === Sentiment scores (P8 quantity, -10..+10) ===
    ("Q13", "P8", "3"),
    ("Q14", "P8", "5"),
    ("Q15", "P8", "-2"),
    ("Q16", "P8", "4"),
    ("Q17", "P8", "-4"),
    ("Q18", "P8", "1"),
    ("Q19", "P8", "6"),
    ("Q20", "P8", "-5"),
    ("Q21", "P8", "7"),
    ("Q22", "P8", "2"),
    ("Q23", "P8", "-3"),
]

# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------
ITEM_LABELS = {q: l for q, l, *_ in CLASSES + [(q, l, d) for q, l, d, c in INDIVIDUALS]}
PROP_DATATYPE = {p: dt for p, l, dt, d in PROPERTIES}
ALL_ITEMS = set(ITEM_LABELS)
ITEM_PROPS = {"P1", "P2", "P3", "P9"}  # wikibase-item valued


def integrity_check():
    errors = []
    qids = [q for q, *_ in CLASSES] + [q for q, *_ in INDIVIDUALS]
    if len(qids) != len(set(qids)):
        errors.append("Duplicate QIDs detected.")
    nums = sorted(int(q[1:]) for q in qids)
    if nums != list(range(1, len(nums) + 1)):
        errors.append(f"QIDs are not a clean 1..N sequence: {nums}")
    pnums = sorted(int(p[1:]) for p, *_ in PROPERTIES)
    if pnums != list(range(1, len(pnums) + 1)):
        errors.append(f"PIDs are not a clean 1..N sequence: {pnums}")
    class_ids = {q for q, *_ in CLASSES}
    for q, l, d, c in INDIVIDUALS:
        if c not in class_ids:
            errors.append(f"{q} ({l}) has unknown class {c}")
    for s, p, v in STATEMENTS:
        if s not in ALL_ITEMS:
            errors.append(f"Statement subject {s} undefined")
        if p not in PROP_DATATYPE:
            errors.append(f"Statement property {p} undefined")
        if p in ITEM_PROPS:
            if v not in ALL_ITEMS:
                errors.append(f"Item-valued statement {s} {p} -> {v}: target undefined")
        else:
            dt = PROP_DATATYPE[p]
            if dt in ("string", "url", "commonsMedia") and not (v.startswith('"') and v.endswith('"')):
                errors.append(f"{s} {p}: expected quoted literal, got {v}")
            if dt == "time" and not v.startswith("+"):
                errors.append(f"{s} {p}: expected time literal, got {v}")
            if dt == "quantity":
                try:
                    float(v)
                except ValueError:
                    errors.append(f"{s} {p}: expected numeric quantity, got {v}")
    referenced = set()
    for s, p, v in STATEMENTS:
        referenced.add(s)
        if p in ITEM_PROPS:
            referenced.add(v)
    for q, l, d, c in INDIVIDUALS:
        if q not in referenced:
            errors.append(f"Orphan individual {q} ({l}) has no statements")
    return errors


def write_properties_csv():
    with open(os.path.join(OUT, "properties.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pid", "label", "datatype", "description"])
        for row in PROPERTIES:
            w.writerow(row)


def write_items_csv():
    with open(os.path.join(OUT, "items.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["qid", "label", "description", "instance_of_or_role"])
        for q, l, d in CLASSES:
            w.writerow([q, l, d, "CLASS"])
        for q, l, d, c in INDIVIDUALS:
            w.writerow([q, l, d, f"{c} ({ITEM_LABELS[c]})"])


def write_statements_csv():
    with open(os.path.join(OUT, "statements.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["subject_qid", "subject_label", "property_pid", "property_label",
                    "value", "value_label_or_literal"])
        plabel = {p: l for p, l, *_ in PROPERTIES}
        for s, p, v in STATEMENTS:
            vlabel = ITEM_LABELS.get(v, v.strip('"')) if p in ITEM_PROPS else v.strip('"')
            w.writerow([s, ITEM_LABELS[s], p, plabel[p], v, vlabel])


def write_quickstatements():
    lines = []
    lines.append("# QuickStatements batch -- Chapter 6 teaching dataset")
    lines.append("# IMPORTANT: create the 9 properties FIRST (see import guide), in order P1..P9,")
    lines.append("# on a FRESH Wikibase instance, so that items below receive IDs Q1..Q37.")
    lines.append("# Paste everything below into QuickStatements (Import commands -> v1 syntax).")
    lines.append("")
    lines.append("##### PHASE 1: create class items Q1-Q7 #####")
    for q, l, d in CLASSES:
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{l}"')
        lines.append(f'LAST\tDen\t"{d}"')
    lines.append("")
    lines.append("##### PHASE 2: create individuals Q8-Q37 with instance-of #####")
    for q, l, d, c in INDIVIDUALS:
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{l}"')
        lines.append(f'LAST\tDen\t"{d}"')
        lines.append(f"LAST\tP1\t{c}")
    lines.append("")
    lines.append("##### PHASE 3: statements (links, dates, sentiment, transcripts, media) #####")
    lines.append("# These reference fixed QIDs, valid only if Phases 1-2 produced Q1..Q37.")
    for s, p, v in STATEMENTS:
        lines.append(f"{s}\t{p}\t{v}")
    with open(os.path.join(OUT, "quickstatements_import.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    errs = integrity_check()
    if errs:
        print("INTEGRITY ERRORS:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    write_properties_csv()
    write_items_csv()
    write_statements_csv()
    write_quickstatements()
    print("OK: integrity check passed.")
    print(f"Properties: {len(PROPERTIES)}")
    print(f"Class items: {len(CLASSES)}")
    print(f"Individuals: {len(INDIVIDUALS)}")
    print(f"Statements: {len(STATEMENTS)}")
    print(f"Total items: {len(CLASSES)+len(INDIVIDUALS)}")
