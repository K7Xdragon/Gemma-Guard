# 🏗️ Gemma Guard Architecture

## System Overview

Gemma Guard is a multi-layered wellness monitoring application that combines scientific chronotype analysis, biometric signal simulation, and AI-powered insights to provide personalized stress and burnout detection. It features a **dual-mode analysis system**, where both modes provide comprehensive personality analysis and burnout timing, but the Full Analysis mode additionally includes biometric simulation and extended AI insights.

## 📊 Architecture Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 GEMMA GUARD SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🎨 STREAMLIT UI LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  app/main.py                                                    │
│  ├─ Page 1: Welcome & Consent                                  │
│  ├─ Page 2: User Input (DOB, Symptoms)                         │
│  └─ 🔘 Analysis Mode Choice: [Full Analysis] or [Temporal Pattern] │
└─────┬───────────────────────────────────────────────┬─────────┘
      │ (Full Analysis Path)                          │ (Temporal Pattern Path)
      │                                               │
      ▼                                               ▼
┌──────────────────────────┐             ┌──────────────────────────┐
│  COMPREHENSIVE           │             │  FOCUSED PROCESSING      │
│  PROCESSING              │             ├──────────────────────────┤
├──────────────────────────┤             │ ┌──────────────────────┐ │
│ ┌──────────────────────┐ │             │ │  CHRONO-DECODER      │ │
│ │    SIGNAL ENGINE     │ │             │ │ private/chrono_deco… │ │
│ │  app/signal_engine.py│ │             │ │ • Real Chrono Calc   │ │
│ └──────────┬───────────┘ │             │ │ • Burnout Timing     │ │
│            │             │             │ │ • Recovery Strategy  │ │
│ ┌──────────▼───────────┐ │             │ │ • Personality Traits │ │
│ │ CORE LOGIC (SIMPLE)  │ │             │ └──────────┬───────────┘ │
│ │ private/core_logic…  │ │             │            │             │
│ └──────────┬───────────┘ │             │ ┌──────────▼───────────┐ │
│            │             │             │ │   AI NARRATIVE       │ │
│ ┌──────────▼───────────┐ │             │ │  (in chrono_decoder) │ │
│ │  CHRONO-DECODER      │ │             │ └──────────────────────┘ │
│ │ private/chrono_deco… │ │             └──────────────────────────┘
│ │ • Complete Analysis  │ │
│ │ • Personality Traits │ │
│ │ • Burnout Timing     │ │
│ │ • Recovery Strategy  │ │
│ └──────────┬───────────┘ │
│            │             │
│ ┌──────────▼───────────┐ │
│ │    SIGNAL MATCH      │ │
│ │   app/matcher.py     │ │
│ └──────────┬───────────┘ │
│            │             │
│ ┌──────────▼───────────┐ │
│ │   AI INFERENCE       │ │
│ │ app/gemma_inference… │ │
│ └──────────────────────┘ │
└────────────┬─────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   📊 INSIGHT GENERATION                         │
├─────────────────────────────────────────────────────────────────┤
│  app/insight_generator.py (for Full Analysis additional layer)  │
│  private/chrono_decoder.py (provides core analysis for both)    │
└─────┬───────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     📈 FINAL UI DISPLAY                         │
├─────────────────────────────────────────────────────────────────┤
│  ├─ Full Analysis: Complete personality analysis + burnout      │
│  │   timing + recovery strategies + biometric data + AI summary │
│  └─ Temporal Pattern: Personality analysis + burnout timing +   │
│      recovery strategies (no biometric data)                    │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Component Architecture

### 1. **Frontend Layer** (`app/main.py`)
- **Purpose**: User interface and experience orchestration with a focus on wellness insights.
- **Technology**: Streamlit multi-page application with healing tech aesthetic.
- **Design Philosophy**: 
  - **User-Centric Display**: Technical debugging information (chrono-signature profiles, LLM prompts) is hidden from end users but preserved internally for development.
  - **Wellness-Focused Interface**: Prioritizes actionable health insights over technical complexity.
- **Key Features**:
  - **Dual-Mode Analysis Selection**: Allows users to choose between "Full Analysis" (comprehensive + biometric) and "Temporal Pattern Analysis" (comprehensive only).
  - Real-time Ollama/Gemma status monitoring.
  - Integrated display for both analysis types with consistent personality insights.

### 2. **Full Analysis Components**

#### 2.1. **Signal Processing** (`app/signal_engine.py`)
- **Purpose**: Biometric data simulation for the full analysis mode.
- **Features**: Realistic physiological signal generation (skin conductance, heart rate).

#### 2.2. **Simplified Chrono-Signature Engine** (`private/core_logic_real.py`)
- **Purpose**: Provides a simplified, lookup-based chronotype analysis for the full analysis mode.
- **Data Source**: `chrono_pattern_matrix.json`.

### 3. **Temporal Pattern Analysis Components**

#### 3.1. **Advanced Chrono-Signature Engine** (`private/chrono_decoder.py`)
- **Purpose**: Provides comprehensive, date-based chronotype analysis used by both analysis modes.
- **Core Functions**:
  - `get_chrono_profile_without_biometrics()`: Main public interface for the UI.
  - **Real Chronotype Calculation**: Uses temporal algorithms based on the user's birth date.
  - **Personality Trait Analysis**: Detailed human-centered personality explanations.
  - **Burnout Risk Timing**: Predicts high-risk and recovery periods.
  - **Recovery Strategy Generation**: Creates personalized advice.
- **Usage**: Called by both Full Analysis and Temporal Pattern Analysis modes.

### 4. **Shared Components**

#### 4.1. **AI Integration** (`app/gemma_inference.py` + `private/llm_inference.py`)
- **Purpose**: Real-time AI analysis via Ollama.
- **Usage**:
  - Used by the **Full Analysis** path for general insights.
  - Used by the **Advanced Engine** (`chrono_decoder.py`) to generate scientific narratives.

#### 4.2. **Data Persistence** (`app/utils_data.py`)
- **Purpose**: Local data storage for logs and user profiles.

## 🌊 Data Flow

The system now operates with two distinct data flows based on user choice:

### **Flow A: Full Analysis (with biometric simulation)**
1.  **Input**: User provides birth date and selects "Full Analysis".
2.  **Signal Generation**: `signal_engine.py` creates a simulated biometric data packet.
3.  **Simplified Chrono-Analysis**: `core_logic_real.py` performs a lookup to get a basic chronotype profile for technical matching.
4.  **Advanced Chrono-Analysis**: `chrono_decoder.py` is also called to provide the complete personality analysis, burnout timing, and recovery strategies.
5.  **Signal Matching**: `matcher.py` compares biometric data against the chronotype profile.
6.  **AI Processing**: `gemma_inference.py` sends combined data to the LLM.
7.  **Insight Synthesis**: `insight_generator.py` creates a final summary.
8.  **Display**: The UI shows a user-focused wellness analysis including:
    - **Detailed personality traits** from `chrono_decoder.py`
    - **Burnout timing analysis** (current risk, high-risk months, recovery periods)
    - **Personalized recovery strategies**
    - **Biometric data visualization** (EDA levels, signal analysis)
    - **AI insights and recommendations**
    - **Technical debugging sections** (chrono-signature profile, LLM prompts) are hidden from users but remain active internally

### **Flow B: Temporal Pattern Analysis (signature-based)**
1.  **Input**: User provides birth date and selects "Temporal Pattern Analysis".
2.  **Advanced Chrono-Analysis**: `chrono_decoder.py` is called directly.
    - It calculates the real chrono-signature from the birth date.
    - It determines burnout risk periods and recovery strategies.
    - It uses the LLM to generate a scientific narrative about the findings.
3.  **Display**: The UI shows a focused wellness report with:
    - **Detailed personality traits** based on chronotype signature
    - **Burnout timing analysis** (current risk, high-risk months, recovery periods)
    - **Personalized recovery strategies**
    - **Scientific narrative** explaining the analysis in accessible terms

## 🧪 Scientific Foundation

### Chronotype Analysis
- **Method 1 (Simplified)**: A lookup-based system using `core_logic_real.py` for the full analysis mode.
- **Method 2 (Advanced)**: A calculation-based system using `chrono_decoder.py` that analyzes temporal patterns from a birth date to predict burnout cycles.

---

*This updated architecture reflects the new dual-mode capability, offering users flexible and powerful ways to gain wellness insights.*
