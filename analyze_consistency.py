import json
import statistics

with open("data/processed/canonical_map.json", encoding="utf-8") as f:
    canonical = json.load(f)

scores = [
    v["consistency_score"]
    for v in canonical.values()
    if "consistency_score" in v
]

print("Total canonical entries: ", len(scores))
print("Average consistency score: ", round(statistics.mean(scores), 3))
print("Median consistency score: ", round(statistics.median(scores), 3))
print("High consistency entries (≥0.9): ", sum(1 for s in scores if s >= 0.9))
print("Very high consistency (≥0.95): ", sum(1 for s in scores if s >= 0.95))