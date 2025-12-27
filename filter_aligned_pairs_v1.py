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
from difflib import SequenceMatcher

def similarity(a,b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

COMMON_HINDI = {"और","का","की","के","को","में","से","पर"}

BAD_ENGLISH_HEADS = {
    "india", "state", "asia", "china", "bhavan", "rama", "allah",
    "khan", "sabha", "chairman", "islam", "shiva", "nation", "ministry", "training", "licensing"
}

BAD_ENGLISH_EXTRA = {
    "also", "there", "their", "where", "which",
    "hebrew", "arabic", "islamic", "christian"
}

GENERIC_EN = {
    "survey", "report", "system", "project",
    "study", "development", "history"
}

BAD_HINDI_SEMANTIC = {
    "अल्लाह", "युद्ध", "हारा", "बारे",
    "किरण", "कारण", "अपराधियों", "तिब्बती", "हिंदुइज्मइन",
    "अपराधस्वीकरण", "प्रदूषण", "रावण", "व्रिटेन",
    "उससे", "इसके", "देखते", "प्रसन्न", "वाला", "ईमान"
}

BAD_HINDI_SEMANTIC.update({
    "डाला", "पर्ंतु", "भल्ला", "प्रतिदिन", "जाने", "उमरा", "जमदानी", "करने", "ईधारा"
})

BAD_HINDI_EXTRA = {
    "मेरा", "तेरा", "उसका", "इसका", "बारह", "एक", "दो", "तीन",
    "लाना", "देना", "करना"
}

BAD_HINDI_TRANSLATIONS = {
    "त्रिकोणमिति", "निम्न", "उसने", "चाइल्ड"
}

HONORIFIC_HI = {"श्री", "श्रीमती", "कुमार", "कुमारी", "बाई"} 

def is_bad_hi(hi):
    return len(hi) <= 3 or hi in COMMON_HINDI

def min_sim(en):
    return 0.70 if len(en) <= 5 else 0.60

with open("data/processed/aligned_pairs_full.json", encoding = "utf-8") as f:
    pairs = json.load(f)

filtered = []

for en, hi, score in pairs:
    en_l = en.lower()
    
    if "/" in en or "&" in en:
        continue

    if en_l in GENERIC_EN:
        continue

    if en_l in BAD_ENGLISH_HEADS or en_l in BAD_ENGLISH_EXTRA:
        continue

    if " " in en and len(hi) <= 5:
        continue

    if hi in BAD_HINDI_SEMANTIC or hi in BAD_HINDI_TRANSLATIONS or hi in BAD_HINDI_EXTRA or hi in HONORIFIC_HI:
        continue
    
    if hi.endswith(("ता","पन","त्व","मय","शील")):
        continue
    
    if en_l.endswith(("er", "ion", "ism")) and hi in BAD_HINDI_EXTRA:
        continue

    if len(hi) <= 3 or hi in COMMON_HINDI:
        continue

    if hi in en_l or en_l in hi:
        if abs(len(en) - len(hi)) > 4:
            continue

    if score < min_sim(en):
        continue

    if score < 0.7 and " " not in en and en_l not in BAD_ENGLISH_HEADS:
        continue

    if score < 0.75  and abs(len(hi) - len(en)) > max(4, int(len(en) * 0.6)):
        continue

    # Reject clear semantic plural Hindi nouns
    if hi.endswith(("ें", "ों")) and score < 0.75:  
        continue

    filtered.append((en, hi, score))

print("Before:", len(pairs))
print("After:", len(filtered))

with open("data/processed/aligned_pairs_filtered.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)