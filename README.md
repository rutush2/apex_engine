# apex_engine

A backend auditing and intelligence dashboard built with Python. This system automates the tracking of technical findings, calculates priority scores based on impact, and manages remediation strategies.

## 🚀 Features
- Automated Priority: Logic-driven scoring based on impact levels.
- Risk Velocity Heatmap: Visual tracking of findings over time.
- Intelligence Queue: Managed interface for linking mitigation strategies to findings.
- Status Lifecycle: Real-time updates from Identification to Resolution.

## 🛠️ Tech Stack
- Backend: Python, SQLAlchemy (SQLite)
- Frontend: Streamlit
- Visualization: Altair, Pandas

## ⚙️ Setup
```bash
# 1. Clone the repository
git clone [https://github.com/rutush2/apex_engine.git](https://github.com/rutush2/apex_engine.git)

# 2. Install dependencies
pip install streamlit pandas sqlalchemy altair

# 3. Run the engine
streamlit run dashboard.py