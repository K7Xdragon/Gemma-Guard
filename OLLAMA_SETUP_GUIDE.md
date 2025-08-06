# 🚀 Step-by-Step Ollama Setup for Gemma Guard

## 🎯 Current Status: You've installed Ollama, now let's configure it!

### **Step 1: Start Ollama Service**

#### **Option A: Start from Command Line**
```powershell
# Try starting Ollama service
ollama serve
```

#### **Option B: If Ollama isn't in PATH, find and start it**
```powershell
# Check common installation locations
Get-ChildItem -Path "C:\Program Files" -Recurse -Name "ollama.exe" -ErrorAction SilentlyContinue
Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local" -Recurse -Name "ollama.exe" -ErrorAction SilentlyContinue

# Or start Ollama from Start Menu
# Search "Ollama" in Windows Start Menu and click it
```

#### **Option C: Download and Install if needed**
If Ollama isn't found:
1. Go to https://ollama.ai
2. Download "Download for Windows"
3. Run the installer
4. Restart your computer

### **Step 2: Install Gemma Model**

Once Ollama is running, install the Gemma model:

```powershell
# Install the latest Gemma model (recommended)
ollama pull gemma:latest

# OR if you have limited resources, try the smaller version
ollama pull gemma:2b
```

### **Step 3: Verify Everything is Working**

```powershell
# Check available models
ollama list

# Test Gemma
ollama run gemma:latest "Hello, introduce yourself"

# Check if Ollama API is responding
curl http://localhost:11434/api/tags
```

### **Step 4: Update Gemma Guard Configuration**

Your `.env` file should already have:
```
ENABLE_OLLAMA_INTEGRATION=true
OLLAMA_MODEL=gemma:latest
OLLAMA_BASE_URL=http://localhost:11434
```

### **Step 5: Restart Gemma Guard**

1. Stop your current Streamlit app (Ctrl+C in the terminal)
2. Restart it:
```powershell
cd "c:\Users\Bisnes Trading\Desktop\Gemma Guard"
.\venv\Scripts\Activate.ps1
streamlit run app\main.py
```

### **Step 6: Verify Integration**

You should now see:
- ✅ "🤖 Gemma 3n is ready via Ollama" (instead of simulation mode)
- Real AI responses when you run analysis

## 🔧 **Quick Troubleshooting**

### **If Ollama won't start:**
- Check Windows Services: `services.msc` → Look for "Ollama"
- Try running as Administrator
- Restart your computer after installation

### **If model download fails:**
- Check internet connection
- Try smaller model: `ollama pull gemma:2b`
- Free up disk space (models can be 4-7GB)

### **If API connection fails:**
- Check Windows Firewall
- Verify port 11434 isn't blocked
- Try `telnet localhost 11434`

## 🎮 **Test Commands to Run Now**

Try these commands in PowerShell to diagnose:

```powershell
# 1. Check if Ollama is running
Get-Process | Where-Object {$_.ProcessName -like "*ollama*"}

# 2. Try to start Ollama
ollama serve

# 3. In a new terminal, check models
ollama list

# 4. Test API endpoint
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing
```

Once you complete these steps, your Gemma Guard will show the real Ollama integration status!
