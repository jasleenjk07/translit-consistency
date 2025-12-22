import json
import random

with open("data/processed/aligned_pairs_mid_conf.json", encoding="utf-8") as f:
    mid = json.load(f)

print("Total mid-confidence pairs: ", len(mid))
print("\nRandom Samples:")
for p in random.sample(mid, 20):
    print(p)