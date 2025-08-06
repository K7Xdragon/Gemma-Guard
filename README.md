# 🧠 GemmaGuard

GemmaGuard is an AI-powered wellness monitoring application that combines chronotype analysis, biometric simulation, and Gemma 3n integration for personalized burnout detection and wellness insights. Features dual analysis modes for comprehensive health monitoring.

---

## 📘 Overview

GemmaGuard provides scientifically-informed wellness monitoring through dual analysis modes, combining birth date chronotype analysis with optional biometric simulation. The application uses Gemma 3n AI for personalized wellness recommendations while maintaining complete privacy through local processing.

---

## 🔬 GemmaGuard Features

### Core Capabilities
- **Dual Analysis Modes**:
  - **Full Analysis**: Birth date chronotype + simulated biometric data (EDA/skin conductance)
  - **Temporal Pattern Analysis**: Birth date chronotype analysis only
- **Gemma 3n AI Integration**: Personalized wellness recommendations via Ollama
- **Biometric Simulation**: Realistic skin conductance data generation (prototype for future hardware)
- **Chronotype Analysis**: Scientific personality pattern assessment based on birth date
- **Burnout Risk Timing**: Predictions for high-risk and recovery periods
- **Privacy-First Design**: All processing occurs locally with no external data transmission
- **Healing Tech UI**: Modern, calming interface designed for wellness applications

### App Structure
```
GemmaGuard/
├── app/
│   ├── main.py                 # Streamlit main application (4-page flow)
│   ├── gemma_inference.py      # Gemma 3n AI integration
│   ├── signal_engine.py        # Biometric simulation engine
│   ├── matcher.py              # Signal-chronotype correlation
│   ├── insight_generator.py    # Final analysis synthesis
│   └── utils_*.py              # Data and formatting utilities
├── private/                    # Protected core algorithms
│   ├── chrono_decoder.py       # Advanced chronotype analysis
│   ├── core_logic_real.py      # Simplified chronotype lookup
│   ├── chrono_pattern_matrix.json # Chronotype pattern data
│   ├── trait_mapping_table.py  # Personality trait mapping
│   └── llm_inference.py        # LLM management
├── competition_public/         # Educational implementations
│   ├── simple_chrono_calc.py   # Simplified chronotype calculation
│   └── gemma_integration_demo.py # Clear Gemma 3n demonstration
├── data/
│   ├── inference_log.json      # AI analysis logs (auto-generated)
│   ├── signal_log.json         # Biometric data logs (auto-generated)
│   └── user_profile.json       # User profiles (auto-generated)
├── report/
│   └── technical_summary.pdf   # Comprehensive documentation
├── requirements.txt
├── COMPETITION_README.md       # Competition-specific documentation
└── README.md
```

---

## 🏗️ System Architecture

For detailed technical architecture, system flow, and component interactions, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Quick Architecture Overview
```
Mode A: Full Analysis
User Input → Chronotype Analysis → Biometric Simulation → Gemma 3n AI → Comprehensive Wellness
     ↓              ↓                      ↓                    ↓                ↓
 Birth Date    Pattern Analysis      Skin Conductance      AI Processing    Detailed Insights

Mode B: Temporal Pattern Analysis  
User Input → Chronotype Analysis → Gemma 3n AI → Focused Wellness Recommendations
     ↓              ↓                    ↓              ↓
 Birth Date    Pattern Analysis      AI Processing    Personality Insights

Note: Biometric data currently uses simulation (prototype for future hardware device)
```


### Run Instructions
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama + Gemma (for AI features)
curl -fsSL https://ollama.ai/install.sh | sh  # Install Ollama
ollama pull gemma:latest                      # Install latest Gemma model

# Launch the app
streamlit run app/main.py
```

### 🎯 **Competition & Gemma 3n Integration**

This project demonstrates clear **Gemma 3n integration** for the competition:
- See `COMPETITION_README.md` for detailed competition documentation
- Run `python competition_public/gemma_integration_demo.py` to verify Gemma integration
- Educational algorithms available in `competition_public/` directory

---

## 🔐 Privacy & Ethics

GemmaGuard prioritizes user privacy with local-only processing. No personal data is transmitted externally. All analysis occurs on your device, and biometric data is currently simulated for prototype demonstration.

### Competition Transparency
- Educational implementations available in `competition_public/` for transparency
- Clear Gemma 3n integration demonstrated while protecting proprietary algorithms
- Dual-mode architecture shows innovation in wellness monitoring

### Contributing
Fork the repo and submit a pull request with clear documentation. Whether you're improving the UI, tweaking inference logic, or adding a chart module—we welcome contributions.

## 📄 License & Intellectual Property Notice

© Syira, [2025]

This project and its source code are part of a proprietary development initiative submitted to the **Google Gemini 3N Impact Challenge**. All intellectual property rights associated with Gemma Guard—including signal modeling architecture, behavioral inference prompts, and integrated analytics—are protected under applicable copyright laws.

Unauthorized reproduction, distribution, or use of any part of this codebase without explicit written permission is strictly prohibited.

### Permitted Use (By Invitation or Agreement)
- Educational research and impact-driven prototyping
- Non-commercial pilot studies aligned with mental health advancement

### Collaboration Policy
We welcome inquiries for joint development, ethical application, and non-profit usage. To explore collaboration, contact:  
📩 **[syira.datasci@outlook.com]**  

### License Intent
While the core technology is protected, this project may adopt a dual-license or impact-driven open model upon selection by panel juries or research accelerators.

All rights reserved unless stated otherwise in individual module headers or agreed by contributor contract.