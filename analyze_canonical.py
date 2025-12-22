import json
import statistics

with open("data/processed/canonical_map.json", encoding="utf-8") as f:
    canonical = json.load(f)

variant_counts = [len(v["variants"]) for v in canonical.values()]

print("Total canonical entries: ", len(canonical))
print("Average variants per name: ", round(statistics.mean(variant_counts)))
print("Median variants per name: ", statistics.median(variant_counts))
print("Max variants for a single name: ", max(variant_counts))