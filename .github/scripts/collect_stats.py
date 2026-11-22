#!/usr/bin/env python3
"""First Gold daily stats.

Reads GoatCounter's public visitor-counter endpoints (anonymous visitor counts per
step, nothing else) for yesterday (Asia/Shanghai) and appends one row to a CSV.
Usage: collect_stats.py OUT.csv [YYYY-MM-DD]
"""
import csv, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import date, datetime, timedelta, timezone

SITE = os.environ.get("GOATCOUNTER", "first-gold")
COLUMNS = [
    ("total", "TOTAL"),
    ("step0", "/step-0"), ("step1", "/step-1"), ("step2", "/step-2"),
    ("step3", "/step-3"), ("step4", "/step-4"), ("first_gold", "/first-gold"),
    ("open_params", "打开方式-params"), ("open_hash", "打开方式-hash"),
    ("open_saved", "打开方式-saved"), ("open_blank", "打开方式-blank"),
]
HEADER = ["date"] + [c for c, _ in COLUMNS] + ["total_all_time", "collected_at"]


def count(path, start=None, end=None):
    url = "https://%s.goatcounter.com/counter/%s.json" % (SITE, urllib.parse.quote(path, safe=""))
    if start:
        url += "?start=%s&end=%s" % (start, end)  # end is exclusive
    req = urllib.request.Request(url, headers={"User-Agent": "first-gold-daily-stats"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:  # path had no visits in this range
            return 0
        raise
    return int(re.sub(r"\D", "", str(body.get("count", "0"))) or 0)


def main():
    out = sys.argv[1]
    if len(sys.argv) > 2:
        day = date.fromisoformat(sys.argv[2])
    else:
        day = datetime.now(timezone(timedelta(hours=8))).date() - timedelta(days=1)
    nxt = day + timedelta(days=1)

    rows = []
    if os.path.exists(out):
        with open(out, newline="", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f)]
    if any(r.get("date") == day.isoformat() for r in rows):
        print("already have", day)
        return

    row = {"date": day.isoformat()}
    for col, path in COLUMNS:
        row[col] = count(path, day.isoformat(), nxt.isoformat())
    row["total_all_time"] = count("TOTAL")
    row["collected_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    rows.append(row)
    rows.sort(key=lambda r: r["date"])

    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
