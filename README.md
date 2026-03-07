# infoTrace
# 🔍 InfoTrace

> A Cross-Platform Misinformation Detection & Comparison Tool

InfoTrace analyzes how news and information spreads across Twitter/X,
Facebook, and Instagram — detecting misinformation and comparing
narratives across platforms using NLP and Transformer models.

---

## 🧠 Core Features
- Multi-platform data collection (Twitter, Facebook, Instagram)
- Misinformation detection using fine-tuned RoBERTa
- Sentiment & emotion analysis per platform
- Cross-platform narrative comparison using BERTopic
- Interactive dashboard for visualization

---

## 🛠️ Tech Stack
- **AI/ML:** PyTorch, HuggingFace Transformers, BERTopic
- **Backend:** FastAPI
- **Dashboard:** Streamlit
- **Deployment:** HuggingFace Spaces + Railway

---

## 📁 Project Structure
InfoTrace/
├── data/
│   ├── raw/               # Raw collected data
│   └── processed/         # Cleaned, model-ready data
├── models/                # Saved trained models
├── notebooks/             # Experiments and EDA
├── src/
│   ├── data_pipeline/     # Data collection scripts
│   ├── ai_engine/         # ML model code
│   └── utils/             # Helper functions
├── api/                   # FastAPI backend
├── dashboard/             # Streamlit app
├── config.py              # Project configuration
└── requirements.txt       # Dependencies

---

## 🚧 Status
> Phase 1 — Data Pipeline (In Progress)

---

## 👤 Author
Rakshith Vellulla — Graduate Researcher