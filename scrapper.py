from __future__ import annotations
from collections import Counter
from pathlib import Path 

import sys
import csv
import os
import re

TR_OPEN_RE = re.compile()
TR_CLOSE_RE = re.compile()

TD_OPEN_RE = re.compile()
TD_CLOSE_RE = re.compile()

TAG_RE = re.compile()
WS_RE = re.compile()

def clean_text(s: str) -> str:
    s= TAG_RE.sub("", s)
    s = WS_RE.sub(" ", s).strip()
    return s 

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: scrapper.py <html_file>")
        return 2
    
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"{path} aint workin")
        return 2
    

    counts = Counter[str] = Counter()

    in_tr = False
    td_index = -1
    in_td = False
    td_buf: list[str] = []
    row_voter_id: str | None = None 

    rows_seen = 0
    rows_skipped = 0 

    with path.open("r", encoding="utf-8", erros="ignore") as f:
        for line in f:
            if not in_tr and TR_OPEN_RE.search(line):
                in_tr = True 
                td_index = -1
                row_voter_id = None
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
                
            if TR_CLOSE_RE.search(line):
                in_tr = False
                rows_seen += 1

                if row_voter_id and row_voter_id.isdigit():
                    counts[row_voter_id] += 1
                else:
                    rows_skipped += 1
    
    out_csv = Path("voter_vote_counts.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["voter_id", "vote_count"])
        for voter_id, n in sorted(counts.items(), key=lambda kv: (-kv[1], int(kv[0]))):
            w.writerow([voter_id, n])
        
    print("Done")
    print(f"Rows ended (</tr> seen): {rows_seen}")
    print(f"Unique Voter IDs: {len(counts)}")
    print(f"Rows skipped (missing/invalid voter ID): {rows_skipped}")
    print(f"Saved: {out_csv}")
    return 0

if __name__ == "__main__":
    raise(os.system.exit(main()))