import json

with open("data/processed/aligned_pairs_filtered.json", encoding = "utf-8") as f:
    filtered = json.load(f)

high_conf = [p for p in filtered if p[2] >= 0.85]
mid_conf = [p for p in filtered if 0.70<= p[2] < 0.85]
low_conf = [p for p in filtered if p[2] < 0.70]

print("Total: ", len(filtered))
print("High confidence: ", len(high_conf))
print("Mid confidence: ", len(mid_conf))
print("Low confidence: ", len(low_conf))

with open("data/processed/aligned_pairs_high_conf.json", "w", encoding="utf-8") as f:
    json.dump(high_conf, f, ensure_ascii=False, indent=2)

with open("data/processed/aligned_pairs_mid_conf.json", "w", encoding="utf-8") as f:
    json.dump(mid_conf, f, ensure_ascii=False, indent=2)

with open("data/processed/aligned_pairs_low_conf.json", "w", encoding="utf-8") as f:
    json.dump(low_conf, f, ensure_ascii=False, indent=2)