import json

with open("data/processed/canonical_map.json", encoding="utf-8") as f:
    canonical = json.load(f)

high_stability = {
    k: v for k, v in canonical.items()
    if v["consistency_score"] >= 0.95
}

mid_stability = {
    k: v for k, v in canonical.items()
    if 0.9 <= v["consistency_score"] < 0.95
}

low_stability = {
    k: v for k, v in canonical.items()
    if v["consistency_score"] < 0.9
}

print("High stability:", len(high_stability))
print("Mid stability:", len(mid_stability))
print("Low stability:", len(low_stability))

json.dump(high_stability, open("high_stability.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(mid_stability, open("mid_stability.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(low_stability, open("low_stability.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)