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



if __name__ == "__main__":
    raise(os.system.exit(main()))