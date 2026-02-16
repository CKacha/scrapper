# scrapper
scrapping a 150 page document sob 

WHAT YOU CAN DO:
1) count how many times each voter voted  
2) filter voters above a minimum number

Also no external libraries needed yippie
Only Python 3.10+

 
---

FILES

scrapper.py
    Reads the HTML file and creates voter_vote_counts.csv

amountvoters.py
    Reads voter_vote_counts.csv and creates a smaller file
    with voters that meet a minimum vote requirement.

---

INPUT

An HTML file exported from Blazer that contains a table with columns like:

id | project_id | voter_id | time_spent_voting_ms | created_at | updated_at | ballot

Example:
vote mj.html

---

Counting votes

Run:

python scrapper.py "vote mj.html"

This creates:
    voter_vote_counts.csv

Additional feature:
    python scrapper.py "vote mj.html" --start 2025-10-14 --end 2025-10-31

This searches for a specific time range of votes!

Formats used:

YYYY-MM-DD  
YYYY-MM-DD HH:MM:SS -0400

---

FILTER VOTING

Choose the minimum number of votes.

Example: keep voters with 12 or more votes.

python amountvoters.py voter_vote_counts.csv 12

This creates:

voters_min_12.csv

---

OUTPUT FORMAT

voter_id,vote_count
6,12
12,16
13,21

---
