# 🦅 Market Regime & Behavioral Analytics System

### **Primetrade.ai Engineering Assignment**

**Objective:** Analyze how market sentiment (Fear/Greed) relates to trader behavior and performance on Hyperliquid. Main goal is to uncover patterns that could inform smarter trading strategies.

---

## 📑 Quick Links & Deliverables

| **Artifact** | **Description** | **Type** | **Open** |
| --- | --- | --- | --- |
| 📊 **Interactive Dashboard** | The Command Center for Risk & Strategy. Run via Streamlit. | **App** | [Open ↗](https://trade-sentiment-analysisgit-rmgjzah355d2cpywhq9gkr.streamlit.app/) |
| 📄 **Executive Summary** | A 1-page writeup of findings. | **Report** | [Open ↗](https://github.com/Meet3719/trade-sentiment-analysis/blob/main/shortsummary.md) |
| 👨‍💻 **Candidate Resume** | Professional CV & Contact Information. | **PDF** | [Open ↗](https://github.com/Meet3719/trade-sentiment-analysis/blob/main/Meet_Resume.pdf) |

---

## 🚀 Project Overview

This project solves the **"Regime Shift" problem** in algorithmic trading. Most models fail because they assume market conditions are static. This system dynamically adjusts to **Fear** (Mean Reversion) and **Greed** (Momentum) regimes.


---

## 📂 Data Sources & Architecture

The system ingests two primary datasets to engineer **12+ composite features** (e.g., `risk_sentiment_interaction`, `aggression_score`).

| **Dataset** | **Description** | **Source Link** |
| --- | --- | --- |
| **Bitcoin Sentiment** | Daily Fear & Greed Index (0-100). used for Regime Classification. | [Download Here](https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view?usp=sharing) |
| **Trader History** | Tick-level trade data from Hyperliquid (Symbol, Size, Side, PnL, Leverage). | [Download Here](https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view?usp=sharing) |

**Pipeline Architecture:**

`Raw Data` $\rightarrow$ `Cleaning (Nulls/Outliers)` $\rightarrow$ `Feature Engineering (Rolling Windows)` $\rightarrow$ `Modeling (RF/K-Means)` $\rightarrow$ `Dashboard (Streamlit)`

---

## 🛠️ Installation & Usage

### 1️⃣ Environment Setup

Ensure you have **Python 3.9+** installed.
Clone the repository and install all required dependencies.

```bash
# Clone the repository
git clone https://github.com/Meet3719/trade-sentiment-analysis.git
cd trade-sentiment-analysis

# Install required packages
pip install -r requirements.txt

```

---

### 2️⃣ Running the Dashboard (The “Command Center”)

Launch the interactive Streamlit application .

```bash
streamlit run dashboard_app.py
```

📍 Opens automatically in your browser at:
**[http://localhost:8501](http://localhost:8501)**

#### 🚀 Live Demo (Hosted)

https://trade-sentiment-analysisgit-rmgjzah355d2cpywhq9gkr.streamlit.app/

---
---

### 3️⃣ Reproducing the Analysis (Notebooks)

Run the notebooks **in order** to fully regenerate data artifacts and models:

1. `notebooks/01_data_prep.ipynb`
   → Cleans and validates raw CSV datasets.

2. `notebooks/02_feature_engineering.ipynb`
   → Creates sentiment-behavior interaction features.

3. `notebooks/03_analysis.ipynb`
   → Exploratory analysis and validation of “Golden Rules”.

4. `notebooks/04_modeling.ipynb`
   → Trains **Random Forest** (supervised) and **K-Means** (unsupervised) models.



---

## 📁 Project Structure

trade-sentiment-analysis/
├── data/
│   ├── raw/                    
│   └── processed/              
├── notebooks/
│   ├── 01_data_prep.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_modeling.ipynb
├── outputs/
│   ├── tables/                 
│   ├── figures/               
│   └── models/                 
├── dashboard_app.py            
├── requirements.txt            
├── README.md                   
├── shortsummary.md             
└── Meet_Resume.pdf             

---


**Author:** Meet Vora

**Submission Date:** 6 Feb 2026

**For:** Primetrade.ai Engineering Team