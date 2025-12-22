import json
from collections import Counter
import statistics

with open("data/processed/aligned_pairs_high_conf.json", encoding="utf-8") as f:
    high_conf = json.load(f)

english = [en for en, _, _ in high_conf]
scores = [s for _, _, s in high_conf]

print("Total aligned pairs: ", len(high_conf))
print("Unique English names: ", len(set(english)))
print("Average confidence score: ", round(statistics.mean(scores), 3))
print("Median confidence score: ", round(statistics.median(scores), 3))

print("\n Top 15 most frequent English names: ")
for name, c in Counter(english).most_common(15):
    print(f"{name}: {c}")