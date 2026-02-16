from __future__ import annotations
from collections import Counter
from pathlib import Path 
from datetime import datetime, time 

import re
import csv
import argparse

import sys
import os


TR_OPEN_RE = re.compile(r"<tr[^>]*>", re.IGNORECASE)
TR_CLOSE_RE = re.compile(r"</tr\s*>", re.IGNORECASE)

TD_OPEN_RE = re.compile(r"<td[^>]*>", re.IGNORECASE)
TD_CLOSE_RE = re.compile(r"</td\s*>", re.IGNORECASE)

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

CREATED_AT_FMT = "%Y-%m-%d %H:%M:%S %z"

def clean_text(s: str) -> str:
    s= TAG_RE.sub("", s)
    s = WS_RE.sub(" ", s).strip()
    return s 

def parse_start_end(s:str | None, is_end: bool) -> datetime | None:
    if not s:
        return None
    
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        d = datetime.strptime(s, "%Y-%m-%d")
        if is_end:
            return datetime.combine(d.date(), time.max)
        return datetime.combine(d.date(), time.min)
    
    return datetime.strptime(s, CREATED_AT_FMT)

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Count votes per voter_id within a created_at time range from a Blazer HTML export."
    )
    ap.add_argument("html_file", help='Path to the HTML file, e.g. "vote mj.html"')
    ap.add_argument(
        "--start",
        help='Start (inclusive). Use "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS -0400"',
        default=None,
    )
    ap.add_argument(
        "--end",
        help='End (inclusive). Use "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS -0400"',
        default=None,
    )
    ap.add_argument(
        "--out",
        help='Output CSV filename (default: voter_vote_counts.csv)',
        default="voter_vote_counts.csv",
    )
    args = ap.parse_args()

    start_dt = parse_start_end(args.start, is_end=False)
    end_dt = parse_start_end(args.end, is_end=True)

    path = Path(args.html_file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    
    counts: Counter[str] = Counter()

    in_tr = False
    td_index = -1
    in_td = False
    td_buf: list[str] = []

    row_voter_id: str | None = None 
    row_created_at_raw: str | None = None
    
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not in_tr and TR_OPEN_RE.search(line):
                in_tr = True 
                td_index = -1
                row_voter_id = None
                row_created_at_raw = None
                in_td = False
                td_buf.clear()
                continue
            
            if not in_tr:
                continue
            
            if not in_td and TD_OPEN_RE.search(line):
                in_td = True 
                td_index += 1
                td_buf = []
                line = TD_OPEN_RE.sub("", line, count=1)
            
            if in_td:
                td_buf.append(line)

                if TD_CLOSE_RE.search(line):
                    in_td = False
                    cell_html = "".join(td_buf)
                    cell_html = TD_CLOSE_RE.sub("", cell_html)
                    cell_text = clean_text(cell_html)

                    if td_index == 2:
                        row_voter_id = cell_text
                    elif td_index == 4:
                        row_created_at_raw = cell_text
                
            if TR_CLOSE_RE.search(line):
                in_tr = False

                if not row_voter_id or not row_created_at_raw:
                    continue
                if not row_voter_id.isdigit():
                    continue

                try:
                    created_dt = datetime.strptime(row_created_at_raw, CREATED_AT_FMT)
                except ValueError:
                    continue

                if start_dt is not None:
                    sdt = start_dt if start_dt.tzinfo else start_dt.replace(tzinfo=created_dt.tzinfo)
                    if created_dt < sdt:
                        continue
                
                if end_dt is not None:
                    edt = end_dt if end_dt.tzinfo else end_dt.replace(tzinfo=created_dt.tzinfo)
                    if created_dt > edt:
                        continue 

                counts[row_voter_id] += 1

    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["voter_id", "vote_count"])
        for voter_id in sorted(counts.keys(), key=lambda x: int(x)):
            w.writerow([voter_id, counts[voter_id]])
        
    print("Done")
    print(f"Wrote {len(counts):,} voters to {out_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())