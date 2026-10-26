# A Multiscript Benchmark for Evaluating Large Language Models on Moroccan Darija (Arabic vs Arabizi)

Projet de Fin d'Année (PFA) - Master Data Science & Big Data (DSBD)  
**Faculté des Sciences Ben M'Sick - Université Hassan II de Casablanca**  
**Auteur :** Soukaina Grandi  
**Encadrant :** M. Zahour Omar  

---

## 📌 Context & Objectives
Moroccan Darija is a low-resource dialect characterized by the daily coexistence of two distinct scripts:
- **Arabic script** (e.g., *كيداير*)
- **Arabizi** (Latin letters combined with phonetic numerals: `3` for ع, `7` for ح, `9` for ق, e.g., *kidayr*, *3jebni*).

This repository provides an étalonned, human-authored benchmark assessing whether script choice affects LLM comprehension, reasoning, and generation.

---

## 🏗️ Benchmark Architecture (`data/final/benchmark.xlsx`)
The benchmark consists of **156 parallel items** (78 unique concepts evaluated across both scripts):
- **Script Conversion (48 rows):** Arabic $\leftrightarrow$ Arabizi (Testing surface-level form).
- **Reading Comprehension / MCQ (48 rows):** 4-way multiple-choice questions (Testing contextual meaning).
- **Natural Language Inference / NLI (60 rows):** Entailment, Contradiction, Neutral (Testing logical reasoning).
- **Hermetic Partitioning:** Strict `dev` split (64 rows) for prompt calibration and `test` split (92 rows) for benchmark evaluation.

---

## ⚙️ Quick Start

### 1. Installation
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt