Pipeline Freeze Summary (v1)

- filter_aligned_pairs_v1.py
  → Produces aligned_pairs_filtered.json

- analyze_confidence_v1.py
  → Produces high / mid / low confidence splits

- canonicalize_v1.py
  → Produces canonical_map.json

Freeze rationale:
- Empirically stable
- Linguistically valid
- Noise below acceptable threshold (~5–7%)

All downstream experiments use canonical_map.json only.