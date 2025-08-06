# 🚀 Gemma Guard Setup Guide

## Step 1: Install Ollama
1. Download Ollama from https://ollama.ai
2. Install and start Ollama service

## Step 2: Download Gemma Model
```bash
# For Gemma 3n (latest version - recommended)
ollama pull gemma:latest

# Or for specific versions
ollama pull gemma:7b
ollama pull gemma:2b
```

## Step 3: Verify Ollama Installation
```bash
# Check if Ollama is running
ollama list

# Test Gemma
ollama run gemma:latest "Hello, how are you?"
```

## Step 4: Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure Environment
```bash
# Copy environment template
copy env.example .env

# Edit .env file and set:
ENABLE_OLLAMA_INTEGRATION=true
OLLAMA_MODEL=gemma:latest
```

## Step 6: Run the Application
```bash
streamlit run app/main.py
```

## 🔧 Troubleshooting

### If Ollama connection fails:
- Check if Ollama service is running
- Verify model is downloaded: `ollama list`
- Check Ollama logs for errors

### If Gemma model not found:
- Download the model: `ollama pull gemma:latest`
- Update OLLAMA_MODEL in .env file

### Fallback Mode:
Set `ENABLE_OLLAMA_INTEGRATION=false` in .env to use simulation mode while testing.
