#!/usr/bin/env python3
"""
extract_reviews.py — Build a faculty-review CSV from a WhatsApp group export.

Mines a WhatsApp chat (.zip or exported .txt) for what students say about a set
of faculty, classifies the sentiment, and writes a CSV.

USAGE
  python extract_reviews.py --chat "WhatsApp Chat with X.zip" \
      --faculty programsheet.xlsx --out reviews.csv
  python extract_reviews.py --chat chat.txt --names "KRITHIGA R,KALAIPRIYAN" --out r.csv

FACULTY SOURCES (one of)
  --faculty FILE.xlsx   VIT program-sheet style sheet (auto-detects FACULTY NAME /
                        FACULTY ID / Course title columns; course title is forward-filled)
  --faculty FILE.csv    a CSV with a name column (override with --faculty-col)
  --faculty FILE.txt    one faculty name per line
  --names "A,B,C"       inline comma-separated names

OUTPUT COLUMNS
  faculty_id, faculty_name, course, mentions, recommendation,
  sentiment, traits, confidence, caveat, evidence
"""
import argparse, csv, os, re, sys, zipfile, tempfile

# ------------------------- lexicons -------------------------
NEG_PHRASES = ["don't take","do not take","dont take","never take","avoid","is bad",
    "never gives","won't give","wont give","nightmare","run away","steer clear",
    "horrible","pathetic","worst","stay away","trash","useless","do not opt"]
NEG_WORDS   = ["strict","tough","rude","harsh"]
POS_PHRASES = ["best faculty","good teacher","teaches well","teaches good","ez marks",
    "easy marks","easy sub","gives marks","gives full marks","full marks","free marks",
    "max marks","low class avg","low avg","low average","very lenient","quite lenient",
    "go for","take her","take him","min a grade","provides notes","gives notes",
    "fat correction","chill class","decent marks"]
POS_WORDS   = ["lenient","chill","generous"]
# keyword needed for a message to count as a "review" at all
RELEVANT = re.compile(r"lenien|leni(?!ng)|\bez\b|easy mark|easy sub|gives.*mark|full mark|"
    r"free mark|max mark|good teach|teaches well|teaches good|best faculty|low.{0,6}avg|"
    r"low.{0,6}averag|strict|notes|don.?t take|do not take|avoid|worst|chill|attendance|"
    r"fat|generous|nightmare|tough|marks|grade", re.I)
TRAITS = [
    ("lenient",         re.compile(r"lenien|leni(?!ng)", re.I)),
    ("strict",          re.compile(r"strict|tough|harsh", re.I)),
    ("easy_marks",      re.compile(r"\bez\b|easy mark|free mark|max mark|full mark|gives.*mark|decent mark", re.I)),
    ("low_class_avg",   re.compile(r"low.{0,6}(avg|averag)", re.I)),
    ("good_teaching",   re.compile(r"teaches well|good teacher|best faculty|teaches good", re.I)),
    ("no_S_grade",      re.compile(r"won.?t give s|wont give s|no s grade", re.I)),
    ("chill_low_effort",re.compile(r"chill|doesn.?t come|won.?t take attendance|easy attendance|no attendance", re.I)),
    ("gives_notes",     re.compile(r"provides notes|gives notes|sends notes", re.I)),
]
# common first names that collide across many faculty -> require full-name match + caveat
COMMON = {"sudha","devi","kavitha","monica","radha","kiruthika","saravanan","karthikeyan",
    "senthil","raja","ravi","amutha","padma","brindha","geetha","sandhya","priya",
    "rajalakshmi","malathi","sivakumar","manikandan","sridhar","anand","prakash",
    "indira","rathna","revathi","kumar","mohan","suresh","ganesh","ramesh","deepika"}

# ------------------------- chat loading -------------------------
TS = re.compile(r'^\d{1,2}/\d{1,2}/\d{2,4}, ')
PREFIX = re.compile(r'^\d{1,2}/\d{1,2}/\d{2,4}, [^-]+- ([^:]+: )?')

def load_messages(chat_path):
    txt_path = chat_path
    tmp = None
    if chat_path.lower().endswith(".zip"):
        tmp = tempfile.mkdtemp()
        with zipfile.ZipFile(chat_path) as z:
            cand = [n for n in z.namelist() if n.lower().endswith(".txt")]
            if not cand:
                sys.exit("No .txt found inside the zip.")
            z.extract(cand[0], tmp)
            txt_path = os.path.join(tmp, cand[0])
    raw = open(txt_path, encoding="utf-8", errors="ignore").read().split("\n")
    msgs = []
    for ln in raw:
        if TS.match(ln) or not msgs:
            msgs.append(ln)
        else:                       # continuation of a multi-line message
            msgs[-1] += " " + ln
    cleaned = []
    for m in msgs:
        t = PREFIX.sub("", m).strip()
        if t and "omitted" not in t.lower():
            cleaned.append(t)
    return [(t, t.lower()) for t in cleaned]

# ------------------------- faculty loading -------------------------
def load_faculty(args):
    if args.names:
        return [{"id":"","name":n.strip(),"course":""} for n in args.names.split(",") if n.strip()]
    src = args.faculty
    if not src:
        sys.exit("Provide --faculty FILE or --names \"A,B\".")
    ext = src.lower().rsplit(".",1)[-1]
    out = []
    if ext in ("xlsx","xlsm"):
        try:
            import openpyxl
        except ImportError:
            sys.exit("openpyxl needed for xlsx. pip install openpyxl")
        wb = openpyxl.load_workbook(src, data_only=True)
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            if not rows: continue
            hdr = [str(c).strip().lower() if c else "" for c in rows[0]]
            def col(*names):
                for i,h in enumerate(hdr):
                    if any(n in h for n in names): return i
                return None
            ci_name = col("faculty name"); ci_id = col("faculty id")
            ci_course = col("course title")
            if ci_name is None: continue
            course = ""
            for r in rows[1:]:
                if ci_course is not None and r[ci_course]:
                    course = str(r[ci_course]).split(":")[0].strip()
                nm = r[ci_name]
                if nm and str(nm).strip().lower() != "faculty name":
                    out.append({"id": str(r[ci_id]).strip() if ci_id is not None and r[ci_id] else "",
                                "name": str(nm).strip(), "course": course})
    elif ext == "csv":
        with open(src, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            key = args.faculty_col or next((k for k in rd.fieldnames if "name" in k.lower()), rd.fieldnames[0])
            for row in rd:
                if row.get(key,"").strip():
                    out.append({"id":"","name":row[key].strip(),"course":row.get("course","")})
    else:  # plain txt
        for ln in open(src, encoding="utf-8"):
            if ln.strip(): out.append({"id":"","name":ln.strip(),"course":""})
    # dedupe by name
    seen, uniq = set(), []
    for f in out:
        if f["name"].lower() not in seen:
            seen.add(f["name"].lower()); uniq.append(f)
    return uniq

# ------------------------- analysis -------------------------
def keys_for(name):
    n = re.sub(r"\s+"," ",name).strip().lower()
    parts = [p for p in re.split(r"[ .]+", n) if p]
    distinctive = [p for p in parts if len(p) > 4 and p not in COMMON]
    generic = len(distinctive) == 0
    keys = [n] if generic else list({n, *distinctive})
    return keys, generic

def analyze(fac, messages):
    keys, generic = keys_for(fac["name"])
    pats = [re.compile(r"\b"+re.escape(k)+r"\b") for k in keys]
    hits = []
    for txt, lo in messages:
        if any(p.search(lo) for p in pats) and RELEVANT.search(txt):
            hits.append((txt, lo))
    # directional = clear opinion, not just a "who's best?" list mention
    pos = [h for h in hits if any(x in h[1] for x in POS_PHRASES) or
           any(re.search(r"\b"+w+r"\b",h[1]) for w in POS_WORDS)]
    neg = [h for h in hits if any(x in h[1] for x in NEG_PHRASES) or
           any(re.search(r"\b"+w+r"\b",h[1]) for w in NEG_WORDS)]
    directional = {id(h):h for h in pos+neg}.values()
    traits = sorted({tag for tag,rx in TRAITS for h in hits if rx.search(h[0])})
    if pos and neg:   rec, sent = "Mixed / verify", "Mixed"
    elif pos:         rec, sent = "Take", "Positive"
    elif neg:         rec, sent = "Avoid", "Negative"
    elif hits:        rec, sent = "Insufficient data", "Listed only"
    else:             rec, sent = "No data", "—"
    nd = len(list(directional))
    if generic and nd:        conf = "Low"
    elif nd >= 3:             conf = "High"
    elif nd >= 1:            conf = "Medium"
    else:                    conf = "Low"
    caveat = "common name — may collide with other faculty; verify" if generic and hits else ""
    ev = " | ".join(h[0][:160] for h in list(directional)[:3]) or \
         " | ".join(h[0][:160] for h in hits[:2])
    return {"mentions":len(hits),"recommendation":rec,"sentiment":sent,
            "traits":",".join(traits),"confidence":conf,"caveat":caveat,"evidence":ev}

# ------------------------- main -------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat", required=True, help="WhatsApp export .zip or .txt")
    ap.add_argument("--faculty", help="xlsx / csv / txt faculty source")
    ap.add_argument("--names", help="inline comma-separated names")
    ap.add_argument("--faculty-col", help="name column for csv source")
    ap.add_argument("--out", default="faculty_reviews.csv")
    ap.add_argument("--all", action="store_true", help="include rows with no data")
    args = ap.parse_args()

    messages = load_messages(args.chat)
    faculty  = load_faculty(args)
    rows = []
    for fac in faculty:
        a = analyze(fac, messages)
        if a["mentions"] == 0 and not args.all:
            continue
        rows.append({"faculty_id":fac["id"],"faculty_name":fac["name"],
                     "course":fac["course"], **a})
    order = {"Take":0,"Mixed / verify":1,"Avoid":2,"Insufficient data":3,"No data":4}
    rows.sort(key=lambda r:(r["course"], order.get(r["recommendation"],9), -r["mentions"]))
    cols = ["faculty_id","faculty_name","course","mentions","recommendation",
            "sentiment","traits","confidence","caveat","evidence"]
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"Parsed {len(messages)} messages · {len(faculty)} faculty checked · "
          f"{len(rows)} with reviews → {args.out}")

if __name__ == "__main__":
    main()
