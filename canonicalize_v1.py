"""
STATUS: FROZEN (v1)
DATE: 2025-12-18

Purpose:
- Final stabilized logic for transliteration alignment pipeline.
- Do NOT modify this file.
- Any improvements must be done in a new version (v2).

Used outputs:
- aligned_pairs_filtered.json
- aligned_pairs_high_conf.json
- canonical_map.json
"""
import json
from collections import defaultdict, Counter

with open("data/processed/aligned_pairs_high_conf.json", encoding="utf-8") as f:
    high_conf = json.load(f)

groups = defaultdict(list)

for en, hi, score in high_conf:
    groups[en].append((hi, score))

canonical = {}

for en, items in groups.items():
    freq = Counter([hi for hi, _ in items])

    best_hi = max(
        freq,
        key=lambda h: (
            freq[h],
            sum(s for hi, s in items if hi == h)
        )
    )

    total_count = sum(freq.values())
    canonical_count = freq[best_hi]

    avg_score = sum(
        s for hi, s in items if hi == best_hi
    ) / canonical_count

    consistency_score = (canonical_count * avg_score) / total_count
    
    canonical[en] = {
        "canonical": best_hi,
        "variants": sorted(set(h for h, _ in items)),
        "consistency_score": round(consistency_score, 3),
        "frequency": total_count
    }

with open("data/processed/canonical_map.json", "w", encoding="utf-8") as f:
    json.dump(canonical, f, ensure_ascii=False, indent=2)

print("Canonicalization complete")
print("Total canonical entries: ", len(canonical))