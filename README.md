# Transliteration Consistency Pipeline

This project implements a robust data processing pipeline designed to establish a consistent, canonical mapping of English words to their Hindi transliterations. The system processes raw English-Hindi alignment data to filter noise, categorize confidence levels, and compute stability metrics, ultimately producing a high-quality "Canonical Map" for downstream NLP tasks.

## Project Overview

The primary goal is to resolve ambiguity in transliteration by analyzing frequency, alignment confidence, and consensus across a large corpus.

**Key Capabilities:**
*   **Heuristic Noise Filtering**: Removes semantic mismatches, stopwords, and low-quality alignments using rule-based filters.
*   **Confidence Segmentation**: Splits data into High, Mid, and Low confidence tiers to prioritize reliable pairings.
*   **Canonicalization**: Aggregates variants to identify the standard (canonical) transliteration for each English word.
*   **Stability Analysis**: Assigns a consistency score (0.0 - 1.0) to every canonical mapping to quantify its reliability.
*   **Phoneme-to-Grapheme (P2G) Generation**: Experimental rule-based engine to generate Hindi transliterations from English phonemes.

## Project Structure

The codebase is organized into core processing scripts (v2 active pipeline) and analysis utilities.

```
translit-consistency/
├── data/
├── src/
├── PIPELINE_FREEZE.md            # Version control context for the v1 pipeline
├── requirements.txt              # Project dependencies
│
├── # Core Pipeline Scripts (v2 - Active)
├── filter_aligned_pairs_v2.py    # Step 1: Cleans raw data (Enhanced heuristics)
├── analyze_confidence_v2.py      # Step 2: Splits data by confidence score
├── canonicalize_v2.py            # Step 3: Generates canonical map from high-conf data
├── analyze_stability.py          # Step 4: Classifies mappings into stability tiers
│
├── # Experimental & Utility
├── p2g.py                        # Rule-based Phoneme-to-Grapheme engine (g2p_en wrapper)
├── canonicalize_v1.py            # [Frozen] Legacy v1 implementation
├── filter_aligned_pairs_v1.py    # [Frozen] Legacy v1 implementation
│
└── # Analysis & Statistics
    ├── analyze_consistency.py    # Statistics on consistency scores
    ├── analyze_canonical.py      # Statistics on variant counts per word
    └── analyze_high_conf.py      # Statistics on high-confidence dataset
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd translit-consistency
    ```

2.  **Environment Setup**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage: The Processing Pipeline (v2)

The pipeline must be executed in the following order. Ensure your raw input file `aligned_pairs_full.json` is located in `data/processed/`.

### Step 1: Filtering
**Script**: `filter_aligned_pairs_v2.py`

Enhanced cleaning of the raw dataset using stricter heuristic rules:
*   **Stopword Removal**: Filters common English (e.g., "India", "Report") and Hindi stopwords.
*   **Semantic Mismatches**: Removes known bad translations (e.g., specific hardcoded errors, honorifics like "Shri/Smt").
*   **Structure Checks**: Filters pairs with significant length disparities (> 60% diff) or invalid characters.
*   **Similarity Thresholds**: Requires score ≥ 0.60-0.70 depending on word length.

**Input**: `data/processed/aligned_pairs_full.json`
**Output**: `data/processed/aligned_pairs_filtered.json`

```bash
python filter_aligned_pairs_v2.py
```

### Step 2: Confidence Segmentation
**Script**: `analyze_confidence_v2.py`

Splits the filtered dataset into three buckets based on alignment confidence scores:
*   **High Conf**: Score ≥ 0.85
*   **Mid Conf**: 0.70 ≤ Score < 0.85
*   **Low Conf**: Score < 0.70

**Input**: `data/processed/aligned_pairs_filtered.json`
**Outputs**:
*   `data/processed/aligned_pairs_high_conf.json` (Used for canonicalization)
*   `data/processed/aligned_pairs_mid_conf.json`
*   `data/processed/aligned_pairs_low_conf.json`

```bash
python analyze_confidence_v2.py
```

### Step 3: Canonicalization
**Script**: `canonicalize_v2.py`

Aggregates the **High Confidence** pairs to find the most frequent and highest-scoring Hindi transliteration for each English word.
*   Calculates a **Consistency Score** for each entry.
*   Captures all found variants for analysis.

**Input**: `data/processed/aligned_pairs_high_conf.json`
**Output**: `data/processed/canonical_map.json`

```bash
python canonicalize_v2.py
```

### Step 4: Stability Analysis
**Script**: `analyze_stability.py`

Segments the canonical map into stability tiers based on the calculated consistency score. This helps in selecting only the most stable pairs for production use.

**Input**: `data/processed/canonical_map.json`
**Outputs**:
*   `high_stability.json` (Score ≥ 0.95)
*   `mid_stability.json` (0.90 ≤ Score < 0.95)
*   `low_stability.json` (Score < 0.90)

```bash
python analyze_stability.py
```

## Experimental Modules

### P2G (Phoneme-to-Grapheme) Engine
**Script**: `p2g.py`

A rule-based utility that attempts to generate Hindi transliterations from English words using phonetics (`g2p_en`).
*   **Features**:
    *   Full English-to-Hindi phoneme mapping.
    *   Smart schwa deletion and restoration.
    *   Context-aware vowel and nukta handling.
    *   Post-processing for gemination (e.g., "ll" -> "ल्ल") and common suffixes (e.g., "pur" -> "पुर").

**Usage**: Import as a module in other scripts.
```python
from p2g import transliterate_p2g
print(transliterate_p2g("Hello"))
```

## Metrics & Analysis

The project includes helper scripts to inspect the quality of the generated data:
*   **`analyze_consistency.py`**: Reports average/median consistency scores.
*   **`analyze_canonical.py`**: Analyzes the distribution of variants per word.
