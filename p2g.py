from g2p_en import G2p
import re

import warnings
warnings.filterwarnings("ignore")

g2p = G2p()

CONSONANTS = {
    "B": "ब",
    "BH": "भ",

    "CH": "च",

    "D": "द",
    "DH": "ध",

    "F": "फ",
    "G": "ग",
    "GH": "घ",

    "HH": "ह",
    "JH": "झ",

    "K": "क",
    "KH": "ख",

    "L": "ल",
    "M": "म",
    "N": "न",
    "NG": "ङ",

    "P": "प",
    "PH": "फ",

    "R": "र",
    "S": "स",
    "SH": "श",

    "T": "त",
    "TH": "थ",

    "V": "व",
    "W": "व",
    "Y": "य",
    "Z": "ज",
}

VOWEL_MATRAS = {
    "AA": "ा",
    "AE": "ै",
    "AH": "अ",   # schwa fallback
    "AO": "ो",
    "EH": "े",
    "IH": "ि",
    "IY": "ी",
    "UH": "ु",
    "UW": "ू",
    "OW": "ो"
}

FULL_VOWELS = {
    "AA": "आ",
    "AE": "ऐ",
    "AH": "अ",
    "AO": "ओ",
    "EH": "ए",
    "IH": "इ",
    "IY": "ई",
    "UH": "उ",
    "UW": "ऊ",
    "OW": "ओ"
}

def phonemes_to_hindi(phonemes):
    out = []
    pending = None

    for p in phonemes:
        if p in CONSONANTS:
            if pending:
                out.append(pending)
            pending = CONSONANTS[p]

        elif p in VOWEL_MATRAS:
            if p == "EH":
                if pending:
                # consonant + EH → short i (दिल्ली, गिरि)
                    out.append(pending + "ि")
                else:
                # word-initial EH → ए (Betula → बेटुला)
                    out.append("ए")
                pending = None
            else:
                if pending:
                    out.append(pending + VOWEL_MATRAS[p])
                    pending = None
                else:
                    out.append(FULL_VOWELS[p])

    if pending:
        out.append(pending + "्")

    return "".join(out)

def clean_phonemes(phonemes):
    cleaned = []
    for p in phonemes:
        p = re.sub(r"\d", "", p)
        if p.isalpha():
            cleaned.append(p)
    return cleaned

def normalize_hindi_skeleton(text):
    rules = [
        ("ङग", "ंग"),   # बङगलर → बंगलर
        ("नद", "ंद"),   # चनदर → चंदर
        ("शत", "ष्ट"),  # महशतर → महष्ट
        ("झश", "जश"),   # रझशन → रजशन (rare but safe)
    ]

    for a, b in rules:
        text = text.replace(a, b)

    return text

def restore_hindi_structure(text):
    # --- Nasal assimilation (phonotactically safe)
    text = text.replace("ङग", "ंग")
    text = text.replace("नद", "ंद")
    text = text.replace("नद्र", "ंद्र")

    # --- Conjunct normalization
    text = text.replace("षटर", "ष्ट्र")
    text = text.replace("षट्र", "ष्ट्र")
    text = text.replace("ष्टर", "ष्ट्र")

    # --- Vishnu-type cluster (safe phonetic rule)
    text = text.replace("सष्ण", "ष्ण")
    text = text.replace("सनव", "ष्णव")
    text = text.replace("ङह", "ंघ")

    return text

def p2g_suffix_restore(en, hi):
    en = en.lower()

    if en.endswith("pur") and not hi.endswith("पुर"):
        hi += "पुर"

    if en.endswith("gram") and not hi.endswith("ग्राम"):
        hi += "ग्राम"

    return hi

def schwa_cleanup(text):
    # remove inherent schwa before matras
    text = re.sub(r"([क-ह])अ([ािीुूेो])", r"\1\2", text)

    # remove trailing schwa
    if text.endswith("अ"):
        text = text[:-1]

    return text

def restore_schwa(text):
    # restore schwa only at word-final or before sonorants
    text = re.sub(r"([क-ह])्$", r"\1", text)
    text = re.sub(r"([क-ह])्([लरयनम])", r"\1\2", text)
    return text

def vowel_length_restore(en, hi):
    en = en.lower()
    if en.endswith("i") and not hi.endswith("ी"):
        hi += "ी"
    if en.endswith("a") and hi.endswith("अ"):
        hi = hi[:-1] + "ा"
    return hi

def nukta_fix(text):
    text = text.replace("फ", "फ़")
    text = text.replace("ज", "ज़")
    text = text.replace("ड", "ड़")
    text = text.replace("ढ", "ढ़")
    return text

def gemination_fix(en, hi):
    en = en.lower()

    # ll → ल्ल
    if "ll" in en:
        hi = hi.replace("लि", "ल्लि")
        hi = hi.replace("ली", "ल्ली")
        hi = hi.replace("ल", "ल्ल", 1)

    # pp → प्प
    if "pp" in en:
        hi = hi.replace("प", "प्प", 1)

    # tt → त्त
    if "tt" in en:
        hi = hi.replace("त", "त्त", 1)

    return hi

def schwa_deletion(text):
    # Delete schwa at word end
    text = re.sub(r"([क-ह])अ$", r"\1", text)

    # Delete schwa before consonant cluster
    text = re.sub(r"([क-ह])अ([क-ह])", r"\1\2", text)

    return text

def anusvara_fix(text):
    # Convert nasal before stops → anusvara
    text = re.sub(r"न([क-घच-झट-ढत-धप-भ])", r"ं\1", text)
    text = re.sub(r"म([क-घच-झट-ढत-धप-भ])", r"ं\1", text)
    return text

def cluster_fixes(text):
    fixes = {
        "पर": "प्र",
        "तर": "त्र",
        "गर": "ग्र",
        "सव": "स्व",
        "शन": "श्न",
        "कष": "क्ष",
    }
    for a, b in fixes.items():
        text = text.replace(a, b)
    return text

def transliterate_p2g(word):
    phonemes = clean_phonemes(g2p(word))
    hi = phonemes_to_hindi(phonemes)
    hi = normalize_hindi_skeleton(hi)
    hi = restore_hindi_structure(hi)
    hi = p2g_suffix_restore(word, hi)
    hi = schwa_cleanup(hi)
    hi = anusvara_fix(hi)
    hi = cluster_fixes(hi)
    hi = nukta_fix(hi)   
    return hi