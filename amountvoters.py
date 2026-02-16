import csv 
import sys
from pathlib import Path 

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python amountvoters.py <csv_file> <minimum_votes>")
        return 2
    
    in_path = Path(sys.argv[1])
    threshold = int(sys.argv[2])

    if not in_path.exists():
        print(f"File not found: {in_path}")
        return 2
    
    out_path = Path(f"voters_min_{threshold}.csv")

    kept = 0

    with in_path.open("r", encoding="utf-8") as fin, \
        out_path.open("w", newline="", encoding="utf-8") as fout:
        
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=["voter_id", "vote_count"])
        writer.writeheader()

        for row in reader:
            votes = int(row["vote_count"])
            if votes >= threshold:
                writer.writerow(row)
                kept += 1

    print(f"Saved {kept} voters to {out_path}")
    print(f"Voters with >= {threshold} votes: {kept}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())