# 🚀 GemmaGuard User Guide

## Quick Start Instructions

Follow these steps to run GemmaGuard on your local machine.

### 1. **Open Terminal/Command Prompt**
- **Windows**: Press `Win + R`, type `cmd` or `powershell`, and press Enter
- **macOS**: Press `Cmd + Space`, type "Terminal", and press Enter  
- **Linux**: Press `Ctrl + Alt + T` or search for "Terminal"

### 2. **Navigate to the Project Directory**
```bash
# On Windows
cd path\to\GemmaGuard

# On macOS/Linux  
cd path/to/GemmaGuard
```

### 3. **Activate the Virtual Environment**
```bash
# On Windows
.\venv\Scripts\Activate.ps1
# or
venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

### 4. **Start the Streamlit Application**
```bash
streamlit run app/main.py
```

### 5. **Access the Application**
- The application will automatically open in your default web browser
- If it doesn't open automatically, go to: `http://localhost:8501`

## 📋 **Prerequisites**

Before running GemmaGuard, ensure you have:
- Python 3.8+ installed
- Virtual environment set up with required packages
- Ollama installed (optional - app runs in simulation mode without it)

### **Quick Setup**
```bash
# Clone the repository
git clone https://github.com/YourUsername/GemmaGuard.git
cd GemmaGuard

# Create virtual environment
python -m venv venv

# Activate virtual environment (see step 3 above)

# Install dependencies
pip install -r requirements.txt
```

## 🎯 What You'll See as a User

### **Page 1: Welcome & Consent**
- Welcome message with privacy policy
- Ollama/Gemma status indicator:
  - 🤖 Green: "Gemma 3n is ready via Ollama" (if Ollama is running)
  - 🧪 Blue: "Running in simulation mode" (if Ollama is disabled)
  - 🔧 Red: "Ollama connection failed" (if Ollama is not running)
- Checkbox: "I agree to the Terms & Conditions and Privacy Policy"
- "Proceed" button (only enabled after checking the box)

### **Page 2: User Input & Analysis**
Fill out the form:
- **Nickname**: Your preferred name
- **Date of Birth**: Select your birth date
- **Location**: Your city/location
- **Status**: Student or Working
- **Symptoms**: Check any that apply:
  - Feeling tired or drained
  - Frequent headaches or muscle pain
  - Difficulty concentrating
  - Loss of motivation
  - Changes in sleep habits
  - Negative or cynical outlook
  - Feeling trapped or helpless

### **Analysis Mode Selection**
Choose between two analysis types:

#### **Option A: Full Analysis (with biometric simulation)**
- Generates simulated biometric data
- Combines chronotype analysis with "live" signal data
- Shows detailed technical output
- Includes AI inference from Gemma

#### **Option B: Chrono-Signature Only (date-based)**
- Pure chronotype analysis based on birth date
- No biometric simulation
- Focuses on burnout timing and recovery strategies
- Provides personalized recommendations

## 📊 Expected User Experience

### **For Full Analysis:**
```
🔬 Full Chrono-Signature Analysis
📡 Signal Summary:
- Time: 2025-08-06 11:30:00 UTC
- EDA Level: 3.47 µS
- Stimulus Classification: charged

🔍 Chrono-Signature Profile
📊 Chrono-Signature Profile
Tags: creative, adaptive
Rationale:
- Based on chronotype analysis of birth date: [Your Birth Date]
- Chrono-signature identified: [Generated Signature]
- Element profile: {primary_element: "Metal", ...}
- Analysis uses scientifically-derived chronotype patterns

📊 Gemma Insight Summary
✅ Your biometric rhythm aligns well with behavioral traits today.
💡 Maintain consistency in pacing and reinforce familiar habits.
```

### **For Chrono-Signature Only:**
```
🔬 Pure Chrono-Signature Analysis

🔍 Your Chrono-Signature Profile
Chrono-Signature: [Generated Signature]
Pattern Tags: creative, adaptive

Analysis Rationale:
• Based on chronotype analysis of birth date: 15/05/1990
• Chrono-signature identified: Geng-Yin
• Element profile: Metal with Earth influence
• Analysis uses scientifically-derived chronotype patterns

⏰ Burnout Risk Timing
✅ Current Risk Level: Low
Next High-Risk Month: March 2026
Recovery Months: 6, 9, 12

💡 Personalized Recovery Strategies
Energy Management: Focus on sustained effort during morning hours
Stress Response: Use structured problem-solving approaches
Cognitive Style: Channel creative energy into systematic projects
```

## 🔧 Troubleshooting

### **If the app doesn't start:**
1. Make sure you're in the correct directory
2. Check that the virtual environment is activated
3. Try: `python -m streamlit run app\main.py`

### **If you see import errors:**
1. Activate the virtual environment first
2. Install dependencies: `pip install -r requirements.txt`

### **If Ollama integration fails:**
- The app will automatically fall back to simulation mode
- You'll still get full functionality, just without real AI inference

## 🎯 User Testing Scenarios

Try these scenarios to test the application:

### **Scenario 1: Happy Path - Full Analysis**
1. Click "I agree" and proceed
2. Fill out all fields:
   - Nickname: "Alex"
   - DOB: Pick a date from the 1990s
   - Location: "Kuala Lumpur"
   - Status: "Working"
3. Select 2-3 symptoms (e.g., "Feeling tired", "Difficulty concentrating")
4. Choose "Full Analysis (with biometric simulation)"
5. Click "Analyze"

**Expected Results:**
- Should see simulated biometric data (EDA levels, environmental state)
- Chrono-signature profile with pattern tags
- AI-generated insights and recommendations
- Technical details section with signal ID

### **Scenario 2: Chrono-Only Mode**
1. Use different data:
   - Nickname: "Maria"
   - DOB: Different date (try 1985 or 2000)
   - Location: "Singapore"
   - Status: "Student"
2. Don't select any symptoms
3. Choose "Chrono-Signature Only (date-based)"
4. Click "Analyze"

**Expected Results:**
- Pure chronotype analysis without biometrics
- Burnout risk timing (current risk level, high-risk months)
- Recovery strategies tailored to chronotype
- No biometric simulation data

### **Scenario 3: Edge Cases**
- **Recent birth dates**: Try 2005 (younger user)
- **Older birth dates**: Try 1970 (older user)
- **All symptoms selected**: Test with all 7 symptoms checked
- **No symptoms**: Test with zero symptoms selected
- **Different locations**: Try various cities

### **Scenario 4: System Status Testing**
- Check the status indicators on Page 1:
  - Look for Ollama status (likely shows simulation mode)
  - Verify the privacy notice appears
  - Test that "Proceed" only works after agreeing

### **Scenario 5: Data Persistence Testing**
1. Run analysis once with Full Mode
2. Run again with Chrono-Only mode
3. Check if the system handles multiple analyses properly

## 🔍 What to Look For During Testing

### ✅ **Positive Indicators:**
- Smooth page transitions
- Consistent chronotype results for same birth date
- Reasonable biometric values (0.5-6.0 µS for EDA)
- Coherent AI recommendations
- Proper error handling
- Clear, readable output formatting

### ⚠️ **Red Flags to Report:**
- Application crashes or freezes
- Blank or error pages
- Inconsistent results for same input
- Missing UI elements
- Unreadable text or formatting issues

## 🔗 **Additional Resources**

- **README.md**: General project overview and setup instructions
- **ARCHITECTURE.md**: Technical system architecture documentation  
- **setup_gemma.md**: Ollama/Gemma installation guide
- **requirements.txt**: Python package dependencies

## 📧 **Support**

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your Python version is 3.8+
3. Ensure virtual environment is activated
4. Try running in simulation mode if Ollama issues occur

---

*This guide is designed to help users quickly get started with GemmaGuard's wellness monitoring capabilities.*
- Inconsistent results for same input
- Unrealistic biometric values
- Broken formatting or missing data
- Import errors in console

### 📊 **Data Quality Checks:**
- Chrono-signatures should be consistent for same birth date
- Pattern tags should make sense (e.g., "creative", "adaptive")
- Burnout timing should vary by birth date
- Recovery strategies should match chronotype
- AI insights should be relevant to selected symptoms

## 🎮 Interactive Features to Test

### **Page 1 Features:**
- [ ] Privacy checkbox must be checked to proceed
- [ ] Ollama status indicator updates correctly
- [ ] Page navigation works smoothly

### **Page 2 Features:**
- [ ] All form fields accept input properly
- [ ] Date picker works correctly
- [ ] Radio buttons for analysis mode work
- [ ] Symptom checkboxes can be selected/deselected
- [ ] "Analyze" button triggers processing

### **Results Display:**
- [ ] Biometric data displays properly (Full Analysis)
- [ ] Chronotype profile shows correctly
- [ ] AI insights are readable and relevant
- [ ] Technical details expand properly
- [ ] Burnout timing displays correctly (Chrono-Only)

The application should handle all these scenarios gracefully and provide meaningful insights in each case.
