#!/usr/bin/env python3
"""Download VIT past year question papers (PYQs) from vhelpcc.com.

Talks directly to the same Wix backend the vhelpcc website uses — no MCP client,
no scraping. This is a self-contained reimplementation of the
vhelpcc-pyq-mcp-server (github.com/ConTresillo/vhelpcc-pyq-mcp-server) api module
with two fixes that the upstream repo does not have:

  1. PDF URLs: upstream resolves wix:document:// to https://usc1.usrfiles.com/...
     which returns HTTP 403. The working CDN is
     https://static.wixstatic.com/ugd/<file_id>.pdf
  2. SSL: this machine sits behind a MITM proxy with a self-signed cert, so
     certificate verification is disabled for the CDN download.

Stdlib only — no pip/uv/httpx required.

Usage:
  python download_pyqs.py --subject BCSE301L --out pyqs \
      --cat "CAT 1" --cat "CAT 2" --year 24-25 --year 25-26
  python download_pyqs.py --subject BCSE301L --list         # just list papers
"""

import argparse
import base64
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://www.vhelpcc.com/_api/cloud-data/v2/items/query"
APP_ID = "b091403a-daac-4232-936a-eef0d11510b9"
COLLECTION = "Jobs1"
DATA_APP_DEF_ID = "e593b0bd-b783-45b8-97c2-873d42aacaf4"
SITE_BASE = "https://www.vhelpcc.com"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "accept": "application/json, text/plain, */*",
    "referer": SITE_BASE + "/",
}

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

_token = None


def _get(url, headers=None, timeout=60, binary=False):
    req = urllib.request.Request(url, headers=headers or HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
        data = resp.read()
    return data if binary else data.decode("utf-8", "replace")


def _fetch_token():
    global _token
    if _token:
        return _token
    sv = json.loads(_get(f"{SITE_BASE}/_api/v1/access-tokens"))["svSession"]
    body = _get(
        f"{SITE_BASE}/_api/v2/dynamicmodel",
        headers={**HEADERS, "Cookie": f"svSession={sv}"},
    )
    _token = json.loads(body)["apps"][DATA_APP_DEF_ID]["instance"]
    return _token


def encode_r(payload):
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def search(subject=None, cat=None, year=None, slot=None, offset=0, limit=100):
    f = {}
    if subject:
        f["jobType"] = subject
    if cat:
        f["jobType1"] = cat
    if year:
        f["order"] = year
    if slot:
        f["slot"] = slot
    payload = {
        "dataCollectionId": COLLECTION,
        "query": {"filter": f, "paging": {"offset": offset, "limit": limit}, "fields": []},
        "referencedItemOptions": [],
        "returnTotalCount": True,
        "environment": "LIVE",
        "appId": APP_ID,
    }
    url = f"{BASE_URL}?.r={encode_r(payload)}"
    return json.loads(_get(url, headers={**HEADERS, "authorization": _fetch_token()}))


def resolve_pdf_url(paper_pdf):
    if isinstance(paper_pdf, str) and paper_pdf.startswith("wix:document://"):
        path = paper_pdf.replace("wix:document://v1/", "")
        # normally the file id is the first path segment, but some records
        # have a stray extra "ugd/" segment before it, so match by pattern
        seg = next((s for s in path.split("/") if re.match(r"^[0-9a-zA-Z]+_[0-9a-f]+\.pdf$", s)), path.split("/")[0])
        file_id = seg.split(".")[0]
        return f"https://static.wixstatic.com/ugd/{file_id}.pdf"
    if isinstance(paper_pdf, dict):
        return paper_pdf.get("url") or paper_pdf.get("src")
    return None


def safe_name(value):
    return re.sub(r"[^\w\-. ]", "_", value or "").strip() or "anon"


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest.stat().st_size
    data = _get(url, binary=True, timeout=120)
    dest.write_bytes(data)
    return len(data)


def fetch_all(subject, cats, years, slots):
    items = []
    offset = 0
    while True:
        data = search(subject=subject, offset=offset, limit=100)
        page = data.get("dataItems", [])
        total = data.get("pagingMetadata", {}).get("total", 0)
        for it in page:
            d = it.get("data", {})
            if cats and d.get("jobType1") not in cats:
                continue
            if years and d.get("order") not in years:
                continue
            if slots and d.get("slot") not in slots:
                continue
            items.append(it)
        if offset + len(page) >= total or not page:
            break
        offset += len(page)
    return items


def main():
    ap = argparse.ArgumentParser(description="Download PYQs from vhelpcc.com")
    ap.add_argument("--subject", required=True, help="course code, e.g. BCSE301L")
    ap.add_argument("--out", default="pyqs", help="output directory (default: pyqs)")
    ap.add_argument("--cat", action="append", choices=["CAT 1", "CAT 2", "FAT"],
                    help="exam type; repeatable, omit for all")
    ap.add_argument("--year", action="append", help="academic year e.g. 24-25; repeatable")
    ap.add_argument("--slot", action="append", help="slot e.g. F2; repeatable")
    ap.add_argument("--list", action="store_true", help="only list matching papers")
    args = ap.parse_args()

    items = fetch_all(args.subject, args.cat, args.year, args.slot)
    if not items:
        print(f"No papers found for {args.subject}", file=sys.stderr)
        return 1

    rows = []
    for it in items:
        d = it.get("data", {})
        rows.append((it["id"], d.get("jobType"), d.get("jobType1"), d.get("order"),
                     d.get("slot"), d.get("title"), d.get("paperPdf")))

    if args.list:
        print(f"{'id':<38} {'cat':<6} {'year':<6} {'slot':<5} uploader")
        for rid, _, cat, year, slot, title, _ in rows:
            print(f"{rid} {cat:<6} {year:<6} {(slot or '-'):<5} {title}")
        return 0

    out = Path(args.out)
    by_cat: dict[str, list] = {"CAT 1": [], "CAT 2": [], "FAT": []}
    for rid, subj, cat, year, slot, title, pdf in rows:
        url = resolve_pdf_url(pdf)
        if not url:
            print(f"SKIP  {cat} {year} {slot} ({title}): no PDF attached")
            continue
        base = f"{subj}_{cat.replace(' ', '')}_{year}"
        if slot:
            base += f"_{slot}"
        bucket = by_cat.setdefault(cat, [])
        dup = sum(1 for e in bucket if e[0] == base)
        fn = f"{base}_{safe_name(title)}.pdf" if dup else f"{base}.pdf"
        bucket.append((base, fn))
        dest = (out / cat.replace(" ", "").lower() / fn) if cat in ("CAT 1", "CAT 2") else out / fn
        size = download(url, dest)
        print(f"OK    {cat:<6} {year:<6} {(slot or '-'):<5} {size//1024} KB  {dest}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
