# MindBalance: Student Social Media Risk Analyzer

> An end-to-end AI-powered digital wellness suite that analyzes social media usage patterns among students, predicts addiction risk levels, and provides real-time background monitoring — built with Python, scikit-learn, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange?style=flat-square&logo=scikit-learn)
![Cross-Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ⚡ New: MindBalance Screen Guard
The latest update introduces the **MindBalance Screen Guard**, a robust background monitoring system that helps you stay within your digital limits.
- **Auto-Startup**: Automatically starts with your operating system (Windows/Linux/macOS).
- **Desktop Alerts**: Get instant native notifications when reaching 50%, 75%, 90%, and 100% of your limit.
- **Smart Reset**: Intelligently detects system reboots and new days to reset your usage timer.
- **Low-Impact**: Lightweight background process with minimal CPU usage.

---

## 🚀 Live Demo
**Try the web analysis here:** [social-media-risk-annalyzer.streamlit.app](https://social-media-risk-annalyzer-5muhcog2gkgi425d6mcvza.streamlit.app/)

*(Note: The background monitoring features require a local installation to access system-level uptime and notifications.)*

---

## Overview

This project investigates the relationship between social media usage habits and student well-being using a real-world survey dataset of **705 students**. The application takes a student's usage profile as input and outputs a **personalised risk score** along with insights into how their habits compare to the broader student population.

**Key features of this version:**
- 🛡️ **AI Guard**: Real-time screen time tracking and automated safety alerts.
- 📊 **Wellness Stats**: Comparison metrics vs. yesterday and usage trend analysis.
- 🎨 **Glassmorphic UI**: A premium, futuristic interface with smooth 60fps animations.
- 🧠 **Hybrid Risk Index**: Combines ML predictions with clinical Bergen Scale profiling.

---

## Project Structure

```
social-media-risk-annalyzer/
│
├── app.py                          # Main Streamlit UI (Premium Glassmorphic Design)
├── background_monitor.py           # Cross-platform background monitoring logic
├── train_model.py                  # Model training pipeline
├── data_gen.py                     # Dataset preprocessing & feature engineering
│
├── best_model.pkl                  # Saved trained ML model
├── features.pkl                    # Saved feature columns for inference
├── social_media_addiction_data.csv # Dataset (705 students, 13 features)
│
├── screen_config.json              # Local configuration for AI Guard
├── mindbalance.log                 # Background monitoring logs
│
├── requirements.txt                # Python dependencies
└── docs/                           # Architecture & Flow Diagrams
```

---

## Technical Features

### 1. Digital Wellbeing Metrics
The app now tracks **Usage Trends** and **Goal Achievement**. It compares today's usage with yesterday's data to give you a percentage-based improvement score.

### 2. Native Notifications
The background monitor uses `plyer` to send professional system notifications, ensuring you never miss a milestone even when the browser is closed.

### 3. Atomic Data Persistence
All usage data is saved using atomic operations to prevent file corruption during sudden system shutdowns or power cycles.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Core** | Python 3.9+, Streamlit |
| **Machine Learning** | scikit-learn, XGBoost |
| **Backend Guard** | Subprocess, Ctypes, Plyer |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib (60fps CSS injected) |
| **Design** | Glassmorphism, CSS3 Animations |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/pradnya-182006/social-media-risk-annalyzer.git
cd social-media-risk-annalyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the App
streamlit run app.py
```

---

## Developers

**Pradnya Maruti Ghokshe** | **Sanket Khobre** | **Prachi Shinde**

B.Tech — AI and Data Science | NMIET, Pune

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/pradnya-ghokshe-40364b3b7/) 
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/pradnya-182006)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- Dataset: [Kaggle — Social Media Addiction Among Students](https://www.kaggle.com/code/adilshamim8/social-media-addiction-among-students)
- Built as a Data Science Mini Project — NMIET, Pune (2025).
